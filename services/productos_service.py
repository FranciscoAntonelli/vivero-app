class ProductosService:
    def __init__(self, repo):
        self.repo = repo

    def buscar(self, nombre=None, id_usuario=None):
        return self.repo.buscar(nombre, id_usuario)
    
    def eliminar(self, id_producto):
        try:
            self.repo.eliminar(id_producto)
        except Exception as e:
            raise Exception(f"No se pudo eliminar el producto: {str(e)}")

    def agregar(self, producto):
        if self.existe_producto(producto.nombre, producto.ubicacion, producto.medida):
            raise Exception("Ya existe un producto con ese nombre, ubicación y medida.")
        try:
            self.repo.agregar(producto)
        except Exception as e:
            raise Exception(f"No se pudo agregar el producto: {str(e)}")
        
    def editar(self, producto):
        if self.existe_producto(producto.nombre, producto.ubicacion, producto.medida, id_excluir=producto.id_producto):
            raise Exception("Ya existe un producto con ese nombre, ubicación y medida.")
        try:
            self.repo.editar(producto)
        except Exception as e:
            raise Exception(f"No se pudo editar el producto: {str(e)}")
    
    def existe_producto(self, nombre, ubicacion, medida=None, id_excluir=None):
        return self.repo.existe_producto(nombre, ubicacion, medida, id_excluir)