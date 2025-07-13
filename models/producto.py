class Producto:
    def __init__(self, nombre, categoria, ubicacion, medida, cantidad, precio_unitario, creado_por=None, id_producto=None):
        self.id_producto = id_producto
        self.nombre = nombre
        self.categoria = categoria
        self.ubicacion = ubicacion
        self.medida = medida
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.creado_por = creado_por