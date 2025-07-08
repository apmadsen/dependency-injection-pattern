from typing import TypeVar, Callable, Generic, Any, cast
from typingutils import get_optional_type, issubclass_typing, isinstance_typing
from runtime.reflection.lite import Undefined, ParameterKind, reflect_function, get_constructor

from di.core.scope import Scope
from di.core.named_service import NamedService
from di.core.service_request import ServiceRequest

from di.core.exceptions.implementation_exception import ImplementationException
from di.core.exceptions.factory_provide_exception import FactoryProvideException
from di.core.exceptions.provide_exception import ProvideException
from di.core.protocols.container import Container
from di.core.factories.dependency import Dependency

T = TypeVar('T')

class Factory(Generic[T]):
    __slots__ = ["__container", "__service", "__implementation", "__ctor", "__dependencies"]

    def __init__(self, container: Container, service: type[T], implementation: type[T] | Callable[..., T] | T | None = None):
        self.__container = container
        self.__service = service
        self.__implementation = service if implementation is None else implementation
        self.__dependencies: dict[str, Dependency] = {}

        if not implementation:
            if hasattr(service, "__origin__"):
                sig = reflect_function(getattr(service, "__call__"), service)
            else:
                sig = get_constructor(service)
        elif isinstance(implementation, type):
            sig = get_constructor(cast(type, implementation))
            if not service is NamedService and not issubclass_typing(implementation, service):
                raise ImplementationException(service, implementation, "Implementation class is not derived from service")
            elif implementation is service:
                raise ImplementationException(service, implementation, "Implementation equals service")
        elif isinstance_typing(implementation, service, recursive=True):
            sig = None
        elif callable(implementation):
            sig = reflect_function(implementation)
            if sig.return_type:
                implementation_type, _ = get_optional_type(sig.return_type)
            else:
                implementation_type = None

            if service is NamedService:
                pass
            elif not implementation_type:
                raise ImplementationException(service, implementation, "Implementation is missing return annotation")
            elif not issubclass_typing(implementation_type, service):
                raise ImplementationException(service, implementation, "Implementation does not resolve into a class derived from service")
        elif service is NamedService:
            sig = None
        else:
            raise ImplementationException(service, implementation, "Implementation does not resolve into a class derived from service")

        if sig != None:
            parameters = [ p for p in sig.parameters if p.kind == ParameterKind.POSITIONAL_OR_KEYWORD ]
            missing_annotations = [ p.name for p in parameters if not p.parameter_type ]
            self.__dependencies = { p.name: Dependency(p.name, p.parameter_type, p.default) for p in parameters }

            if len(missing_annotations) > 0:
                parameters_missing_ann = ", ".join([f"'{p}'" for p in missing_annotations])
                raise ImplementationException(service, implementation, f"Parameter(s) {parameters_missing_ann} missing annotation")

            def ctor(scope: Scope | None = None) -> T:
                provider = container.provider()
                try:
                    args = [
                        provider._provide( # pyright: ignore[reportPrivateUsage]
                            ServiceRequest(
                                p.name,
                                cast(type[T], p.parameter_type),
                                None if p.default is Undefined else p.default
                            ),
                            scope
                        ) for p in parameters
                    ]
                    return cast(Callable[[Any], T], self.__implementation)(*args)
                except ProvideException as ex:
                    failed_args = {
                        p.name: cast(type, p.parameter_type)
                        for p in parameters
                        if not provider.provides(cast(type, p.parameter_type))
                    }
                    raise FactoryProvideException(service, failed_args) from ex

            self.__ctor = ctor

    @property
    def container(self) -> Container:
        return self.__container # pragma: no cover

    @property
    def service(self) -> type[T]:
        return self .__service

    @property
    def dependencies(self) -> dict[str, Dependency]:
        return self.__dependencies

    def provide(self, scope: Scope | None = None) -> T:
        return self.__ctor(scope)


