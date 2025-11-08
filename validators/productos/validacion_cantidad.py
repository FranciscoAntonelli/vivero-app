from validators.productos.validacion_producto import IValidacionProducto


class ValidacionCantidad(IValidacionProducto):
    def validar(self, productos):
        errores = []
        cantidad = productos.get("cantidad")
        
        if cantidad == 0:
            errores.append("La cantidad debe ser mayor que cero.")

        return errores