# pragma: no cover
class AddException(Exception):
    """
    The AddException is raised when container cannot add a service either because service is already registered
    or because the container encountered an error with the specified service and implementation arguments.
    """

