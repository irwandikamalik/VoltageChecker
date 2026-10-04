from abc import ABC, abstractmethod


class BaseConnection(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def write(self, command):
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def query(self, command):
        pass