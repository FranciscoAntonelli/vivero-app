from models.resultado import Resultado
from use_cases.reportes.ireportes_use_case import IReportesUseCase


class ReportesUseCase(IReportesUseCase):
    def __init__(self, reportes_service, rango_fechas_validador):
        self.service = reportes_service
        self.rango_fechas_validador = rango_fechas_validador

    def obtener_reporte_diario(self, usuario_id, fecha_desde=None, fecha_hasta=None):
        error = self.rango_fechas_validador.validar(fecha_desde, fecha_hasta)
        if error:
            return Resultado(
                exito=False,
                errores=[error]
            )
        
        datos = self.service.obtener_reporte_diario(usuario_id, fecha_desde, fecha_hasta)

        return Resultado(
                exito=True,
                valor=datos
            )

    def obtener_stock_por_producto(self, usuario_id):
        return self.service.obtener_stock_por_producto(usuario_id)

    def obtener_ventas_mensuales(self, usuario_id):
        return self.service.obtener_ventas_mensuales(usuario_id)

    def obtener_stock_por_categoria(self, usuario_id):
        return self.service.obtener_stock_por_categoria(usuario_id)
    
    def obtener_productos_mas_vendidos(self, usuario_id, top_n):
        # Por defecto, devuelve los 10 productos más vendidos
        return self.service.obtener_productos_mas_vendidos(usuario_id, top_n)