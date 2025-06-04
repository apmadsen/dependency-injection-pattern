class NamedService():
    def __new__(cls):
        raise Exception("The NamedService is a special class not meant to be instantiated") # pragma: no cover
