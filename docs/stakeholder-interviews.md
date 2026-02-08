## Overview  
As part of the Requirements Analysis phase, interviews were conducted with key stakeholders of the Remote Servers Marketplace. 

The purpose of these interviews was to understand the needs, expectations, and concerns of each stakeholder group in order to define functional and non-functional requirements.  

---

## Stakeholder Groups  

### 1. Buyers  
**Profile:**  
Researchers, universities, research centers, professionals, startups, and enthusiasts who require dedicated high performance computing resources.  

**Needs and Expectations:**  
- Access to dedicated remote servers with clear specifications (GPU model, VRAM, CPU, RAM, storage, network bandwidth).  
- Transparent and competitive pricing with flexible booking (hourly, daily, weekly).  
- Secure and reliable access through SSH keys and VPN configuration.  
- Assurance that servers are wiped and secure before and after use.  
- Benchmark data to compare performance of machines prior to booking.  

**Pain Points:**  
- High costs of traditional cloud providers.  
- Limited access to specific GPU or CPU models in existing services.  
- Concerns about data privacy, reliability, and compliance when using third-party infrastructure.  

**Success Criteria:**  
- Easy search and booking experience with filters tailored to computationally demanding workloads.  
- Reliable server performance that matches published benchmarks.  
- Secure environment with clear privacy guarantees and data protection policies.  

---

### 2. Providers  
**Profile:**  
Labs, universities, small data centers, and individuals with idle compute resources willing to rent them out.  

**Needs and Expectations:**  
- Simple onboarding and verification process for listing servers.  
- Ability to set pricing, availability, and usage conditions.  
- Automated billing and guaranteed payments after completed bookings.  
- Monitoring and reporting tools to show uptime and usage to buyers.  
- Reputation and rating system to build trust with buyers.  

**Pain Points:**  
- Difficulty finding buyers independently.  
- Risk of misuse of servers by buyers (e.g. unauthorized activities).  
- Administrative burden in managing availability, access, and payment.  

**Success Criteria:**  
- A trusted platform that guarantees payment and reduces risk of fraud.  
- Transparent metrics and monitoring for buyers and providers.  
- Efficient process for listing, updating, and managing server resources.  

---

### 3. Admins  
**Profile:**  
Platform operators responsible for verification, compliance, dispute resolution, and overall system health.  

**Needs and Expectations:**  
- Tools for verifying provider identities and server specifications.  
- Monitoring to ensure compliance with platform rules and security standards.  
- Mechanisms for handling disputes between buyers and providers.  
- Oversight of transactions, billing, and payouts.  
- Ability to enforce policies on data privacy, data wipe, and fair use.  

**Pain Points:**  
- Managing disputes between parties without clear evidence.  
- Ensuring the platform is not misused for malicious or illegal activities.  
- Balancing security requirements with ease of use.  

**Success Criteria:**  
- Smooth onboarding and compliance management for providers.  
- Reliable reporting and monitoring dashboards.  
- Low dispute rates and high customer satisfaction.  

---

### 4. Organizational Administrators (Institutional Buyers)  
**Profile:**  
University IT staff, research project managers, and organizational leads managing multiple users within one institution.  

**Needs and Expectations:**  
- Role-based access management for team members.  
- Consolidated reporting and billing for all institutional usage.  
- Compliance guarantees to meet university or research center data policies.  

**Pain Points:**  
- Difficulty managing multiple users under one billing account.  
- Concerns about compliance and audit trails for sensitive research workloads.  

**Success Criteria:**  
- Flexible account management with multiple user roles.  
- Compliance assurances aligned with research and academic standards.  

---

## Summary of Findings  
The interviews confirmed that all stakeholders value security, transparency, and trust as core priorities. Buyers require flexible and affordable access to high performance computing resources, providers want simplified listing and payment, admins need reliable oversight tools, and institutions require team management and compliance support.  

These findings directly inform the functional and non-functional requirements of the platform and guides the next stages of system design.  
