class ProductosUseCase:
    def __init__(self, productos_service, categorias_service, meta_service, validador, impresora):
        self.service = productos_service
        self.categorias_service = categorias_service
        self.meta_service = meta_service
        self.validador = validador
        self.impresora = impresora


    def obtener_productos(self, id_usuario, nombre=None):
        return self.service.buscar(nombre, id_usuario)

    def obtener_nombre_categoria(self, id_categoria):
        return self.categorias_service.obtener_nombre_por_id(id_categoria)

    def registrar_modificacion(self, id_usuario):
        self.meta_service.registrar_modificacion(id_usuario)

    def obtener_ultima_modificacion(self, id_usuario):
        return self.meta_service.obtener_ultima_modificacion(id_usuario)

    def eliminar_producto(self, id_producto):
        try:
            self.service.eliminar(id_producto)
        except Exception as e:
            raise Exception(f"No se pudo eliminar el producto: {e}")

    def imprimir(self, productos, ventana):
        self.impresora.imprimir(productos, ventana)

    def agregar_producto(self, producto):
        # valido que no haya duplicado
        self._validar_no_existe_producto(producto)
        
        # agrego el producto con el service
        self.service.agregar(producto)

    def _validar_no_existe_producto(self, producto):
        if self.service.existe_producto(
            producto.nombre,
            producto.ubicacion,
            producto.medida,
            id_excluir=producto.id_producto
        ):
            raise Exception("Ya existe un producto con ese nombre, ubicación y medida.")
        
    def editar_producto(self, producto):
        # valido que no haya duplicado
        self._validar_no_existe_producto(producto)

        # Edito el producto con el service que dentro tiene el repo
        self.service.editar(producto)