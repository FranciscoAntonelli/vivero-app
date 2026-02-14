from use_cases.meta.iproductos_meta_use_case import IProductosMetaUseCase


class ProductosMetaUseCase(IProductosMetaUseCase):
    def __init__(self, meta_service):
        self.meta_service = meta_service

    def registrar_modificacion(self, id_usuario):
        self.meta_service.registrar_modificacion(id_usuario)

    def obtener_ultima_modificacion(self, id_usuario):
        return self.meta_service.obtener_ultima_modificacion(id_usuario)