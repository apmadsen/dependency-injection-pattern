from typing import Protocol, TypeVar, Generic, runtime_checkable

T = TypeVar("T", covariant=True)

@runtime_checkable
class Factory(Generic[T], Protocol): # pragma: no cover
    ...