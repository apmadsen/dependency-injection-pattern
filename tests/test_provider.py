# pyright: basic
from typing import cast, Sequence, MutableSequence, Generic, TypeVar, Any, ClassVar
from pytest import raises as assert_raises

from di import Container, Factory, Provider
from di.exceptions import ImplementationException, AddException, SealException, FactoryProvideException, ProvideException

from tests.classes import *


def test_dependencies():
    container = Container()
    container.add_transient(Service)
    container.add_singleton(Options1, Options1("test", 35))
    container.add_transient(DependentService)
    provider = container.provider()

    with assert_raises(ProvideException):
        provider.provide(DependentServiceFail2)

    assert isinstance(cast(object, provider.provide(DependentService)), DependentService)

def test_seal_error():
    container = Container()
    container.add_transient(Service)
    container.add_singleton(Options1, Options1("test", 35))
    container.add_transient(DependentService)
    container.add_transient(DependentServiceFail2)

    with assert_raises(SealException):
        provider = container.provider()

def test_collections():
    container = Container()
    container.add_singleton(Sequence[IService], [ Service(), Service2() ])
    provider = container.provider()
    provider.provide(Sequence[IService])
    assert provider.provides(Sequence[IService])
    assert len(provider.provide(Sequence[IService])) == 2

def test_optional():

    def create_optional() -> DependentService3 | None:
        pass

    class Dependent1:
        def __init__(self, dep: DependentService3):
            pass
    class Dependent2:
        def __init__(self, dep: DependentService3 | None):
            pass

    container = Container()

    container.add_singleton(DependentService1)
    container.add_singleton(DependentService2)
    provider = container.provider()
    assert provider.provide(DependentService1).service is None
    assert provider.provide(DependentService2).service is None

    container = Container()

    container.add_singleton(DependentService3, create_optional)
    container.add_singleton(Dependent1)
    container.add_singleton(Dependent2)
    provider = container.provider()

    assert provider.provide(DependentService3 | None) is None # pyright: ignore[reportArgumentType]

    with assert_raises(FactoryProvideException):
        provider.provide(DependentService3)
    assert provider.provide(Dependent2) is not None
    with assert_raises(FactoryProvideException):
        provider.provide(Dependent1)



    container = Container()

    container.add_singleton(DependentService1)
    container.add_singleton(Service)
    provider = container.provider()
    assert provider.provide(DependentService1).service is not None

    container = Container()

    container.add_singleton(DependentService3)
    provider = container.provider()

    assert provider.provide(DependentService3).services == []





def test_default():
    container = Container()

    container.add_singleton(DependentService4)
    container.add_singleton(ServiceWithDefault)
    provider = container.provider()
    assert provider.provide(DependentService4).services == []
    assert provider.provide(ServiceWithDefault).test == "Hi"


def test_provide_factory():
    container = Container()
    container.add_singleton(Service)
    provider = container.provider()
    factory = provider.provide(Factory[Service])
    assert isinstance(cast(object, factory()), Service)

    container = Container()

    container.add_singleton(Service)
    container.add_singleton(WithFactory)
    provider = container.provider()
    obj = provider.provide(WithFactory)

def test_generic_service():
    T = TypeVar('T')
    class GenericClass(Generic[T]):
        pass

    container = Container()

    container.add_singleton(GenericClass[str])
    container.add_singleton(GenericClass[int])
    provider = container.provider()

    assert provider.provides(GenericClass[str]) == True
    assert provider.provides(GenericClass[int]) == True
    provider.provide(GenericClass[str])
    provider.provide(GenericClass[int])

