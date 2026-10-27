from di.core.exceptions.internal_exception import InternalException


class NamedService:
    def __new__(cls):
        raise InternalException("The NamedService is a special class not meant to be instantiated") # pragma: no cover
