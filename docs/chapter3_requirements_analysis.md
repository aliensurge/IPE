# Chapter 3: Requirements and Analysis

## 3.1 Introduction

This chapter defines the functional and non-functional requirements for the WebGuard platform, derived from the problem statement and literature review. Requirements are structured using user stories, use cases, and prioritisation frameworks to guide system design and development.

## 3.2 Functional Requirements

### 3.2.1 Website Monitoring Requirements

**FR1: Website Registration**
- The system SHALL allow administrators to register websites for monitoring by providing a URL and optional display name.
- The system SHALL validate URL format and accessibility before accepting registration.
- The system SHALL support HTTP and HTTPS protocols.

**FR2: Uptime Monitoring**
- The system SHALL perform periodic availability checks on registered websites at configurable intervals (minimum 1 minute, default 5 minutes).
- The system SHALL record response times for each check.
- The system SHALL detect and log downtime incidents when websites fail to respond within a configurable timeout period (default 30 seconds).
- The system SHALL distinguish between different types of failures (timeout, connection refused, HTTP error codes).

**FR3: Defacement Detection**
- The system SHALL capture baseline content from registered websites upon initial registration.
- The system SHALL perform content comparison during each monitoring cycle to detect unauthorised changes.
- The system SHALL utilise hash-based comparison (MD5/SHA256) for efficient change detection.
- The system SHALL support configurable content selectors to focus monitoring on critical page sections (e.g., header, footer, main content).
- The system SHALL flag potential defacement when content hash differs from baseline.

**FR4: SSL Certificate Monitoring**
- The system SHALL extract SSL certificate information from HTTPS websites during monitoring checks.
- The system SHALL calculate days until certificate expiry.
- The system SHALL trigger alerts when certificates are within configurable warning thresholds (default: 30 days, 14 days, 7 days, expired).
- The system SHALL store certificate details including issuer, validity period, and subject.

**FR5: Alert and Notification System**
- The system SHALL send Telegram notifications when downtime is detected.
- The system SHALL send Telegram notifications when defacement is suspected.
- The system SHALL send Telegram notifications when SSL certificates approach expiry thresholds.
- The system SHALL include relevant details in notifications (website URL, incident type, timestamp, severity).
- The system SHALL support configurable notification preferences per website.

**FR6: Dashboard Interface**
- The system SHALL provide a web-based dashboard displaying all monitored websites.
- The system SHALL show real-time status for each website (online, offline, warning).
- The system SHALL display response time metrics and uptime percentages.
- The system SHALL show SSL certificate expiry countdowns.
- The system SHALL provide historical data visualisation (uptime trends, response time graphs).
- The system SHALL allow administrators to manually trigger monitoring checks.

**FR7: Data Management**
- The system SHALL store monitoring history for configurable retention periods (default: 90 days).
- The system SHALL allow administrators to view historical incidents and status changes.
- The system SHALL support export of monitoring data in standard formats (CSV, JSON).

### 3.2.2 System Administration Requirements

**FR8: Configuration Management**
- The system SHALL allow configuration of monitoring intervals per website.
- The system SHALL support global default settings that apply to new websites.
- The system SHALL allow configuration of notification channels and preferences.
- The system SHALL persist configuration changes to local storage.

**FR9: Website Management**
- The system SHALL allow administrators to add, edit, and remove monitored websites.
- The system SHALL support bulk operations for multiple websites.
- The system SHALL allow temporary suspension of monitoring without deletion.

## 3.3 Non-Functional Requirements

### 3.3.1 Performance Requirements

**NFR1: Response Time**
- The system SHALL complete individual website checks within 30 seconds under normal network conditions.
- The dashboard SHALL load within 2 seconds on standard broadband connections.
- The system SHALL support monitoring of up to 50 websites concurrently without performance degradation.

**NFR2: Scalability**
- The system SHALL handle monitoring schedules for up to 100 websites without requiring additional infrastructure.
- The system SHALL efficiently manage database growth, with monitoring history queries completing within 1 second for 90-day periods.

**NFR3: Resource Usage**
- The system SHALL operate on systems with minimum 2GB RAM and 1GB available disk space.
- The system SHALL not consume more than 500MB RAM during normal operation.
- The system SHALL minimise CPU usage, allowing concurrent operation with other applications.

### 3.3.2 Reliability Requirements

**NFR4: Availability**
- The monitoring engine SHALL maintain 99% uptime, excluding planned maintenance windows.
- The system SHALL automatically recover from transient network failures without manual intervention.
- The system SHALL log all errors and failures for diagnostic purposes.

**NFR5: Data Integrity**
- The system SHALL ensure monitoring data is not lost due to application crashes or system restarts.
- The system SHALL utilise database transactions to maintain data consistency.
- The system SHALL perform regular database integrity checks.

### 3.3.3 Security Requirements

**NFR6: Data Protection**
- The system SHALL store sensitive configuration data (API keys, credentials) using secure storage mechanisms.
- The system SHALL not log or transmit website credentials unless explicitly configured for authenticated monitoring.
- The system SHALL implement appropriate access controls to prevent unauthorised dashboard access.

