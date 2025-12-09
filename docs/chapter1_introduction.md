# Chapter 1: Introduction

## 1.1 Problem Statement

Small and medium-sized enterprises (SMEs) face significant cybersecurity challenges in an increasingly digital business environment. Unlike large corporations with dedicated IT security teams and substantial budgets for enterprise monitoring solutions, SMEs must operate with limited resources while facing the same threats. The problem statement for this project addresses three critical security monitoring gaps:

- **Website Defacement Detection**: SMEs lack automated mechanisms to detect when their websites have been compromised or defaced, often discovering incidents only after customers report issues or search engines flag malicious content.

- **Downtime Monitoring**: Unplanned website outages directly impact revenue and customer trust, yet many SMEs rely on manual checks or discover downtime through customer complaints rather than proactive monitoring.

- **SSL Certificate Management**: Expired SSL certificates result in security warnings that erode customer trust and can lead to compliance violations, yet certificate expiry dates are easily overlooked without automated tracking.

## 1.2 Importance of Security Monitoring for SMEs

The importance of security monitoring for small businesses cannot be overstated. Research indicates that SMEs are increasingly targeted by cybercriminals, with studies showing that 43% of cyber attacks target small businesses (Verizon, 2023). The consequences extend beyond immediate financial losses:

- **Reputational Damage**: Security incidents can permanently damage customer trust, particularly for businesses that handle sensitive information or rely on e-commerce.

- **Regulatory Compliance**: Many industries require demonstrable security monitoring capabilities, with regulations such as GDPR mandating breach notification within 72 hours.

- **Operational Continuity**: Unplanned downtime directly impacts revenue, with e-commerce businesses losing an average of $5,600 per minute during outages (Gartner, 2023).

- **Competitive Disadvantage**: Businesses without adequate security monitoring appear less professional and trustworthy compared to competitors with robust security postures.

## 1.3 Website Defacement Threat Justification

Website defacement represents a significant threat vector that is often underestimated by SMEs. Defacement attacks serve multiple purposes for attackers:

- **Brand Damage**: Attackers may replace legitimate content with political messages, offensive material, or competitor advertisements, causing immediate reputational harm.

- **Credential Harvesting**: Defaced websites are frequently used to host phishing pages that capture user credentials, extending the attack's impact beyond the initial breach.

- **SEO Poisoning**: Search engines may index defaced content, causing long-term damage to search rankings and discoverability.

- **Precursor to Data Breaches**: Defacement often indicates deeper system compromise, with attackers using website access as an entry point for data exfiltration.

The automated detection of defacement is critical because manual monitoring is impractical for businesses operating 24/7, and the window between compromise and discovery can be hours or days, during which customers may be exposed to malicious content.

## 1.4 SSL Certificate Expiry Impact on Trust

SSL certificate expiry creates cascading trust and security implications:

- **Browser Security Warnings**: Modern browsers display prominent warnings when certificates expire, causing immediate user abandonment and loss of conversions.

- **Search Engine Penalties**: Google and other search engines may reduce rankings for sites with expired certificates, impacting organic traffic.

- **Compliance Violations**: Industries such as healthcare and finance require valid SSL certificates for regulatory compliance, with expired certificates potentially resulting in fines or loss of accreditation.

- **Customer Perception**: Expired certificates signal neglect and lack of technical competence, damaging brand perception even after certificates are renewed.

Automated monitoring of SSL certificate expiry dates enables proactive renewal, preventing these consequences and maintaining uninterrupted service.

## 1.5 Project Aims and Objectives

### Primary Aim
To develop a local, cost-effective security monitoring platform that enables SMEs to automatically detect website defacement, monitor downtime, and track SSL certificate expiry without reliance on external cloud services or recurring subscription fees.

### Primary Objectives
1. **Develop Automated Monitoring Engine**: Create a Python-based backend system capable of performing scheduled checks for website availability, content integrity, and SSL certificate status.

2. **Implement Defacement Detection**: Design and implement content comparison algorithms that can detect unauthorised changes to website content, distinguishing between legitimate updates and malicious modifications.

3. **Create Real-Time Dashboard**: Build a React-based web interface providing visual representation of monitoring status, historical data, and alert management.

