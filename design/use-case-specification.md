## Purpose of the Document  
This document provides a structured description of the **use cases** for the Remote Servers Marketplace.  

It explains how different stakeholders interact with the platform and outlines the system functions needed to support their goals.  

A visual representation of the core stakeholder interactions is given in `design/use-cases-uml.png`.

---

## Actor-Centered Analysis  

### Buyer  
**Description:** Individual professionals, organizations, universities, research centers, and enthusiasts seeking computing resources.  

| Use Case | Goal | Notes |
|----------|------|-------|
| Search and Filter Servers | Identify machines by GPU, CPU, memory, storage, bandwidth, price, and location | Supports reproducible research and workload-specific needs |
| Review Benchmarks | Compare performance results before booking | Benchmark badges ensure transparency |
| Secure Booking | Reserve servers and pay through the marketplace | Escrow ensures trust between parties |
| Access Server | Obtain SSH key and VPN configuration | Direct access to dedicated server, no multi-tenancy |
| Privacy Protection | Guarantee data is deleted at end of session | Wipe data confirm compliance |

---

### Provider  
**Description:** Individuals, labs, small data centers, and universities offering idle capacity.  

| Use Case | Goal | Notes |
|----------|------|-------|
| Create Listing | Publish machine specifications, availability, and pricing | Requires admin verification before going live |
| Update Availability | Adjust schedules and resource details | Prevents double-bookings |
| Verification | Prove identity and machine specifications | Builds buyer confidence |
| Monitor Metrics | Provide uptime, usage, and health data | Agent software collects and reports |
| Receive Payments | Secure payout after completed bookings | Funds released from escrow |

---

### Admin  
**Description:** Platform operators maintaining trust, compliance, and operational health.  

| Use Case | Goal | Notes |
|----------|------|-------|
| Verify Providers | Ensure only legitimate providers join | Includes identity and hardware checks |
| Monitor Compliance | Check wipe attestations, logs, and data handling | Critical for trust and legal obligations |
| Resolve Disputes | Intervene in conflicts between buyers and providers | Requires access to logs and metrics |
| Oversee Transactions | Manage billing, payouts, and records | Ensures platform integrity |

---

### Organizational Administrator  
**Description:** University IT managers, institutional leads, or research coordinators.  

| Use Case | Goal | Notes |
|----------|------|-------|
| Manage Users | Add, remove, and assign roles to team members | Facilitates group access to shared resources |
| Consolidated Billing | Generate invoices covering all usage | Simplifies reporting for institutions |
| Procurement Compliance | Align bookings with internal financial procedures | Ensures institutional policies are respected |

---

## System View of Interactions  
- Buyers request computing capacity and receive secure access.  
- Providers supply servers and publish benchmarks and metrics.  
- Admins verify all listings and oversee disputes, compliance, and payouts.  
- Organizational Administrators extend buyer functionality by managing billing and team access at the institutional level.  

---

## Reflection  
The actor-centered approach highlights **security, trust, and transparency** as the foundation of the marketplace. 

By mapping out use cases per stakeholder, the document shows clear alignment between requirements and design decisions.  

This analysis guides the subsequent development of system architecture and database models.  
