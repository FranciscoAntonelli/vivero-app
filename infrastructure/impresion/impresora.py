from abc import ABC, abstractmethod

class Impresora(ABC):

    @abstractmethod
    def imprimir(self, datos):
        pass