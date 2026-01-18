from fastapi import FastAPI

from api.routers.credit_applications import router as credit_applications_router
from api.errors import (
    validation_error_handler,
    invalid_state_error_handler,
    not_found_error_handler,
    permission_error_handler,
)
from core.exceptions import (
    ValidationError,
    InvalidStateError,
    NotFoundError,
    PermissionError,
)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Fintech-Multipais",
        version="1.0.0",
    )

    # Routers
    app.include_router(
        credit_applications_router,
        prefix="/credit-applications",
        tags=["Credit Applications"],
    )

    # Domain → HTTP error mapping
    app.add_exception_handler(ValidationError, validation_error_handler)
    app.add_exception_handler(InvalidStateError, invalid_state_error_handler)
    app.add_exception_handler(NotFoundError, not_found_error_handler)
    app.add_exception_handler(PermissionError, permission_error_handler)

    return app


app = create_app()
