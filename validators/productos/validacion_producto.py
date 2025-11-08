from abc import ABC, abstractmethod


class IValidacionProducto(ABC):
    @abstractmethod
    def validar(self, productos):
        """Recibe un diccionario con los datos del producto y devuelve errores (lista)"""
        pass