**NFR7: Secure Communications**
- The system SHALL utilise HTTPS for dashboard access when deployed in production environments.
- The system SHALL validate SSL certificates when connecting to monitored websites.
- The system SHALL implement rate limiting to prevent abuse of monitoring endpoints.

### 3.3.4 Usability Requirements

**NFR8: User Interface**
- The dashboard SHALL be intuitive and require minimal training for administrators.
- The system SHALL provide clear visual indicators for website status (colour coding, icons).
- The system SHALL display error messages in plain language with actionable guidance.

**NFR9: Documentation**
- The system SHALL include comprehensive installation and configuration documentation.
- The system SHALL provide inline help and tooltips for configuration options.
- The system SHALL document API endpoints for potential future integrations.

### 3.3.5 Maintainability Requirements

**NFR10: Code Quality**
- The system SHALL follow established coding standards and best practices.
- The system SHALL include code comments and documentation for complex logic.
- The system SHALL utilise version control for all source code.

**NFR11: Extensibility**
- The system architecture SHALL support future enhancements without major refactoring.
- The system SHALL utilise modular design principles to enable feature additions.
- The system SHALL provide extension points for custom monitoring plugins.

## 3.4 User Stories

### 3.4.1 Administrator User Stories

**US1: Website Registration**
- **As an** administrator
- **I want to** register websites for monitoring by providing a URL
- **So that** I can begin tracking their security status automatically

**US2: Status Visibility**
- **As an** administrator
- **I want to** view the current status of all monitored websites on a dashboard
- **So that** I can quickly identify any issues requiring attention

**US3: Incident Notification**
- **As an** administrator
- **I want to** receive immediate notifications when websites go offline
- **So that** I can respond quickly to downtime incidents

**US4: Defacement Alerts**
- **As an** administrator
- **I want to** be alerted when website content changes unexpectedly
- **So that** I can investigate potential security breaches

**US5: SSL Expiry Warnings**
- **As an** administrator
- **I want to** receive advance warnings before SSL certificates expire
- **So that** I can renew certificates proactively and avoid service disruption

**US6: Historical Analysis**
- **As an** administrator
- **I want to** view historical monitoring data and trends
- **So that** I can identify patterns and improve website reliability

**US7: Configuration Management**
- **As an** administrator
- **I want to** configure monitoring intervals and alert thresholds
- **So that** I can customise monitoring to match my specific needs

## 3.5 Use Case Diagram

[INSERT DIAGRAM: use_case_diagram.png]

*Use case diagram showing interactions between Administrator actor and WebGuard system, including: Register Website, View Dashboard, Configure Monitoring, Receive Notifications, View History, Export Data.*

## 3.6 Use Case Descriptions

### 3.6.1 UC1: Register Website for Monitoring

**Actors**: Administrator

**Preconditions**: 
- Administrator has access to the dashboard
- Website URL is known and accessible

**Main Flow**:
1. Administrator navigates to "Add Website" section
2. System displays website registration form
3. Administrator enters website URL and optional display name
4. System validates URL format
5. System performs initial connectivity check
6. System captures baseline content and SSL certificate information
7. System confirms successful registration
8. System begins scheduled monitoring

**Alternative Flows**:
- 4a. Invalid URL format: System displays error message, administrator corrects URL
- 5a. Website unreachable: System displays error message, administrator verifies URL or network connectivity
- 6a. HTTPS website with invalid certificate: System warns administrator but allows registration with monitoring disabled for SSL checks

**Postconditions**: Website is registered and monitoring has commenced

### 3.6.2 UC2: Receive Downtime Alert

**Actors**: System (monitoring engine), Administrator (notification recipient)

**Preconditions**:
- Website is registered and being monitored
- Telegram bot is configured

**Main Flow**:
1. System performs scheduled availability check
2. Website fails to respond within timeout period
3. System logs downtime incident
4. System sends Telegram notification to administrator
5. Administrator receives notification on mobile device
6. Administrator acknowledges notification

**Alternative Flows**:
- 2a. Website responds but with error code (e.g., 500): System treats as downtime incident
- 4a. Telegram API unavailable: System logs notification failure and retries according to retry policy

**Postconditions**: Administrator is aware of downtime incident

### 3.6.3 UC3: Detect Potential Defacement

**Actors**: System (monitoring engine), Administrator (notification recipient)

**Preconditions**:
- Website is registered with baseline content captured
- Defacement detection is enabled for website

**Main Flow**:
1. System performs scheduled content check
2. System retrieves current website content
3. System calculates content hash
4. System compares hash with stored baseline
5. Hashes differ significantly
6. System flags potential defacement
7. System sends Telegram alert with content comparison details
8. Administrator reviews alert and investigates

**Alternative Flows**:
- 5a. Hashes match: System logs successful check, continues monitoring
- 5b. Minor hash differences (e.g., timestamp updates): System applies configurable threshold to reduce false positives

**Postconditions**: Administrator is alerted to potential security incident

## 3.7 Requirements Prioritisation (MoSCoW)

