from __future__ import annotations
from typing import TypeVar, Callable, Any, cast, overload, TYPE_CHECKING
from typingutils import is_type, isinstance_typing, get_optional_type, AnyFunction
from types import FunctionType
from weakref import ref
from runtime.reflection.lite import reflect_function

from di.core.log import LOG
from di.core.scope import Scope
from di.core.service_request import ServiceRequest
from di.core.factories.singleton_factory import SingletonFactory
from di.core.factories.transient_factory import TransientFactory
from di.core.factories.scoped_factory import ScopedFactory
from di.core.default_scope import DefaultScope
from di.core.named_service import NamedService
from di.core.helpers import clean_service_name, get_service_name, is_context
from di.core.exceptions.provide_exception import ProvideException
from di.core.exceptions.add_exception import AddException
from di.core.exceptions.seal_exception import SealException
from di.core.exceptions.container_sealed_error import ContainerSealedError

if TYPE_CHECKING:
    from di.core.provider import Provider
    from di.core.factories.factory import Factory

T = TypeVar('T')

class Container:
    """
    The Container handles the definition of services and implementations.

    Example:
        container = Container()
        container.add_transient(Service)
        provider = container.provider() # container is sealed, and no more services can be added beyound this point
        provider.provide(Service) # => Service
    """
    __slots__ = ["__factories", "__named_factories", "__list_factories", "__default_scope", "__provider", "__weakref__"]

    def __init__(self):
        self.__factories: dict[type[Any], Factory[Any]] = {}
        self.__named_factories: dict[str, tuple[type[Any], Factory[Any]]] = {}
        self.__provider: ref[Provider] | None = None
        self.__default_scope = DefaultScope()

    @property
    def default_scope(self) -> Scope:
        return self.__default_scope

    @overload
    def add_singleton(self, service: type, /) -> None:
        """Adds a singleton service to provider, which will result in same instance every time it's provided.

        Args:
            service (type): The service interface
        """
        ...
    @overload
    def add_singleton(self, implementation: AnyFunction, /) -> None:
        """Adds a singleton service to provider, which will result in same instance every time it's provided.

        Args:
            implementation (AnyFunction) The service implementation
        """
        ...
    @overload
    def add_singleton(self, service: type[T], implementation: type[T] | Callable[..., T] | T, /) -> None:
        """Adds a singleton service to provider, which will result in same instance every time it's provided.
        Implementation may be a type derived from service, a callable or an object derived from, service.

        Args:
            service (type[T]) The service interface
            implementation (type[T] | Callable[..., T] | T) The service implementation
        """
        ...
    @overload
    def add_singleton(self, service: str, implementation: type[T] | Callable[..., T] | T, /) -> None:
        """Adds a singleton service to provider, which will result in same instance every time it's provided.
        Implementation may be a type derived from service, a callable or an object derived from, service.

        Args:
            service (str) The service name
            implementation (type[T] | Callable[..., T] | T) The service implementation
        """
        ...
    def add_singleton(self, *args: Any) -> None:
        self.__add_factory_pre(SingletonFactory, *args)

    @overload
    def add_transient(self, service: type, /) -> None:
        """Adds a transient service to provider, which will result in a new instance every time it's provided.

        Args:
            service (type) The service interface

        """
        ...
    @overload
    def add_transient(self, implementation: AnyFunction, /) -> None:
        """Adds a transient service to provider, which will result in a new instance every time it's provided.

        Args:
            implementation (AnyFunction) The service implementation
        """
        ...
    @overload
    def add_transient(self, service: type[T], implementation: type[T] | Callable[..., T], /) -> None:
        """Adds a transient service to provider, which will result in a new instance every time it's provided.
        Implementation may be a type derived from service or a callable.

        Args:
            service (str | type[T]) The service interface
            implementation (type[T] | Callable[..., T]) The service implementation
        """
        ...
    @overload
    def add_transient(self, service: str, implementation: type[T] | Callable[..., T] | T, /) -> None:
        """Adds a transient service to provider, which will result in a new instance every time it's provided.
        Implementation may be a type derived from service or a callable.

        Args:
            service (str) The service name
            implementation (type[T] | Callable[..., T] | T) The service implementation
        """
        ...
    def add_transient(self, *args: Any) -> None:
        self.__add_factory_pre(TransientFactory, *args)

    @overload
    def add_scoped(self, service: type, /) -> None:
        """Adds a scoped service to provider, which will result in one instance every time it's provided in the same scope.
        The default scope is thread-based, and bound to the lifetime of the thread in which a given service is provided.

        Note: Scoped services should implement the ContextManager pattern.

        Args:
            service (type) The service interface
        """
        ...
    @overload
    def add_scoped(self, implementation: AnyFunction, /) -> None:
        """Adds a scoped service to provider, which will result in one instance every time it's provided in the same scope.
        The default scope is thread-based, and bound to the lifetime of the thread in which a given service is provided.

        Note: Scoped services should implement the ContextManager pattern.

        Args:
            implementation (AnyFunction) The service implementation
        """
        ...
    @overload
    def add_scoped(self, service: type[T], implementation: type[T] | Callable[..., T], /) -> None:
        """Adds a scoped service to provider, which will result in one instance every time it's provided in the same scope.
        The default scope is thread-based, and bound to the lifetime of the thread in which a given service is provided.
        Implementation may be a type derived from service or a callable.

        Note: Scoped services should implement the ContextManager pattern.

        Args:
            service (str | type[T]) The service interface
            implementation (type[T] | Callable[..., T]) The service implementation
        """
        ...
    @overload
    def add_scoped(self, service: str, implementation: type[T] | Callable[..., T] | T, /) -> None:
        """Adds a scoped service to provider, which will result in one instance every time it's provided in the same scope.
        The default scope is thread-based, and bound to the lifetime of the thread in which a given service is provided.
        Implementation may be a type derived from service or a callable.

        Note: Scoped services should implement the ContextManager pattern.

        Args:
            service (str) The service name
            implementation (type[T] | Callable[..., T] | T) The service implementation
        """
        ...
    def add_scoped(self, *args: Any) -> None:
        service, svc_type = self.__add_factory_pre(ScopedFactory, *args)

        if not is_context(svc_type):
            LOG.warning(f"Scoped service '{service}' does not implement the context-manager pattern")

    def provider(self) -> Provider:
        """Seals Container and returns a Provider

        Returns:
            Provider -- The Provider instance
        """
        from di.core.provider import Provider
        if self.__provider is None:
            provider = Provider(self)
            self.__provider = ref(provider)
            self.__add_factory(SingletonFactory, Provider, self.provider)

            factories = { **self.__factories, **{ service: factory for service, factory in self.__named_factories.values() } }
            for service, factory in factories.items():
                for dep in factory.dependencies.values():
                    if not dep.service in factories:
                        if not dep.is_optional and not dep.has_default:
                            raise SealException(f"Service '{get_service_name(service)}' depends on service '{get_service_name(dep.service)}' which is not defined in container.")
                        else:
                            LOG.warning(f"Service '{get_service_name(service)}' depends on service '{get_service_name(dep.service)}' which is not defined in container.")
                    elif not dep.is_factory and isinstance(factory, SingletonFactory):
                        if isinstance(factories[dep.service], ScopedFactory):
                            raise SealException(f"Singleton service '{get_service_name(service)}' depends on scoped service '{get_service_name(dep.service)}' which is not permitted.")
                        elif isinstance(factories[dep.service], TransientFactory):
                            raise SealException(f"Singleton service '{get_service_name(service)}' depends on transient service {get_service_name(dep.service)}' which is not permitted.")

            return provider
        elif provider :=self.__provider():
            return provider
        else:
            provider = Provider(self)
            self.__provider = ref(provider)
            return provider

    def __add_factory_pre(self, factory_type: type[Factory[T]], *args: Any) -> tuple[str, type[Any]]:
        if self.__provider != None:
            raise ContainerSealedError

        if len(args) == 2:
            if not is_type(args[0]) and not isinstance_typing(args[0], str):
                raise AddException("Service must be a string or a type")

            service = cast(str | type, args[0])
            implementation = cast(type | Callable[..., Any] | Any | None, args[1])
        elif is_type(args[0]) or isinstance(args[0], str):
            service = cast(str | type, args[0])
            implementation = None
        else:
            if not isinstance(args[0], FunctionType):
                raise AddException("Implementation must be a function or a type when no service is specified.")
            implementation = cast(Callable[..., Any], args[0])
            signature = reflect_function(implementation)
            service, _ = get_optional_type(cast(type, signature.return_type))

        return get_service_name(service), self.__add_factory(factory_type, cast(str | type[Any], service), implementation)


    def __add_factory(self, factory_type: type[Factory[T]], service: str | type[T], implementation: type[T] | Callable[..., T] | T | None = None) -> type[T]:
        if isinstance(service, str):
            service = clean_service_name(service)
            if service in self.__named_factories:
                raise AddException(f"Service '{get_service_name(service)}' is already defined in provider")
            elif implementation is None:
                raise AddException(f"Cannot add named service '{get_service_name(service)}' without providing an implementation.")

            if is_type(implementation):
                svc_type = cast(type[T], implementation)
            elif callable(implementation):
                signature = reflect_function(implementation)
                svc_type = cast(type[T], signature.return_type)
            else:
                svc_type = cast(type[T], type(implementation))

            factory = factory_type(self, NamedService, implementation) # pyright: ignore[reportArgumentType]
            self.__named_factories[service] = (svc_type, factory)
            return svc_type

        else:
            if service in self.__factories:
                raise AddException(f"Service '{get_service_name(service)}' is already defined in provider.")
            else:
                factory = factory_type(self, service, implementation)
                self.__factories[cast(type, service)] = factory

            return service

    def _defines(self, service: str | type) -> bool:
        """Indicates whether or not the specified service interface is defined.

        Args:
            service (str | type[T]) The service interface or name

        Returns:
            True or false (bool)
        """
        from di.core.provider import Provider

        if isinstance(service, str):
            return clean_service_name(service) in self.__named_factories
        elif isinstance(service, type) and issubclass(service, Provider): # pyright: ignore[reportUnnecessaryIsInstance]
            return True
        elif is_type(service):
            return service in self.__factories

        return False

    def _get_factory(self, service: type[T] | ServiceRequest[T]) -> tuple[Factory[T] | None, T | None, bool]:
        svc_name: str | None = None
        svc_type: type | None = None
        is_optional = False
        default: T | None = None
        factory: Factory[T] | None = None

        if isinstance(service, ServiceRequest):
            svc_name = service.name
            svc_type = service.type
            default = service.default
            svc_type, is_optional = cast(tuple[type[Any], bool], get_optional_type(svc_type))
        else:
            service, is_optional = get_optional_type(service)


        for svc in [svc_type, svc_name, service]: # pyright: ignore[reportUnknownVariableType]
            if svc is None:
                pass
            elif isinstance(svc, str):
                svc = clean_service_name(svc)
                if svc in self.__named_factories:
                    svc_def = self.__named_factories[svc]
                    if svc_def[0] is svc_type:
                        factory = svc_def[1]
                        break
            elif is_type(svc):
                if svc in self.__factories:
                    factory = self.__factories[cast(type, svc)]
                    break

        return factory, default, is_optional

    def _get(self, service: type[T] | ServiceRequest[T]) -> Factory[T] | T | None:
        """Returns the factory for the specified service interface

        Arguments:
            service {type[T] | ServiceRequest[T]} -- The service interface

        Raises:
            ProvideException: If service cannot be resolved

        Returns:
            Factory[T] | T | None -- The service factory
        """
        factory, default, is_optional = self._get_factory(service)

        if factory:
            return factory
        elif default != None:
            return default
        elif not is_optional:
            if isinstance(service, ServiceRequest):
                raise ProvideException(service.type)
            else:
                raise ProvideException(service)