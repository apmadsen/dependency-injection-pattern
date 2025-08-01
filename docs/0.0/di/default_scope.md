[Documentation](/docs/documentation.md) >
 [v0.0](/docs/0.0/version.md) >
  [di](/docs/0.0/di/module.md) >
   DefaultScope

# DefaultScope : [Scope](scope.md)

The `DefaultScope` class is, as the name implies, the default scope used for providing services that are registered using the `add_scoped(...)` function. The class is not intended for usage outside the `di` module, which is why it's not documented in-depth.

Internally the class uses a thread bound dictionary to keep track of provided services, and performs cleanup tasks when thread is closing/finalizing. This cleanup requires services to implement the `ContextManager` pattern (`__enter__` and `__exit__` functions) to work properly.
