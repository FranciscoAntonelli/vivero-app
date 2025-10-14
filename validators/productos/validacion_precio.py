from validators.productos.validacion_producto import IValidacionProducto


class ValidacionPrecio(IValidacionProducto):
    def validar(self, producto_data):
        errores = []
        precio = producto_data.get("precio_unitario")

        if precio == 0:
            errores.append("El precio debe ser mayor que cero.")

        return errores