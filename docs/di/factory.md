[Documentation](/docs/documentation.md) > [di](/docs/di/di.md) > Factory class

# `Factory` class

The `Factory[T]` class is used to get the Provider to provide a factory instead of a service implementation ie. a lazy implementation. This is useful if lazy provision is required, or when service was registered using the `add_scoped(...)` function, because Scoped services, using the `DefaultScope` scope cannot be provided in the main thread (that would defeat the purpose of a scoped service).

## Example:
```python
from di import Container, Factory
from di.core.service_request import ServiceRequest
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
```