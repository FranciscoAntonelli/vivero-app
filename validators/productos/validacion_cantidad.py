from validators.productos.validacion_producto import IValidacionProducto


class ValidacionCantidad(IValidacionProducto):
    def validar(self, producto_data):
        errores = []
        cantidad = producto_data.get("cantidad")

        if cantidad is None:
            errores.append("La cantidad debe ser un número entero válido.")
        elif cantidad <= 0:
            errores.append("La cantidad debe ser mayor que cero.")

        return errores