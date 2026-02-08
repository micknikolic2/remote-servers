# Logical Entity–Relationship Model

This document defines the **Logical Entity-Relationship model** for the Remote Servers Marketplace.

At this level we:

- Define **entities, attributes, primary keys (PK), and foreign keys (FK)**.
- Keep the model **technology-agnostic** (no vendor-specific types).
- Make relationships **explicit** (1–N, N–1, N-M).
- Build directly on the conceptual model (`conceptual-erd.md`) and prepare for the Physical Entity-Relationship diagram.

Core entities:

- `User`
- `Machine`
- `Listing`
- `Booking`
- `Benchmark`
- `Payment`
- `DataWipe`

> Note: Roles (Buyer, Provider, Administrator, Organizational Administrator) are treated as *roles of `User`* at this stage and are not modeled as separate entities.

---

## 1. Entities and Attributes

### 1.1 User

Represents any authenticated account on the platform (Buyer, Provider, Administrator, Organizational Administrator).

**Primary key**

- `customer_id` – logical unique identifier for a user (internal ID used across the system).

**Attributes (logical types are indicative, not physical)**

| Attribute         | Type        | Description                                                         |
|------------------|------------ |---------------------------------------------------------------------|
| `customer_id`    | string      | Unique user identifier (PK).                                       |
| `email`          | string      | Unique email address for login and notifications.                  |
| `organization_name` | string  | Optional: organization or company name, if applicable.             |
| `is_billing_account` | boolean | Whether this user is the primary receiver of invoices.             |
| `signup_date`    | datetime    | When the user registered.                                          |


---

### 1.2 Machine

Represents a **physical server** provided by a User (acting as Provider).

**Primary key**

- `hardware_id` – unique identifier for a machine in the platform (logical machine key).

**Foreign keys**

- `customer_id` → `User.customer_id` (owner / provider).

**Attributes**

| Attribute             | Type       | Description                                                     |
|-----------------------|----------- |-----------------------------------------------------------------|
| `hardware_id`         | string     | Unique machine identifier (PK).                                 |
| `customer_id`         | string     | FK to `User` (the provider who owns/manages this machine).      |
| `gpu_model`           | string     | GPU model (e.g. "RTX 4090").                                   |
| `cpu_model`           | string     | CPU model (e.g. "AMD EPYC 7742").                              |
| `ram_gb`              | integer    | Primary memory size in GB.                                     |
| `disk_type`           | string     | Type of disk (e.g. "NVMe", "SSD", "HDD").                       |
| `disk_size_gb`        | integer    | Secondary storage size in GB.                                  |
| `network_bandwidth`   | string     | Network link characteristics (e.g. "10 Gbps").                  |
| `os`                  | string     | Operating system (e.g. "Ubuntu 22.04").                         |
| `provider_agent_status` | string   | Status of the provider agent ("online", "offline").             |
| `health_indicators`   | json       | Structured health metrics (CPU load, GPU load, temp, RAM, etc).|

> `health_indicators` is modeled as a logical structured field (e.g. JSON or sub-entity) and can be normalized later if needed.

---

### 1.3 Listing

Represents a **commercial offering** of a Machine (how it appears on the marketplace).

**Primary key**

- `listing_id` – surrogate ID for the listing.

**Foreign keys**

- `hardware_id` → `Machine.hardware_id`.

**Attributes**

| Attribute        | Type       | Description                                                       |
|------------------|----------- |-------------------------------------------------------------------|
| `listing_id`     | string     | Unique listing identifier (PK).                                   |
| `hardware_id`    | string     | FK to `Machine` (machine being offered).                          |
| `price_hour`     | float      | Price per hour.                                                   |
| `price_day`      | float      | Price per day.                                                    |
| `price_week`     | float      | Price per week.                                                   |
| `currency`       | string     | Currency code (e.g. "EUR", "USD").                               |
| `status`         | string     | Listing status (e.g. "active", "paused", "archived").             |
| `created_at`     | datetime   | When the listing was created.                                     |
| `updated_at`     | datetime   | Last time the listing was modified.                               |

---

### 1.4 Booking

Represents a **reservation / contractual usage** of a Listing by a Buyer.

**Primary key**

- `booking_id` – surrogate ID for the booking.

**Foreign keys**

- `listing_id` → `Listing.listing_id`.  
- `hardware_id` → `Machine.hardware_id` (denormalized for easier analysis and traceability).  
- `buyer_id` → `User.customer_id`.

**Attributes**

| Attribute        | Type       | Description                                                       |
|------------------|----------- |-------------------------------------------------------------------|
| `booking_id`     | string     | Unique booking identifier (PK).                                   |
| `listing_id`     | string     | FK to `Listing` that was booked.                                 |
| `hardware_id`    | string     | FK to `Machine` (same as listing’s machine; kept for analytics).  |
| `buyer_id`       | string     | FK to `User` (Buyer).                                             |
| `start_timestamp`| datetime   | Booking start time.                                               |
| `end_timestamp`  | datetime   | Booking end time (reserved until).                               |
| `created_at`     | datetime   | When booking was created.                                         |
| `booking_status` | string     | "pending", "active", "completed", "canceled", "disputed".         |

---

### 1.5 Benchmark

Represents **performance measurement results** for a Machine.

**Primary key**

- `benchmark_id` – surrogate ID for the benchmark run.

