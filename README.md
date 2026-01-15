# Fintech-Multipais

This project implements the core domain of a multi-country credit application system, focusing on clean domain modeling and business rule isolation.
The design allows the solution to scale by adding new countries, rules, and integrations without impacting existing functionality.

Project Status

This project is under active development.

✔ Core layer is fully implemented and unit tested
✔ Application layer (use cases) is implemented and tested
🚧 Infrastructure layer is intentionally minimal (in-memory, fakes only)


## Architecture

The solution follows a layered architecture:

- **Core (Domain)**: Business rules and domain model
- **Applications (Use Cases)**: Orchestration and workflows
- **Infrastructure**: API, persistence, external services *(fakes)*
- **Tests**: All necessary units at this point

## Core Domain

The core domain contains all business rules related to multi-country credit applications.
It is completely independent of frameworks, databases, and external services.
Core has no dependencies on outer layers.
Outer layers depend on the core.

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
│   └── events.py
└── countries/
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

### Implemented Use Cases

    - Create credit application
    - Attach bank snapshot
    - Approve credit application
    - Reject credit application
    - Update application state

## Infrastructure 
The infrastructure layer contains replaceable adapters.

Current implementations:
    - In-memory repositories (for testing)
    - Fake bank providers (Spain, Portugal)

This layer exists to support integration, not to define behavior.

Use cases are explicit, testable, and side-effect free except for persistence calls.

## Testing

The core domain is fully covered by unit tests.

- Tests are pure Python and framework-independent
