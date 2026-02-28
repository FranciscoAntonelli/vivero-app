class Venta:
    def __init__(self, id_usuario, total, fecha=None, id_venta=None):
        self.id_venta = id_venta
        self.id_usuario = id_usuario
        self.total = total
        self.fecha = fecha 