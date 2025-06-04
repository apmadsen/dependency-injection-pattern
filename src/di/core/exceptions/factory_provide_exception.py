# pragma: no cover
from typing import Mapping, overload
from typingutils import AnyType

from di.core.helpers import get_service_name

class FactoryProvideException(Exception):
    """
    The FactoryProvideException is raised when factory cannot provide service, because one or more
    of it's arguments cannot be provided, or when implementation returns an unexpected value
    or raises an exception.
    """
    @overload
    def __init__(self, service: AnyType | str) -> None:
        ...
    @overload
    def __init__(self, service: AnyType | str, failed_args: Mapping[str, type]) -> None:
        ...
    def __init__(self, service: AnyType | str, failed_args: Mapping[str, type] | None = None):
        service = get_service_name(service)
        if failed_args:
            f_args = ", ".join([ f"'{arg}'({get_service_name(arg_type)})" for arg, arg_type in failed_args.items() ])
            super().__init__(f"Cannot provide service '{service}' because argument(s) {f_args} cannot be provided")
        else:
            super().__init__(f"Cannot provide service '{service}'")
