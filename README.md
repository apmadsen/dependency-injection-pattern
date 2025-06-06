[![Test](https://github.com/apmadsen/dependency-injection-pattern/actions/workflows/python-test.yml/badge.svg)](https://github.com/apmadsen/dependency-injection-pattern/actions/workflows/python-test.yml)
[![Coverage](https://github.com/apmadsen/dependency-injection-pattern/actions/workflows/python-test-coverage.yml/badge.svg)](https://github.com/apmadsen/dependency-injection-pattern/actions/workflows/python-test-coverage.yml)
[![Stable Version](https://img.shields.io/pypi/v/dependency-injection-pattern?label=stable&sort=semver&color=blue)](https://github.com/apmadsen/dependency-injection-pattern/releases)
![Pre-release Version](https://img.shields.io/github/v/release/apmadsen/dependency-injection-pattern?label=pre-release&include_prereleases&sort=semver&color=blue)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dependency-injection-pattern)
[![PyPI Downloads](https://static.pepy.tech/badge/dependency-injection-pattern/week)](https://pepy.tech/projects/dependency-injection-pattern)

# dependency-injection-pattern
> A Python implementation of the Dependency Injection pattern.

This project extends python with a real dependency injection or Inversion of Control (IoC) implementation, relying on typing and inspection to achieve a seamless injection of dependencies.

Though not normally associated with Python applications, dependency injection can greatly reduce time spent during development and testing. Usually, in a longrunning Python application or service, you would put the container registration inside the `__main_.py` file and similar code in test files, where service implementations can easily be substituted.

## How it works
When a service is requested, the provider looks it up in the factory dictionary, which then gets or creates a fitting instance. Any parameters needed for instantiation is supplied (injected) by the provider.

A service implementation may be inferred by a service in which case the service constructor is used, and correspondingly a service may be inferred by the return type of an implementation function.

## Conventions
- All dependencies are resolved when container is sealed, which implements a fail-fast pattern. Only exceptions are optional dependencies or dependencies with a default value.

- Singleton services may not depend on scoped or transient services, as this would negate the "transient" or "scoped" part since a singleton service would keep a reference to it's dependencies indefinitely.

## Example:

```python
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

provider = container.provider() # container is sealed beyond this point

app = provider.provide(Application)

value = app.get_value() # => "Service2 returned: Service1 returned: Some value"
```

## Full documentation

[Go to documentation](https://github.com/apmadsen/dependency-injection-pattern/blob/main/docs/documentation.md)