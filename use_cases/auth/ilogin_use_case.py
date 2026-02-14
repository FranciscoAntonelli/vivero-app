from abc import ABC, abstractmethod
class ILoginUseCase(ABC):

    @abstractmethod
    def autenticar(self, usuario, clave):
       pass
    