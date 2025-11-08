from validators.productos.validacion_producto import IValidacionProducto


class ValidacionNombre(IValidacionProducto):
    def validar(self, productos):
        errores = []
        nombre = productos.get("nombre", "").strip()
        if not nombre:
            errores.append("El nombre no puede estar vacío.")
        return errores