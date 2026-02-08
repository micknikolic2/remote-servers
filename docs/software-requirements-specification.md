## 1. Introduction  

### 1.1 Purpose  
The purpose of this document is to specify the requirements for the remote servers marketplace platform. 

The platform (i) allows providers to rent out dedicated remote servers equipped for computationally demanding workloads (e.g. high performance computing, artificial intelligence, gaming), and (ii) enables buyers to securely leise these resources. Both providers and buyers can be individuals or organizations.

### 1.2 Scope  
The system will act as a web-based marketplace connecting buyers, providers, and administrators.  

It will include functionalities for (i) server listings (i.e. providers will be allowed to rent out their infrastructure), (ii) regular search, (iii) advanced search (i.e. buyers will be allowed to search resources based on detailed technical and business criteria), (iv) secure booking (i.e. a buyer rents out a machine for a specific period of time using a secure, protected workflow), (v) automated access provisioning (i.e. once a hardware is booked, the system automatically provides the access to a buyer, without manual work from the provider), (vi) metrics and benchmarks (i.e. the system provides performance insights about every listed server, so buyers know what they’re renting), (vii) billing (the platform handles billing, payments, and invoices), and compliance monitoring (i.e. the platform ensures ethical and legal functional requirements).

### 1.3 Objectives  
- Ensure a transparent, secure, and reliable environment for remote server rentals.  
- Support computationally heavy workloads by providing benchmarked, reproducible performance data.  
- Address institutional needs for compliance, user management, and financial reporting.  
- Provide an MVP that is feasible to build and extend in later phases.  

---

## 2. Stakeholders

### 2.1 Buyers  
- Researchers, professionals, startups, enthusiasts.  
- Require reliable, secure, and affordable access to computational resources.  

### 2.2 Providers  
- Individuals, labs, small data centers, universities.  
- Seek simple onboarding, verified listings, guaranteed payment.  

### 2.3 Admins  
- Platform operators.  
- Responsible for compliance checks, dispute resolution, and trust-building.  

### 2.4 Organizational Administrators  
- Institutional IT staff or project managers on buyers' or providers' side.  
- Need centralized billing, user management, and compliance guarantees.  

---

## 3. Functional Requirements  

### 3.1 Buyer Functions  
- Search and Filtering: Search listings by GPU, CPU, RAM, storage, bandwidth, region, and price.  
- Benchmark Access: View reproducible benchmark results for each server.  
- Booking and Payment: Book servers with secure payment flow.  
- Secure Access: Receive SSH and VPN configuration for dedicated access.  
- Privacy Assurance: Access wipe after booking ends.  

### 3.2 Provider Functions  
- Create Listing: Add servers with full technical specifications, pricing, and availability.  
- Update and Manage Listings: Modify details and availability.  
- Verification Process: Complete identity and machine verification.  
- Metrics Reporting: Provide uptime and usage metrics via agent.  
- Receive Payments: Collect funds after booking completion.  

### 3.3 Admin Functions  
- Verification and Approval: Review provider onboarding and server specifications.  
- Monitoring and Compliance: Track wipe operations, metrics, and privacy reports.  
- Dispute Handling: Access logs to resolve buyer–provider conflicts.  
- Transaction Oversight: Monitor billing, payouts, and refund processes.  

### 3.4 Organizational Administrator Functions  
- Manage Users: Add and assign roles for team members.  
- Centralized Billing: Consolidate invoices for multiple bookings.  
- Usage Reporting: View institution-wide reports of bookings and metrics.  

---

## 4. Non-Functional Requirements  

### 4.1 Security  
- All sessions must use VPN and SSH encryption.  
- Wipe after each booking ends.  
- Role-based access control for institutional accounts.  

### 4.2 Reliability  
- Providers' agents send regular heartbeats to confirm availability (each 60 seconds).  
- Automatic listing pause if a server becomes unavailable.  

### 4.3 Usability  
- Interface must allow buyers to filter and book servers in ≤ 5 steps.  
- Providers must be able to publish a listing in ≤ 10 minutes.  

