from abc import ABC, abstractmethod

class ValidadorLoginBase(ABC):
    @abstractmethod
    def validar(self, usuario, clave):
        pass