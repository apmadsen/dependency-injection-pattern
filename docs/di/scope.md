[Documentation](/docs/documentation.md) > [di](/docs/di/module.md) > Scope class

# `Scope` class

The `Scope` class is the base class of scopes used for providing services that are registered using the `add_scoped(...)` function.

This project has one scope which is `DefaultScope` and that's a threaded scope.

## Functions

### provide(service: _type[T]_, factory: _Callable[..., T]_) -> _T_

The `provide(self, service: type[T], factory: Callable[..., T]) -> T` function is used by the `ScopedFactory` factory to provide and cleanup services.