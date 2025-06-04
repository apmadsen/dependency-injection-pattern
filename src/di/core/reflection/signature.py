from typing import Any
from typingutils import get_type_name

from di.core.reflection.parameter_mapper import ParameterMapper

class Signature:
    __slots__ = ["__parameters", "__return_type"]

    def __init__(
        self,
        parameters: ParameterMapper,
        return_type: type[Any]
    ):
        self.__parameters = parameters
        self.__return_type = return_type

    @property
    def parameters(self) -> ParameterMapper:
        """The signature parameters
        """
        return self.__parameters

    @property
    def return_type(self) -> type[Any]:
        """The signature return type
        """
        return self.__return_type



    def __repr__(self) -> str:
        str_parameters = ", ".join([ str(p) for p in self.__parameters ]) if self.__parameters else ""
        str_return = f" -> {get_type_name(self.__return_type)}" if self.__return_type else ""
        return f"({str_parameters}){str_return}"

    def __eq__(self, o: object) -> bool: # pragma: no cover
        if self is o:
            return True
        elif isinstance(o, Signature):
            return (
                self.parameters == o.parameters
                and self.return_type == o.return_type
            )
        return False