### Must Have (Critical)
- FR1: Website Registration
- FR2: Uptime Monitoring
- FR3: Defacement Detection (basic hash-based)
- FR4: SSL Certificate Monitoring
- FR5: Alert and Notification System
- FR6: Dashboard Interface (basic status display)
- NFR1-NFR5: Performance and Reliability requirements

### Should Have (Important)
- FR7: Data Management (historical data)
- FR8: Configuration Management
- FR9: Website Management (edit/delete)
- NFR6-NFR7: Security requirements
- NFR8: Usability requirements

### Could Have (Desirable)
- Advanced defacement detection (DOM tree comparison)
- Multiple notification channels (email, SMS)
- Dashboard data visualisation (charts, graphs)
- Export functionality
- NFR9-NFR11: Maintainability and extensibility

### Won't Have (Out of Scope)
- Multi-user authentication
- Cloud deployment options
- Automated remediation
- Integration with third-party SIEM systems
- Mobile applications

## 3.8 Database Requirements

### 3.8.1 Data Entities

**Websites Table**
- website_id (Primary Key)
- url (Unique, Not Null)
- display_name
- monitoring_enabled (Boolean)
- check_interval (Integer, seconds)
- created_at (Timestamp)
- updated_at (Timestamp)

**Monitoring Checks Table**
- check_id (Primary Key)
- website_id (Foreign Key)
- check_type (Enum: uptime, defacement, ssl)
- status (Enum: success, failure, warning)
- response_time (Integer, milliseconds)
- http_status_code (Integer, nullable)
- error_message (Text, nullable)
- checked_at (Timestamp)

**SSL Certificates Table**
- certificate_id (Primary Key)
- website_id (Foreign Key)
- issuer (Text)
- subject (Text)
- valid_from (Date)
- valid_to (Date)
- days_until_expiry (Integer)
- last_checked (Timestamp)

**Defacement Baselines Table**
- baseline_id (Primary Key)
- website_id (Foreign Key)
- content_hash (Text)
- content_selector (Text, nullable)
- captured_at (Timestamp)

**Incidents Table**
- incident_id (Primary Key)
- website_id (Foreign Key)
- incident_type (Enum: downtime, defacement, ssl_expiry)
- severity (Enum: low, medium, high, critical)
- detected_at (Timestamp)
- resolved_at (Timestamp, nullable)
- description (Text)

**Notifications Table**
- notification_id (Primary Key)
- incident_id (Foreign Key)
- notification_channel (Enum: telegram)
- sent_at (Timestamp)
- delivery_status (Enum: sent, failed, pending)

## 3.9 Risk Analysis

### 3.9.1 Technical Risks

**Risk 1: False Positive Defacement Alerts**
- **Probability**: Medium
- **Impact**: High (unnecessary administrator attention, potential alert fatigue)
- **Mitigation**: Implement configurable thresholds, content selector focusing, and manual verification workflows

**Risk 2: Monitoring Engine Failure**
- **Probability**: Low
- **Impact**: Critical (complete loss of monitoring capability)
- **Mitigation**: Implement robust error handling, automatic restart mechanisms, and comprehensive logging

**Risk 3: Database Corruption**
- **Probability**: Low
- **Impact**: High (loss of historical data)
- **Mitigation**: Regular database backups, transaction-based writes, integrity checks

**Risk 4: Telegram API Dependency**
- **Probability**: Medium
- **Impact**: Medium (notification delivery failure)
- **Mitigation**: Implement retry mechanisms, fallback notification methods, local alert logging

### 3.9.2 Operational Risks

**Risk 5: Resource Exhaustion**
- **Probability**: Medium
- **Impact**: Medium (system performance degradation)
- **Mitigation**: Implement resource monitoring, configurable check intervals, efficient database queries

**Risk 6: Network Connectivity Issues**
- **Probability**: Medium
- **Impact**: Medium (temporary monitoring failures)
- **Mitigation**: Implement retry logic, distinguish between network and website failures, timeout configuration

### 3.9.3 Security Risks

**Risk 7: Unauthorised Dashboard Access**
- **Probability**: Low
- **Impact**: High (exposure of monitoring data, potential system compromise)
- **Mitigation**: Implement authentication mechanisms, HTTPS deployment, access logging

**Risk 8: Sensitive Data Exposure**
- **Probability**: Low
- **Impact**: High (exposure of website URLs, monitoring patterns)
- **Mitigation**: Secure credential storage, encrypted database options, access control

## 3.10 Chapter Summary

This chapter has defined comprehensive functional and non-functional requirements for the WebGuard platform, derived from the problem statement and literature review. Functional requirements cover website monitoring, defacement detection, SSL certificate tracking, alerting, and dashboard functionality. Non-functional requirements address performance, reliability, security, usability, and maintainability concerns. User stories provide user-centric perspectives on system capabilities, while use cases detail specific interaction flows. Requirements have been prioritised using the MoSCoW framework to guide development focus. Database requirements have been specified to support all functional requirements. Risk analysis has identified potential technical, operational, and security risks with corresponding mitigation strategies. These requirements provide the foundation for the system design detailed in the following chapter.

