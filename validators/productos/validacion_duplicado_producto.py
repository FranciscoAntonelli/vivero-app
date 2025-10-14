from validators.productos.validacion_producto import IValidacionProducto

class ValidadorDuplicadoProducto(IValidacionProducto):
    """revisa si ya existe un producto con el mismo nombre, ubicacion y medida."""

    def __init__(self, producto_service):
        self.producto_service = producto_service

    def validar(self, producto_data):
        if self.producto_service.existe_producto(
            producto_data["nombre"],
            producto_data["ubicacion"],
            producto_data["medida"],
            id_excluir = producto_data.get("id_producto")
        ):
            return ["Ya existe un producto con ese nombre y ubicación."]
        return []
