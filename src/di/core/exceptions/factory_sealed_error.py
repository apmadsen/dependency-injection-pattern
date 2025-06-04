# pragma: no cover
class FactorySealedError(Exception):
    """
    The FactorySealedError is raised when container has been sealed, and additional services are being added afterwards.
    """
