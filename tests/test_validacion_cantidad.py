import unittest
from validators.productos.validacion_cantidad import ValidacionCantidad

class TestValidacionCantidad(unittest.TestCase):
    def setUp(self):
        self.validador = ValidacionCantidad()

    def test_cantidad_cero_devuelve_error(self):
        producto = {"cantidad": 0}
        errores = self.validador.validar(producto)
        self.assertIn("La cantidad debe ser mayor que cero.", errores)

    def test_cantidad_positiva_no_devuelve_error(self):
        producto = {"cantidad": 5}
        errores = self.validador.validar(producto)
        self.assertEqual(errores, [])