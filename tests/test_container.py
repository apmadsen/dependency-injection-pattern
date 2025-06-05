# pyright: basic
# from __future__ import annotations
from typing import cast, Sequence
from pytest import raises as assert_raises
from threading import Thread

from di import Container, Provider
from di.exceptions import ImplementationException, AddException, SealException, ProvideException, ContainerSealedError

from tests.classes import Service, Options1, DependentService, DependentServiceFail1, IService, Service2



def test_dependencies():
    container = Container()
    container.add_transient(Service)
    container.add_singleton(Options1, Options1("test", 35))
    container.add_transient(DependentService)

    with assert_raises(ImplementationException):
        container.add_transient(DependentServiceFail1)

    with assert_raises(AddException):
        container.add_transient(Service)

    with assert_raises(AddException):
        container.add_transient("test") # pyright: ignore[reportCallIssue, reportArgumentType]

    with assert_raises(AddException):
        container.add_transient(123) # pyright: ignore[reportCallIssue, reportArgumentType]

    with assert_raises(AddException):
        container.add_transient(123, "abc") # pyright: ignore[reportCallIssue, reportArgumentType]

    assert container._defines(Service)
    assert not container._defines(12345) # pyright: ignore[reportCallIssue, reportArgumentType]

    with assert_raises(ProvideException):
        container._get(123) # pyright: ignore[reportCallIssue, reportArgumentType]


def test_container():
    container = Container()

    container.add_transient(Service)
    provider = container.provider()

    assert provider.provides(Provider)
    assert provider is provider.provide(Provider)
    assert provider.provides(Provider)
    assert provider is provider.provide(Provider)

    with assert_raises(ContainerSealedError):
        container.add_transient(Service)
    with assert_raises(ContainerSealedError):
        container.add_singleton(Service)
    with assert_raises(ContainerSealedError):
        container.add_scoped(Service)

def test_singleton_transient_dependency():
    class Service3:
        ...
    class Service4:
        def __init__(self, service: Service3):
            ...

    container = Container()
    container.add_transient(Service3)
    container.add_singleton(Service4)

    with assert_raises(SealException):
        provider = container.provider()

def test_singleton_scoped_dependency():
    class Service5:
        ...
    class Service6:
        def __init__(self, service: Service5):
            ...

    container = Container()
    container.add_scoped(Service5)
    container.add_singleton(Service6)

    with assert_raises(SealException):
        provider = container.provider()


def test_collections():

    container = Container()

    with assert_raises(ImplementationException):
        container.add_singleton(Sequence[IService], [ Service, Service2 ])

