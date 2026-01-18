class CoreError(Exception):
    """
    Base class for all domain-related errors.
    """
    pass


class ValidationError(CoreError):
    """
    Raised when business rules are violated.
    """
    pass


class InvalidStateTransition(CoreError):
    """
    Raised when an invalid state change is attempted.
    """
    pass

class InvalidStateError(CoreError):
    """Illegal state transition attempted"""


class NotFoundError(CoreError):
    """Entity not found"""


class PermissionError(CoreError):
    """Action not allowed by business rules"""