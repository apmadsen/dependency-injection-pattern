from typing import MutableMapping, Protocol, TypeVar, cast, runtime_checkable
from di.core.factory import Factory
from types import TracebackType
from typingutils import AnyType, issubclass_typing, get_type_name

from di.core.factory import Factory


T = TypeVar('T', covariant=True)

@runtime_checkable
class ContextManager(Protocol[T]): # pragma: no cover
    def __enter__(self) -> T: ...
    def __exit__(self, __exc_type: type[BaseException] | None, __exc_value: BaseException | None, __traceback: TracebackType | None) -> None: ...


def get_service_name(service: AnyType | str) -> str: # pragma: no cover
    if isinstance(service, str):
        return service
    elif hasattr(service, "__name__"):
        return getattr(service, "__name__")
    else:
        return get_type_name(service)

def clean_service_name(service: str) -> str:
    return service.lower()

def get_provided_service_from_annotation(annotation: AnyType) -> tuple[AnyType, bool]:
    if issubclass_typing(annotation, Factory):
        return cast(tuple[type], getattr(annotation, "__args__"))[0], True
    else:
        return annotation, False


__CONTEXT_SERVICES__: MutableMapping[type, bool] = {}

def is_context(cls: type) -> bool:
    if not cls in __CONTEXT_SERVICES__:
        # reflection = reflect_class(cls)

        # if "__enter__" in reflection.functions and "__exit__" in reflection.functions:
        #     result = reflection.functions["__enter__"].return_type is cls
        # else:
        #     result = False
        if issubclass(cls, ContextManager):
            result = True
        else:
            result = False

        __CONTEXT_SERVICES__[cls] = result
    return __CONTEXT_SERVICES__[cls]
