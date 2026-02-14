class CategoriasUseCase:
    def __init__(self, categorias_service):
        self.categorias_service = categorias_service

    def obtener_nombre_categoria(self, id_categoria):
        return self.categorias_service.obtener_nombre_por_id(id_categoria)