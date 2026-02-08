# System Architecture

This document describes the architecture of the Remote Servers Marketplace across two complementary dimensions:
1. **C4-style structural views (System Context and Container views)**, providing the high-level system decomposition.
2. **4+1 view model** of software achitecture which comprises: 
- A `logical view`: shows key abstractions in the system as objects or object classes.
- A `process view`: shows how, at run-time, the system is composed of interacting processes. 
- A `development view`: shows how the software is decomposed for development. 
- A `physical view`: shows the system hardware and how software components are distributed across the processors in the system.

Component-level details are documented separately in `~/design/class-diagrams.md` and `~/design/data-model-er.md`.

---

## 1) High-Level Architecture (C4 Level-2: Container View)

The high-level structure of the system is represented using a C4 Level-2 Container Diagram (`~/diagrams/system-architecture.mmd`). It shows the major runtime containers, their responsibilities, and the communication paths between them. 

The main containers are as follows:

- **Web Clients**: Buyer, Provider, Administrator, and Organizational Administrator that access the system via HTTPS.  
- **Control Plane (Backend APIs)**: API Gateway, Authentication, Listings, Bookings, Billing, Benchmarking, Compliance/Data Wiping, Admin/Moderation, and Async Jobs/Queue.  
- **Secure Access Layer**: WireGuard VPN for network isolation; SSH key management for account-less server access.  
- **Provider Host**: Provider Agent (provisioning, metrics, wipe) + Metrics Exporter.  
- **Data Plane**: PostgreSQL (to store main entities and their attributes), Object Storage (as a file/blob store which will be used for benchmark artifacts and wipe evidences), Message Queue (a transport for async jobs).  

---

## 2) 4+1 Views

### Logical View (Domain and Services)
- **Core entities**: User, Machine, Listing, Booking, Benchmark, Payment, DataWipe.  
- **Core services**: Authenthication, Listings, Booking, Billing, Benchmarks, Compliance, Admin.  
- **External services**: Payment Processor.

### Process View (Runtime and Concurrency)
- **API Gateway** fronts modular services (start as modular monolith; keep boundaries to support later split).  
- **Async Jobs** handle long-running tasks (provisioning, wipe verification).  
- **Provider Agent** communicates via message queue + HTTPS callbacks; sends heartbeats and metrics.  
- **Observability** central logs & metrics for reliability/SLA alerts.

### Development View
- `backend/`: packages per service (+ shared libs for DTOs/clients).  
- `agent/`: separate package for Provider Agent.  
- `frontend/`: portals (separate apps or a single app with role-based routing).  
- `infra/`: for IaC/CI-CD; 
- `diagrams/`: for Mermaid sources (e.g. class diagram, system architecture).

### Physical View (Deployment)
- **Cloud**: API and DB in VPC; VPN gateway; object storage; queue; monitoring stack.  
- **Provider hosts**: run the agent container; outbound-only to control plane; mutual TLS for trust.  
- **Network**: Buyers connect through VPN to reach dedicated host; SSH keys for shell access.  
- **Transaction-style web system**: deployed in multi-tier client-server layout.

### Scenarios (+1)
- **Booking flow**: Search → Book → Provision VPN/SSH → Use → Checkout → Wipe → Release.  
- **Dispute resolution**: Admin inspects logs/metrics and listing policy compliance.

---

## 3) Architectural Style and Patterns

- **Layered**: Presentation ↔ Application ↔ Data; supports security (inner layers protect critical assets) and maintainability.
- **Client-Server / Microservices-ready**: Clear separation of concerns; can start modular and evolve. 
- **MVC (front-end)** for views/controllers around listing, booking, admin screens.  
- **Repository & DAO** for persistence boundaries (clean testing/mocking). 
- **Strategy** for pluggable benchmarking and wipe/attestation mechanisms.  

---

## 4) Security and Compliance Considerations

- VPN-only ingress to hosts; **no public SSH**, short-lived keys.  
- **Wipe** evidence stored with each booking; Admin compliance dashboard.  
- **RBAC** for Organizational Administrators and platform Administrators; audit logs for sensitive operations.  
- **Escrow** protects both buyer and provider; PCI scope offloaded to the payment processor.

---

## 5) Trade-offs and Risks
- **Complexity vs MVP**: start modular monolith for speed; keep boundaries clean to split later if needed. 
- **Provider network variability**: enforce baseline configs via Agent; health checks & auto-pause listings.  
- **Performance vs isolation**: dedicated servers → strong isolation at slightly higher cost; acceptable for our target users.

---

## 6. Design Artifacts in This Repository

The following design artifacts complement the system architecture by detailing specific implementation views:

- `design/data-model-er.md` — Logical data model and ER diagram (UML class-to-ER mapping).  
- `design/class-diagrams.md` — Domain and service layer classes (inheritance, associations, aggregations).  
- `design/design-patterns.md` — Documented design pattern choices, benefits, trade-offs, and anti-patterns to avoid.
