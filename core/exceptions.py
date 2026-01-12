class CoreError(Exception):
    """
    Base class for all domain-related errors.
    """
    pass


class CoreValidationError(CoreError):
    """
    Raised when business rules are violated.
    """
    pass


class InvalidStateTransition(CoreError):
    """
    Raised when an invalid state change is attempted.
    """
    pass
