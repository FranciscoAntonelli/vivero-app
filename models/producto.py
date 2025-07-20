class Producto:
    def __init__(self, id_producto, nombre, categoria_id, ubicacion, medida, precio_unitario, cantidad, creado_por):
        self.id_producto = id_producto
        self.nombre = nombre
        self.categoria_id = categoria_id
        self.ubicacion = ubicacion
        self.medida = medida
        self.precio_unitario = precio_unitario
        self.cantidad = cantidad
        self.creado_por = creado_por