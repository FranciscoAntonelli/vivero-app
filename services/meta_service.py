class MetaService:
    def __init__(self, meta_repository):
        self.meta_repository = meta_repository

    def obtener_ultima_modificacion(self, usuario):
        return self.meta_repository.obtener_fecha_modificacion(usuario)
    
    def registrar_modificacion(self, usuario):
        self.meta_repository.actualizar_fecha_modificacion(usuario)