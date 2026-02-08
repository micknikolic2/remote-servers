# Conceptual Entity–Relationship Model

This document defines the Conceptual Entity-Relationship model for the Remote Servers Marketplace.

At this level, we model only the **core business entities** and the **relationships between them**, without attributes, data types, primary and foreign keys, or implementation concerns. The conceptual model is:

- **Technology-agnostic** (no PostgreSQL or schema details).
- **Role-agnostic** (Buyer, Provider, Administrator, Organizational Administrator are *roles* of `User`).
- A bridge between the **System Architecture** (`system-architecture.md`) and the **Logical / Physical ERDs**.

---

## 1. Modeling Scope

The conceptual model focuses on the core marketplace flows:

- Users offering machines as commercial listings.
- Other users booking those listings.
- Benchmarks that characterize machine performance.
- Payments for completed bookings.
- Data wipe events that ensure post-usage security and compliance.

The core entities at this level are:

- `User`
- `Machine`
- `Listing`
- `Booking`
- `Benchmark`
- `Payment`
- `DataWipe`

---

## 2. Core Entities

> Note: At the conceptual level, entities are defined by their **role in the domain**, not by their attributes.

### 2.1 User
Represents any authenticated actor on the platform:
- Can act as **Buyer**, **Provider**, **(Platform) Administrator**, or **Organizational Administrator**.
- Interacts with listings, bookings, payments, and benchmark workflows.

### 2.2 Machine
Represents a **physical server** owned or controlled by a Provider:
- A machine is the technical resource that will be exposed to Buyers via Listings.
- Health, capacity, and performance are associated with the Machine in the domain.

### 2.3 Listing
Represents a **commercial offering** of a Machine:
- Defines how a Machine is exposed on the marketplace (availability and pricing bundles).
- A single Machine may have one or more Listings (e.g. different pricing plans or configurations), or exactly one depending on future policy.

### 2.4 Booking
Represents a **reservation / contract** between a Buyer and a Listing:
- Captures the time-bounded right of a Buyer to use a specific Machine via a Listing.
- Acts as the central transactional entity in the marketplace.

### 2.5 Benchmark
Represents **performance measurement results** for a Machine:
- Produced by Provider Agents and verified by Platform Administrators.
- Used to build trust and transparency for Buyers choosing between Listings.

### 2.6 Payment
Represents a **financial transaction** linked to a Booking:
- Encapsulates the monetary settlement for usage of a Machine under a Booking.
- May integrate with external payment processors / invoicing.

### 2.7 DataWipe
Represents a **data sanitization event** executed after or around Machine usage:
- Captures that a Machine has been wiped (or attempted to be wiped) after a Booking.
- Supports compliance, security guarantees, and dispute resolution.

---

## 3. Relationships

This section describes **how entities relate** in the business domain. Cardinalities here are conceptual and may be refined in the Logical Entity-Relationship diagram.

1. **User — Machine**
   - A `User` (acting as Provider) **owns or manages** one or more `Machine` entities.
   - A `Machine` is owned/managed by exactly one `User`, i.e. one Admin of a provider account (in case of institutions – it is the Organizational Administrator).
   - **Conceptual relationship**:  
     - `User (Provider)` 1 → * `Machine`

2. **Machine — Listing**
   - A `Machine` is **offered on the marketplace** via one or more `Listing` entries (or at least one).
   - A `Listing` is always associated with exactly one `Machine`. A machine can be a single machine or a cluster machine with multiple nodes.
   - **Conceptual relationship**:  
     - `Machine` 1 → * `Listing`

3. **Listing — Booking**
   - A `Listing` can have multiple `Booking` records over time (different Buyers, time windows).
   - Each `Booking` refers to exactly one `Listing`.
   - **Conceptual relationship**:  
     - `Listing` 1 → * `Booking`

4. **User — Booking**
   - A `User` (acting as Buyer) can create many `Booking` entities over time.
   - Each `Booking` is initiated by exactly one Buyer `User`.
   - **Conceptual relationship**:  
     - `User (Buyer)` 1 → * `Booking`

5. **Machine — Benchmark**
   - A `Machine` can have many `Benchmark` runs over time (periodic or on-demand).
   - A `Benchmark` is associated with exactly one `Machine`.
   - **Conceptual relationship**:  
     - `Machine` 1 → * `Benchmark`

6. **Booking — Payment**
   - A `Booking` may be associated with one or more `Payment` records (partial payments, retries, refunds etc.), depending on business rules.
   - A `Payment` always relates to exactly one `Booking`.
   - **Conceptual relationship**:  
     - `Booking` 1 → * `Payment`

7. **Booking — DataWipe**
   - A `Booking` may generate zero, one, or multiple `DataWipe` events (initial wipe, re-wipe, partial failures, retries).
   - A `DataWipe` event is conceptually tied to at least one `Booking` (driving the wipe) and one `Machine` (target of the wipe).
   - **Conceptual relationship**:  
     - `Booking` 1 → * `DataWipe`  
     - `Machine` 1 → * `DataWipe`

8. **User — Payment**
   - A `User` (as Buyer) is the payer in one or more `Payment` records.
   - Optionally, a `User` (as Provider) may be the recipient in payout flows (modeled in logical/physical layers via additional entities if required).
   - **Conceptual relationship**:  
     - `User (Buyer)` 1 → * `Payment`

---
