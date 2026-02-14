from abc import ABC, abstractmethod
class IProductosMetaUseCase(ABC):

    @abstractmethod
    def registrar_modificacion(self, id_usuario):
        pass

    @abstractmethod
    def obtener_ultima_modificacion(self, id_usuario):
        pass