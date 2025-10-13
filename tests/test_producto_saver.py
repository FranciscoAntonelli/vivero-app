from unittest import TestCase
from unittest.mock import MagicMock, Mock
from models.producto import Producto
from use_cases.productos.producto_saver import ProductoSaver

class TestProductoSaver(TestCase):

    def setUp(self):
        self.mock_service = MagicMock()
        self.saver = ProductoSaver(self.mock_service)
        self.producto_dict = {
            "nombre": "Planta Rosa",
            "categoria": 1,
            "ubicacion": "Exterior",
            "medida": "Mediana",
            "cantidad": 10,
            "precio_unitario": 150.0,
            "creado_por": "Admin"
        }

    def test_guardar_nuevo_producto(self):
        producto = self.saver.guardar(self.producto_dict)

        # Verifica que se haya llamado agregar una sola vez
        self.mock_service.agregar.assert_called_once()
        self.mock_service.editar.assert_not_called()

        # Verifica que el producto se haya creado correctamente
        self.assertIsInstance(producto, Producto)
        self.assertEqual(producto.nombre, self.producto_dict["nombre"])
        self.assertEqual(producto.categoria_id, self.producto_dict["categoria"])
        self.assertEqual(producto.ubicacion, self.producto_dict["ubicacion"])
        self.assertEqual(producto.medida, self.producto_dict["medida"])
        self.assertEqual(producto.cantidad, self.producto_dict["cantidad"])
        self.assertEqual(producto.precio_unitario, self.producto_dict["precio_unitario"])

    def test_guardar_producto_existente(self):
        producto_existente = Producto(
            id_producto=5,
            nombre="Planta Vieja",
            categoria_id=1,
            ubicacion="Interior",
            medida="Chica",
            cantidad=5,
            precio_unitario=100.0,
            creado_por="Admin"
        )

        producto = self.saver.guardar(self.producto_dict, producto_existente)

        # Verifica que se haya llamado editar una sola vez
        self.mock_service.editar.assert_called_once()
        self.mock_service.agregar.assert_not_called()

        # Verifica que el id se mantenga
        self.assertEqual(producto.id_producto, producto_existente.id_producto)
        # Y que los demás datos se actualicen
        self.assertEqual(producto.nombre, self.producto_dict["nombre"])
        self.assertEqual(producto.medida, self.producto_dict["medida"])
        self.assertEqual(producto.cantidad, self.producto_dict["cantidad"])