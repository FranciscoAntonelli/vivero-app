from models.producto import Producto


class ProductoPopupController:
    def __init__(self, producto_service, categorias_service, validador):
        self.producto_service = producto_service
        self.categorias_service = categorias_service
        self.validador = validador

    def listar_categorias(self):
        return self.categorias_service.listar_categorias()
    
    def validar_y_guardar(self, producto_dict, producto_existente=None):
        errores = self.validador.validar(producto_dict)
        if errores:
            return False, errores
        
        # Evito duplicados
        if self.producto_service.existe_producto(
            producto_dict["nombre"],
            producto_dict["ubicacion"],
            producto_dict["medida"],
            id_excluir=producto_existente.id_producto if producto_existente else None
        ):
            return False, ["Ya existe un producto con ese nombre y ubicación."]
        
        # Creo el producto
        producto_obj = Producto(
            id_producto=producto_existente.id_producto if producto_existente else None,
            nombre=producto_dict["nombre"],
            categoria_id=producto_dict["categoria"],
            ubicacion=producto_dict["ubicacion"],
            medida=producto_dict["medida"],
            cantidad=producto_dict["cantidad"],
            precio_unitario=producto_dict["precio_unitario"],
            creado_por=producto_dict["creado_por"]
        )

        # Guardo
        if producto_existente:
            self.producto_service.editar(producto_obj)
        else:
            self.producto_service.agregar(producto_obj)

        return True, None