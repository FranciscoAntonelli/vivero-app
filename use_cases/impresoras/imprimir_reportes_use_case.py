from use_cases.impresoras.iimprimir_reportes_use_case import IImprimirReportesUseCase


class ImprimirReportesUseCase(IImprimirReportesUseCase):
    def __init__(self, reportes_service, impresora):
        self.reportes_service = reportes_service
        self.impresora = impresora

    def ejecutar(self, usuario_id, fecha_desde=None, fecha_hasta=None):
        reportes = self.reportes_service.obtener_reporte_diario(
            usuario_id, fecha_desde, fecha_hasta
        )

        self.impresora.imprimir(reportes)


       