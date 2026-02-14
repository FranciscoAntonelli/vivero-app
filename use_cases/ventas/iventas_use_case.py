from abc import ABC, abstractmethod


class IVentasUseCase(ABC):
    @abstractmethod
    def obtener_ventas(self, usuario_id, filtro_texto=None, fecha_inicio=None, fecha_fin=None):
        pass

    @abstractmethod
    def obtener_detalles(self, id_venta):
        pass
    
    @abstractmethod
    def registrar_venta(self, carrito, usuario_id):
       pass
