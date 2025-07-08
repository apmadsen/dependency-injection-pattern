from typing import Any, cast
from typingutils import get_optional_type
from runtime.reflection.lite import Undefined

from di.core.helpers import get_provided_service_from_annotation

class Dependency:
    __slots__ = [ "__name", "__service", "__factory", "__optional", "__default" ]

    def __init__(self, name: str, service: type[Any], default: Any ):
        self.__name = name
        service, self.__optional = cast(tuple[type[Any], bool], get_optional_type(service))
        self.__service, self.__factory = cast(tuple[type[Any], bool], get_provided_service_from_annotation(service))
        self.__default = default

    @property
    def name(self) -> str:
        return self.__name # pragma: no cover

    @property
    def service(self) -> type[Any]:
        return self.__service

    @property
    def is_optional(self) -> bool:
        return self.__optional

    @property
    def is_factory(self) -> bool:
        return self.__factory

    @property
    def has_default(self) -> bool:
        return self.__default is not Undefined

    @property
    def default(self) -> Any:
        return self.__default # pragma: no cover