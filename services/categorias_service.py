class CategoriasService:
    def __init__(self, repo):
        self.repo = repo

    def listar_categorias(self):
        return self.repo.obtener_todas()
    
    def obtener_nombre_por_id(self, id_categoria):
        categoria = self.repo.obtener_por_id(id_categoria)  
        return categoria.nombre if categoria else ""