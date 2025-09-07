class CategoriasService:
    def __init__(self, repo):
        self.repo = repo

    def listar_categorias(self):
        return self.repo.obtener_todas()
    
    def obtener_nombre_por_id(self, id_categoria):
        categorias = self.listar_categorias()
        for categoria in categorias:
            if categoria.id_categoria == id_categoria:
                return categoria.nombre
        return ""