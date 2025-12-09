# Chapter 5: Development

## 5.1 Introduction

This chapter documents the development process of WebGuard, detailing the implementation of the system design presented in Chapter 4. The development followed an iterative approach, building core functionality first and then enhancing features based on testing and requirements refinement. This chapter covers environment setup, feature-by-feature development, technical challenges encountered, and key implementation decisions.

## 5.2 Development Environment Setup

### 5.2.1 Backend Environment

**Python Environment**:
- Python 3.11 selected for modern language features and performance improvements
- Virtual environment created using `venv` to isolate dependencies
- Requirements file (`requirements.txt`) created for dependency management

**Key Dependencies Installed**:
- Flask 2.3.0: Web framework for REST API
- APScheduler 3.10.0: Task scheduling for monitoring engine
- requests 2.31.0: HTTP library for website checks
- cryptography 41.0.0: SSL certificate parsing
- python-telegram-bot 20.0: Telegram notification integration
- SQLAlchemy 2.0.0: Database ORM for simplified data access

[INSERT CODE SNIPPET: requirements.txt]

### 5.2.2 Frontend Environment

**Node.js Setup**:
- Node.js 18.x LTS for stable React development
- npm package manager for dependency installation
- Vite 5.0.8 selected over Create React App for faster development experience

**Key Dependencies Installed**:
- React 18.2.0: UI framework
- React DOM 18.2.0: React rendering
- TypeScript 5.2.2: Type safety
- Tailwind CSS 3.3.6: Utility-first CSS framework
- Lucide React 0.294.0: Icon library
- Axios 1.5.0: HTTP client for API communication

[INSERT CODE SNIPPET: package.json]

### 5.2.3 Database Setup

**SQLite Initialisation**:
- Database file created at `data/webguard.db`
- Schema initialisation script developed to create all required tables
- Migration system considered but deferred due to project scope

[INSERT CODE SNIPPET: database_schema.py]

### 5.2.4 Development Tools

- **Version Control**: Git repository initialised with appropriate `.gitignore`
- **Code Editor**: VS Code with Python and TypeScript extensions
- **API Testing**: Postman for REST API endpoint testing
- **Database Management**: DB Browser for SQLite for database inspection

## 5.3 Feature Development

### 5.3.1 Phase 1: Core Backend Infrastructure

**Database Layer Implementation**:

The database layer was implemented first to provide foundation for all other features. SQLAlchemy ORM was selected to simplify database operations and reduce SQL boilerplate code.

**Key Implementation Decisions**:
- Utilised SQLAlchemy declarative base for model definitions
- Implemented database connection pooling for performance
- Created repository pattern for data access abstraction

[INSERT CODE SNIPPET: models.py]

**Challenges Encountered**:
- SQLite concurrency limitations required careful transaction management
- Solved by implementing connection pooling and read/write separation

**Flask API Server Setup**:

The Flask application was structured using blueprints for modular organisation:

```
backend/
  app.py                 # Application entry point
  config.py              # Configuration management
  routes/
    websites.py          # Website management endpoints
    monitoring.py        # Monitoring data endpoints
    config.py            # Configuration endpoints
  models/
    database.py          # Database models
  services/
    monitoring.py        # Monitoring engine
    notifications.py     # Notification service
```

[INSERT CODE SNIPPET: app.py]

**CORS Configuration**:
- Enabled CORS for React frontend communication
- Configured appropriate headers for API responses
- Implemented error handling middleware

### 5.3.2 Phase 2: Monitoring Engine Development

**Scheduler Implementation**:

APScheduler was configured with thread pool executor to enable concurrent website checks:

[INSERT CODE SNIPPET: monitoring_scheduler.py]

**Website Check Function**:

The core monitoring function implements the check execution flow defined in the design:

1. **HTTP Request Execution**:
   - Utilised `requests` library with configurable timeout
   - Implemented retry logic for transient network failures
   - Captured response time using timing measurements

[INSERT CODE SNIPPET: website_check.py]

2. **Content Hash Calculation**:
   - MD5 hashing selected for performance (SHA256 available as option)
   - Content extraction with BeautifulSoup for HTML parsing
   - Content selector support for focused monitoring

[INSERT CODE SNIPPET: defacement_detection.py]

3. **SSL Certificate Extraction**:
   - Utilised `cryptography` library for certificate parsing
   - Extracted validity dates and calculated expiry countdown
   - Handled certificate chain validation

[INSERT CODE SNIPPET: ssl_monitoring.py]

**Challenges and Solutions**:

**Challenge 1: Dynamic Content False Positives**
- **Problem**: Websites with timestamps or dynamic content caused frequent false defacement alerts
- **Solution**: Implemented "False Positive" feature allowing administrators to update baseline when legitimate changes occur
- **Implementation**: API endpoint to capture current content hash and update baseline, resolving defacement incidents automatically

