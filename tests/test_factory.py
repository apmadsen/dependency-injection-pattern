# pyright: basic
from __future__ import annotations
from time import sleep
from threading import Thread
from typing import cast, Sequence, MutableSequence, Generic, TypeVar, Any, ClassVar
from pytest import raises as assert_raises

from di import Container, Factory, Provider
from di.core.service_request import ServiceRequest
from di.exceptions import ImplementationException, AddException, SealException, FactoryProvideException, ProvideException

from tests.classes import *


def test_factory():
    container = Container()

    def cs():
        return Service

    def cs1() -> Service:
        return Service()

    class Test1: pass
    class Test2: pass
    class Test3: pass

    def impl1() -> Test1:
        return Test1()
    def impl2() -> Test2:
        return Test2()
    def impl3() -> Test3:
        return Test3()

    with assert_raises(ImplementationException):
        container.add_singleton(Service, Service) #impl same as svc
    with assert_raises(ImplementationException):
        container.add_singleton(Service, cs) #impl has no return annotation
    with assert_raises(ImplementationException):
        container.add_singleton(IService, Service1) #imp not derived from svc

    container.add_singleton(Service, cs1)
    container.add_singleton(impl1)
    container.add_transient(impl2)
    container.add_scoped(impl3)
    container.add_singleton(IService, Service)

    provider = container.provider()
    assert provider.provides(Test1)
    assert provider.provides(Test2)
    assert provider.provides(Test3)

    container = Container()
    container.add_singleton(Service)
    with assert_raises(AddException):
        container.add_singleton(Service, Service)


def test_factory_provide():
    container = Container()

    container.add_transient(Service)
    container.add_transient(DependentService)
    container.add_singleton(Options1, Options1("test", 35))

    provider = container.provider()
    factory, *_ = container._get_factory(DependentService)

    del cast(dict, getattr(container, "_Container__factories"))[Service] # forcefully remove the factory of Service

    with assert_raises(FactoryProvideException):
        cast(Factory[DependentService], factory).provide()

def test_named_factory():
    container = Container()
    container.add_singleton('Name', "Test")
    with assert_raises(AddException):
        container.add_singleton('Name', "Other")
    provider = container.provider()
    assert provider.provides('Name')
    assert provider.provides('name')
    assert provider._provide(ServiceRequest('name', str, None)) == provider._provide(ServiceRequest('Name', str, None))
    assert provider._provide(ServiceRequest('name', str, None)) == "Test"


    def cs() -> Service:
        return Service()

    container = Container()
    container.add_singleton('Name1', Service)
    container.add_singleton('Name2', cs)
    provider = container.provider()

    assert provider.provides('Name1')
    assert provider.provides('name2')
    provider._provide(ServiceRequest('Name1', Service, None))
    with assert_raises(ProvideException):
        provider._provide(ServiceRequest('Name1', Service1, None))


def test_transient_factory():
    Service.INST.clear()

    container = Container()
    container.add_transient(Service)
    provider = container.provider()
    provider.provide(Service)
    provider.provide(Service)
    assert isinstance(cast(object, provider.provide(Service)), Service)
    assert len(Service.INST) == 3

def test_singleton_factory():
    Service.INST.clear()

    container = Container()
    container.add_singleton(Service)
    container.add_singleton(Options1, Options1("test", 35))
    provider = container.provider()
    provider.provide(Service)
    provider.provide(Service)
    assert isinstance(cast(object, provider.provide(Service)), Service)
    assert isinstance(cast(object, provider.provide(Options1)), Options1)

    assert len(Service.INST) == 1

    container = Container()
    container.add_transient(Service)
    container.add_singleton(Options1, Options1("test", 35))
    container.add_singleton(DependentService)
    with assert_raises(SealException):
        container.provider()


def test_scoped_factory():
    class CTX:
        classes: ClassVar[MutableSequence[CTX]] = []
        entered = 0
        exited = 0
        def __init__(self):
            CTX.classes.append(self)
        def __enter__(self) -> CTX:
            self.entered += 1
            return self
        def __exit__(self, *args: Any, **kwargs: Any):
            self.exited += 1

    Service.INST.clear()

    container = Container()
    container.add_scoped(Service)
    container.add_scoped(CTX)
    provider = container.provider()

    with assert_raises(ProvideException):
        provider.provide(Service) # should raise exception in the main thread


    def thread_f():
        s1 = provider.provide(Service)
        s2 = provider.provide(Service)
        assert isinstance(cast(object, provider.provide(Service)), Service)
        assert s1 == s2
        provider.provide(CTX)


    thread1 = Thread(target=thread_f)
    thread1.start()
    thread1.join()

    thread2 = Thread(target=thread_f)
    thread2.start()
    thread2.join()

    sleep(0.1) # wait for thread finalizer to run

    assert len(Service.INST) == 2
    assert len([ inst for inst in CTX.classes if inst.entered != 1 ]) == 0
    assert len([ inst for inst in CTX.classes if inst.exited != 1 ]) == 0



