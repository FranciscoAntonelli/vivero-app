import unittest
from validators.login.validacion_campos_obligatorios import ValidacionCamposObligatorios

class TestValidacionCamposObligatorios(unittest.TestCase):
    def setUp(self):
        self.validador = ValidacionCamposObligatorios()

    def test_usuario_y_clave_correctos(self):
        errores = self.validador.validar("usuario", "clave123")
        self.assertEqual(errores, [])

    def test_usuario_vacio(self):
        errores = self.validador.validar("", "clave123")
        self.assertEqual(errores, ["El usuario no puede estar vacío."])

    def test_clave_vacia(self):
        errores = self.validador.validar("usuario", "")
        self.assertEqual(errores, ["La contraseña no puede estar vacía."])

    def test_usuario_y_clave_vacios(self):
        errores = self.validador.validar("", "")
        self.assertEqual(
            errores, 
            ["El usuario no puede estar vacío.", "La contraseña no puede estar vacía."]
        )

    def test_usuario_con_espacios(self):
        errores = self.validador.validar("   ", "clave123")
        self.assertEqual(errores, ["El usuario no puede estar vacío."])