from typing import Generic, Protocol, TypeVar, runtime_checkable

T = TypeVar("T", covariant=True)  # noqa: PLC0105

@runtime_checkable
class Factory(Protocol, Generic[T]): # pragma: no cover
    ...