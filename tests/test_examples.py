# pyright: basic

def test_example_1():
    from logging import Logger
    from di import Container

    def get_logger() -> Logger:
        return Logger("app")

    class Service1:
        def get_value(self) -> str:
            return "Some value"

    class Service2:
        def __init__(self, service1: Service1, log: Logger):
            self.service1 = service1
            self.log = log

        def get_value(self) -> str:
            self.log.debug("Someone requested value...")
            return f"Service1 returned: {self.service1.get_value()}"

    class Application:
        def __init__(self, service2: Service2, log: Logger):
            self.service2 = service2
            log.info("Application starting")

        def get_value(self) -> str:
            return f"Service2 returned: {self.service2.get_value()}"


    container = Container()
    container.add_singleton(get_logger)
    container.add_transient(Service1)
    container.add_transient(Service2)
    container.add_transient(Application)

    provider = container.provider()

    app = provider.provide(Application)

    value = app.get_value() # => "Service2 returned: Service1 returned: Some value"

    assert value == "Service2 returned: Service1 returned: Some value"

def test_example_2():
    from di import Container

    class Service:
        def get_value(self) -> str:
            return "Some value"

    container = Container()
    container.add_singleton(Service)
    provider = container.provider()
    service = provider.provide(Service) # => Service

    assert isinstance(service, Service)


def test_example_3():
    from logging import Logger
    from di import Container

    def get_logger() -> Logger:
        return Logger("app")

    container = Container()
    container.add_singleton(Logger, get_logger)
    provider = container.provider()
    log = provider.provide(Logger) # => Logger

    assert isinstance(log, Logger)

def test_example_4():
    from di import Container
    from di.core.service_request import ServiceRequest

    class Application:
        def __init__(self, app_name: str):
            self.name = app_name

    container = Container()

    container.add_transient(Application)
    container.add_singleton("app_name", "App using Dependency Injection :)")

    provider = container.provider()
    name = provider._provide(ServiceRequest("app_name", str, None)) # => "App using Dependency Injection :)"
    app = provider.provide(Application)
    app_name = app.name # => "App using Dependency Injection :)"

    assert name == "App using Dependency Injection :)"
    assert name == app_name


def test_example_5():
    from logging import Logger
    from di import Container

    def get_logger(name: str = "app-log") -> Logger: # default name arg will be used later on
        return Logger(name)

    container = Container()
    container.add_singleton(get_logger)
    provider = container.provider()
    log = provider.provide(Logger) # => Logger

    assert isinstance(log, Logger)
    assert log.name == "app-log"


def test_example_6():
    from di import Container, Factory
    from di.exceptions import ProvideException
    from threading import Thread

    class Service:
        def get_value(self) -> str:
            return "Some value"

    class Application:
        def __init__(self, service: Factory[Service]):
            self.service_factory = service

    container = Container()

    container.add_transient(Application)
    container.add_scoped(Service)

    provider = container.provider()
    app = provider.provide(Application)

    values: list[str] = []

    def fn(app: Application):
        values.append(app.service_factory().get_value())

    thread = Thread(target = fn, args = (app,))
    thread.start()
    thread.join()

    try:
        value = app.service_factory().get_value()
    except ProvideException as ex:
        # => ProvideException("Cannot provide service 'Service': Using DefaultScope on main thread is not permitted.
        # If referencing a scoped service on a transient or singleton service, consider using the Factory[Service] method")
        pass

    value = values[0] # => "Some value"
    assert values[0] == "Some value"

def test_example_7():
    from di import Container, Provider
    from tests.classes import Service1, Service2

    class Application:
        def __init__(self, provider: Provider):
            self.services = (
                provider.provide(service)
                for service in [
                    Service1,
                    Service2
                ]
            )

    container = Container()
    container.add_transient(Application)
    container.add_transient(Service1)
    container.add_transient(Service2)

    provider = container.provider()

    app = provider.provide(Application)
    service1, service2 = app.services # => Service1, Service2

    assert isinstance(service1, Service1)
    assert isinstance(service2, Service2)


def test_example_8():
    from di import Container, DefaultScope, Scope, Provider
    from random import Random
    from threading import Thread

    class RandGen:
        rnd: Random | None

        def generate(self) -> int:
            if self.rnd:
                return self.rnd.randint(0, 100)
            else:
                return -1

        def __enter__(self):
            self.rnd = Random()
            return self

        def __exit__(self):
            del self.rnd

    container = Container()
    container.add_scoped(RandGen)

    scope = DefaultScope()
    provider = container.provider()

    generators: set[int] = set()
    ints: list[int] = []

    def fn(provider: Provider, scope: Scope):
        for i in range(3):
            gen = provider.provide(RandGen, scope)
            generators.add(id(gen))
            ints.append(gen.generate())

    thread1 = Thread(target = fn, args = (provider, scope))
    thread1.start()
    thread2 = Thread(target = fn, args = (provider, scope))
    thread2.start()
    thread1.join()
    thread2.join()

    assert len(generators) == 2
    assert len(ints) == 6

