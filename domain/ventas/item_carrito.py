class ItemCarrito:
    def __init__(self, producto, cantidad):
        self.producto = producto
        self.cantidad = cantidad

    @property
    def precio_unitario(self):
        return self.producto.precio_unitario

    @property
    def subtotal(self):
        return self.precio_unitario * self.cantidad