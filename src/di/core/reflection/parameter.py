from typing import Any, cast
from typingutils import get_type_name
from inspect import Parameter as InspectParameter

from di.core.reflection.undefined import Undefined
from di.core.reflection.parameter_kind import ParameterKind

class Parameter:
    __slots__ = ["__name", "__kind", "__doc", "__type", "__default"]

    def __init__(
        self,
        name: str,
        kind: ParameterKind,
        parameter_type: type[Any],
        default: Any
    ):
        self.__name = name
        self.__kind = kind
        self.__type = parameter_type
        self.__default = default

    @property
    def name(self) -> str:
        """The parameter name
        """
        return self.__name

    @property
    def kind(self) -> ParameterKind:
        """The parameter kind
        """
        return self.__kind

    @property
    def parameter_type(self) -> type[Any]:
        """The parameter type
        """
        return self.__type

    @property
    def default(self) -> Any:
        """The parameter default
        """
        return self.__default

    def __repr__(self) -> str:
        str_type = f": {get_type_name(cast(type, self.__type))}" if self.__type and self.__type != Undefined else ""
        str_default = f"={self.__default}" if self.__default else ""
        return f"{self.__name}{str_type}{str_default}"

    def __eq__(self, o: object) -> bool: # pragma: no cover
        if isinstance(o, Parameter):
            return (
                self.name == o.name
                and self.kind == o.kind
                and self.parameter_type == o.parameter_type
            )
        elif isinstance(o, InspectParameter):
            return (
                self.name == o.name
                and cast(int, self.kind) == o.kind
                and self.parameter_type == o.annotation
            )

        return False