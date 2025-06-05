# pyright: basic
from typing import Callable, ClassVar, List, Dict, Set, Tuple, TypeVar, Any, overload, cast
from types import FunctionType, MethodType
from os import path, makedirs
from shutil import rmtree
from threading import Thread
from unittest import TestCase, main

T = TypeVar("T")

from di.core.reflection import reflect_function, get_constructor, Undefined, ParameterKind

from tests.reflection.explore import explore
from tests.reflection.reflection_classes import Class1, Class4, Class6, Class5
from tests.reflection.reflection_functions import fn_test3, fn_test4, fn_test5, fn_test6, fn_test7

def test_reflect_function():

    test = Class6()

    signature1 = reflect_function(Class6.Class7()._test2)
    e1 = explore(signature1)
    assert e1 == (
        str,
        [
            ("y", ParameterKind.POSITIONAL_OR_KEYWORD, float, Undefined)
        ]
    )

    signature2 = reflect_function(Class6.Class7._test2)
    e2 = explore(signature2)
    assert e2 == (
        str,
        [
            ("y", ParameterKind.POSITIONAL_OR_KEYWORD, float, Undefined)
        ]
    )


    signature3 = reflect_function(Class6._test1)
    e3 = explore(signature3)
    assert e3 == (
        bool,
        [
            ("x", ParameterKind.POSITIONAL_OR_KEYWORD, str | int, Undefined)
        ]
    )

    signature4 = reflect_function(fn_test3)
    e4 = explore(signature4)
    assert e4 == (
        bool,
        [
            ("x", ParameterKind.POSITIONAL_OR_KEYWORD, str | int, Undefined)
        ]
    )

    signature5 = reflect_function(test._test1)
    e5 = explore(signature5)
    assert e5 == (
        bool,
        [
            ("x", ParameterKind.POSITIONAL_OR_KEYWORD, str | int, Undefined)
        ]
    )

    signature6 = reflect_function(test._test2)
    e6 = explore(signature6)
    assert e6 == (
        None,
        [
            ("x", ParameterKind.POSITIONAL_OR_KEYWORD, List[str], [ "test" ])
        ]
    )

    signature7 = reflect_function(fn_test4)
    e7 = explore(signature7)
    assert e7 == (
        bool,
        [
            ("kwargs", ParameterKind.KWARGS, Any, Undefined)
        ]
    )

    signature8 = reflect_function(object.__init__)
    e8 = explore(signature8)


    signature9 = reflect_function(fn_test5)
    e9 = explore(signature9)
    assert e9 == (
        Undefined,
        [
            ("kwargs", ParameterKind.KWARGS, Any, Undefined)
        ]
    )


    signature10 = reflect_function(fn_test6)
    e10 = explore(signature10)
    assert e10 == (
        Undefined,
        [
            ("x", ParameterKind.POSITIONAL_OR_KEYWORD, Undefined, Undefined)
        ]
    )



def test_reflect_function_in_frame():
    class Test1:
        @overload
        def test1(self, x: str) -> bool:
            ...
        @overload
        def test1(self, x: int) -> bool:
            ...
        def test1(self, x: str | int) -> bool:
            return True

        def test2(self, x: List[str] = [ "test" ]) -> None:
            ...

        class Test2:
            def test2(self, y: float) -> str:
                return "Hey"

    def test3(x: str | int) -> bool:
        return True

    def test4(**kwargs: Any) -> bool:
        return True

    test = Test1()

    signature1 = reflect_function(Test1.Test2().test2)
    e1 = explore(signature1)
    assert e1 == (
        str,
        [
            ("y", ParameterKind.POSITIONAL_OR_KEYWORD, float, Undefined)
        ]
    )

    signature2 = reflect_function(Test1.Test2.test2)
    e2 = explore(signature2)
    assert e2 == (
        str,
        [
            ("y", ParameterKind.POSITIONAL_OR_KEYWORD, float, Undefined)
        ]
    )

    signature3 = reflect_function(Test1.test1)
    e3 = explore(signature3)
    assert e3 == (
        bool,
        [
            # ("self", ParameterKind.POSITIONAL_OR_KEYWORD, Undefined, Undefined),
            ("x", ParameterKind.POSITIONAL_OR_KEYWORD, str | int, Undefined)
        ]
    )

    signature4 = reflect_function(test3)
    e4 = explore(signature4)
    assert e4 == (
        bool,
        [
            ("x", ParameterKind.POSITIONAL_OR_KEYWORD, str | int, Undefined)
        ]
    )

    signature5 = reflect_function(test.test1)
    e5 = explore(signature5)
    assert e5 == (
        bool,
        [
            ("x", ParameterKind.POSITIONAL_OR_KEYWORD, str | int, Undefined)
        ]
    )

    signature6 = reflect_function(test.test2)
    e6 = explore(signature6)
    assert e6 == (
        None,
        [
            ("x", ParameterKind.POSITIONAL_OR_KEYWORD, List[str], [ "test" ])
        ]
    )

    signature7 = reflect_function(test4)
    e7 = explore(signature7)
    assert e7 == (
        bool,
        [
            ("kwargs", ParameterKind.KWARGS, Any, Undefined)
        ]
    )


