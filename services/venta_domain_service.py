from domain.models.detalle_venta import DetalleVenta


class VentaDomainService:

    def __init__(self, ventas_service, detalle_service, productos_service):
        self.ventas_service = ventas_service
        self.detalle_service = detalle_service
        self.productos_service = productos_service

    def procesar_venta(self, venta, carrito):
        id_venta = self.ventas_service.agregar(venta)

        for item in carrito.items:
            self.detalle_service.agregar(
                DetalleVenta(
                    id_venta=id_venta,
                    id_producto=item.producto.id_producto,
                    cantidad=item.cantidad,
                    subtotal=item.subtotal
                )
            )
            self.productos_service.descontar_stock(
                item.producto.id_producto,
                item.cantidad
            )

        return id_venta