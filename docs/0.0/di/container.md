[Documentation](/docs/documentation.md) >
 [v0.0](/docs/0.0/version.md) >
  [di](/docs/0.0/di/module.md) >
   Container

# Container

The `Container` class is the class where all service registration takes place.

### Example:
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

## Functions

### add_singleton(service: _type[Any]_)

Registers a singleton service based on a type. When resolved, the types constructor dependencies are injected automatically.

- service `type[Any]`: The service type.

### add_singleton(implementation: _Callable[..., T]_)

Registers a singleton service based on the return type of the implementation. When resolved, the implementations dependencies (in case of it being a function) are injected automatically. This service can be used to inject simple objects like strings and integers.

- implementation `(...) -> T`: The implementation function.

### add_singleton(service: _type[T]_, implementation: _Callable[..., T] | type[T] | T_)

Registers a singleton service based on a type and an implementation of either a derived type or a function returning a derived type. When resolved, the implementations dependencies (in case of it being a function or a type) are injected automatically.

- service `type[Any]`: The service type.
- implementation `(...) -> T | type[T]`: The implementation function or type.

### add_singleton(service: _str_, implementation: _Callable[..., T] | type[T] | T_)

Registers a singleton service based on a name and an implementation of either a derived type or a function returning a derived type. When resolved, the implementations dependencies (in case of it being a function) are injected automatically. This method can be used to inject simple objects like strings and integers.

- service `str`: The service name.
- implementation `(...) -> T | type[T]`: The implementation function or type.

### add_transient(service: _type[Any]_)

Registers a transient service based on a type. When resolved, the types constructor dependencies are injected automatically.

- service `type[Any]`: The service type.

### add_transient(implementation: _Callable[..., T]_)

Registers a transient service based on the return type of the implementation. When resolved, the implementations dependencies (in case of it being a function) are injected automatically. This service can be used to inject simple objects like strings and integers.

- implementation `(...) -> T`: The implementation function.

### add_transient(service: _type[T]_, implementation: _Callable[..., T] | type[T] | T_)

Registers a transient service based on a type and an implementation of either a derived type or a function returning a derived type. When resolved, the implementations dependencies (in case of it being a function or a type) are injected automatically.

- service `type[Any]`: The service type.
- implementation `(...) -> T | type[T]`: The implementation function or type.

### add_transient(service: _str_, implementation: _Callable[..., T] | type[T] | T_)

Registers a transient service based on a name and an implementation of either a derived type or a function returning a derived type. When resolved, the implementations dependencies (in case of it being a function) are injected automatically. This method can be used to inject simple objects like strings and integers.

- service `str`: The service name.
- implementation `(...) -> T | type[T]`: The implementation function or type.

### add_scoped(service: _type[Any]_)

Registers a scoped service based on a type. When resolved, the types constructor dependencies are injected automatically.

- service `type[Any]`: The service type.

### add_scoped(implementation: _Callable[..., T]_)

Registers a scoped service based on the return type of the implementation. When resolved, the implementations dependencies (in case of it being a function) are injected automatically. This service can be used to inject simple objects like strings and integers.

- implementation `(...) -> T`: The implementation function.

### add_scoped(service: _type[T]_, implementation: _Callable[..., T] | type[T] | T_)

Registers a scoped service based on a type and an implementation of either a derived type or a function returning a derived type. When resolved, the implementations dependencies (in case of it being a function or a type) are injected automatically.

- service `type[Any]`: The service type.
- implementation `(...) -> T | type[T]`: The implementation function or type.

### add_scoped(service: _str_, implementation: _Callable[..., T] | type[T] | T_)

Registers a scoped service based on a name and an implementation of either a derived type or a function returning a derived type. When resolved, the implementations dependencies (in case of it being a function) are injected automatically. This method can be used to inject simple objects like strings and integers.

- service `str`: The service name.
- implementation `(...) -> T | type[T]`: The implementation function or type.

### provider() -> _[Provider](provider.md)_

Seals the container and returns a `Provider`. When container is sealed, no more services can be registered.


#### Example:
```python
from di import Container

class Service:
    def get_value(self) -> str:
        return "Some value"

container = Container()
# register service by its type only
container.add_singleton(Service)
provider = container.provider()
service = provider.provide(Service) # => Service
```


#### Example:
```python
from logging import Logger
from di import Container

def get_logger() -> Logger:
    return Logger("app")

container = Container()
# register service by its type and a function which
# will be responsible for providing it at runtime
container.add_singleton(Logger, get_logger)
provider = container.provider()
log = provider.provide(Logger) # => Logger
```

#### Example:
```python
from di import Container

class Application:
    def __init__(self, app_name: str):
        self.name = app_name

container = Container()

container.add_transient(Application)
# register service by its name and a literal value
container.add_singleton("app_name", "App using Dependency Injection :)")
provider = container.provider()
app = provider.provide(Application)
app_name = app.name # => "App using Dependency Injection :)"
```

#### Example:
```python
from logging import Logger
from di import Container

def get_logger(name: str = "app-log") -> Logger: # default name arg will be used later on
    return Logger(name)

container = Container()
# register service by its implementation function - type is inferred by
# the functions return type
container.add_singleton(get_logger)
provider = container.provider()
log = provider.provide(Logger) # => Logger
```