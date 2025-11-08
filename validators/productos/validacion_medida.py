from validators.productos.validacion_producto import IValidacionProducto


class ValidacionMedida(IValidacionProducto):
    def validar(self, productos):
        errores = []
        medida = productos.get("medida")
        if medida and len(medida.strip()) > 30:
            errores.append("La medida es demasiado larga.")
        return errores