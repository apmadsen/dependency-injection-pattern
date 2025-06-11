# pyright: basic
# from __future__ import annotations
from typing import cast, Sequence
from pytest import raises as assert_raises
from threading import Thread
from weakref import ref
from gc import get_referrers, collect

from di import Container, Provider, Factory
from di.exceptions import ImplementationException, AddException, SealException, ProvideException, ContainerSealedError

from tests.classes import Service, Options1, DependentService, DependentServiceFail1, IService, Service2, Service5, DependentService5, Application



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

def test_lifetime():

    container = Container()
    container.add_transient(Service5)

    provider = container.provider()
    provider_id = id(provider)
    svc = provider.provide(Service5)
    provider = ref(provider)

    collect()

    assert not provider() # provider should have been collected

    provider = container.provider()
    assert id(provider) != provider_id # this provider be a new instance

    provider = ref(provider)
    container = ref(container)

    collect()

    # provider and container should have been collected
    assert not provider()
    assert not container()

    ### cleanup
    del container
    del provider
    del svc
    collect()
    ###

    container = Container()
    container.add_transient(Application)
    container.add_transient(Service5)
    container.add_transient(DependentService5)
    provider = container.provider()

    app = provider.provide(Application)
    svc = app.service_factory()

    container = ref(container)
    provider = ref(provider)

    collect()

    # app has a live reference to Factory[Service5],
    # so neither container or provider should be collected
    assert container()
    assert provider()

    app = ref(app)

    collect()

    # app has been collected thus any references to container and provider
    # has been removed and container and provider has therefore
    # also been collected
    assert not app()
    assert not provider()
    assert not container()
