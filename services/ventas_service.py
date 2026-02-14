class VentasService:
    def __init__(self, repo):
        self.repo = repo

    def buscar(self, usuario_id, fecha_inicio=None, fecha_fin=None):
        return self.repo.buscar_ventas(usuario_id, fecha_inicio, fecha_fin)

    def agregar(self, venta):
        id_venta = self.repo.registrar_venta(venta)
        return id_venta