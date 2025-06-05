# pragma: no cover
class SealException(Exception):
    """
    The SealException is raised when container is being sealed and a preliminary check reveals that one or more
    services cannot be provided. This could be due to a singleton service depending on a transient or scoped service which
    isn't allowed..
    """
    def __init__(self, msg: str):
        super().__init__(msg)
