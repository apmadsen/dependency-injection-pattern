from __future__ import annotations
from typing import TypeVar, Callable, MutableMapping, cast
from threading import Thread, local, current_thread, main_thread

from di.core.log import LOG
from di.core.scope import Scope
from di.core.exceptions.provide_exception import ProvideException
from di.core.helpers import is_context, get_service_name

T = TypeVar('T')


class DefaultScope(Scope):
    """
    DefaultScope is as the name implies the default scope. This scope is thread-based, meaning it will supply
    the same instance of a service, each time it's requested on the same thread.
    It will automatically handle object lifetime of scoped services, which are required to implement
    the Contextmanager pattern (supplying  standard Python __enter__ and __exit__ methods),
    by finalizing them at the end of scope (i.e. thread exit).
    """
    __slots__ = ["__local"]

    def __init__(self):
        if not hasattr(self, "_DefaultScope__local"): # pragma: no cover
            self.__local = local()

    def provide(self, service: type[T], factory: Callable[[], T]) -> T:
        if current_thread() == main_thread():
            raise ProvideException(service,
                """Using DefaultScope on main thread is not permitted.
                If referencing a scoped service on a transient or singleton service,
                consider using the Factory[Service] method""")

        if not hasattr(self.__local, "dict"):
            LOG.debug(f"Initializing scope for thread '{current_thread().name}'")
            dict: MutableMapping[type[T], T] = {}
            self.__local.dict = dict

            def finalize(thread: Thread, dict: MutableMapping[type[T], T]) -> None:
                thread.join() # wait until thread is finished
                LOG.debug(f"Finalizing scope for thread '{current_thread().name}'")
                for service, implementation in dict.items():
                    try:
                        if is_context(service):
                            LOG.debug(f"Disposing service '{get_service_name(service)}' on thread '{current_thread().name}'")
                            getattr(implementation, "__exit__")()

                    except Exception as ex: # pragma: no cover
                        # swallow exception, as it's caught in the finalizer thread
                        LOG.error(f"Disposing of service '{get_service_name(service)}' failed: {ex}")


                dict.clear()

            if current_thread() != main_thread(): # only implement finalizer if thread is not main thread # pragma: no cover
                self.__local.finalizer = Thread(target = finalize, args = [ current_thread(), dict ])
                self.__local.finalizer.start()

        if not service in self.__local.dict:
            impl = factory()
            if current_thread() != main_thread() and is_context(service):
                # finalizer is only implemented when thread is not main thread, otherwise object would never be exited (eg. finalized)
                LOG.debug(f"Initializing service '{get_service_name(service)}' on thread '{current_thread().name}'")
                impl = cast(T, getattr(impl, "__enter__")())
                if not isinstance(impl, service): # pragma: no cover
                    raise ProvideException(service, f"Service '{get_service_name(service)}' implementation's __enter__() method returned an object of different type than service")

            self.__local.dict[service] = impl

        return cast(T, self.__local.dict[service])

