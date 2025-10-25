from abc import ABC, abstractmethod


class IProductoSaver(ABC):
    @abstractmethod
    def guardar(self, producto_dict, producto_existente=None):
        pass