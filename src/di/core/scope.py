from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Callable, TypeVar

T = TypeVar('T')

class Scope(ABC):
    """
    Scope is the base class from which scopes are derived, and its superclasses handle provision of
    scoped services.
    """

    @abstractmethod
    def provide(self, service: type[T], factory: Callable[[], T]) -> T:
        """This function function is used by the `ScopedFactory` factory to provide and cleanup services.

        Args:
            service (type[T]): The service type.
            factory (Callable[[], T]): The factory function.

        Returns:
            T: Returns an object.
        """
        ...