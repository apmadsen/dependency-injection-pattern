[Documentation](/docs/documentation.md) >
 [v0.0](/docs/0.0/version.md) >
  [di](/docs/0.0/di/module.md) >
   [exceptions](/docs/0.0/di/exceptions/module.md) >
    ImplementationException class

# ImplementationException : Exception

The `ImplementationException` exception is raised at initialization time when factory cannot provide service using the specified implementation. This could be due to implementation not resolving to a class derived from service, or that implementaion cannot be resolved at all due to missing type annotations.
