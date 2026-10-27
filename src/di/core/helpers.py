from collections.abc import MutableMapping
from types import TracebackType
from typing import Protocol, TypeVar, cast, runtime_checkable

from typingutils import AnyType, get_type_name, issubclass_typing

from di.core.factory import Factory

T = TypeVar('T', covariant=True)  # noqa: PLC0105

@runtime_checkable
class ContextManager(Protocol[T]): # pragma: no cover
    def __enter__(self) -> T: ...
    def __exit__(self, /, __exc_type: type[BaseException] | None, __exc_value: BaseException | None, __traceback: TracebackType | None) -> None: ...


def get_service_name(service: AnyType | str) -> str: # pragma: no cover
    if isinstance(service, str):
        return service
    elif hasattr(service, "__name__"):
        return cast(str, service.__name__) # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
    else:
        return get_type_name(service)

def clean_service_name(service: str) -> str:
    return service.lower()

def get_provided_service_from_annotation(annotation: AnyType) -> tuple[AnyType, bool]:
    if issubclass_typing(annotation, Factory):
        return cast(tuple[type], annotation.__args__)[0], True # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
    else:
        return annotation, False


__CONTEXT_SERVICES__: MutableMapping[type, bool] = {}

def is_context(cls: type) -> bool:
    if cls not in __CONTEXT_SERVICES__:
        if issubclass(cls, ContextManager):
            result = True
        else:
            result = False

        __CONTEXT_SERVICES__[cls] = result
    return __CONTEXT_SERVICES__[cls]
