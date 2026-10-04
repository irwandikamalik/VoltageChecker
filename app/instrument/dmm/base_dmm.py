from abc import ABC, abstractmethod


class BaseDMM(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def identify(self):
        pass

    @abstractmethod
    def read_voltage(self):
        pass

    @abstractmethod
    def read_current(self):
        pass