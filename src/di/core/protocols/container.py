from typing import Protocol, TypeVar, runtime_checkable

from di.core.protocols.provider import Provider
from di.core.protocols.factory import Factory
from di.core.scope import Scope
from di.core.service_request import ServiceRequest


T = TypeVar("T")

@runtime_checkable
class Container(Protocol): # pragma: no cover

    @property
    def default_scope(self) -> Scope:
        ...

    def provider(self) -> Provider:
        ...

    def _defines(self, service: str | type) -> bool:
        ...

    def _get(self, service: type[T] | ServiceRequest[T]) -> Factory[T] | T | None:
        ...