[![Test](https://github.com/apmadsen/dependency-injection-pattern/actions/workflows/python-test.yml/badge.svg)](https://github.com/apmadsen/dependency-injection-pattern/actions/workflows/python-test.yml)
[![Coverage](https://github.com/apmadsen/dependency-injection-pattern/actions/workflows/python-test-coverage.yml/badge.svg)](https://github.com/apmadsen/dependency-injection-pattern/actions/workflows/python-test-coverage.yml)
[![Stable Version](https://img.shields.io/pypi/v/dependency-injection-pattern?label=stable&sort=semver&color=blue)](https://github.com/apmadsen/dependency-injection-pattern/releases)
![Pre-release Version](https://img.shields.io/github/v/release/apmadsen/dependency-injection-pattern?label=pre-release&include_prereleases&sort=semver&color=blue)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dependency-injection-pattern)
[![PyPI Downloads](https://static.pepy.tech/badge/dependency-injection-pattern/week)](https://pepy.tech/projects/dependency-injection-pattern)

# Dependency Injection Pattern (Python)

A typed dependency injection framework for Python — focused on clarity, structure, and maintainability.

## 🚀 Why this exists

As Python applications grow, managing dependencies becomes increasingly difficult:

- Hidden dependencies make systems harder to understand
- Tight coupling reduces flexibility
- Testing requires complex setup and mocking
- Structure becomes inconsistent across modules

Unlike many other ecosystems, Python lacks a widely adopted, structured approach to dependency injection.

👉 This project aims to introduce **clear, typed dependency management** to Python applications.


## ✨ Features

- 🧩 Strongly typed dependency injection
- 🧠 Explicit dependency definitions
- 🔄 Clear separation of concerns
- 🧪 Improved testability
- 🏗 Support for structured application architecture
- ⚡ Lightweight and Python-native design


## 📦 Use cases

This library is particularly useful when building:

- Backend services
- Data engineering workflows
- ETL pipelines
- Modular applications
- Systems with complex dependency graphs

👉 Especially valuable in projects where maintainability and scalability matter.


## 🏗 Design philosophy

This project is built around a few key principles:

### 1. Explicit over implicit
Dependencies should be visible and well-defined — not hidden in implementation details.

### 2. Type-driven structure
Type hints are used as a foundation for defining and resolving dependencies.

### 3. Maintainability over convenience
The goal is not to reduce lines of code — but to make systems easier to evolve.

### 4. Minimal abstraction
The framework avoids unnecessary complexity and stays close to Python’s core concepts.

---

## 🔗 What this enables

By introducing structured dependency injection, you get:

- Clear boundaries between components
- Easier reasoning about system design
- More predictable runtime behavior
- Improved ability to refactor safely

👉 This is especially powerful in larger systems where complexity grows over time.


## ⚖️ Trade-offs

| Focus ✅ | Not a goal ❌ |
|---------|--------------|
| Structured architecture | Magic-based auto-wiring |
| Type safety | Implicit dependency resolution |
| Clarity and control | Minimal configuration at all costs |

👉 This library prioritizes **explicit design over automation**.


## 🧠 Inspiration

Inspired by dependency injection patterns from ecosystems such as:

- C# / .NET (built-in DI container)
- Java (Spring, Guice)

But intentionally adapted to fit Python’s dynamic nature
without introducing heavy frameworks or unnecessary indirection.


## 🎯 When to use

Use this library if you:

- Are building medium to large Python applications
- Want clearer separation between components
- Need better testability
- Prefer structured architecture over ad-hoc patterns

---

## 🚫 When not to use

This library may be unnecessary if:

- Your project is small or short-lived
- Dependency complexity is minimal
- Simplicity is more important than structure


## 🔗 Related projects

Part of a broader focus on:

- Clean architecture
- Runtime abstractions
- Developer tooling in Python

👉 https://github.com/apmadsen



## 🤝 Contributing

Feedback, ideas, and contributions are welcome!


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