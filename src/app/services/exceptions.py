class ServiceError(Exception):
    """Base service exception."""


class NotFoundError(ServiceError):
    """Entity not found."""


class ConflictError(ServiceError):
    """Conflict with current state."""


class PermissionDeniedError(ServiceError):
    """Actor does not have required permission."""


class ValidationError(ServiceError):
    """Business validation error."""
