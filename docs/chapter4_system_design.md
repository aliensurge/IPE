# Chapter 4: System Design

## 4.1 Introduction

This chapter presents the system architecture and design decisions for WebGuard, translating the requirements defined in Chapter 3 into a concrete technical design. The design emphasises modularity, maintainability, and the local-first architecture principle that distinguishes WebGuard from cloud-based alternatives.

## 4.2 High-Level Architecture

[INSERT DIAGRAM: system_architecture.png]

*High-level architecture diagram showing: React Frontend, Flask REST API, Python Monitoring Engine, SQLite Database, Telegram Bot API, and their interconnections.*

### 4.2.1 Architecture Overview

WebGuard follows a three-tier architecture:

**Presentation Layer (Frontend)**
- React-based single-page application
- Tailwind CSS for styling
- Real-time updates via REST API polling
- Responsive design for desktop and mobile viewing

**Application Layer (Backend)**
- Flask REST API server
- Python monitoring engine with scheduled task execution
- Business logic and data processing
- Notification management

**Data Layer**
- SQLite database for persistent storage
- File system for configuration and logs
- In-memory caching for performance optimisation

### 4.2.2 Component Interaction

The system consists of five primary components:

1. **React Dashboard**: User interface for visualising monitoring status and managing configuration
2. **Flask API Server**: RESTful API providing data access and configuration endpoints
3. **Monitoring Engine**: Python service performing scheduled website checks
4. **Database Layer**: SQLite storing monitoring data and configuration
5. **Notification Service**: Telegram bot integration for alert delivery

## 4.3 Data Flow Architecture

### 4.3.1 Monitoring Check Flow

[INSERT DIAGRAM: monitoring_flow_sequence.png]

*Sequence diagram showing: Monitoring Engine → Website Check → Database Update → Notification Service → Telegram API*

**Step-by-Step Flow**:
1. Monitoring Engine triggers scheduled check based on website configuration
2. Engine performs HTTP request to target website
3. Engine captures response time, status code, and content
4. Engine compares content hash with stored baseline (defacement check)
5. Engine extracts SSL certificate information (if HTTPS)
6. Engine stores check results in database
7. Engine evaluates results against alert thresholds
8. If threshold exceeded, Notification Service sends Telegram alert
9. Dashboard polls API for updated status and displays changes

### 4.3.2 User Interaction Flow

**Dashboard Access Flow**:
1. User opens dashboard URL in web browser
2. React application loads and initialises
3. Application requests website list from Flask API
4. API queries database and returns JSON response
5. React renders dashboard with current status
6. Application polls API every 5 seconds for updates
7. User interacts with dashboard (add website, view details, configure settings)
8. User actions trigger API requests
9. API updates database and returns confirmation
10. Dashboard reflects changes immediately

## 4.4 Database Design

### 4.4.1 Entity Relationship Diagram

[INSERT DIAGRAM: database_er_diagram.png]

*ER diagram showing relationships between Websites, Monitoring_Checks, SSL_Certificates, Defacement_Baselines, Incidents, and Notifications tables.*

### 4.4.2 Database Schema

