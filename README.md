[![Test](https://github.com/apmadsen/dependency-injection-pattern/actions/workflows/python-test.yml/badge.svg)](https://github.com/apmadsen/dependency-injection-pattern/actions/workflows/python-test.yml)
[![Coverage](https://github.com/apmadsen/dependency-injection-pattern/actions/workflows/python-test-coverage.yml/badge.svg)](https://github.com/apmadsen/dependency-injection-pattern/actions/workflows/python-test-coverage.yml)
[![Stable Version](https://img.shields.io/pypi/v/dependency-injection-pattern?label=stable&sort=semver&color=blue)](https://github.com/apmadsen/dependency-injection-pattern/releases)
![Pre-release Version](https://img.shields.io/github/v/release/apmadsen/dependency-injection-pattern?label=pre-release&include_prereleases&sort=semver&color=blue)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dependency-injection-pattern)
[![PyPI Downloads](https://static.pepy.tech/badge/dependency-injection-pattern/week)](https://pepy.tech/projects/dependency-injection-pattern)

# dependency-injection-pattern: Python implementation of the Dependency Injection pattern.

Dependency-injection-pattern extends python with a real dependency injection or Inversion of Control (IoC) implementation, relying on typing to achieve a seamless injection of dependencies.

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

## API

[Go to API documentation](https://github.com/apmadsen/pyproject.toml/blob/main/docs/api.md)