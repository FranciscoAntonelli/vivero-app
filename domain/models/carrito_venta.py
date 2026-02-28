from decimal import Decimal
from domain.models.item_carrito import ItemCarrito

class CarritoVenta:
    def __init__(self):
        self._items = []

    @property
    def items(self):
        return self._items.copy()

    def agregar(self, producto, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")

        # cantidad ya en el carrito
        cantidad_actual = 0
        for item in self._items:
            if item.producto.id_producto == producto.id_producto:
                cantidad_actual = item.cantidad
                break

        if cantidad_actual + cantidad > producto.cantidad:
            raise ValueError(
                f"Stock insuficiente. Disponible: {producto.cantidad}"
            )

        for item in self._items:
            if item.producto.id_producto == producto.id_producto:
                item.cantidad += cantidad
                return

        self._items.append(ItemCarrito(producto, cantidad))

    def eliminar(self, id_producto):
        self._items = [
            item for item in self._items
            if item.producto.id_producto != id_producto
        ]

    def vacio(self):
        return len(self._items) == 0

    def total(self):
        return sum((item.subtotal for item in self.items), Decimal("0.00"))

  