**Websites Table**
```sql
CREATE TABLE websites (
    website_id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL UNIQUE,
    display_name TEXT,
    monitoring_enabled BOOLEAN DEFAULT 1,
    check_interval INTEGER DEFAULT 300,
    defacement_detection_enabled BOOLEAN DEFAULT 1,
    ssl_monitoring_enabled BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Monitoring_Checks Table**
```sql
CREATE TABLE monitoring_checks (
    check_id INTEGER PRIMARY KEY AUTOINCREMENT,
    website_id INTEGER NOT NULL,
    check_type TEXT NOT NULL,
    status TEXT NOT NULL,
    response_time INTEGER,
    http_status_code INTEGER,
    error_message TEXT,
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (website_id) REFERENCES websites(website_id)
);
```

**SSL_Certificates Table**
```sql
CREATE TABLE ssl_certificates (
    certificate_id INTEGER PRIMARY KEY AUTOINCREMENT,
    website_id INTEGER NOT NULL,
    issuer TEXT,
    subject TEXT,
    valid_from DATE,
    valid_to DATE,
    days_until_expiry INTEGER,
    last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (website_id) REFERENCES websites(website_id)
);
```

**Defacement_Baselines Table**
```sql
CREATE TABLE defacement_baselines (
    baseline_id INTEGER PRIMARY KEY AUTOINCREMENT,
    website_id INTEGER NOT NULL,
    content_hash TEXT NOT NULL,
    content_selector TEXT,
    captured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (website_id) REFERENCES websites(website_id)
);
```

**Incidents Table**
```sql
CREATE TABLE incidents (
    incident_id INTEGER PRIMARY KEY AUTOINCREMENT,
    website_id INTEGER NOT NULL,
    incident_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    description TEXT,
    FOREIGN KEY (website_id) REFERENCES websites(website_id)
);
```

**Notifications Table**
```sql
CREATE TABLE notifications (
    notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    incident_id INTEGER,
    notification_channel TEXT NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    delivery_status TEXT DEFAULT 'pending',
    FOREIGN KEY (incident_id) REFERENCES incidents(incident_id)
);
```

### 4.4.3 Database Indexes

Indexes are created to optimise query performance:

- `websites.url`: Unique index for URL lookups
- `monitoring_checks.website_id`: Index for filtering checks by website
- `monitoring_checks.checked_at`: Index for time-based queries
- `incidents.website_id`: Index for incident lookups
- `incidents.detected_at`: Index for chronological incident queries

## 4.5 API Design

### 4.5.1 REST API Endpoints

**Website Management**
- `GET /api/websites` - Retrieve all monitored websites
- `GET /api/websites/{id}` - Retrieve specific website details
- `POST /api/websites` - Register new website
- `PUT /api/websites/{id}` - Update website configuration
- `DELETE /api/websites/{id}` - Remove website from monitoring
- `POST /api/websites/{id}/check` - Manually trigger monitoring check

**Monitoring Data**
- `GET /api/websites/{id}/checks` - Retrieve monitoring check history
- `GET /api/websites/{id}/incidents` - Retrieve incident history
- `GET /api/websites/{id}/status` - Get current website status

**Configuration**
- `GET /api/config` - Retrieve system configuration
- `PUT /api/config` - Update system configuration

**Statistics**
- `GET /api/stats/overview` - Get dashboard overview statistics
- `GET /api/stats/uptime/{id}` - Get uptime percentage for website

### 4.5.2 API Response Format

All API responses follow consistent JSON structure:

**Success Response**:
```json
{
    "status": "success",
    "data": { ... },
    "timestamp": "2024-01-15T10:30:00Z"
}
```

**Error Response**:
```json
{
    "status": "error",
    "message": "Error description",
    "code": "ERROR_CODE",
    "timestamp": "2024-01-15T10:30:00Z"
}
```

## 4.6 User Interface Design

### 4.6.1 Dashboard Wireframes

[INSERT IMAGE: dashboard_wireframe.png]

*Wireframe showing: Header with logo and current time, Overview cards (Total Sites, Online, Warning, Offline), Main table with website status, Action buttons (Add Website, View Analytics).*

### 4.6.2 UI Component Structure

**Header Component**
- Logo and application title
- Current system time display
- Navigation menu (future enhancement)

**Overview Cards Component**
- Total monitored websites count
- Online websites count
- Warning status count
- Offline websites count
- Real-time updates via API polling

**Website Table Component**
- Status indicator (colour-coded dot and icon)
- Website name and URL
- Response time display
- Uptime percentage with progress bar
- Action buttons (View Details, Edit, Delete)

**Add Website Form Component**
- URL input with validation
- Display name input (optional)
- Monitoring interval selector
- Feature toggles (defacement detection, SSL monitoring)
- Submit and cancel buttons

### 4.6.3 Design Principles

- **Dark Theme**: Professional appearance suitable for 24/7 monitoring environments
- **Colour Coding**: Green (online), Yellow (warning), Red (offline) for instant status recognition
- **Responsive Design**: Adapts to different screen sizes while maintaining usability
- **Minimalist Interface**: Focus on essential information without clutter
- **Real-Time Updates**: Automatic refresh ensures current status visibility

## 4.7 Monitoring Engine Design

### 4.7.1 Scheduling Architecture

The monitoring engine utilises APScheduler for task management:

- **Interval-Based Scheduling**: Each website has independent check interval
- **Thread Pool Execution**: Concurrent checks for multiple websites
- **Error Handling**: Failed checks are logged and retried according to retry policy
- **Resource Management**: Rate limiting prevents overwhelming target websites

### 4.7.2 Check Execution Flow

1. **Pre-Check Validation**
   - Verify website is enabled for monitoring
   - Check if sufficient time has passed since last check
   - Validate network connectivity

2. **HTTP Request Execution**
   - Send GET request with configurable timeout
   - Capture response time
   - Record HTTP status code
   - Handle exceptions (timeout, connection errors)

3. **Content Analysis**
   - Extract HTML content from response
   - Apply content selector if configured
   - Calculate content hash (MD5 or SHA256)
   - Compare with stored baseline

4. **SSL Certificate Extraction**
   - For HTTPS URLs, extract certificate chain
   - Parse certificate validity dates
   - Calculate days until expiry
   - Store certificate information

5. **Result Processing**
   - Determine check status (success, failure, warning)
   - Create database records
   - Evaluate alert conditions
   - Trigger notifications if thresholds exceeded

### 4.7.3 Defacement Detection Algorithm

**Hash-Based Detection**:
1. Capture baseline content hash upon website registration
2. During each check, calculate current content hash
3. Compare hashes using exact match
4. If hashes differ, flag potential defacement
5. Store incident record and send notification

**Content Selector Support**:
- Administrators can specify CSS selectors to focus monitoring on critical sections
- Only selected content is hashed, reducing false positives from dynamic elements
- Example: Monitoring only `<header>` and `<footer>` sections

## 4.8 Notification System Design

### 4.8.1 Telegram Bot Integration

**Bot Setup**:
- Bot created via BotFather on Telegram
- Bot token stored securely in configuration
- Webhook or polling mechanism for receiving commands (future enhancement)

**Notification Format**:
```
🚨 Website Alert

