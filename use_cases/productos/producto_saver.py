from models.producto import Producto


class ProductoSaver:
    """Esta clase se encarga de la creacion o actualizacion del producto"""
    def __init__(self, producto_service):
        self.producto_service = producto_service

    def guardar(self, producto_dict, producto_existente=None):
        producto = Producto(
            id_producto=producto_existente.id_producto if producto_existente else None,
            nombre=producto_dict["nombre"],
            categoria_id=producto_dict["categoria"],
            ubicacion=producto_dict["ubicacion"],
            medida=producto_dict["medida"],
            cantidad=producto_dict["cantidad"],
            precio_unitario=producto_dict["precio_unitario"],
            creado_por=producto_dict["creado_por"]
        )

        if producto_existente:
            self.producto_service.editar(producto)
        else:
            self.producto_service.agregar(producto)

        return producto