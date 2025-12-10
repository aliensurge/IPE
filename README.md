# WebGuard: Local Security Monitoring Platform

WebGuard is a lightweight website monitoring platform designed to help small businesses detect website defacement, downtime, and SSL certificate expiry through automated checks and real-time alerting.

## Features

- **Uptime Monitoring**: Automated checks to detect website downtime
- **Defacement Detection**: Content hash comparison to detect unauthorized changes
- **SSL Certificate Tracking**: Monitor SSL certificate expiry dates
- **Real-Time Dashboard**: Web-based interface for managing monitored sites
- **Telegram Notifications**: Instant alerts when incidents are detected
- **Local-First Architecture**: All data stored locally, no cloud dependencies

## Technology Stack

### Backend
- Python 3.14+
- Flask (REST API)
- APScheduler (Task scheduling)
- SQLite (Database)
- BeautifulSoup (Content parsing)
- Cryptography (SSL certificate handling)

### Frontend
- React 18
- TypeScript
- Tailwind CSS
- Vite
- Axios

## Prerequisites

- Python 3.11 or higher
- Node.js 18+ and npm
- (Optional) Telegram Bot Token for notifications

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/aliensurge/IPE.git
cd IPE
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from example
copy .env.example .env  # Windows
# cp .env.example .env   # Linux/Mac

# Edit .env file and add your Telegram bot token (optional)
# TELEGRAM_BOT_TOKEN=your-bot-token-here
# TELEGRAM_CHAT_ID=your-chat-id-here
```

### 3. Frontend Setup

```bash
# From project root
npm install
```

## Running the Application

### Start Backend Server

```bash
# From backend directory
cd backend
python app.py
```

The API server will start on `http://127.0.0.1:5000`

### (Optional) Start Local Test Sites

**Defacement Demo Site** (Port 8001):
```bash
# From backend directory
python test_site.py
```
Add `http://127.0.0.1:8001/` to WebGuard. Click "Deface me" to simulate defacement and "Restore original" to revert.

**Uptime/Downtime Demo Site** (Port 8002):
```bash
# From backend directory
python test_site_uptime.py
```
Add `http://127.0.0.1:8002/` to WebGuard. Click "Take Down" to simulate downtime (503) and "Bring Up" to restore service (200).

### Start Frontend Development Server

```bash
# From project root (in a new terminal)
npm run dev
```

The dashboard will be available at `http://localhost:5173`

## Telegram Bot Setup (Optional)

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` and follow instructions to create a bot
3. Copy the bot token
4. Start a chat with your bot and send any message
5. Get your chat ID by visiting: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
6. Add both values to your `.env` file:
   ```
   TELEGRAM_BOT_TOKEN=your-bot-token-here
   TELEGRAM_CHAT_ID=your-chat-id-here
   ```

**Note**: The chat ID should be a number (no quotes). For group chats, use the negative group ID (usually starts with `-100`).

**Testing**: After setup, you can test notifications by visiting: `http://127.0.0.1:5000/api/notifications/test` or using PowerShell:
```powershell
Invoke-WebRequest -Uri http://127.0.0.1:5000/api/notifications/test -Method POST
```

## Usage

1. Open the dashboard at `http://localhost:5173`
2. Click "Add Website" to register a website for monitoring
3. Enter the website URL (must start with http:// or https://)
4. Optionally provide a display name
5. The system will automatically start monitoring the website
6. View real-time status on the dashboard
7. Receive Telegram notifications when incidents are detected

### Testing Defacement Detection

A test website is included for demonstrating defacement detection:

1. Start the test site: `python backend/test_site.py` (runs on port 8001)
2. Add `http://127.0.0.1:8001/` to WebGuard
3. Click "Deface me" on the test site to trigger a defacement alert
4. Click "Restore original" to revert and clear the alert
5. Click "Update" to simulate a legitimate website update (will trigger defacement unless marked as false positive)
6. Use "False Positive" button in dashboard to update baseline for legitimate changes

## Project Structure

```
IPE/
├── backend/                 # Python backend
│   ├── app.py              # Flask API server
│   ├── config.py           # Configuration
│   ├── database.py         # Database layer
│   ├── monitoring.py       # Monitoring engine
│   ├── notifications.py    # Notification service
│   ├── scheduler.py        # Task scheduler
│   └── requirements.txt   # Python dependencies
├── src/                    # React frontend
│   ├── components/         # React components
│   ├── services/          # API service
│   └── ...
```

## Development

### Backend Development

```bash
cd backend
python app.py  # Runs with DEBUG=True by default
```

### Frontend Development

```bash
npm run dev  # Hot reload enabled
```

## Production Build

### Frontend

```bash
npm run build
```

Built files will be in the `dist/` directory.

### Backend

For production deployment:
1. Set `DEBUG=False` in `.env`
2. Use a production WSGI server (e.g., Gunicorn)
3. Configure reverse proxy (nginx) for HTTPS
4. Set up systemd service for auto-start

## Configuration

Key configuration options in `backend/.env`:

- `DATABASE_PATH`: Path to SQLite database file
- `FLASK_PORT`: API server port (default: 5000)
- `DEFAULT_CHECK_INTERVAL`: Default monitoring interval in seconds (default: 300)
- `TELEGRAM_BOT_TOKEN`: Telegram bot token for notifications
- `TELEGRAM_CHAT_ID`: Telegram chat ID for notifications
