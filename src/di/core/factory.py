from typing import Generic, TypeVar

from di.core.exceptions.internal_exception import InternalException
from di.core.scope import Scope

T = TypeVar("T")

class Factory(Generic[T]):
    """
    The Factory[T] class is used to get the Provider to provide a factory instead of a service implementation ie. a lazy implementation.

    Example:
        class SomeClass:
            def __init__(self, service: Factory[Service]):
                svc = service() # => Service
    """

    def __new__(cls):
        raise InternalException("The Factory class is not intended for instantation") # pragma: no cover

    def provide(self, scope: Scope | None = None) -> T: # pragma: no cover
        raise NotImplementedError

    def __call__(self, scope: Scope | None = None) -> T: # pragma: no cover
        raise NotImplementedError