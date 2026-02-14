from abc import ABC, abstractmethod

class ICategoriasUseCase(ABC):

    @abstractmethod
    def obtener_nombre_categoria(self, id_categoria):
       pass