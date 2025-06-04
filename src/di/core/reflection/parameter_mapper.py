from typing import Iterator, Mapping, Iterable, Sequence

from di.core.reflection.parameter import Parameter

class ParameterMapper(Iterable[Parameter]):
    __slots__ = ["__parameters", "__index"]

    def __init__(self, parameters: Sequence[Parameter]):
        self.__parameters = list(parameters)
        self.__index: Mapping[str, int] | None = None

    def __get_index(self) -> Mapping[str, int]:
        if not self.__index:
            self.__index = {
                parameter.name: self.__parameters.index(parameter)
                for parameter in self.__parameters
            }
        return self.__index # pragma: no cover

    def __getitem__(self, index: int | str) -> Parameter: # pragma: no cover
        if isinstance(index, int):
            return self.__parameters[index]
        else:
            p_index = self.__get_index()

            if index in p_index:
                return self.__parameters[p_index[index]]
            else:
                raise KeyError(index)

    def __iter__(self) -> Iterator[Parameter]:
        return iter(self.__parameters)

    def __len__(self) -> int: # pragma: no cover
        return len(self.__parameters)

    def __delitem__(self, index: int | str) -> None: # pragma: no cover
        if isinstance(index, int):
            del self.__parameters[index]
        else:
            p_index = self.__get_index()

            if index in p_index:
                del self.__parameters[p_index[index]]
            else:
                raise KeyError(index)

    def __contains__(self, name: str) -> bool: # pragma: no cover
        p_index = self.__get_index()
        return name in p_index

    def __eq__(self, o: object) -> bool: # pragma: no cover
        if isinstance(o, ParameterMapper):
            return self.__parameters == o.__parameters
        return False
