from models.resultado import Resultado
from use_cases.ventas.iventas_use_case import IVentasUseCase


class VentaUseCase(IVentasUseCase):

    def __init__(self, venta_creator, venta_domain_service, ventas_query_service, rango_fechas_validador):
        self.venta_creator = venta_creator
        self.venta_domain_service = venta_domain_service
        self.ventas_query_service = ventas_query_service
        self.rango_fechas_validador = rango_fechas_validador

    def obtener_ventas(self, usuario_id, fecha_inicio=None, fecha_fin=None):
        error = self.rango_fechas_validador.validar(fecha_inicio, fecha_fin)
        if error:
            return Resultado(False, None, errores=[error])

        ventas = self.ventas_query_service.obtener_ventas(
            usuario_id, fecha_inicio, fecha_fin
        )

        return Resultado(True, ventas)

    def obtener_detalles(self, id_venta):
        return self.ventas_query_service.obtener_detalles(id_venta)

    def registrar_venta(self, carrito, usuario_id):
        venta = self.venta_creator.crear(carrito, usuario_id)
        
        # Verificar stock para cada producto en el carrito
        for item in carrito.items:
            if not self.venta_domain_service.productos_service.verificar_stock(item.producto.id_producto, item.cantidad):
                raise ValueError(f"Stock insuficiente para el producto {item.producto.nombre}")
        
        return self.venta_domain_service.procesar_venta(venta, carrito)