def test_reflect_function_in_frame_async():
    # when reflection is done outside the stack which created the function,
    # the scope.parent cannot be resolved, however reflection should
    # be able to proceed anyway

    def test(p1: List[str], p2: int, p3: bool):
        for item in p1:
            pass

    async_result: dict[str, Any] = { "result": None }
    def async_reflector(fn: Callable[..., Any]):
        try:
            signature = reflect_function(fn)
            async_result["result"] = signature
        except Exception as ex:
            from traceback import print_exc
            print_exc()
            async_result["result"] = ex

    t = Thread(target=async_reflector, args=[test])
    t.start()
    t.join()

    result = async_result["result"]

    assert not isinstance(result, Exception)
    assert explore(result) == (
        Undefined,
        [
            ("p1", ParameterKind.POSITIONAL_OR_KEYWORD, List[str], Undefined),
            ("p2", ParameterKind.POSITIONAL_OR_KEYWORD, int, Undefined),
            ("p3", ParameterKind.POSITIONAL_OR_KEYWORD, bool, Undefined)
        ]
    )



def test_default_values():
    tmp_list = [ "a", "b", "c" ]
    tmp_dict = { "a": 1, "b": 2, "c": 3 }

    def default() -> str:
        return "default_str"

    def test1_1( x: List[str] = [ "test" ]) -> None:
        ...
    signature1_1 = reflect_function(test1_1)
    assert signature1_1.parameters["x"].default == [ "test" ]

    def test2_1( x: dict[str, int] = { "test": 2}) -> None:
        ...
    signature2_1 = reflect_function(test2_1)
    assert signature2_1.parameters["x"].default == { "test": 2}

    def test3( x: set[str] = { "test" }) -> None:
        ...
    signature3 = reflect_function(test3)
    assert signature3.parameters["x"].default == { "test" }

    def test4( x: Tuple[str, int] = ( "test", 2)) -> None:
        ...
    signature4 = reflect_function(test4)
    assert signature4.parameters["x"].default == ( "test", 2)



    def test1_2( x: List[str] = [ o for o in tmp_list ]) -> None:
        ...
    signature1_2 = reflect_function(test1_2)
    assert signature1_2.parameters["x"].default == [ o for o in tmp_list ]

    def test1_3( x: List[str] = [ *tmp_list, "test" ]) -> None:
        ...
    signature1_3 = reflect_function(test1_3)
    assert signature1_3.parameters["x"].default == [ *tmp_list, "test" ]


    def test2_2( x: dict[str, int] = { k: v for k,v in tmp_dict.items() }) -> None:
        ...
    signature2_2 = reflect_function(test2_2)
    assert signature2_2.parameters["x"].default == { k: v for k,v in tmp_dict.items() }

    def test2_3( x: dict[str, int] = { **tmp_dict, "test": 2}) -> None:
        ...
    signature2_3 = reflect_function(test2_3)
    assert signature2_3.parameters["x"].default == { **tmp_dict, "test": 2}


    def test5( x: str = default()) -> None:
        ...
    signature5 = reflect_function(test5)
    assert signature5.parameters["x"].default == default()



def test_method_vs_function():
    test1 = Class6()

    f1 = Class6._test1
    f2 = test1._test1
    r1 = reflect_function(f1)
    r2 = reflect_function(f2)


    x = 0

def test_shadowing_class():
    class Class1: # Class1 shadows Class1 already in global scope
        ...
    class Class2:
        def __init__(self, class1: Class1):
            ...


    signature = get_constructor(Class2)
    e = explore(signature)
    assert e == (
        Undefined,
        [
            ("class1", ParameterKind.POSITIONAL_OR_KEYWORD, Class1, Undefined)
        ]
    )