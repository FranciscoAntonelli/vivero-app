class VentasQuery:

    def __init__(self, ventas_service, detalle_service):
        self.ventas_service = ventas_service
        self.detalle_service = detalle_service

    def obtener_ventas(self, usuario_id, fecha_inicio, fecha_fin):
        return self.ventas_service.buscar(usuario_id, fecha_inicio, fecha_fin)

    def obtener_detalles(self, id_venta):
        return self.detalle_service.buscar(id_venta)