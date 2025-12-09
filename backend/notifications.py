import logging
import asyncio
from datetime import datetime, timedelta
from telegram import Bot
from telegram.error import TelegramError
from database import Database
from config import Config
import threading

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self):
        self.db = Database()
        self.bot_token = Config.TELEGRAM_BOT_TOKEN
        self.chat_id = Config.TELEGRAM_CHAT_ID
        self.cooldown = Config.NOTIFICATION_COOLDOWN
        self.bot = None
        self._loop = None
        self._loop_thread = None
        self._lock = threading.Lock()
        
        if self.bot_token:
            try:
                self.bot = Bot(token=self.bot_token)
                # Create a dedicated event loop in a background thread for async operations
                self._start_event_loop()
            except Exception as e:
                logger.error(f"Failed to initialize Telegram bot: {str(e)}")
    
    def _start_event_loop(self):
        """Start a dedicated event loop in a background thread"""
        def run_loop():
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            self._loop.run_forever()
        
        self._loop_thread = threading.Thread(target=run_loop, daemon=True)
        self._loop_thread.start()
        # Wait a bit for loop to start
        import time
        time.sleep(0.1)
    
    def _run_async(self, coro):
        """Run async function in the dedicated event loop"""
        if self._loop is None or not self._loop.is_running():
            # Fallback to asyncio.run if loop not available
            return asyncio.run(coro)
        
        future = asyncio.run_coroutine_threadsafe(coro, self._loop)
        return future.result(timeout=10)  # 10 second timeout
    
    def send_notification(self, website_id, incident_type, severity, message, website_url=None, website_name=None):
        """Send notification via configured channels"""
        if not self.bot or not self.chat_id:
            logger.warning("Telegram not configured, skipping notification")
            return False
        
        # Check cooldown to prevent spam
        if self._should_suppress_notification(website_id, incident_type):
            logger.info(f"Notification suppressed due to cooldown for website {website_id}, incident {incident_type}")
            return False
        
        try:
            # Format message
            formatted_message = self._format_message(
                incident_type, severity, message, website_url, website_name
            )
            
            logger.debug(f"Sending Telegram message to chat_id: {self.chat_id}")
            
            # Send via Telegram - python-telegram-bot v20+ requires async/await
            with self._lock:
                try:
                    result = self._run_async(self.bot.send_message(
                        chat_id=self.chat_id,
                        text=formatted_message,
                        parse_mode='HTML'
                    ))
                    logger.debug(f"Telegram message sent, message_id: {result.message_id if result else 'None'}")
                except Exception as html_error:
                    logger.warning(f"HTML parse mode failed: {html_error}, trying without HTML")
                    plain_message = formatted_message.replace('<b>', '').replace('</b>', '').replace('<i>', '').replace('</i>', '')
                    result = self._run_async(self.bot.send_message(
                        chat_id=self.chat_id,
                        text=plain_message
                    ))
                    logger.debug(f"Telegram message sent (plain), message_id: {result.message_id if result else 'None'}")
            
            # Record notification
            self._record_notification(website_id, incident_type, 'telegram', 'sent')
            
            logger.info(f"Notification sent successfully for website {website_id}: {incident_type}")
            return True
            
        except TelegramError as e:
            logger.error(f"Telegram API error: {str(e)}")
            self._record_notification(website_id, incident_type, 'telegram', 'failed')
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending notification: {str(e)}", exc_info=True)
            return False
    
    def _format_message(self, incident_type, severity, message, website_url, website_name):
        """Format notification message"""
        emoji_map = {
            'downtime': '🔴',
            'defacement': '⚠️',
            'ssl_expiry': '🔒',
            'critical': '🚨',
            'high': '⚠️',
            'medium': '⚡',
            'low': 'ℹ️'
        }
        
        incident_emoji = emoji_map.get(incident_type, '📢')
        severity_emoji = emoji_map.get(severity, '')
        
        formatted = f"{incident_emoji} <b>WebGuard Alert</b>\n\n"
        formatted += f"<b>Type:</b> {incident_type.replace('_', ' ').title()}\n"
        if severity_emoji:
            formatted += f"<b>Severity:</b> {severity_emoji} {severity.title()}\n\n"
        else:
            formatted += f"<b>Severity:</b> {severity.title()}\n\n"
        
        if website_name:
            formatted += f"<b>Website:</b> {website_name}\n"
        if website_url:
            formatted += f"<b>URL:</b> {website_url}\n"
        
        formatted += f"\n<b>Details:</b>\n{message}\n\n"
        formatted += f"<i>Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>"
        
        return formatted
    
    def _should_suppress_notification(self, website_id, incident_type):
        """Check if notification should be suppressed due to cooldown"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cutoff_time = datetime.now() - timedelta(seconds=self.cooldown)
            
            cursor.execute('''
                SELECT COUNT(*) as count
                FROM notifications n
                JOIN incidents i ON n.incident_id = i.incident_id
                WHERE i.website_id = ? 
                AND i.incident_type = ?
                AND n.sent_at > ?
            ''', (website_id, incident_type, cutoff_time.isoformat()))
            
            result = cursor.fetchone()
            return result['count'] > 0 if result else False
    
    def _record_notification(self, website_id, incident_type, channel, status):
        """Record notification in database"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                # Get most recent incident for this website and type
                cursor.execute('''
                    SELECT incident_id
                    FROM incidents
                    WHERE website_id = ? AND incident_type = ?
                    ORDER BY detected_at DESC
                    LIMIT 1
                ''', (website_id, incident_type))
                
                incident = cursor.fetchone()
                if incident:
                    cursor.execute('''
                        INSERT INTO notifications (incident_id, notification_channel, delivery_status)
                        VALUES (?, ?, ?)
                    ''', (incident['incident_id'], channel, status))
                    conn.commit()
        except Exception as e:
            logger.error(f"Error recording notification: {str(e)}")

