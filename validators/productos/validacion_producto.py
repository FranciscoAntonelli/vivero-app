from abc import ABC, abstractmethod


class IValidacionProducto(ABC):
    @abstractmethod
    def validar(self, producto_data):
        """Recibe un diccionario con los datos del producto y devuelve errores (lista)"""
        pass