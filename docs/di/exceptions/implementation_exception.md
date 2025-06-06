[Documentation](/docs/documentation.md) > [di](/docs/di/module.md) > [exceptions](/docs/di/exceptions/module.md) > ImplementationException class

# `ImplementationException` exception

The `ImplementationException` exception is raised at initialization time when factory cannot provide service using the specified implementation. This could be due to implementation not resolving to a class derived from service, or that implementaion cannot be resolved at all due to missing type annotations.
