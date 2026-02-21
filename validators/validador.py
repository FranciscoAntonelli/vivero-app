from abc import ABC, abstractmethod

class Validador(ABC):
    @abstractmethod
    def validar(self, data):
        pass