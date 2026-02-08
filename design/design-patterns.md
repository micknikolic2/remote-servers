# Design Patterns – Remote Servers Marketplace

This document describes the **software design patterns** applied in the Remote Servers Marketplace backend. 

It connects the high-level architecture (`system-architecture.md`), data model (`data-model/*`), and code structure (FastAPI app, services, repositories, models, schemas) to well-known patterns from software engineering.

The goal is to make explicit:

- Which patterns we use.
- Why we chose them.
- Where they appear in the codebase.
- How they support extensibility, testability, and maintainability.

---

## 1. Architectural Patterns

### 1.1 Layered Architecture (Presentation → Application → Data)

**Pattern:** Layered Architecture  
**Where:** Entire backend (FastAPI + services + repositories + models).

We structure the backend into three main layers:

1. **Presentation / API Layer**  
   - FastAPI application and routers (e.g. `AuthRouter`, `ListingsRouter`, `BookingsRouter`).  
   - Responsible for HTTP endpoints, request validation, and response formatting.

2. **Application / Service Layer**  
   - Service classes (e.g. `AuthService`, `ListingsService`, `BookingsService`, `PaymentsService`).  
   - Encapsulate use cases and business rules (e.g. “create booking”, “list active listings”).

3. **Data / Persistence Layer**  
   - Repositories (e.g. `UserRepository`, `ListingRepository`, `BookingRepository`) and ORM models (`UserModel`, `ListingModel`, `BookingModel`).  
   - Encapsulate all database access using SQLAlchemy and the Physical ERD.

This separation:

- Keeps controllers thin and focused on HTTP concerns.
- Centralizes business logic in services.
- Isolates persistence concerns in repositories, which can be mocked in tests.

---

### 1.2 Client–Server with Modular Monolith

**Pattern:** Client–Server, Modular Monolith  
**Where:** Overall system (frontend + backend), as described in `system-architecture.md`.

The system uses a **client–server** pattern:

- **Client:** Web frontend (React or similar), talking over HTTPS.
- **Server:** FastAPI backend exposing JSON APIs.

Within the backend, we adopt a **modular monolith** style:

- Logical modules: auth, users, listings, bookings, benchmarks, payments, data wipes.
- Each module has its own routers, services, repositories, and models.

This allows:

- Clear boundaries and independent evolution per feature area.
- A straightforward path to split into separate services later if needed.

---

## 2. Object-Level Patterns

### 2.1 Repository Pattern

**Pattern:** Repository  
**Where:** `UserRepository`, `MachineRepository`, `ListingRepository`, `BookingRepository`, `PaymentRepository`, `BenchmarkRepository`, `DataWipeRepository`.

Repositories act as **abstractions over the database**. Each repository:

- Exposes clear methods such as `get_by_id`, `list_by_user`, `list_active`, `create`, etc.
- Hides SQLAlchemy queries and joins behind a stable interface.
- Works with domain models (`UserModel`, `BookingModel`, etc.) instead of raw rows.

Benefits:

- Tests can mock repositories instead of touching the real database.
- The service layer does not depend on SQLAlchemy directly, just on repository interfaces.
- Data access logic is centralized and easier to optimize (indexes, query tuning).

---

### 2.2 Service Layer / Facade

**Pattern:** Service Layer (also similar to Facade)  
**Where:** `AuthService`, `UsersService`, `ListingsService`, `BookingsService`, `PaymentsService`, `BenchmarksService`, `DataWipesService`.

Services represent **use-case–oriented facades** over the domain and repositories:

- `BookingsService.create_booking(...)` coordinates:
  - Validation of input data.
  - Fetching listing and machine data.
  - Checking user role / permissions.
  - Creating a `BookingModel` via `BookingRepository`.
  - Optionally triggering payment and wipe scheduling.

- `ListingsService.list_active_listings()`:
  - Delegates to `ListingRepository.list_active()`.
  - Applies any extra filtering or sorting rules.

Benefits:

- Business logic is not scattered across routers or models.
- One “entry point” per use case, which is easy to test and reason about.
- Services act as facades that hide internal complexity of repositories and integrations.

---

### 2.3 Data Transfer Object (DTO) / Schema Pattern

**Pattern:** Data Transfer Object (DTO)  
**Where:** Pydantic schemas such as `UserCreate`, `UserRead`, `ListingCreate`, `ListingRead`, `BookingCreate`, `BookingRead`.

Schemas serve as **DTOs** between API and domain:

- They define exactly what the API accepts and returns.
- They are independent of SQLAlchemy ORM models.
- Routers use schemas to validate requests and serialize responses.

Typical flow:

1. Router receives a request body deserialized into a `*Create` schema.
2. Router forwards this DTO to the corresponding service.
3. Service creates or updates ORM models.
4. Router returns a `*Read` schema to the client.

Benefits:

- Clean separation between API contracts and storage layer.
- Easier evolution of the API without breaking database schema immediately.
- Strong runtime validation via Pydantic.

---

### 2.4 Strategy Pattern (Benchmarks and Data Wipes)

**Pattern:** Strategy  
**Where:** Planned and partially implied around benchmarking and data wipe workflows.

The domain includes **pluggable behaviors** for:

- Different **benchmarking strategies** (e.g. GPU-focused, CPU-focused, storage-focused).
- Different **data wiping strategies** (e.g. “user_deletion”, “ssh_key_removal”, “home_directory_purge”, “container_destroy”).

Conceptually, each strategy implements a common interface:

- `BenchmarkStrategy.run(machine)`  
- `DataWipeStrategy.execute(machine, booking)`

Concrete strategies can be:

- Selected based on machine type, provider configuration, or policy.
- Extended without changing callers (e.g., adding a new wipe method later).

Even if not yet fully implemented as explicit classes, the design is aligned with Strategy and can be refactored into a formal Strategy pattern when needed.

---

## 3. Cross-Cutting Patterns and Practices

### 3.1 Dependency Injection via FastAPI

**Pattern:** Dependency Injection (DI)  
**Where:** FastAPI dependency system (`Depends`).

The backend uses FastAPI’s DI features to:

- Inject database sessions.
- Inject services and repositories.
- Inject the current authenticated user.

Routers declare dependencies in function signatures, allowing FastAPI to:

- Construct and provide the needed objects.
- Make testing easier by overriding dependencies in test cases.

---

### 3.2 Configuration as a Centralized Object

**Pattern:** Configuration / Singleton-like central config  
**Where:** `core/config.py` (or equivalent).

Application configuration (database URL, Supabase settings, etc.) is managed in a centralized module and imported where needed.  
This is not a strict Singleton class, but the pattern is similar: one configuration source used by multiple parts of the system.

---

### 3.3 Transaction Script (for some simple flows)

Not all flows need complex object collaboration. 
 
In some simple endpoints, we effectively use **Transaction Script**:

- Simple service methods that:
  - Validate input.
  - Perform one or two repository calls.
  - Return a result.

This is appropriate for straightforward operations and coexists with more object-oriented patterns for complex scenarios.

---

## 4. Relationship to Other Design Documents

This document is intended to be read alongside:

- `system-architecture.md` – high-level C4 / 4+1 architecture.
- `class-diagram.md` – routers, services, repositories, and models.
- `data-model/conceptual-erd.md` – conceptual domain relationships.
- `data-model/logical-erd.md` and `data-model/physical-erd.md` – logical and physical database models.

Together, these documents show:

1. **What** the system does (use cases and requirements).  
2. **How** it is structured (architecture and class diagrams).  
3. **Which** design patterns were chosen to keep it maintainable and extendable.

---