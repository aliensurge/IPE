#!/usr/bin/env python3
"""
WebGuard Backend Server
Run this script to start the monitoring API server
"""

import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from config import Config
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.info(f"Starting WebGuard API server on {Config.FLASK_HOST}:{Config.FLASK_PORT}")
    logger.info(f"Database: {Config.DATABASE_PATH}")
    logger.info(f"Debug mode: {Config.DEBUG}")
    
    app.run(
        host=Config.FLASK_HOST,
        port=Config.FLASK_PORT,
        debug=Config.DEBUG
    )

