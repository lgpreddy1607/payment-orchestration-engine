class DomainError(Exception):
    """Base class for domain-level exceptions."""


class InvariantViolation(DomainError):
    """Raised when a domain invariant is broken."""


class CurrencyMismatch(DomainError):
    """Raised when operations involve mismatched currencies."""


class InvalidStateTransition(DomainError):
    pass

