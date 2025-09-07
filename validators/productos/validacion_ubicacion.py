from validators.productos.validacion_producto import IValidacionProducto


class ValidacionUbicacion(IValidacionProducto):
    def __init__(self, ubicaciones_validas):
        self.ubicaciones_validas = ubicaciones_validas

    def validar(self, producto):
        errores = []
        ubicacion = getattr(producto, "ubicacion", None)

        # Permito None o vacio
        if ubicacion and ubicacion not in self.ubicaciones_validas:
            errores.append("Ubicación debe ser Interior, Exterior o Ambas")

        return errores