import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from database import Database
from monitoring import MonitoringEngine
from notifications import NotificationService
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MonitoringScheduler:
    def __init__(self):
        self.db = Database()
        self.monitoring_engine = MonitoringEngine()
        self.notification_service = NotificationService()
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        logger.info("Monitoring scheduler initialized")
    
    def start_monitoring(self, website_id):
        """Start monitoring a website"""
        website = self._get_website(website_id)
        if not website:
            logger.error(f"Website {website_id} not found")
            return
        
        if not website['monitoring_enabled']:
            logger.info(f"Monitoring disabled for website {website_id}")
            return
        
        interval = max(website['check_interval'], Config.MIN_CHECK_INTERVAL)
        
        # Add job to scheduler
        job_id = f"website_{website_id}"
        self.scheduler.add_job(
            func=self._check_website_job,
            trigger=IntervalTrigger(seconds=interval),
            id=job_id,
            args=[website_id],
            replace_existing=True
        )
        
        logger.info(f"Started monitoring website {website_id} with interval {interval}s")
    
    def stop_monitoring(self, website_id):
        """Stop monitoring a website"""
        job_id = f"website_{website_id}"
        try:
            self.scheduler.remove_job(job_id)
            logger.info(f"Stopped monitoring website {website_id}")
        except Exception as e:
            logger.error(f"Error stopping monitoring for website {website_id}: {str(e)}")
    
    def _check_website_job(self, website_id):
        """Job function to check a website"""
        try:
            website = self._get_website(website_id)
            if not website or not website['monitoring_enabled']:
                return
            
            logger.info(f"Checking website {website_id}: {website['url']}")
            
            # Perform checks
            results = self.monitoring_engine.check_website(
                website_id,
                website['url'],
                check_defacement=website['defacement_detection_enabled'],
                check_ssl=website['ssl_monitoring_enabled']
            )
            
            # Process results and send notifications
            self._process_results(website_id, website, results)
            
        except Exception as e:
            logger.error(f"Error in monitoring job for website {website_id}: {str(e)}")
    
    def _process_results(self, website_id, website, results):
        """Process monitoring results and trigger notifications"""
        # Check uptime results
        if results.get('uptime'):
            uptime = results['uptime']
            if uptime['status'] == 'failure':
                self.notification_service.send_notification(
                    website_id=website_id,
                    incident_type='downtime',
                    severity='critical',
                    message=f"Website is offline. Error: {uptime.get('error_message', 'Unknown error')}",
                    website_url=website['url'],
                    website_name=website.get('display_name')
                )
        
        # Check defacement results
        if results.get('defacement'):
            defacement = results['defacement']
            logger.info(f"Defacement check result: {defacement.get('status')}")
            if defacement.get('status') == 'defacement_detected':
                logger.info(f"Defacement detected for website {website_id}, sending notification")
                result = self.notification_service.send_notification(
                    website_id=website_id,
                    incident_type='defacement',
                    severity='high',
                    message="Potential website defacement detected. Content hash mismatch.",
                    website_url=website['url'],
                    website_name=website.get('display_name')
                )
                if result:
                    logger.info(f"Notification sent successfully for website {website_id}")
                else:
                    logger.warning(f"Notification failed or was suppressed for website {website_id}")
            else:
                logger.debug(f"No defacement detected (status: {defacement.get('status')})")
        
        # Check SSL results
        if results.get('ssl'):
            ssl_data = results['ssl']
            days_until_expiry = ssl_data.get('days_until_expiry', 999)
            
            # Check if within warning thresholds
            if days_until_expiry in Config.SSL_WARNING_THRESHOLDS or days_until_expiry < 0:
                severity = 'critical' if days_until_expiry < 0 else 'high' if days_until_expiry <= 7 else 'medium'
                message = f"SSL certificate expires in {days_until_expiry} days" if days_until_expiry >= 0 else "SSL certificate has expired"
                
                self.notification_service.send_notification(
                    website_id=website_id,
                    incident_type='ssl_expiry',
                    severity=severity,
                    message=message,
                    website_url=website['url'],
                    website_name=website.get('display_name')
                )
    
    def _get_website(self, website_id):
        """Get website from database"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM websites WHERE website_id = ?', (website_id,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None
    
    def start_all_monitoring(self):
        """Start monitoring all enabled websites"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT website_id FROM websites WHERE monitoring_enabled = 1')
            websites = cursor.fetchall()
            
            for website in websites:
                self.start_monitoring(website['website_id'])
        
        logger.info(f"Started monitoring {len(websites)} websites")
    
    def shutdown(self):
        """Shutdown scheduler"""
        self.scheduler.shutdown()
        logger.info("Monitoring scheduler shut down")

