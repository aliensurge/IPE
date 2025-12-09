# WebGuard: Local Security Monitoring Platform - Development Report

## Project Overview
WebGuard is a lightweight website monitoring platform designed to help small businesses detect website defacement, downtime, and SSL certificate expiry through automated checks and real-time alerting. The system consists of a Python-based backend monitoring engine and a React-based web dashboard.

## Technology Stack

### Backend
- **Language**: Python 3.11+
- **Web Framework**: Flask 3.0.0
- **Task Scheduler**: APScheduler 3.10.4
- **HTTP Client**: Requests 2.31.0
- **Content Parsing**: BeautifulSoup4 4.12.2
- **SSL Handling**: Cryptography 41.0.7
- **Notifications**: Python-Telegram-Bot 20.7
- **Database**: SQLite (via sqlite3)

### Frontend
- **Framework**: React 18.2.0
- **Language**: TypeScript 5.2.2
- **Build Tool**: Vite 5.0.8
- **Styling**: Tailwind CSS 3.3.6
- **Icons**: Lucide React 0.294.0
- **HTTP Client**: Axios 1.5.0

## Project Setup

### Initial Setup
- Project initialized with Vite + React + TypeScript template
- Dependencies installed and configured
- Development server configured to run on `http://localhost:5173`

## Development Timeline

### Phase 1: Project Initialization ✅
- [x] Project structure created
- [x] Dependencies installed
- [x] Development environment configured
- [x] Git repository initialized
- [x] GitHub repository connected

### Phase 2: Backend Development ✅
- [x] Database schema design and implementation
- [x] Flask REST API server setup
- [x] Monitoring engine development (uptime, defacement, SSL)
- [x] Task scheduler implementation (APScheduler)
- [x] Telegram notification service
- [x] API endpoints for website management
- [x] Configuration management system

### Phase 3: Frontend Development ✅
- [x] React dashboard component
- [x] API service integration (Axios)
- [x] Real-time data fetching and display
- [x] Website add/delete functionality
- [x] Status visualization
- [x] Error handling and user feedback

### Phase 4: Integration & Testing 🔄
- [ ] End-to-end testing
- [ ] Performance testing
- [ ] Documentation completion

---

## Features Implemented

### Core Features ✅

1. **Website Registration & Management**
   - Add websites for monitoring via web interface
   - URL validation and accessibility checking
   - Display name customization
   - Delete websites from monitoring

2. **Uptime Monitoring**
   - Automated periodic availability checks (configurable intervals)
   - Response time measurement
   - HTTP status code tracking
   - Downtime detection and logging

3. **Defacement Detection**
   - Baseline content capture on registration
   - Hash-based content comparison (MD5)
   - Automatic detection of unauthorized content changes
   - Incident creation and alerting

4. **SSL Certificate Monitoring**
   - Automatic certificate information extraction
   - Expiry date calculation
   - Configurable warning thresholds (30, 14, 7 days, expired)
   - Certificate details storage

5. **Real-Time Dashboard**
   - Overview statistics (total, online, warning, offline)
   - Website status table with real-time updates
   - Response time display
   - SSL certificate expiry countdown
   - Defacement status column with visual indicators (green/red/yellow)
   - Manual check triggers
   - False positive marking for defacement alerts
   - Auto-refresh every 5 seconds
   - Alert banners for defacement incidents

6. **Telegram Notifications**
   - Instant alerts for downtime incidents
   - Defacement detection notifications
   - SSL certificate expiry warnings
   - Formatted messages with severity indicators
   - Notification deduplication (5-minute cooldown)

7. **Database Storage**
   - SQLite database for local data storage
   - Monitoring check history
   - Incident tracking
   - SSL certificate records
   - Defacement baselines

8. **Test Sites for Demonstrations**
   - **Defacement Demo Site** (`backend/test_site.py` on port 8001)
     - Toggle button to simulate defacement and restore state
     - Used for validating hash-based detection end-to-end
   - **Uptime/Downtime Demo Site** (`backend/test_site_uptime.py` on port 8002)
     - Toggle button to simulate downtime (503) and restore service (200)
     - Used for testing downtime detection and notifications

---

## Technical Decisions

### Why Vite?
- Fast development server with HMR (Hot Module Replacement)
- Optimized production builds
- Excellent TypeScript support

### Why Tailwind CSS?
- Utility-first CSS framework
- Rapid UI development
- Consistent design system

---

## Challenges & Solutions

### Challenge 1: Real-Time Data Synchronization
**Problem**: Frontend needed to display up-to-date monitoring status without manual refresh.

**Solution**: Implemented polling mechanism with 5-second intervals. The dashboard automatically fetches latest data from the API, ensuring real-time status visibility.

