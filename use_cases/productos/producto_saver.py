from models.producto import Producto
from use_cases.productos.iproducto_saver import IProductoSaver


class ProductoSaver(IProductoSaver):

    def __init__(self, producto_service):
        self.producto_service = producto_service

    def guardar(self, producto_dict, producto_existente=None):
        producto = self._crear_producto(producto_dict, producto_existente)

        if producto_existente:
            self.producto_service.editar(producto)
        else:
            self.producto_service.agregar(producto)

        return producto

    def _crear_producto(self, data, existente):
        return Producto(
            id_producto=existente.id_producto if existente else None,
            nombre=data["nombre"],
            categoria_id=data["categoria"],
            ubicacion=data["ubicacion"],
            medida=data["medida"],
            cantidad=data["cantidad"],
            precio_unitario=data["precio_unitario"],
            creado_por=data["creado_por"]
        )