class MetaService:
    def __init__(self, meta_repository):
        self.meta_repository = meta_repository

    def obtener_ultima_modificacion(self, usuario):
        fecha = self.meta_repository.obtener_fecha_modificacion(usuario)
        return fecha if fecha else "No registrada"
    
    def registrar_modificacion(self, usuario):
        self.meta_repository.actualizar_fecha_modificacion(usuario)