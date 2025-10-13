import unittest
from validators.productos.validacion_precio import ValidacionPrecio


class TestValidacionPrecio(unittest.TestCase):
    def setUp(self):
        self.validador = ValidacionPrecio()

    def test_precio_cero_devuelve_error(self):
        producto = {"precio_unitario": 0}
        errores = self.validador.validar(producto)
        self.assertIn("El precio debe ser mayor que cero.", errores)

    def test_precio_positivo_no_devuelve_errores(self):
        producto = {"precio_unitario": 100}
        errores = self.validador.validar(producto)
        self.assertEqual(errores, [])
