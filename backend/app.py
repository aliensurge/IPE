from flask import Flask, request, jsonify
from flask_cors import CORS
from database import Database
from monitoring import MonitoringEngine
from scheduler import MonitoringScheduler
from config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

db = Database()
monitoring_engine = MonitoringEngine()
scheduler = MonitoringScheduler()

# Start monitoring all enabled websites on startup
scheduler.start_all_monitoring()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'WebGuard API'})

@app.route('/api/notifications/test', methods=['POST'])
def test_notification():
    """Send a test Telegram notification to verify bot config"""
    try:
        sent = scheduler.notification_service.send_notification(
            website_id=0,
            incident_type='downtime',
            severity='low',
            message='Test notification from WebGuard',
            website_url='test.local',
            website_name='WebGuard Test'
        )
        if sent:
            return jsonify({'status': 'success', 'message': 'Test notification sent'}), 200
        return jsonify({'status': 'error', 'message': 'Failed to send test notification (check token/chat id or cooldown)'}), 500
    except Exception as e:
        logger.error(f"Error sending test notification: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/websites', methods=['GET'])
def get_websites():
    """Get all monitored websites"""
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM websites ORDER BY created_at DESC')
            websites = [dict(row) for row in cursor.fetchall()]
            
            # Get latest status for each website
            for website in websites:
                website['status'] = get_website_status(website['website_id'])
                website['ssl_info'] = get_ssl_info(website['website_id'])
                website['defacement_status'] = get_defacement_status(website['website_id'])
            
            return jsonify({'status': 'success', 'data': websites})
    except Exception as e:
        logger.error(f"Error getting websites: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/websites', methods=['POST'])
def add_website():
    """Add a new website for monitoring"""
    try:
        data = request.json
        url = data.get('url', '').strip()
        display_name = data.get('display_name', '').strip()
        check_interval = data.get('check_interval', Config.DEFAULT_CHECK_INTERVAL)
        
        if not url:
            return jsonify({'status': 'error', 'message': 'URL is required'}), 400
        
        # Validate URL format
        if not (url.startswith('http://') or url.startswith('https://')):
            return jsonify({'status': 'error', 'message': 'URL must start with http:// or https://'}), 400
        
        # Check if URL already exists
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT website_id FROM websites WHERE url = ?', (url,))
            if cursor.fetchone():
                return jsonify({'status': 'error', 'message': 'Website already registered'}), 400
        
        # Perform initial check - allow down sites to be added for monitoring
        initial_check = monitoring_engine._check_uptime(url)
        warning_message = None
        if initial_check['status'] == 'failure':
            warning_message = f"Website appears to be down: {initial_check.get('error_message', 'Unknown error')}. It will still be added for monitoring."
            logger.warning(f"Adding website {url} that is currently down: {initial_check.get('error_message')}")
        
        # Insert website
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO websites (url, display_name, check_interval, 
                                    defacement_detection_enabled, ssl_monitoring_enabled)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                url,
                display_name or url,
                max(check_interval, Config.MIN_CHECK_INTERVAL),
                1,  # defacement enabled
                1 if url.startswith('https://') else 0  # SSL monitoring for HTTPS only
            ))
            website_id = cursor.lastrowid
            conn.commit()
        
        # Capture baseline for defacement detection (only if site is accessible)
        if initial_check['status'] == 'success':
            if url.startswith('https://') or url.startswith('http://'):
                try:
                    monitoring_engine.check_website(website_id, url, check_defacement=True, check_ssl=True)
                except Exception as e:
                    logger.warning(f"Error capturing baseline for {url}: {str(e)}")
        else:
            # Site is down, but still store the initial check result
            try:
                monitoring_engine._store_check(website_id, 'uptime', initial_check)
            except Exception as e:
                logger.warning(f"Error storing initial check for {url}: {str(e)}")
        
        # Start monitoring (will check periodically even if site is currently down)
        scheduler.start_monitoring(website_id)
        
        response_message = 'Website added successfully'
        if warning_message:
            response_message += f'. Note: {warning_message}'
        
        return jsonify({
            'status': 'success',
            'message': response_message,
            'data': {'website_id': website_id},
            'warning': warning_message
        }), 201
        
    except Exception as e:
        logger.error(f"Error adding website: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/websites/<int:website_id>', methods=['GET'])
def get_website(website_id):
    """Get specific website details"""
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM websites WHERE website_id = ?', (website_id,))
            row = cursor.fetchone()
            
            if not row:
                return jsonify({'status': 'error', 'message': 'Website not found'}), 404
            
            website = dict(row)
            website['status'] = get_website_status(website_id)
            website['ssl_info'] = get_ssl_info(website_id)
            
            return jsonify({'status': 'success', 'data': website})
    except Exception as e:
        logger.error(f"Error getting website: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/websites/<int:website_id>', methods=['DELETE'])
def delete_website(website_id):
    """Delete a website from monitoring"""
    try:
        # Stop monitoring
        scheduler.stop_monitoring(website_id)
        
        # Delete from database (cascade will handle related records)
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM websites WHERE website_id = ?', (website_id,))
            conn.commit()
            
            if cursor.rowcount == 0:
                return jsonify({'status': 'error', 'message': 'Website not found'}), 404
        
        return jsonify({'status': 'success', 'message': 'Website deleted successfully'})
    except Exception as e:
        logger.error(f"Error deleting website: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/websites/<int:website_id>/check', methods=['POST'])
def trigger_check(website_id):
    """Manually trigger a monitoring check"""
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM websites WHERE website_id = ?', (website_id,))
            row = cursor.fetchone()
            
            if not row:
                return jsonify({'status': 'error', 'message': 'Website not found'}), 404
            
            website = dict(row)
            results = monitoring_engine.check_website(
                website_id,
                website['url'],
                check_defacement=website['defacement_detection_enabled'],
                check_ssl=website['ssl_monitoring_enabled']
            )

            # Process results to trigger notifications
            try:
                scheduler._process_results(website_id, website, results)
            except Exception as e:
                logger.error(f"Error processing results for manual check: {str(e)}", exc_info=True)
            
            return jsonify({'status': 'success', 'data': results})
    except Exception as e:
        logger.error(f"Error triggering check: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/websites/<int:website_id>/defacement/false-positive', methods=['POST'])
def mark_false_positive(website_id):
    """Mark defacement as false positive and update baseline"""
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM websites WHERE website_id = ?', (website_id,))
            row = cursor.fetchone()
            
            if not row:
                return jsonify({'status': 'error', 'message': 'Website not found'}), 404
            
            website = dict(row)
            
            # Get current content and create new baseline
            import requests
            from bs4 import BeautifulSoup
            import hashlib
            
            response = requests.get(
                website['url'],
                timeout=30,
                allow_redirects=True,
                headers={'User-Agent': 'WebGuard/1.0'}
            )
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                content = soup.get_text()
                new_hash = hashlib.md5(content.encode()).hexdigest()
                
                # Update baseline
                cursor.execute('''
                    INSERT INTO defacement_baselines (website_id, content_hash, content_selector)
                    VALUES (?, ?, ?)
                ''', (website_id, new_hash, None))
                
                # Resolve all open defacement incidents
                cursor.execute('''
                    UPDATE incidents
                    SET resolved_at = CURRENT_TIMESTAMP
                    WHERE website_id = ? 
                    AND incident_type = 'defacement'
                    AND resolved_at IS NULL
                ''', (website_id,))
                
                conn.commit()
                
                logger.info(f"Updated baseline for website {website_id} and resolved defacement incidents")
                
                return jsonify({
                    'status': 'success',
                    'message': 'Baseline updated and defacement incidents resolved'
                })
            else:
                return jsonify({
                    'status': 'error',
                    'message': f'Cannot fetch website content: HTTP {response.status_code}'
                }), 400
                
    except Exception as e:
        logger.error(f"Error marking false positive: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/websites/<int:website_id>/checks', methods=['GET'])
def get_checks(website_id):
    """Get monitoring check history for a website"""
    try:
        limit = request.args.get('limit', 100, type=int)
        
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM monitoring_checks
                WHERE website_id = ?
                ORDER BY checked_at DESC
                LIMIT ?
            ''', (website_id, limit))
            
            checks = [dict(row) for row in cursor.fetchall()]
            return jsonify({'status': 'success', 'data': checks})
    except Exception as e:
        logger.error(f"Error getting checks: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/stats/overview', methods=['GET'])
def get_overview_stats():
    """Get dashboard overview statistics"""
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Total websites
            cursor.execute('SELECT COUNT(*) as count FROM websites')
            total = cursor.fetchone()['count']
            
            # Get status counts
            cursor.execute('SELECT website_id FROM websites')
            websites = cursor.fetchall()
            
            online = 0
            warning = 0
            offline = 0
            
            for website in websites:
                status = get_website_status(website['website_id'])
                if status == 'online':
                    online += 1
                elif status == 'warning':
                    warning += 1
                else:
                    offline += 1
            
            return jsonify({
                'status': 'success',
                'data': {
                    'total': total,
                    'online': online,
                    'warning': warning,
                    'offline': offline
                }
            })
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

def get_website_status(website_id):
    """Get current status of a website"""
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT status FROM monitoring_checks
                WHERE website_id = ? AND check_type = 'uptime'
                ORDER BY checked_at DESC
                LIMIT 1
            ''', (website_id,))
            
            row = cursor.fetchone()
            if row:
                status = row['status']
                if status == 'success':
                    return 'online'
                elif status == 'warning':
                    return 'warning'
                else:
                    return 'offline'
            return 'unknown'
    except Exception as e:
        logger.error(f"Error getting website status: {str(e)}")
        return 'unknown'

def get_ssl_info(website_id):
    """Get SSL certificate information"""
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM ssl_certificates
                WHERE website_id = ?
                ORDER BY last_checked DESC
                LIMIT 1
            ''', (website_id,))
            
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None
    except Exception as e:
        logger.error(f"Error getting SSL info: {str(e)}")
        return None

def get_defacement_status(website_id):
    """Get defacement status for a website"""
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Check if there's a recent defacement incident
            cursor.execute('''
                SELECT incident_id, detected_at, resolved_at
                FROM incidents
                WHERE website_id = ? AND incident_type = 'defacement'
                ORDER BY detected_at DESC
                LIMIT 1
            ''', (website_id,))
            
            incident = cursor.fetchone()
            
            if incident:
                # If incident exists and not resolved, defacement detected
                if not incident['resolved_at']:
                    return {
                        'status': 'defacement_detected',
                        'detected_at': incident['detected_at'],
                        'has_incident': True
                    }
                else:
                    # Incident was resolved
                    return {
                        'status': 'clean',
                        'last_incident': incident['detected_at'],
                        'resolved_at': incident['resolved_at'],
                        'has_incident': False
                    }
            
            # Check if baseline exists (means defacement monitoring is active)
            cursor.execute('''
                SELECT COUNT(*) as count
                FROM defacement_baselines
                WHERE website_id = ?
            ''', (website_id,))
            
            baseline = cursor.fetchone()
            if baseline and baseline['count'] > 0:
                # Baseline exists, no incidents = clean
                return {
                    'status': 'clean',
                    'has_incident': False
                }
            
            # No baseline yet (first check pending)
            return {
                'status': 'pending',
                'has_incident': False
            }
            
    except Exception as e:
        logger.error(f"Error getting defacement status: {str(e)}")
        return {
            'status': 'unknown',
            'has_incident': False
        }

if __name__ == '__main__':
    logger.info(f"Starting WebGuard API server on {Config.FLASK_HOST}:{Config.FLASK_PORT}")
    app.run(host=Config.FLASK_HOST, port=Config.FLASK_PORT, debug=Config.DEBUG)

