from abc import ABC, abstractmethod


class GraficoRenderer(ABC):
    @abstractmethod
    def render_stock_producto(self, datos):
        pass
    @abstractmethod
    def render_stock_categoria(self, datos):
        pass
    @abstractmethod
    def render_ventas_mensuales(self, datos): 
        pass
    @abstractmethod
    def render_productos_mas_vendidos(self, datos):
        pass