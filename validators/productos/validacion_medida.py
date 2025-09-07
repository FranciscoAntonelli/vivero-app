from validators.productos.validacion_producto import IValidacionProducto


class ValidacionMedida(IValidacionProducto):
    def validar(self, producto_data):
        errores = []
        medida = producto_data.get("medida")
        if medida and len(medida.strip()) > 30:
            errores.append("La medida es demasiado larga.")
        return errores