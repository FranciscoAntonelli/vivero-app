from abc import ABC, abstractmethod
class IProductoPopupUseCase(ABC):

    @abstractmethod
    def listar_categorias(self):
        pass
    
    @abstractmethod
    def guardar_producto(self, producto_dict, producto_existente=None):
        pass