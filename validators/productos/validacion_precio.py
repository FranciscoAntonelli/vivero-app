from validators.productos.validacion_producto import IValidacionProducto


class ValidacionPrecio(IValidacionProducto):
    def validar(self, productos):
        errores = []
        precio = productos.get("precio_unitario")

        if precio == 0:
            errores.append("El precio debe ser mayor que cero.")

        return errores