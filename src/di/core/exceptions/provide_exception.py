# pragma: no cover
from typing import overload

from di.core.helpers import get_service_name

class ProvideException(Exception):
    """
    The ProvideException is raised when provider cannot provide service.
    """

    @overload
    def __init__(self, service: type | str) -> None:
        ...
    @overload
    def __init__(self, service: type | str, reason: str) -> None:
        ...
    def __init__(self, service: type | str, reason: str | None = None):
        service = get_service_name(service)
        if reason:
            super().__init__(f"Cannot provide service '{service}': {reason}")
        else:
            super().__init__(f"Cannot provide service '{service}'")