### Challenge 2: Content Hash False Positives
**Problem**: Websites with dynamic content (timestamps, ads) caused frequent false defacement alerts.

**Solution**: Implemented baseline capture system that stores initial content hash. Future enhancement: Content selector support to focus monitoring on static sections.

### Challenge 3: Database Concurrency
**Problem**: SQLite write locks when multiple monitoring checks run simultaneously.

**Solution**: Implemented proper transaction management and connection pooling. Write operations are properly serialized to prevent conflicts.

### Challenge 4: Notification Spam Prevention
**Problem**: Rapid status changes could result in notification flooding.

**Solution**: Implemented 5-minute cooldown period preventing duplicate notifications for the same incident type on the same website.

### Challenge 5: Telegram Bot Async/Await Issue
**Problem**: `python-telegram-bot` v20+ uses async/await, but the notification service was calling it synchronously, causing `'coroutine' object has no attribute 'message_id'` errors.

**Solution**: Wrapped `bot.send_message()` calls with `asyncio.run()` to properly await the async function, enabling successful Telegram notification delivery.

---

## Future Enhancements

### Planned Features
- [ ] Content selector support for defacement detection (CSS selectors)
- [ ] Historical data visualization (charts and graphs)
- [ ] Email notification support (in addition to Telegram)
- [ ] Multi-user authentication system
- [ ] Advanced filtering and search
- [ ] Export functionality (CSV, JSON)
- [ ] Uptime percentage calculation from check history
- [ ] Response time trend analysis

### Technical Improvements
- [ ] Automated system restart on crash (systemd service)
- [ ] Database migration system
- [ ] API rate limiting
- [ ] HTTPS support for dashboard
- [ ] Docker containerization
- [ ] Cloud deployment option (optional)

---

## Build & Deployment

### Development Setup

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python app.py
```

**Frontend:**
```bash
npm install
npm run dev
```

### Production Build

**Frontend:**
```bash
npm run build
```

**Backend:**
- Set `DEBUG=False` in `.env`
- Use production WSGI server (Gunicorn)
- Configure reverse proxy (nginx) for HTTPS
- Set up systemd service for auto-start

### Running the Complete System

1. Start backend server: `cd backend && python app.py`
2. Start frontend dev server: `npm run dev`
3. Access dashboard at: `http://localhost:5173`
4. API available at: `http://127.0.0.1:5000/api`

---

## Repository Information
- **Repository URL**: https://github.com/aliensurge/IPE.git
- **GitHub Repository**: https://github.com/aliensurge/IPE
- **Status**: ✅ Connected and synced

---

## Project Structure

```
IPE/
├── backend/                 # Python backend
│   ├── app.py              # Flask API server
│   ├── run.py              # Server entry point
│   ├── config.py           # Configuration management
│   ├── database.py         # Database layer (SQLite)
│   ├── monitoring.py       # Monitoring engine
│   ├── notifications.py    # Telegram notification service
│   ├── scheduler.py        # Task scheduler (APScheduler)
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment variables template
├── src/                    # React frontend
│   ├── components/         # React components
│   │   └── WebsiteMonitoringDashboard.tsx
│   ├── services/          # API service layer
│   │   └── api.ts
│   └── ...
├── docs/                   # Project documentation
│   ├── abstract.md
│   ├── chapter1_introduction.md
│   ├── chapter2_literature_review.md
│   ├── chapter3_requirements_analysis.md
│   ├── chapter4_system_design.md
│   ├── chapter5_development.md
│   └── chapter6_testing.md
└── README.md              # Setup and usage instructions
```

## Key Implementation Details

### Monitoring Engine
- Performs HTTP requests with configurable timeout (30s default)
- Calculates response times in milliseconds
- Captures baseline content hash on first check
- Compares subsequent checks against baseline
- Extracts SSL certificate information for HTTPS sites

### Database Schema
- **websites**: Registered websites and configuration
- **monitoring_checks**: Historical check results
- **ssl_certificates**: SSL certificate information
- **defacement_baselines**: Content hash baselines
- **incidents**: Security incidents and alerts
- **notifications**: Notification delivery records

### API Endpoints
- `GET /api/websites` - List all monitored websites
- `POST /api/websites` - Add new website
- `DELETE /api/websites/{id}` - Remove website
- `POST /api/websites/{id}/check` - Trigger manual check
- `GET /api/stats/overview` - Dashboard statistics

## Notes
- System requires both backend and frontend to be running simultaneously
- Database is created automatically on first run
- Telegram notifications are optional but recommended
- All monitoring data is stored locally in SQLite database
- System designed for single-user deployment (authentication not implemented)


