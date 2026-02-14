from abc import ABC, abstractmethod


class IImprimirProductosUseCase(ABC):
   
    @abstractmethod
    def ejecutar(self, datos):
        pass