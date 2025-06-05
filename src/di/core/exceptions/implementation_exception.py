# pragma: no cover
from typing import Any

from di.core.helpers import get_service_name

class ImplementationException(Exception):
    """
    The ImplementationException is raised at initialization time when factory cannot provide service using the
    specified implementation. This could be due to implementation not resolving to a class derived from service,
    or that implementaion cannot be resolved at all due to missing type annotations.
    """
    def __init__(self, service: type | str, implementation: Any, error: str):
        super().__init__(f"Factory cannot implement service '{get_service_name(service)}' via '{implementation}': {error}")
