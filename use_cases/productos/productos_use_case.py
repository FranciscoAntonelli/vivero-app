from exceptions.producto_con_ventas_error import ProductoConVentasError
from models.resultado_eliminacion import ResultadoEliminacion
from use_cases.productos.iproductos_use_case import IProductosUseCase


class ProductosUseCase(IProductosUseCase):

    def __init__(self, productos_service):
        self.productos_service = productos_service

    def obtener_productos(self, id_usuario, nombre=None):
        return self.productos_service.buscar(nombre, id_usuario)

    def eliminar_producto(self, id_producto):
            try:
                self.productos_service.eliminar(id_producto)

                return ResultadoEliminacion(exito=True)

            except ProductoConVentasError:
                return ResultadoEliminacion(
                    exito=False,
                    errores=["No se puede eliminar el producto porque tiene ventas asociadas."]
                )

            except Exception as e:
                return ResultadoEliminacion(
                    exito=False,
                    errores=[f"Ocurrió un error inesperado al eliminar el producto: {e}"]
                )
       
    def obtener_nombre(self, id_producto):
        return self.productos_service.buscar_por_id(id_producto)