class CategoriasService:
    def __init__(self, repo):
        self.repo = repo

    def listar_categorias(self):
        return self.repo.obtener_todas()
    
    def agregar_categoria(self, nombre_categoria):
        if not nombre_categoria or not nombre_categoria.strip():
            raise ValueError("El nombre de la categoría no puede estar vacío.")
        if self.repo.existe_categoria(nombre_categoria):
            raise ValueError("La categoría ya existe.")
        self.repo.agregar_categoria(nombre_categoria.strip())

    def obtener_id_por_nombre(self, nombre):
        categorias = self.listar_categorias()
        for categoria in categorias:
            if categoria.nombre.strip().lower() == nombre.strip().lower():
                return categoria.id_categoria
        raise ValueError(f"La categoría '{nombre}' no existe.")
    
    def obtener_nombre_por_id(self, id_categoria):
        categorias = self.listar_categorias()
        for categoria in categorias:
            if categoria.id_categoria == id_categoria:
                return categoria.nombre
        return ""