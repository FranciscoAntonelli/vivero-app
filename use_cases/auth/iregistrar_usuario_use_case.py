from abc import ABC, abstractmethod
class IRegistrarUsuarioUseCase(ABC):

    @abstractmethod
    def ejecutar(self, nombre_usuario, password, password_confirm):
        pass