# pyright: basic
from typing import Any


def fn_test3(x: str | int) -> bool:
    return True

def fn_test4(**kwargs: Any) -> bool:
    return True

def fn_test5(**kwargs: Any):
    pass

def fn_test6(x):
    pass

def fn_test7() -> None:
    """Test
    """
    ...

