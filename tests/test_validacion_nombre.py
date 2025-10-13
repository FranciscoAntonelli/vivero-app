import unittest
from validators.productos.validacion_nombre import ValidacionNombre

class TestValidacionNombre(unittest.TestCase):
    def setUp(self):
        self.validador = ValidacionNombre()

    def test_nombre_vacio_devuelve_error(self):
        producto = {"nombre": ""}
        errores = self.validador.validar(producto)
        self.assertIn("El nombre no puede estar vacío.", errores)


    def test_nombre_valido_no_devuelve_error(self):
        producto = {"nombre": "Rosa"}
        errores = self.validador.validar(producto)
        self.assertEqual(errores, [])

    def test_nombre_con_espacios_solo_devuelve_error(self):
        producto = {"nombre": "     "}
        errores = self.validador.validar(producto)
        self.assertIn("El nombre no puede estar vacío.", errores)