**Challenge 2: Rate Limiting Concerns**
- **Problem**: Aggressive monitoring schedules could overwhelm target websites
- **Solution**: Implemented configurable minimum check intervals (5 minutes default) and request rate limiting
- **Implementation**: Scheduler validation prevents intervals shorter than 1 minute

**Challenge 3: SSL Certificate Parsing Errors**
- **Problem**: Some websites presented certificate chains that caused parsing failures
- **Solution**: Implemented robust error handling with fallback to basic certificate information extraction
- **Implementation**: Try-except blocks with detailed error logging for diagnostic purposes

### 5.3.3 Phase 3: Notification System

**Telegram Bot Integration**:

The Telegram notification system was implemented using the `python-telegram-bot` library:

[INSERT CODE SNIPPET: telegram_notifier.py]

**Notification Formatting**:

Notifications were designed to be informative yet concise:
- Emoji indicators for quick visual recognition
- Structured information layout
- Direct links to dashboard when applicable

**Alert Triggering Logic**:

Notifications are triggered based on incident severity and type:
- **Critical**: Immediate notification (downtime, defacement)
- **Warning**: Scheduled notifications (SSL expiry warnings)
- **Info**: Optional notifications for status changes

**Challenges and Solutions**:

**Challenge: Notification Deduplication**
- **Problem**: Rapid status changes could result in notification spam
- **Solution**: Implemented incident cooldown period (5 minutes) preventing duplicate notifications for same incident type
- **Implementation**: Database query checking for recent incidents before sending notification

### 5.3.4 Phase 4: REST API Development

**Endpoint Implementation**:

All API endpoints were implemented following RESTful principles:

**Website Management Endpoints**:
[INSERT CODE SNIPPET: websites_api.py]

**Monitoring Data Endpoints**:
[INSERT CODE SNIPPET: monitoring_api.py]

**Error Handling**:
- Consistent error response format
- HTTP status codes following REST conventions
- Detailed error messages for debugging

**API Testing**:
- Postman collection created for endpoint testing
- Unit tests developed for critical endpoints
- Integration testing with database operations

### 5.3.5 Phase 5: Frontend Dashboard Development

**React Component Structure**:

The dashboard was built using functional components with React Hooks:

```
src/
  components/
    WebsiteMonitoringDashboard.tsx    # Main dashboard component
    WebsiteTable.tsx                  # Website status table
    OverviewCards.tsx                 # Statistics cards
    AddWebsiteForm.tsx                # Website registration form
  services/
    api.ts                            # API client
  types/
    website.ts                        # TypeScript interfaces
```

**State Management**:

- Utilised React `useState` and `useEffect` hooks for component state
- Implemented polling mechanism for real-time updates
- API client abstraction using Axios

[INSERT CODE SNIPPET: api_client.ts]

**UI Component Development**:

**Overview Cards Component**:
- Real-time statistics calculation from API data
- Colour-coded status indicators
- Responsive grid layout

[INSERT CODE SNIPPET: OverviewCards.tsx]

**Website Table Component**:
- Sortable columns (future enhancement)
- Status indicators with icons
- Action buttons for website management
- Responsive design for mobile viewing

[INSERT CODE SNIPPET: WebsiteTable.tsx]

**Styling with Tailwind CSS**:

Tailwind CSS enabled rapid UI development:
- Utility classes for consistent styling
- Dark theme implementation
- Responsive breakpoints
- Custom colour palette for status indicators

[INSERT SCREENSHOT: react_dashboard.png]

**Challenges and Solutions**:

**Challenge: Real-Time Updates**
- **Problem**: Dashboard needed to reflect monitoring changes without manual refresh
- **Solution**: Implemented polling mechanism with 5-second intervals
- **Implementation**: `useEffect` hook with `setInterval` for automatic API polling

**Challenge: API Error Handling**
- **Problem**: Network errors or API failures needed graceful handling
- **Solution**: Implemented error boundaries and user-friendly error messages
- **Implementation**: Try-catch blocks in API client with error state management

**Challenge: Telegram Bot Async/Await Compatibility**
- **Problem**: `python-telegram-bot` library v20+ migrated to async/await pattern, but notification service was implemented synchronously, causing `AttributeError: 'coroutine' object has no attribute 'message_id'` errors
- **Solution**: Wrapped async `bot.send_message()` calls with `asyncio.run()` to properly execute coroutines in synchronous context
- **Implementation**: Added `import asyncio` and modified notification sending to use `asyncio.run(self.bot.send_message(...))` ensuring proper async execution

### 5.3.6 Phase 6: Test Website Development

**Test Site for Defacement Demonstration**:

A simple Flask-based test website was developed to demonstrate defacement detection capabilities:

[INSERT CODE SNIPPET: test_site.py]

**Features**:
- "Deface me" button to simulate website defacement with dramatic visual changes
- "Restore original" button to revert to clean state
- "Update" button to simulate legitimate website updates (background and font color changes)
- Visual styling to clearly distinguish between defaced, updated, and original states