Website: Example.com
URL: https://example.com
Type: Downtime Detected
Time: 2024-01-15 10:30:00
Status: Offline
Response Time: Timeout

View Dashboard: [Link]
```

### 4.8.2 Notification Routing

- **Immediate Alerts**: Downtime and defacement incidents trigger immediate notifications
- **Scheduled Warnings**: SSL expiry warnings sent according to configured thresholds (30, 14, 7 days)
- **Deduplication**: Multiple incidents for same website within short time window result in single notification
- **Retry Logic**: Failed notification deliveries are retried with exponential backoff

## 4.9 Security Design Considerations

### 4.9.1 Authentication and Authorisation

**Initial Implementation**:
- Single-user system assumes trusted environment
- No authentication required for dashboard access
- Future enhancement: Basic HTTP authentication or API key system

**Security Recommendations**:
- Deploy behind reverse proxy (nginx) with HTTPS
- Implement IP whitelisting for production deployments
- Utilise environment variables for sensitive configuration

### 4.9.2 Data Protection

- **Credential Storage**: Telegram bot tokens stored in environment variables or encrypted configuration files
- **Database Security**: SQLite database file permissions restricted to application user
- **Logging**: Sensitive information excluded from application logs
- **Network Security**: All external communications utilise HTTPS where possible

### 4.9.3 Input Validation

- **URL Validation**: Strict validation of website URLs before registration
- **SQL Injection Prevention**: Parameterised queries for all database operations
- **XSS Prevention**: React's built-in XSS protection for user-generated content
- **Rate Limiting**: API endpoints implement rate limiting to prevent abuse

## 4.10 Local-First Architecture Justification

### 4.10.1 Data Sovereignty

The local-first architecture ensures:
- All monitoring data remains on-premises
- No dependency on external cloud services for core functionality
- Compliance with data residency requirements
- Protection of sensitive website information

### 4.10.2 Cost Effectiveness

- **No Subscription Fees**: Eliminates recurring costs associated with cloud monitoring services
- **Infrastructure Efficiency**: Utilises existing SME IT infrastructure
- **Scalability**: No per-monitor or per-site pricing limitations

### 4.10.3 Reliability

- **Reduced Dependencies**: Fewer external service dependencies reduce failure points
- **Network Independence**: Local operation continues during internet connectivity issues (for local dashboard access)
- **Customisation Freedom**: No vendor-imposed limitations on features or modifications

### 4.10.4 Trade-offs

**Accepted Limitations**:
- Requires dedicated server or workstation for 24/7 operation
- No built-in redundancy without additional infrastructure
- Manual backup and maintenance responsibilities
- Limited remote access without additional configuration

## 4.11 Chapter Summary

This chapter has presented the comprehensive system design for WebGuard, including high-level architecture, data flow, database schema, API design, user interface structure, monitoring engine architecture, notification system, and security considerations. The design emphasises modularity, maintainability, and the local-first principle that addresses identified gaps in commercial solutions. The three-tier architecture separates concerns effectively, enabling independent development and testing of components. The database design supports all functional requirements while maintaining performance through appropriate indexing. The REST API provides clean separation between frontend and backend, facilitating future enhancements. The monitoring engine design ensures reliable, efficient website checking with configurable scheduling. Security considerations address authentication, data protection, and input validation requirements. The local-first architecture justification explains the design decisions that distinguish WebGuard from cloud-based alternatives. The following chapter will document the implementation of this design, detailing the development process and technical decisions made during construction.

