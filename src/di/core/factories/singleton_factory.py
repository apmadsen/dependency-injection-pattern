from typing import TypeVar, Callable, cast
from typingutils import is_type, isinstance_typing

from di.core.log import LOG
from di.core.helpers import get_service_name
from di.core.scope import Scope
from di.core.named_service import NamedService
from di.core.factories.factory import Factory
from di.core.protocols.container import Container

T = TypeVar('T')

class SingletonFactory(Factory[T]):
    __slots__ = ["__inst"]

    def __init__(self, container: Container, service: type[T], implementation: type[T] | Callable[..., T] | T | None = None):
        super().__init__(container, service, implementation)

        if implementation and is_type(service) and isinstance_typing(implementation, service, recursive=True):
            self.__inst: T | None = cast(T, implementation)
        elif callable(implementation):
            self.__inst: T | None = None
        elif service is NamedService:
            self.__inst: T | None = implementation
        else:
            self.__inst: T | None = None

    def provide(self, scope: Scope | None = None) -> T:
        if self.__inst is None:
            LOG.debug(f"Creating singleton object for service '{get_service_name(self.service)}'")
            self.__inst = super().provide(scope)
        return self.__inst
