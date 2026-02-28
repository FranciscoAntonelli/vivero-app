class DetalleVenta:
    def __init__(self, id_producto, cantidad, subtotal, id_venta=None, id_detalle=None):
        self.id_detalle = id_detalle
        self.id_venta = id_venta  
        self.id_producto = id_producto
        self.cantidad = cantidad
        self.subtotal = subtotal
