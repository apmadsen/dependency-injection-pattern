[Documentation](/docs/documentation.md) >
 [v0.0](/docs/0.0/version.md) >
  [di](/docs/0.0/di/module.md) >
   Provider

# `Provider` class

The `Provider` class is created by the container when sealing it, and is the class that provides the services registered on that container.

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

## Functions

### provides(service: _str | type[Any]_) -> _bool_

The `provides(service: str | type[Any])` function returns a boolean value indicating if a service of specified type of name can be provided or not.

### provide(self, service: _type[T]_) -> _T_

The `provide(self, service: type[T]) -> T` function returns the service with specified type.

#### Example:
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

### provide(self, service: _type[T]_, scope: _Scope_) -> _T_

The `provide(self, service: type[T], scope: Scope) -> T` function returns the service with specified type. If a scope is specified, that scope handles the lifetime of the service - otherwise the default scope eg. `Container.default_scope` is used.

Note that only scoped services registered using the `add_scoped(...)` function uses the scope to handle lifetime.


### Example:
```python
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

len(generators) # => 2
len(ints) # => 6
```