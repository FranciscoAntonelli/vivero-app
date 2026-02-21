from abc import ABC, abstractmethod

class IReportesUseCase(ABC):
    @abstractmethod
    def obtener_reporte_diario(self, usuario_id, fecha_desde=None, fecha_hasta=None):
        pass

    @abstractmethod
    def obtener_stock_por_producto(self, usuario_id):
        pass
    
    @abstractmethod
    def obtener_ventas_mensuales(self, usuario_id):
        pass

    @abstractmethod
    def obtener_stock_por_categoria(self, usuario_id):
        pass