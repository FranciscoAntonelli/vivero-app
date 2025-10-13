import unittest
from unittest.mock import Mock
from validators.login.coordinador_validaciones_login import CoordinadorValidacionesLogin

class TestCoordinadorValidacionesLogin(unittest.TestCase):
    def setUp(self):
        # Creamos mock de validadores
        self.validador1 = Mock()
        self.validador2 = Mock()
        self.coordinador = CoordinadorValidacionesLogin([self.validador1, self.validador2])

    def test_validar_con_errores(self):
        self.validador1.validar.return_value = ["error1"]
        self.validador2.validar.return_value = ["error2"]

        resultado = self.coordinador.validar("usuario", "clave")

        self.validador1.validar.assert_called_once_with("usuario", "clave")
        self.validador2.validar.assert_called_once_with("usuario", "clave")
        self.assertEqual(resultado, ["error1", "error2"])

    def test_validar_sin_errores(self):
        self.validador1.validar.return_value = []
        self.validador2.validar.return_value = []

        resultado = self.coordinador.validar("usuario", "clave")

        self.assertEqual(resultado, [])