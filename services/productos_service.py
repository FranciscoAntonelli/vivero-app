class ProductosService:
    def __init__(self, repo):
        self.repo = repo

    def buscar(self, nombre=None, id_usuario=None):
        return self.repo.buscar(nombre, id_usuario)
    
    def eliminar(self, id_producto):
        # Solo elimina
        self.repo.eliminar(id_producto)

    def agregar(self, producto):
        self.repo.agregar(producto)
        
    def editar(self, producto):
        self.repo.editar(producto)