4. **Enable Notification System**: Integrate Telegram bot functionality to deliver immediate alerts when security incidents or anomalies are detected.

5. **Ensure Local-First Architecture**: Design the system to operate entirely on-premises, ensuring data sovereignty and eliminating dependency on external services for core functionality.

### Secondary Objectives
- Document the complete development process for academic and practical reference
- Evaluate the effectiveness of open-source technologies in addressing SME security needs
- Provide a foundation for future enhancements including cloud deployment options and AI-assisted anomaly detection

## 1.6 Project Scope

### In-Scope
- Monitoring of HTTP/HTTPS websites for availability and response times
- Content-based defacement detection using hash comparison and content analysis
- SSL certificate expiry tracking with configurable warning thresholds
- Real-time dashboard displaying monitoring status and historical trends
- Telegram-based notification system for incident alerts
- Local database storage for monitoring history and configuration
- Support for multiple concurrent website monitoring

### Out-of-Scope
- Cloud-based deployment or SaaS functionality (future enhancement)
- Advanced threat detection beyond defacement (malware scanning, DDoS detection)
- Automated remediation or incident response actions
- Integration with third-party security tools or SIEM systems
- Mobile application development
- Multi-user authentication and role-based access control (single-user focus)

## 1.7 Limitations and Constraints

### Technical Limitations
- **Detection Accuracy**: Content-based defacement detection may produce false positives when legitimate content updates occur, requiring manual verification.

- **Monitoring Frequency**: The system's monitoring frequency is constrained by the need to avoid overwhelming target websites with excessive requests, potentially missing very brief incidents.

- **Single-User Focus**: The initial implementation assumes a single administrator, limiting scalability for organisations requiring team-based access.

- **Local Deployment Requirement**: The system requires a continuously running server or workstation, which may not be feasible for all SME environments.

### Resource Constraints
- **Development Timeline**: The project was completed within a single academic semester, limiting the scope of features that could be implemented and tested.

- **Budget Constraints**: As a student project, development was constrained to free and open-source technologies, excluding commercial monitoring APIs or premium services.

- **Testing Environment**: Testing was conducted using controlled test scenarios rather than production SME environments, potentially missing edge cases encountered in real-world deployments.

## 1.8 Legal, Ethical, and Professional Issues

### Legal Considerations
- **Website Monitoring Permissions**: The system requires explicit permission from website owners before monitoring, as automated monitoring without consent may violate terms of service or computer misuse legislation.

- **Data Privacy**: Monitoring data must be handled in accordance with GDPR and local data protection regulations, particularly when monitoring customer-facing websites.

- **Intellectual Property**: The project utilises open-source technologies with appropriate licensing, ensuring compliance with MIT, Apache, and other relevant licenses.

### Ethical Considerations
- **Responsible Disclosure**: When defacement or security issues are detected, responsible disclosure practices must be followed, notifying website owners before public disclosure.

- **Rate Limiting**: The monitoring system implements appropriate rate limiting to avoid causing denial-of-service conditions on monitored websites.

- **Transparency**: Website owners must be informed about what is being monitored and how data is stored and used.

### Professional Issues
- **Accuracy of Alerts**: False positive alerts can cause unnecessary concern and resource expenditure, requiring careful tuning of detection algorithms.

- **Dependency Management**: The system's reliance on third-party services (Telegram API) creates a dependency that must be managed and documented.

- **Maintenance Responsibility**: As a local deployment, ongoing maintenance and updates become the responsibility of the deploying organisation, requiring appropriate documentation and support.

## 1.9 Chapter Summary

This chapter has established the foundation for the WebGuard project by clearly articulating the problem statement facing SMEs in cybersecurity monitoring. The importance of automated security monitoring has been justified through reference to industry statistics and real-world consequences. Website defacement and SSL certificate expiry have been identified as critical threats requiring automated detection capabilities. The project's aims and objectives have been defined, establishing clear success criteria for development. The scope has been delineated to focus on core monitoring capabilities while acknowledging future enhancement possibilities. Limitations and constraints have been honestly assessed, and legal, ethical, and professional considerations have been addressed to ensure responsible development and deployment. The following chapters will build upon this foundation, examining existing solutions, defining requirements, and documenting the complete development process.

