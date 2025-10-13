import unittest
from unittest.mock import Mock
from utils.impresion.impresora_productos import ImpresoraProductos


class TestImpresoraProductos(unittest.TestCase):
    def setUp(self):
        self.impresora = ImpresoraProductos()

    # --- preparar_datos_productos ---
    def test_preparar_datos_productos_calculo_correcto(self):
        p1 = Mock(nombre="Maceta", precio_unitario=100.0, cantidad=2)
        p2 = Mock(nombre="Tierra", precio_unitario=50.0, cantidad=3)
        p3 = Mock(nombre="Planta", precio_unitario=120.0, cantidad=1)
        productos = [p1, p2, p3]

        lineas, total = self.impresora.preparar_datos_productos(productos)

        self.assertEqual(len(lineas), 3)
        self.assertEqual(lineas[0]["subtotal"], 200.0)
        self.assertEqual(lineas[1]["subtotal"], 150.0)
        self.assertEqual(lineas[2]["subtotal"], 120.0)
        self.assertEqual(total, 470.0)

    def test_preparar_datos_productos_lista_vacia(self):
        productos = []

        lineas, total = self.impresora.preparar_datos_productos(productos)

        self.assertEqual(lineas, [])
        self.assertEqual(total, 0)

    def test_preparar_datos_productos_con_decimales(self):
        p1 = Mock(nombre="Abono", precio_unitario=33.33, cantidad=3)
        productos = [p1]

        lineas, total = self.impresora.preparar_datos_productos(productos)

        self.assertAlmostEqual(lineas[0]["subtotal"], 99.99, places=2)
        self.assertAlmostEqual(total, 99.99, places=2)

    # --- dibujar_productos ---
    def test_dibujar_productos_invoca_metodos(self):
        painter_mock = Mock()
        lineas = [
            {"nombre": "Maceta", "precio": 100.0, "cantidad": 2, "subtotal": 200.0},
            {"nombre": "Planta", "precio": 120.0, "cantidad": 1, "subtotal": 120.0},
        ]
        total = 320.0

        self.impresora.dibujar_productos(painter_mock, lineas, total)

        # Se asegura que el painter fue usado
        painter_mock.drawText.assert_called()
        painter_mock.drawLine.assert_called()