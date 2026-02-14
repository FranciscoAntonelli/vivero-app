from datetime import datetime
from models.venta import Venta


class VentaCreator:
    def crear(self, carrito, usuario_id):
        if carrito.vacio():
            raise Exception("El carrito está vacío")

        return Venta(
            id_usuario=usuario_id,
            total=carrito.total(),
            fecha=datetime.now()
        )