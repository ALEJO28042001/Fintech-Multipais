# Fintech-Multipais

This project implements the core domain of a multi-country credit application system, focusing on clean domain modeling and business rule isolation.
The design allows the solution to scale by adding new countries, rules, and integrations without impacting existing functionality.

# Project Status

This project is under active development.

✅ Core domain implemented
✅ Application use cases implemented
✅ API layer implemented
✅ Bank providers implemented
✅ In-memory and PostgreSQL repositories implemented
✅ Database schema created
✅ End-to-end flows tested


## Architecture

The solution follows a layered architecture:

- **Core (Domain)**: Business rules and domain model
- **Applications (Use Cases)**: Orchestration and workflows
- **Infrastructure**: API, persistence, external services *(fakes)*
- **Tests**: All necessary units at this point

api → applications → core
           ↑
     infrastructure


## Core Domain

The core domain contains all business rules related to multi-country credit applications.
It is completely independent of frameworks, databases, and external services.
Core has no dependencies on outer layers.
Outer layers depend on the core.

### Credit Application Lifecycle

CREATED → VALIDATED | UNDER_REVIEW | REJECTED
VALIDATED / UNDER_REVIEW → APPROVED | REJECTED


### Responsibilities

The core domain is responsible for:
- Enforcing business invariants via value objects
- Managing credit application lifecycle and state transitions
- Applying country-specific validation rules
- Emitting domain events

### Structure

core/
├── credit_applications/
│   ├── entities.py
│   ├── value_objects.py
│   ├── enums.py
│   ├── repository.py
│   └── events.py
└── policies/
    ├── base.py
    ├── spain.py
    └── portugal.py

    - **Entities** model long-lived domain objects with identity
    - **Value Objects** enforce domain invariants and are immutable
    - **Country policies** encapsulate country-specific rules
    - **Core events** capture important state changes

## Country Rules

Each country defines its own validation policy, isolated from others.

Examples:
- Spain requires a valid DNI and flags large amounts for additional review
- Portugal requires a verified NIF and applies an affordability rule based on income

## Applications

The applications layer defines the system’s workflows. (Use Cases)
Each use case:

    - Represents a single business action
    - Coordinates core logic
    - Persists changes via repositories
    - Enforces business intent

### Structure

applications/
└── credit_applications/
    │
    ├── use_cases/
    │   ├── approve_credit_application.py
    │   ├── attach_bank_snapshot.py
    │   ├── create_credit_application.py
    │   ├── get_credit_application.py
    │   ├── list_credit_applications.py
    │   ├── reject_credit_application.py
    │   └── __init__.py
    │
    ├── policy_registry.py
    ├── update_application_state.py
    └── __init__.py


### Implemented Use Cases

    - Create credit application
    - Attach bank snapshot
    - Approve credit application
    - Reject credit application
    - Update credit application state
    - Get credit application
    - List credit applications

## Infrastructure 
The infrastructure layer contains replaceable adapters.

Current implementations:
    - In-memory,PostgreSQL repositories
    - Bank providers per country for Portugal and Spain
    - SQLAlchemy models and database configuration
    - External system adapters

### Bank Integration

    - Bank providers are implemented per country
    - Providers fetch raw external data and adapt it into an immutable domain BankSnapshot
    - Bank snapshots:
        - Can only be attached in VALIDATED or UNDER_REVIEW
        - Are required before approval
        - Are immutable once attached

### Persistence Strategy

#### Repositories

    - Repository interfaces are defined in core
    - Implementations live in infrastructure
    - Two implementations exist:
        - In-memory (tests)
        - PostgreSQL (production)

#### Domain ↔ Persistence Mapping

    - Domain objects are never persisted directly
    - Value objects and snapshots are serialized at repository boundaries
    - BankSnapshot is stored as JSON and rehydrated when loading

This preserves domain purity while allowing flexible storage.

### Database

    - PostgreSQL
    - SQLAlchemy ORM
    - Timezone-aware timestamps
    - JSON storage for bank snapshots
    - Simple string storage for enums (country, status,money,bank snapshot)

### Structure

infrastructure/
├── bank_providers/
│   ├── countries/
│   │   ├── portugal.py
│   │   ├── spain.py
│   │   └── __init__.py
│   │
│   ├── base.py
│   ├── exceptions.py
│   ├── registry.py
│   └── __init__.py
│
├── database/
│   ├── models/
│   │   ├── __init__.py
│   │   └── credit_application.py
│   │
│   ├── session.py
|   ├── base.py
│   └── __init__.py
│
├── repositories/
│   ├── __init__.py
│   ├── in_memory_credit_application.py
│   └── postgres_credit_application.py
│
└── __init__.py

## API 

    - FastAPI-based HTTP layer
    - Request / response DTOs
    - Dependency injection for repositories and use cases
    - Domain errors mapped to HTTP responses
    - Explicit request and response models

### Structure

api/
│
├── auth/
│   ├── dependencies.py
│   └── jwt.py
│
├── realtime/
│   └── websocket_manager.py
│
├── routers/
│   └── credit_applications.py
│
├── schemas/
│   ├── requests.py
│   └── responses.py
│
├── dependencies.py
├── errors.py
└── main.py


## Testing

The core domain is fully covered by unit tests.

- Tests are pure Python and framework-independent
