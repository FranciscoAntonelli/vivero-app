from use_cases.reportes.ireportes_use_case import IReportesUseCase


class ReportesUseCase(IReportesUseCase):
    def __init__(self, reportes_service):
        self.service = reportes_service

    def obtener_reporte_diario(self, usuario_id, fecha_desde=None, fecha_hasta=None):
        return self.service.obtener_reporte_diario(usuario_id, fecha_desde, fecha_hasta)

    def obtener_stock_por_producto(self, usuario_id):
        return self.service.obtener_stock_por_producto(usuario_id)

    def obtener_ventas_mensuales(self, usuario_id):
        return self.service.obtener_ventas_mensuales(usuario_id)

    def obtener_stock_por_categoria(self, usuario_id):
        return self.service.obtener_stock_por_categoria(usuario_id)
    
    def obtener_productos_mas_vendidos(self, usuario_id, top_n):
        # Por defecto, devuelve los 10 productos más vendidos
        return self.service.obtener_productos_mas_vendidos(usuario_id, top_n)