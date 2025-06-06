[Documentation](/docs/documentation.md) > [di](/docs/di/module.md) > [exceptions](/docs/di/exceptions/module.md) > SealException class

# `SealException` exception

The `SealException` exception is raised when container is being sealed and a preliminary check reveals that one or more services cannot be provided. This could be due to a singleton service depending on a transient or scoped service which isn't allowed or a service with a dependency that cannot be resolved.