**Purpose**:
- Enables controlled testing of defacement detection without modifying production websites
- Demonstrates hash-based detection in action
- Allows testing of false positive handling workflow

### 5.3.7 Phase 7: Integration and Configuration

**Configuration Management**:

Configuration was implemented using environment variables and configuration files:

[INSERT CODE SNIPPET: config.py]

**Key Configuration Options**:
- Database path
- Telegram bot token
- Default monitoring intervals
- Notification thresholds
- API server port and host

**System Integration**:

Components were integrated to form complete system:
- Monitoring engine connected to database
- API server connected to monitoring engine
- Frontend connected to API server
- Notification service integrated with monitoring engine

**False Positive Handling**:

Implemented API endpoint to handle false positive defacement alerts:
- `/api/websites/<id>/defacement/false-positive` endpoint
- Captures current website content and updates baseline hash
- Automatically resolves all open defacement incidents for the website
- Integrated into dashboard with "False Positive" button visible when defacement is detected

**Startup Scripts**:

Development and production startup scripts created:
- `run_dev.py`: Development server with hot reload
- `run_prod.py`: Production server with optimised settings
- Systemd service file for Linux deployments (future enhancement)

## 5.4 Technical Decisions and Rationale

### 5.4.1 Python vs. Node.js for Backend

**Decision**: Python selected for monitoring engine

**Rationale**:
- Superior library ecosystem for HTTP requests and SSL certificate handling
- APScheduler provides robust task scheduling capabilities
- Better suited for system-level operations and file handling
- Established patterns for security monitoring tools

### 5.4.2 SQLite vs. PostgreSQL

**Decision**: SQLite selected for database

**Rationale**:
- Zero configuration aligns with local-first architecture
- Sufficient for single-user, moderate-scale deployments
- Eliminates database server dependency
- Easy backup and portability

**Trade-off Accepted**: Limited concurrent write performance (acceptable for monitoring use case)

### 5.4.3 Hash-Based vs. DOM Tree Comparison for Defacement

**Decision**: Hash-based detection implemented initially

**Rationale**:
- Simpler implementation with lower computational overhead
- Sufficient accuracy for initial version
- Faster execution enabling more frequent checks
- Content selector support mitigates false positives

**Future Enhancement**: DOM tree comparison can be added as advanced feature

### 5.4.4 Polling vs. WebSockets for Real-Time Updates

**Decision**: HTTP polling implemented

**Rationale**:
- Simpler implementation without additional infrastructure
- Sufficient for monitoring dashboard update frequency
- Works behind firewalls and proxies without special configuration
- Lower complexity reduces maintenance burden

**Trade-off Accepted**: Slightly higher server load (negligible for single-user deployment)

## 5.5 Development Challenges

### 5.5.1 Challenge: Concurrent Monitoring Checks

**Problem**: Monitoring multiple websites simultaneously required careful thread management to avoid resource exhaustion.

**Solution**: Implemented thread pool with configurable size (default: 5 concurrent checks), preventing system overload while maintaining reasonable check throughput.

### 5.5.2 Challenge: Database Lock Contention

**Problem**: SQLite's write locking caused delays when multiple monitoring checks attempted simultaneous database writes.

**Solution**: Implemented write queue with single writer thread, ensuring sequential database writes while maintaining concurrent check execution.

### 5.5.3 Challenge: Timezone Handling

**Problem**: Timestamp storage and display required consistent timezone handling across backend and frontend.

**Solution**: Standardised on UTC for all database timestamps, with timezone conversion handled in frontend for user display.

### 5.5.4 Challenge: Content Hash Stability

**Problem**: Websites with frequently changing content (advertisements, timestamps) caused excessive false positives.

**Solution**: Implemented content selector feature and configurable hash comparison thresholds, allowing administrators to focus monitoring on stable content sections.

## 5.6 Code Quality and Best Practices

### 5.6.1 Code Organisation

- Modular structure with clear separation of concerns
- Consistent naming conventions (PEP 8 for Python, camelCase for TypeScript)
- Comprehensive code comments for complex logic
- Type hints in Python for improved code clarity

### 5.6.2 Error Handling

- Try-except blocks for all external API calls
- Graceful degradation when services unavailable
- Comprehensive error logging for diagnostic purposes
- User-friendly error messages in API responses

### 5.6.3 Documentation

- Inline code documentation for all functions
- API endpoint documentation
- Configuration file comments
- README with setup and usage instructions

## 5.7 Chapter Summary

This chapter has documented the complete development process of WebGuard, from initial environment setup through to final integration. The development followed a phased approach, building core infrastructure before adding advanced features. Key technical decisions were made with careful consideration of project requirements and constraints. Challenges encountered during development were addressed through iterative problem-solving and design refinement. The implementation successfully realises the system design presented in Chapter 4, providing a functional monitoring platform that addresses the requirements defined in Chapter 3. The following chapter will detail the testing methodology and results, validating that the developed system meets all specified requirements and performs reliably under various conditions.

