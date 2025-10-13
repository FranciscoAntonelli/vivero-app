import unittest
from validators.login.validacion_longitud_usuario import ValidacionLongitudUsuario

class TestValidacionLongitudUsuario(unittest.TestCase):
    def setUp(self):
        self.min_longitud = 5
        self.validador = ValidacionLongitudUsuario(self.min_longitud)

    def test_usuario_suficiente_longitud(self):
        errores = self.validador.validar("usuario", "clave123")
        self.assertEqual(errores, [])

    def test_usuario_corto(self):
        errores = self.validador.validar("usr", "clave123")
        self.assertEqual(
            errores,
            [f"El nombre de usuario debe tener al menos {self.min_longitud} caracteres."]
        )

    def test_usuario_espacios(self):
        errores = self.validador.validar("   usr  ", "clave123")
        self.assertEqual(
            errores,
            [f"El nombre de usuario debe tener al menos {self.min_longitud} caracteres."]
        )