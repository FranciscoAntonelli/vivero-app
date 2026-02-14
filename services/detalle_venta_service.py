class DetalleVentaService:
    def __init__(self, repo):
        self.repo = repo

    def buscar(self, id_venta=None):
        return self.repo.buscar_detalles_por_venta(id_venta)

    def agregar(self, detalle):
        self.repo.agregar_detalle_venta(detalle)