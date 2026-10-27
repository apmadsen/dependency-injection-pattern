from collections.abc import Callable
from typing import TypeVar

from di.core.factories.factory import Factory
from di.core.protocols.container import Container
from di.core.scope import Scope

T = TypeVar('T')

class TransientFactory(Factory[T]):
    __slots__ = []

    def __init__(self, container: Container, service: type[T], implementation: type[T] | Callable[..., T] | None = None):
        super().__init__(container, service, implementation)

    def provide(self, scope: Scope | None = None) -> T:
        return Factory[T].provide(self, scope)

