# Class Diagram – Remote Servers Marketplace (FastAPI Backend)

This document describes the **class-level architecture** of the Remote Servers Marketplace backend.

It complements:

- `design/system-architecture.md` (C4 + 4+1 views)
- `design/data-model/*` (Conceptual / Logical / Physical Entity-Relationship diagrams)

and focuses on how the **FastAPI application**, **services**, **repositories**, and **domain models** are structured around the core entities:

- `User`
- `Machine`
- `Listing`
- `Booking`
- `Benchmark`
- `Payment`
- `DataWipe`

---

## 1. Architectural Style

The backend is implemented as a **modular monolith** using **FastAPI**, following a layered structure:

- **API Layer (Presentation)**  
  - FastAPI application and routers (endpoints).
  - Responsible for HTTP concerns (routing, status codes, request/response mapping).

- **Service Layer (Application / Domain Logic)**  
  - Services encapsulate use cases such as “create booking”, “list listings”, “record benchmark”.
  - Orchestrate repositories, external integrations (Supabase Auth), and domain rules.

- **Repository Layer (Persistence)**  
  - Repositories encapsulate database access using SQLAlchemy.
  - Implement CRUD operations against PostgreSQL tables defined in the Physical ERD.

- **Domain Model Layer (Data / ORM)**  
  - SQLAlchemy ORM models mapped to physical tables (users, machines, listings, bookings, benchmarks, payments, data_wipes).

- **Schema Layer (DTOs)**  
  - Pydantic models for request/response bodies.
  - Decouple API contracts from domain models.

- **Integrations Layer**  
  - Supabase Auth client and any external services (e.g., payment processor).

The diagram in `diagrams/class-diagram.mmd` visualizes these layers and their dependencies.

---

## 2. Package Overview (Backend)

A typical layout for the FastAPI backend is assumed:

```text
app/
  main.py
  api/
    v1/
      routers/
        auth.py
        users.py
        listings.py
        bookings.py
        payments.py
        benchmarks.py
        data_wipes.py
  services/
    auth_service.py
    users_service.py
    listings_service.py
    bookings_service.py
    payments_service.py
    benchmarks_service.py
    data_wipes_service.py
  repositories/
    user_repository.py
    machine_repository.py
    listing_repository.py
    booking_repository.py
    payment_repository.py
    benchmark_repository.py
    data_wipe_repository.py
  models/
    user.py
    machine.py
    listing.py
    booking.py
    payment.py
    benchmark.py
    data_wipe.py
  schemas/
    auth.py
    user.py
    listing.py
    booking.py
    payment.py
    benchmark.py
    data_wipe.py
  integrations/
    supabase_client.py
  core/
    config.py
    database.py