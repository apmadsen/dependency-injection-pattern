[Documentation](/docs/documentation.md) >
 [v0.0](/docs/0.0/version.md) >
  [di](/docs/0.0/di/module.md) >
   [exceptions](/docs/0.0/di/exceptions/module.md) >
    SealException class

# SealException : Exception

The `SealException` exception is raised when container is being sealed and a preliminary check reveals that one or more services cannot be provided. This could be due to a singleton service depending on a transient or scoped service which isn't allowed or a service with a dependency that cannot be resolved.
