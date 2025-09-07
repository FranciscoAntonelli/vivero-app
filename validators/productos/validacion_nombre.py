from validators.productos.validacion_producto import IValidacionProducto


class ValidacionNombre(IValidacionProducto):
    def validar(self, producto_data):
        errores = []
        nombre = producto_data.get("nombre", "").strip()
        if not nombre:
            errores.append("El nombre no puede estar vacío.")
        return errores