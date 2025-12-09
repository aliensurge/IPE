import requests
import hashlib
import ssl
import socket
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from database import Database
from config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MonitoringEngine:
    def __init__(self):
        self.db = Database()
        self.timeout = Config.CHECK_TIMEOUT
    
    def check_website(self, website_id, url, check_defacement=True, check_ssl=True):
        """Perform comprehensive website check"""
        results = {
            'uptime': None,
            'defacement': None,
            'ssl': None
        }
        
        try:
            # Uptime check
            uptime_result = self._check_uptime(url)
            results['uptime'] = uptime_result
            
            # Store uptime check result
            self._store_check(website_id, 'uptime', uptime_result)
            
            # Defacement check (only if website is online)
            if check_defacement and uptime_result['status'] == 'success':
                defacement_result = self._check_defacement(website_id, url)
                results['defacement'] = defacement_result
                # Store defacement check result (whether incident or not)
                if defacement_result.get('status') in ['defacement_detected', 'no_change', 'baseline_created']:
                    self._store_check(website_id, 'defacement', defacement_result)
            
            # SSL check (only for HTTPS)
            if check_ssl and url.startswith('https://'):
                ssl_result = self._check_ssl_certificate(url)
                results['ssl'] = ssl_result
                if ssl_result:
                    self._store_ssl_certificate(website_id, ssl_result)
            
            return results
            
        except Exception as e:
            logger.error(f"Error checking website {url}: {str(e)}")
            return results
    
    def _check_uptime(self, url):
        """Check website availability and response time"""
        start_time = datetime.now()
        
        try:
            response = requests.get(
                url,
                timeout=self.timeout,
                allow_redirects=True,
                headers={'User-Agent': 'WebGuard/1.0'}
            )
            
            response_time = int((datetime.now() - start_time).total_seconds() * 1000)
            
            status_code = response.status_code
            
            # Classify status codes:
            # 200-299: Success (online)
            # 300-499: Warning (client errors, redirects - site responding but issues)
            # 500-599: Failure (server errors - site is down/offline)
            if 200 <= status_code < 300:
                return {
                    'status': 'success',
                    'response_time': response_time,
                    'http_status_code': status_code,
                    'checked_at': datetime.now().isoformat()
                }
            elif 300 <= status_code < 500:
                # Client errors (4xx) or redirects (3xx) - warning but not offline
                return {
                    'status': 'warning',
                    'response_time': response_time,
                    'http_status_code': status_code,
                    'error_message': f'HTTP {status_code}',
                    'checked_at': datetime.now().isoformat()
                }
            else:
                # Server errors (5xx) - considered offline
                return {
                    'status': 'failure',
                    'response_time': response_time,
                    'http_status_code': status_code,
                    'error_message': f'HTTP {status_code} - Server Error',
                    'checked_at': datetime.now().isoformat()
                }
                
        except requests.exceptions.Timeout:
            return {
                'status': 'failure',
                'response_time': None,
                'error_message': 'Request timeout',
                'checked_at': datetime.now().isoformat()
            }
        except requests.exceptions.ConnectionError:
            return {
                'status': 'failure',
                'response_time': None,
                'error_message': 'Connection error',
                'checked_at': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'status': 'failure',
                'response_time': None,
                'error_message': str(e),
                'checked_at': datetime.now().isoformat()
            }
    
    def _check_defacement(self, website_id, url):
        """Check for website defacement by comparing content hash"""
        try:
            response = requests.get(
                url,
                timeout=self.timeout,
                allow_redirects=True,
                headers={'User-Agent': 'WebGuard/1.0'}
            )
            
            if response.status_code != 200:
                return {'status': 'skipped', 'reason': f'HTTP {response.status_code}'}
            
            # Get current content
            soup = BeautifulSoup(response.text, 'html.parser')
            content = soup.get_text()
            current_hash = hashlib.md5(content.encode()).hexdigest()
            
            # Get baseline
            baseline = self._get_baseline(website_id)
            
            if not baseline:
                # First check - store baseline
                self._store_baseline(website_id, current_hash)
                return {'status': 'baseline_created', 'hash': current_hash}
            
            # Compare with baseline
            if current_hash != baseline['content_hash']:
                # Potential defacement detected
                incident = self._create_incident(
                    website_id,
                    'defacement',
                    'high',
                    'Content hash mismatch detected'
                )
                return {
                    'status': 'defacement_detected',
                    'baseline_hash': baseline['content_hash'],
                    'current_hash': current_hash,
                    'incident': incident
                }
            else:
                # If previously defaced, resolve the incident when content matches baseline
                self._resolve_defacement_incident(website_id)
                return {'status': 'no_change', 'hash': current_hash}
                
        except Exception as e:
            logger.error(f"Error checking defacement for {url}: {str(e)}")
            return {'status': 'error', 'error_message': str(e)}
    
    def _check_ssl_certificate(self, url):
        """Extract and analyze SSL certificate"""
        try:
            hostname = url.replace('https://', '').split('/')[0].split(':')[0]
            port = 443
            
            # Create SSL context
            context = ssl.create_default_context()
            
            with socket.create_connection((hostname, port), timeout=self.timeout) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert_der = ssock.getpeercert(binary_form=True)
                    cert = x509.load_der_x509_certificate(cert_der, default_backend())
                    
                    # Extract certificate information
                    issuer = cert.issuer.rfc4514_string()
                    subject = cert.subject.rfc4514_string()
                    valid_from = cert.not_valid_before.date()
                    valid_to = cert.not_valid_after.date()
                    
                    # Calculate days until expiry
                    days_until_expiry = (valid_to - datetime.now().date()).days
                    
                    return {
                        'issuer': issuer,
                        'subject': subject,
                        'valid_from': valid_from.isoformat(),
                        'valid_to': valid_to.isoformat(),
                        'days_until_expiry': days_until_expiry,
                        'checked_at': datetime.now().isoformat()
                    }
                    
        except Exception as e:
            logger.error(f"Error checking SSL certificate for {url}: {str(e)}")
            return None
    
    def _get_baseline(self, website_id):
        """Get defacement baseline for website"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT content_hash, content_selector, captured_at
                FROM defacement_baselines
                WHERE website_id = ?
                ORDER BY captured_at DESC
                LIMIT 1
            ''', (website_id,))
            row = cursor.fetchone()
            if row:
                return {
                    'content_hash': row['content_hash'],
                    'content_selector': row['content_selector'],
                    'captured_at': row['captured_at']
                }
            return None
    
    def _store_baseline(self, website_id, content_hash, content_selector=None):
        """Store defacement baseline"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO defacement_baselines (website_id, content_hash, content_selector)
                VALUES (?, ?, ?)
            ''', (website_id, content_hash, content_selector))
            conn.commit()
    
    def _store_check(self, website_id, check_type, result):
        """Store monitoring check result"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            # For defacement checks, map status appropriately for database
            status = result.get('status', 'unknown')
            if check_type == 'defacement':
                if status == 'defacement_detected':
                    db_status = 'failure'  # Mark as failure to indicate issue
                elif status == 'no_change':
                    db_status = 'success'  # No change = success
                elif status == 'baseline_created':
                    db_status = 'success'  # Baseline created = success
                else:
                    db_status = status
            else:
                db_status = status
            
            cursor.execute('''
                INSERT INTO monitoring_checks 
                (website_id, check_type, status, response_time, http_status_code, error_message)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                website_id,
                check_type,
                db_status,
                result.get('response_time'),
                result.get('http_status_code'),
                result.get('error_message')
            ))
            conn.commit()
    
    def _store_ssl_certificate(self, website_id, ssl_data):
        """Store SSL certificate information"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            # Delete old certificate record
            cursor.execute('DELETE FROM ssl_certificates WHERE website_id = ?', (website_id,))
            # Insert new record
            cursor.execute('''
                INSERT INTO ssl_certificates 
                (website_id, issuer, subject, valid_from, valid_to, days_until_expiry)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                website_id,
                ssl_data['issuer'],
                ssl_data['subject'],
                ssl_data['valid_from'],
                ssl_data['valid_to'],
                ssl_data['days_until_expiry']
            ))
            conn.commit()
    
    def _create_incident(self, website_id, incident_type, severity, description):
        """Create incident record"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO incidents (website_id, incident_type, severity, description)
                VALUES (?, ?, ?, ?)
            ''', (website_id, incident_type, severity, description))
            conn.commit()
            return cursor.lastrowid

    def _resolve_defacement_incident(self, website_id):
        """Mark the latest defacement incident as resolved if one exists."""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE incidents
                    SET resolved_at = ?
                    WHERE incident_id = (
                        SELECT incident_id
                        FROM incidents
                        WHERE website_id = ? AND incident_type = 'defacement' AND resolved_at IS NULL
                        ORDER BY detected_at DESC
                        LIMIT 1
                    )
                ''', (datetime.now().isoformat(), website_id))
                conn.commit()
        except Exception as e:
            logger.error(f"Error resolving defacement incident for website {website_id}: {str(e)}")

