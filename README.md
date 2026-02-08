# Remote Servers Marketplace

## **Overview**

Remote Servers Marketplace is a platform that connects providers of high-performance computing (HPC) resources with users who require scalable and secure remote servers for AI, ML, and other computational workloads (such as gaming).

It supports secure access, flexible pricing, organizational accounts, and compliance-ready billing.

The system aims to democratize access to computing power by allowing verified individuals and institutions to list, book, and manage remote servers through a transparent and extensible architecture.

---

## **Objectives**

1. Provide a secure and modular platform for remote server provisioning.  
2. Enable providers to list and monetize idle computing resources.  
3. Support buyers in renting GPU/CPU servers for short- or long-term tasks.  
4. Facilitate organizational accounts.  
5. Ensure compliance and security through access control and monitoring.  

---

## **Repository Structure**

<pre>
├── db/
│   └── schema/
│       └── initial_schema_001.sql               # PostgreSQL physical schema
│
├── design/                                      # System and design documentation
│   ├── data-model/                              # ERDs: conceptual → logical → physical
│   │   ├── diagrams/                            # Mermaid source diagrams (ERDs)
│   │   │   ├── conceptual-erd.mmd
│   │   │   ├── logical-erd.mmd
│   │   │   └── physical-erd.mmd
│   │   │
│   │   ├── conceptual-erd.md                    # Conceptual ER model
│   │   ├── logical-erd.md                       # Logical ER model
│   │   └── physical-erd.md                      # Physical PostgreSQL ERD
│   │
│   ├── class-diagrams.md                        # Class diagram explanation
│   ├── design-patterns.md                       # Applied design patterns and rationale
│   ├── system-architecture.md                   # High-level and layered system architecture
│   ├── use-case-specification.md                # Use case descriptions and flows
│   └── use-case-uml.png                         # Exported UML use case diagram
│
├── diagrams/                                    # High-level Mermaid diagrams
│   ├── class-diagram.mmd
│   └── system-architecture.mmd
│
├── docs/                                        # Project documentation and requirements
│   ├── software-requirements-specification.md   # Functional and non-functional requirements
│   ├── stakeholder-interviews.md                # Interview summaries
│   └── user-stories.md                          # User stories and acceptance criteria
│
├── LICENSE
└── README.md
</pre>

---

## **Data Model**

The data model defines entities such as:

- User, Role, Machine, Listing, Booking, Benchmark, Payment, Data Wipe

Each entity attributes are explained in the `dosc/software-requirements-specification.md`.

Entities' relationships are explained in the Conceptual Entity-Relationship model (`~design/data-model/conceptual-erd.md` and `~design/data-model/diagrams/conceptual-erd.mmd`).

Entities' attributes and primary and foreign keys are mapped in the Logical Entity-Relationship model (`~design/data-model/logical-erd.md` and `~design/data-model/diagrams/logical-erd.mmd`).

Entities operationalization through PostgreSQL, including tables, columns, data types, indexes, and constraints are explained in the Physical Entity-Relationship model (`~design/data-model/physical-erd.md` and `~design/data-model/diagrams/physical-erd.mmd`).

---

## **Design Patterns**

Documented in `~design/design-patterns.md`, the system adopts:

- **Repository Pattern** for data abstraction  
- **Strategy Pattern** for pricing and billing models  
- **Factory Pattern** for server instance creation  
- **Observer Pattern** for monitoring and notifications  

---

## **Documentation and Requirements**

- `software-equirements-specification.md` → Captures all functional and non-functional requirements on both user- and system-level.  
- `stakeholder-interviews.md` → Summarizes stakeholder goals and system expectations.  
- `user-stories.md` → Defines user journeys and acceptance criteria aligned with requirements.  

---

## **License**


This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.