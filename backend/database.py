import sqlite3
import os
from datetime import datetime
from contextlib import contextmanager
from config import Config

class Database:
    def __init__(self, db_path=None):
        self.db_path = db_path or Config.DATABASE_PATH
        self._ensure_db_directory()
        self._init_database()
    
    def _ensure_db_directory(self):
        """Ensure the database directory exists"""
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
    
    def _init_database(self):
        """Initialize database schema"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Websites table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS websites (
                    website_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL UNIQUE,
                    display_name TEXT,
                    monitoring_enabled BOOLEAN DEFAULT 1,
                    check_interval INTEGER DEFAULT 300,
                    defacement_detection_enabled BOOLEAN DEFAULT 1,
                    ssl_monitoring_enabled BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Monitoring checks table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS monitoring_checks (
                    check_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    website_id INTEGER NOT NULL,
                    check_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    response_time INTEGER,
                    http_status_code INTEGER,
                    error_message TEXT,
                    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (website_id) REFERENCES websites(website_id)
                )
            ''')
            
            # SSL certificates table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ssl_certificates (
                    certificate_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    website_id INTEGER NOT NULL,
                    issuer TEXT,
                    subject TEXT,
                    valid_from DATE,
                    valid_to DATE,
                    days_until_expiry INTEGER,
                    last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (website_id) REFERENCES websites(website_id)
                )
            ''')
            
            # Defacement baselines table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS defacement_baselines (
                    baseline_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    website_id INTEGER NOT NULL,
                    content_hash TEXT NOT NULL,
                    content_selector TEXT,
                    captured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (website_id) REFERENCES websites(website_id)
                )
            ''')
            
            # Incidents table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS incidents (
                    incident_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    website_id INTEGER NOT NULL,
                    incident_type TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    resolved_at TIMESTAMP,
                    description TEXT,
                    FOREIGN KEY (website_id) REFERENCES websites(website_id)
                )
            ''')
            
            # Notifications table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS notifications (
                    notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    incident_id INTEGER,
                    notification_channel TEXT NOT NULL,
                    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    delivery_status TEXT DEFAULT 'pending',
                    FOREIGN KEY (incident_id) REFERENCES incidents(incident_id)
                )
            ''')
            
            # Create indexes
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_checks_website ON monitoring_checks(website_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_checks_time ON monitoring_checks(checked_at)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_incidents_website ON incidents(website_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_incidents_time ON incidents(detected_at)')
            
            conn.commit()
    
    @contextmanager
    def get_connection(self):
        """Get database connection with proper cleanup"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        try:
            yield conn
        finally:
            conn.close()
    
    def execute_query(self, query, params=()):
        """Execute a query and return results"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.fetchall()
    
    def execute_one(self, query, params=()):
        """Execute a query and return single result"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.fetchone()

