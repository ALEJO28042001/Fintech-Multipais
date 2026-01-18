from fastapi import Request
from fastapi.responses import JSONResponse
from core.exceptions import (
    ValidationError,
    InvalidStateError,
    NotFoundError,
    PermissionError,
)

def validation_error_handler(_: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content={"error": "validation_error", "detail": str(exc)},
    )

def invalid_state_error_handler(_: Request, exc: InvalidStateError):
    return JSONResponse(
        status_code=409,
        content={"error": "invalid_state", "detail": str(exc)},
    )

def not_found_error_handler(_: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=404,
        content={"error": "not_found", "detail": str(exc)},
    )

def permission_error_handler(_: Request, exc: PermissionError):
    return JSONResponse(
        status_code=403,
        content={"error": "forbidden", "detail": str(exc)},
    )
