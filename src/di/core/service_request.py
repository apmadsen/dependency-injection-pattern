from typing import Generic, TypeVar

T = TypeVar("T")

class ServiceRequest(Generic[T]):
    """
    The ServiceRequest[T] class is used internally to request a service by name.
    """
    __slots__ = ["__default", "__name", "__type"]

    def __init__(self, name: str, type: type[T], default: T):
        self.__name = name.lower()
        self.__type = type
        self.__default = default

    @property
    def name(self) -> str:
        return self.__name

    @property
    def type(self) -> type[T]:
        return self.__type

    @property
    def default(self) -> T:
        return self.__default