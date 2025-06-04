from typing import Protocol, Any, TypeVar, overload, runtime_checkable

from di.core.scope import Scope
from di.core.service_request import ServiceRequest

T = TypeVar("T")

@runtime_checkable
class Provider(Protocol): # pragma: no cover

    def provides(self, service: str | type[Any]) -> bool:
        ...

    @overload
    def provide(self, service: type[T]) -> T:
        ...
    @overload
    def provide(self, service: type[T], scope: Scope) -> T:
        ...
    def provide(self, service: type[T], scope: Scope | None = None) -> T:
        ...

    def _provide(self, service: type[T] | ServiceRequest[T], scope: Scope | None = None) -> T:
        ...