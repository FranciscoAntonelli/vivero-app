from abc import ABC, abstractmethod

class IProductosUseCase(ABC):

    @abstractmethod 
    def obtener_productos(self, id_usuario, nombre=None):
        pass
    @abstractmethod
    def eliminar_producto(self, id_producto):
        pass
    @abstractmethod
    def obtener_nombre(self, id_producto):
        pass