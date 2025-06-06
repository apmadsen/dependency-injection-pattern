[Documentation](/docs/documentation.md) > [di](/docs/di/di.md) > Provider class

# `Provider` class

The `Provider` class is created by the container when sealing it, and is the class that provides the services registered on that container.

## Example:
```python
from logging import Logger
from di import Container

def get_logger(name: str = "app-log") -> Logger: # default name arg will be used later on
    return Logger(name)

container = Container()
container.add_singleton(get_logger)
provider = container.provider()
log = provider.provide(Logger) # => Logger
```
The provider can also be used as a service, ie. when an arbitrary no. of services must be resolved:

```python
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
```

## provides(service: _str | type[Any]_) -> _bool_

The `provides(service: str | type[Any])` function returns a boolean value indicating if a service of specified type of name can be provided or not.

## provide(self, service: _type[T]_) -> _T_

The `provide(self, service: type[T]) -> T` function returns the service with specified type.

## provide(self, service: _type[T]_, scope: _Scope_) -> _T_

The `provide(self, service: type[T], scope: Scope) -> T` function returns the service with specified type. If a scope is specified, that scope handles the lifetime of the service - otherwise the default scope eg. `Container.default_scope` is used.

Note that only scoped services registered using the `add_scoped(...)` function uses the scope to handle lifetime.

