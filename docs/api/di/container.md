[API](/docs/api.md) > [di](/docs/api/di/di.md) > Container class

# `Container` class

The `Container` class is the class where all service registration takes place.

## Example:
```python
from logging import Logger
from di import Container

def get_logger() -> Logger:
    return Logger("app")


container = Container()
container.add_singleton(get_logger)
```

The class has three main scopes for registering services:

- `add_singleton(...)`: Adds a singleton service to the container. When service is requested, the same instance will be returned each time.
- `add_transient(...)`: Adds a transient service to the container. When service is requested, a new instance will be returned each time.
- `add_scoped(...)`: Adds a scoped service to the container. When service is requested within the same scope, the same instance will be returned each time.

Common to all three scopes, are four patterns:

## add_xxx(service: _type[Any]_)

The `add_xxx(service: type[Any])` function registers a service based on a type. When resolved, the types constructor dependencies are injected automatically.

### Example:
```python
from di import Container

class Service:
    def get_value(self) -> str:
        return "Some value"

container = Container()
container.add_singleton(Service)
provider = container.provider()
service = provider.provide(Service) # => Service
```

## add_xxx(service: _type[T]_, implementation: _Callable[..., T] | type[T] | T_)

The `add_xxx(service: type[T], implementaion: Callable[..., T] | type[T] | T)` function registers a service based on a type and an implementation of either a derived type or a function returning a derived type. When resolved, the implementations dependencies (in case of it being a function or a type) are injected automatically.

### Example:
```python
from logging import Logger
from di import Container

def get_logger() -> Logger:
    return Logger("app")

container = Container()
container.add_singleton(Logger, get_logger)
provider = container.provider()
log = provider.provide(Logger) # => Logger
```

## add_xxx(service: _str_, implementation: _Callable[..., T] | type[T] | T_)

The `add_xxx(service: str, implementaion: Callable[..., T] | type[T] | T)` function registers a service based on a name and an implementation of either a derived type or a function returning a derived type. When resolved, the implementations dependencies (in case of it being a function) are injected automatically. This method can be used to inject simple objects like strings and integers.

### Example:
```python
from di import Container

class Application:
    def __init__(self, app_name: str):
        self.name = app_name

container = Container()

container.add_transient(Application)
container.add_singleton("app_name", "App using Dependency Injection :)")
provider = container.provider()
app = provider.provide(Application)
app_name = app.name # => "App using Dependency Injection :)"
```

## add_xxx(implementation: _Callable[..., T]_)

The `add_xxx(implementaion: Callable[..., T] | type[T] | T)` function registers a service based on the return type of the implementation. When resolved, the implementations dependencies (in case of it being a function) are injected automatically. This service can be used to inject simple objects like strings and integers.

### Example:
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

## provider() -> _Provider_

The `provider()` function seals the container and returns a `Provider`. When container i sealed, no more services can be registered.