### 4.4 Performance and Scalability  
- System must support 1,000 concurrent buyers and listings without degradation. This number can be updated during the software evolution.  
- Benchmark publishing ensures workloads are reproducible (i.e. published benchmarks must be deterministic).  

### 4.5 Compliance  
- Must adhere to GDPR and institutional data handling policies.  
- Provide data deletion guarantees within a specified timeframe.  

---

## 5. Constraints and Assumptions  

- MVP will only support dedicated single-tenant servers and multi-node cluster servers (no GPU slicing).  
- Payments will be processed through a secure payment processor to ensure trust.  
- Storage and orchestration are out of scope for MVP.  
- Providers are assumed to supply their own network and hardware.  

---

## 6. System Models  
 
- Architecture Diagram: control plane, provider host (a provider's agent sends heartbeats at each 60 seconds), data plane (PostgreSQL, object storage, message queue), and secure networking layer (SSH/VPN tunnel, API gateways, firewalls).  
- Use Case Diagram: shows interactions between Buyers, Providers, Admins, and Organizational Administrators.  
- Data Model: entities include  
  1. `User` (any authenticated user): key attributes include customer_id (unique internal user identifier; it will serve as primary – foreign key in future analysis), email, organization_name (optional – if organization), is_billing_account (whether this user is the primary receiver of invoices), signup_date;  
  2. `Machine` (physical hardware): key attributes include customer_id, gpu_model (e.g. RTX 4090), cpu_model (e.g. AMD EPYC 7742), ram_gb (primary memory size), disk_type, disk_size_gb (secondary memory size), network_bandwidth (network interface speed), os (e.g. Ubuntu 22.04), hardware_id (unique ID for a machine), provider_agent_status (online, offline), health_indicators (data sent by the agent inside of the heartbeat: timestamp, CPU load, GPU load and temperature, RAM usage, disk usage, machine uptime);  
  3. `Listing` (commercial offering of a machine): key attributes include hardware_id, price_hour (price per hour), price_day (price per day), price_week (price per week);
  4. `Booking` (reservation data; a core transactional entity): key attributes include hardware_id, start_timestamp, end_timestamp, timestamp, booking_status (pending, active, completed, canceled, disputed);  
  5. `Benchmark` (performance data generated by providers' agents and confirmed by platform administrators): key attributes include hardware_id, gpu_throughput_fp16, gpu_throughput_fp32, cpu_score, disk_read_mb_s, disk_write_mb_s, network_bandwidth_gbps, collected_at (timestamp when benchmark was run), admin_verification_status (pending, approved, rejected);
  6. `Payment` (transactions): key attributes include hardware_id, amount_total, payment_status (incomplete, paid, failed), timestamp, invoice_number; 
  7. `DataWipe` (wipe records): key attributes include hardware_id, timestamp, wipe_method_executed (e.g. user_deletion, ssh_key_removal, home_directory_purge, temp_directory_cleanup, process_termination, container_destroy), status (success, failed, partial), wipe_evidence_uri (a reference to logs/artifacts in object storage);

---

## 7. Validation  

Requirements for the system will be validated using a combination of structured review techniques and practical verification methods to ensure correctness, completeness, realism, and verifiability. Validation activities include:
  - User story acceptance criteria (i.e. each user story will include explicit acceptance criteria that define how the requirement will be satisfied).  
  - UML diagrams and sequence flows (i.e. behavioral and structural models (use-case diagrams, sequence diagrams, architecture diagrams) will be used to validate requirement consistency and completeness).  
  - Test cases during implementation (i.e. test scenarios and test cases will be derived directly from requirements; if a requirement cannot produce a test case, it indicates ambiguity or incompleteness).  
  - Stakeholder review during evaluation phase (i.e. stakeholders will review the requirements to confirm that they correctly reflect business needs).  

---

## 8. Summary  

This requirements specification defines the functional and non-functional scope of the Remote Servers Marketplace.  
It emphasizes security, transparency, and institutional readiness** as the foundation of the MVP.  

The document serves as a reference point for system design, implementation, and evaluation in the later phases of development.  
