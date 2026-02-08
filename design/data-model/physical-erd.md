# Physical Entity–Relationship Model (PostgreSQL)

This document defines the **Physical Entity–Relationship Model** for the Remote Servers Marketplace.  

It refines the Logical Entity-Relationship model into a fully specified PostgreSQL database schema, including:

- Tables  
- Column data types  
- Primary keys (PK)  
- Foreign keys (FK)  
- Constraints  
- Indexes  
- CHECK conditions  
- Status enumerations  
- Physical Entity-Relationship diagram (`diagrams/physical-erd.mmd`)

This document is database-specific and corresponds to the tables that can be found in the
`~/db/schema/initial_schema_001.sql`.

---

# 1. Global Design Decisions

- **Database**: PostgreSQL 15+
- **Primary keys**: `UUID` with `DEFAULT gen_random_uuid()`
- **Timestamps**: `TIMESTAMP` for all time values
- **Structured fields**: JSON stored as `JSONB` (machine metrics, etc.)
- **Monetary values**: `NUMERIC(12,2)`
- **Status fields** stored as `TEXT` with strict `CHECK` constraints (upgradeable to ENUM)
- **Naming conventions**:
  - Tables: snake_case plural (e.g. `users`, `machines`, `listings`)
  - Columns: snake_case
  - Indexes: `idx_<table>_<column>`
  - Constraints: `fk_<table>_<column>`

> NOTE: This design is normalized (3NF), with selective denormalization for analytics (`hardware_id` appears in multiple tables to ensure traceability).

---

# 2. Required Extensions

```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;  -- required for gen_random_uuid()
