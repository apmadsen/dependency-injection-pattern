# pragma: no cover
class ContainerSealedError(Exception):
    """
    The ContainerSealedError is raised when container has been sealed, and additional services are being added afterwards.
    """