**Foreign keys**

- `hardware_id` → `Machine.hardware_id`. (Through `Machine.hardware_id` it can be related to `User.customer_id`.) 

**Attributes**

| Attribute                | Type       | Description                                                |
|--------------------------|----------- |------------------------------------------------------------|
| `benchmark_id`           | string     | Unique benchmark identifier (PK).                          |
| `hardware_id`            | string     | FK to `Machine` (machine evaluated).                       |
| `gpu_throughput_fp16`    | float      | GPU throughput at FP16.                                    |
| `gpu_throughput_fp32`    | float      | GPU throughput at FP32.                                    |
| `cpu_score`              | float      | CPU benchmark score.                                       |
| `disk_read_mb_s`         | float      | Disk read throughput (MB/s).                               |
| `disk_write_mb_s`        | float      | Disk write throughput (MB/s).                              |
| `network_bandwidth_gbps` | float      | Effective network bandwidth.                               |
| `collected_at`           | datetime   | When this benchmark was executed.                          |
| `admin_verification_status` | string  | "pending", "approved", "rejected".                         |

---

### 1.6 Payment

Represents a **financial transaction** associated with a Booking.

**Primary key**

- `payment_id` – surrogate ID for the payment.

**Foreign keys**

- `booking_id` → `Booking.booking_id`.  
- `hardware_id` → `Machine.hardware_id` (for traceability, optional but useful).  
- `payer_id` → `User.customer_id` (Buyer).  
- Optionally `provider_id` → `User.customer_id` (Provider) for payouts.

**Attributes**

| Attribute        | Type       | Description                                                        |
|------------------|----------- |--------------------------------------------------------------------|
| `payment_id`     | string     | Unique payment identifier (PK).                                    |
| `booking_id`     | string     | FK to `Booking` (which this payment settles).                      |
| `hardware_id`    | string     | FK to `Machine` (denormalized for analysis).                       |
| `payer_id`       | string     | FK to `User` (Buyer who pays).                                     |
| `provider_id`    | string     | FK to `User` (Provider being paid), if modeled at this level.      |
| `amount_total`   | decimal    | Total amount billed to the buyer.                                  |
| `currency`       | string?    | Currency code.                                                     |
| `payment_status` | string     | "incomplete", "paid", "failed".                                    |
| `timestamp`      | datetime   | When the payment attempt / event occurred.                         |
| `invoice_number` | string     | External or internal invoice reference.                            |

---

### 1.7 DataWipe

Represents a **data sanitization / wipe event** related to usage of a Machine (typically after a booking).

**Primary key**

- `wipe_id` – surrogate ID for the wipe event.

**Foreign keys**

- `hardware_id` → `Machine.hardware_id`.  
- `booking_id` → `Booking.booking_id` (when the wipe is associated with a specific booking).

**Attributes**

| Attribute             | Type       | Description                                                      |
|-----------------------|----------- |------------------------------------------------------------------|
| `wipe_id`             | string     | Unique wipe event identifier (PK).                               |
| `hardware_id`         | string     | FK to `Machine` (machine wiped).                                 |
| `booking_id`          | string     | FK to `Booking` that triggered the wipe (nullable for manual ops).|
| `timestamp`           | datetime   | When the wipe operation was executed.                            |
| `wipe_method_executed`| string     | e.g. "user_deletion", "ssh_key_removal", "home_directory_purge". |
| `status`              | string     | "success", "failed", "partial".                                  |
| `wipe_evidence_uri`   | string     | Reference to logs/artifacts in object storage (if available).    |

---

## 2. Relationships (Logical)

Cardinalities here are refined from the conceptual model.

1. **User–Machine**
   - `User` (Provider) **1 → N** `Machine`  
   - Implemented via `Machine.customer_id` → `User.customer_id`.

2. **Machine–Listing**
   - `Machine` **1 → N** `Listing`  
   - Implemented via `Listing.hardware_id` → `Machine.hardware_id`.

3. **Listing–Booking**
   - `Listing` **1 → N** `Booking`  
   - Implemented via `Booking.listing_id` → `Listing.listing_id`.

4. **User–Booking**
   - `User` (Buyer) **1 → N** `Booking`  
   - Implemented via `Booking.buyer_id` → `User.customer_id`.

5. **Machine–Benchmark**
   - `Machine` **1 → N** `Benchmark`  
   - Implemented via `Benchmark.hardware_id` → `Machine.hardware_id`.

6. **Booking–Payment**
   - `Booking` **1 → N** `Payment`  
   - Implemented via `Payment.booking_id` → `Booking.booking_id`.

7. **User–Payment**
   - `User` (Buyer) **1 → N** `Payment`  
   - Implemented via `Payment.payer_id` → `User.customer_id`.  
   - Optionally `User` (Provider) **1 → N** payouts via `Payment.provider_id`.

8. **Booking–DataWipe**
   - `Booking` **0..1 → N** `DataWipe`  
   - Implemented via `DataWipe.booking_id` → `Booking.booking_id` (nullable).

9. **Machine–DataWipe**
   - `Machine` **1 → N** `DataWipe`  
   - Implemented via `DataWipe.hardware_id` → `Machine.hardware_id`.

10. **Machine–Payment / Booking–Machine denormalization**
   - `Payment.hardware_id` and `Booking.hardware_id` are **denormalized FKs** for easier analytics and traceability.

---
