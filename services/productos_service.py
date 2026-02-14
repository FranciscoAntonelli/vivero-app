class ProductosService:
    def __init__(self, repo):
        self.repo = repo

    def buscar(self, nombre=None, id_usuario=None):
        return self.repo.buscar(nombre, id_usuario)
    
    def eliminar(self, id_producto):
        self.repo.eliminar(id_producto)

    def agregar(self, producto):
        self.repo.agregar(producto)
        
    def editar(self, producto):
        self.repo.editar(producto)
    
    def buscar_por_id(self, id_producto):
        return self.repo.buscar_por_id(id_producto)
    
    def descontar_stock(self, id_producto, cantidad):
        self.repo.descontar_stock(id_producto, cantidad)

    def verificar_stock(self, id_producto, cantidad):
        stock = self.repo.obtener_stock(id_producto)
        return stock >= cantidad