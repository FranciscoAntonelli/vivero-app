import unittest
from validators.productos.validacion_medida import ValidacionMedida

class TestValidacionMedida(unittest.TestCase):
    def setUp(self):
        self.validador = ValidacionMedida()

    def test_medida_demasiado_larga_devuelve_error(self):
        producto = {"medida": "x" * 31}
        errores = self.validador.validar(producto)
        self.assertIn("La medida es demasiado larga.", errores)

    def test_medida_valida_no_devuelve_error(self):
        producto = {"medida": "kg"}
        errores = self.validador.validar(producto)
        self.assertEqual(errores, [])

    def test_medida_vacia_no_devuelve_error(self):
        producto = {"medida": ""}
        errores = self.validador.validar(producto)
        self.assertEqual(errores, [])
