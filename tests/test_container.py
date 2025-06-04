# pyright: basic
from __future__ import annotations
from typing import cast, Sequence, MutableSequence, Generic, TypeVar, Any, ClassVar
from pytest import raises as assert_raises

from di import Container, Factory, Provider
from di.exceptions import FactoryImplementException, AddException, FactorySealException, FactoryProvideException, ProvideException, FactorySealedError

from tests.classes import *



def test_dependencies():
    Service.INST.clear()

    container = Container()
    container.add_transient(Service)
    container.add_singleton(Options1, Options1("test", 35))
    container.add_transient(DependentService)

    with assert_raises(FactoryImplementException):
        container.add_transient(DependentServiceFail1)

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

    with assert_raises(FactorySealedError):
        container.add_transient(Service)
    with assert_raises(FactorySealedError):
        container.add_singleton(Service)
    with assert_raises(FactorySealedError):
        container.add_scoped(Service)

def test_collections():

    container = Container()

    with assert_raises(FactoryImplementException):
        container.add_singleton(Sequence[IService], [ Service, Service2 ])

