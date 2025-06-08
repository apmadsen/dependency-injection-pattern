from typing import TypeVar, Any, cast, overload
from typingutils import issubclass_typing, get_optional_type

from di.core.exceptions.factory_provide_exception import FactoryProvideException
from di.core.scope import Scope
from di.core.factory import Factory as PublicFactory
from di.core.factories.factory import Factory
from di.core.service_request import ServiceRequest
from di.core.protocols.container import Container

T = TypeVar('T')

class Provider:
    """
    The Provider is connected to the Container and provides the services defined.
    """
    __slots__ = ["__container", "__weakref__"]

    def __init__(self, container: Container):
        self.__container = container


    def provides(self, service: str | type[Any]) -> bool:
        """
        Indicates whether or not the specified service can be provided.

        Args:
            service (str | type[Any]) The service interface or name.

        Returns:
            bool: Returns True if specified service can be provided.
        """
        return self.__container._defines(service) # pyright: ignore[reportPrivateUsage]

    @overload
    def provide(self, service: type[T]) -> T:
        """
        Provides the specified service.

        Args:
            service (type[Any]) The service interface.

        """
        ...
    @overload
    def provide(self, service: type[T], scope: Scope) -> T:
        """
        Provides the specified service.

        Args:
            service (type[Any]) The service interface.
            scope (Scope) A custom scope.
        """
        ...
    def provide(self, service: type[T], scope: Scope | None = None) -> T:
        return self._provide(service, scope)


    def _provide(self, service: type[T] | ServiceRequest[T], scope: Scope | None = None) -> T:
        scope = scope or self.__container.default_scope
        svc_type = service.type if isinstance(service, ServiceRequest) else service
        svc_type, is_optional = get_optional_type(svc_type)

        if svc_type and issubclass_typing(svc_type, PublicFactory):
            def factory() -> T:
                return self._provide(cast(type[T], getattr(svc_type, "__args__")[0]))
            return factory # pyright: ignore[reportReturnType]
        else:
            result = self.__container._get(cast(type[T], service)) # pyright: ignore[reportPrivateUsage]

            if result == None:
                # optional requirements may return None
                if is_optional:
                    return None # pyright: ignore[reportReturnType]
                else:
                    raise FactoryProvideException(svc_type) # pragma: no cover

            elif isinstance(result, Factory):
                result = cast(T | None, result.provide(scope))
                if result or is_optional:
                    return cast(T, result)
                else:
                    raise FactoryProvideException(svc_type)
            else:
                return cast(T, result)