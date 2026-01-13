# Fintech-Multipais

This project implements the core domain of a multi-country credit application system, focusing on clean domain modeling and business rule isolation.
The design allows the solution to scale by adding new countries, rules, and integrations without impacting existing functionality.

## Project Status

This project is being developed incrementally.

At this stage, the **core domain layer** is fully implemented and covered by unit tests.

## Architecture

The solution follows a layered architecture:

- **Core (Domain)**: Business rules and domain model
- **Application (Use Cases)**: Orchestration and workflows *(next phase)*
- **Infrastructure**: API, persistence, external services *(future phase)*

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
    - **Domain events** capture important state changes

## Country Rules

Each country defines its own validation policy, isolated from others.

Examples:
- Spain requires a valid DNI and flags large amounts for additional review
- Portugal requires a verified NIF and applies an affordability rule based on income


## Testing

The core domain is fully covered by unit tests.

- Tests are pure Python and framework-independent
