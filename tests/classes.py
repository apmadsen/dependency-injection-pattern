# pyright: basic
from __future__ import annotations
from typing import Sequence, MutableSequence, Any

from di import Factory

class IService():
    def __init__(self, arg1: str):
        pass

class Service1():
    pass

class Service(IService):
    INST: MutableSequence[Any] = []
    def __new__(cls):
        inst = object.__new__(cls)
        Service.INST.append(inst)
        return inst

    def __init__(self):
        pass

class Service2(IService):
    INST: Sequence[Any] = []
    def __new__(cls):
        inst = object.__new__(cls)
        Service.INST.append(inst)
        return inst

    def __init__(self):
        pass


class DependentServiceFail1():
    def __init__(self, service):
        self.service = service

class DependentServiceFail2():
    def __init__(self, service: str):
        self.service = service

class DependentService():
    def __init__(self, service: Service, opts: Options1):
        self.service = service

class DependentService1():
    def __init__(self, service: Service | None = None):
        self.service = service


class DependentService2():
    def __init__(self, service: Service | None):
        self.service = service


class DependentService3():
    def __init__(self, services: Sequence[Service] | None = []):
        self.services = services


class DependentService4():
    def __init__(self, services: Sequence[Service]=[]):
        self.services = services


class ServiceWithDefault():
    def __init__(self, test: str = "Hi"):
        self.test = test
class Options1():
    def __init__(self, o1: str, o2: int):
        self.option1 = o1
        self.option2 = o2


class WithFactory():
    def __init__(self, a: Factory[Service]):
        self.arg = a

    def get_svc(self) -> Service:
        return self.arg()
