# pyright: basic
from pytest import raises as assert_raises

from di.core.reflection import ParameterKind, Undefined, get_constructor, reflect_function


from tests.reflection.explore import explore
from tests.reflection.reflection_classes import Class4, Test1, TestClass

def test_get_constructor():
    signature1 = get_constructor(dict)
    e1 = explore(signature1)
    assert e1 ==  (
        Undefined,
        [
            ("args", ParameterKind.ARGS, Undefined, Undefined),
            ("kwargs", ParameterKind.KWARGS, Undefined, Undefined),
        ]
    )

    signature2 = get_constructor(Class4)
    e2 = explore(signature2)
    assert e2 ==  (
        Undefined,
        [
            ("args", ParameterKind.ARGS, Undefined, Undefined),
            ("kwargs", ParameterKind.KWARGS, Undefined, Undefined),
        ]
    )

    signature21 = reflect_function(Class4().__init__)
    assert signature2 == signature21

    signature3 = get_constructor(Test1)
    e3 = explore(signature3)
    assert e3 ==  (
        Undefined,
        [
            ("args", ParameterKind.ARGS, Undefined, Undefined),
            ("kwargs", ParameterKind.KWARGS, Undefined, Undefined),
        ]
    )

    signature31 = reflect_function(Test1().__init__)
    assert signature3 == signature31

    signature4 = get_constructor(TestClass)
    e4 = explore(signature4)
    assert e4 ==  (
        Undefined, []
    )

    signature41 = reflect_function(TestClass().__init__)
    assert signature4 == signature41
