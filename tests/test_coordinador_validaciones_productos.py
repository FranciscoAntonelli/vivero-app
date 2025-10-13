import unittest
from unittest.mock import Mock
from validators.productos.coordinador_validaciones_productos import CoordinadorValidaciones

class TestCoordinadorValidaciones(unittest.TestCase):
    def setUp(self):
        self.validador1 = Mock()
        self.validador2 = Mock()
        self.coordinador = CoordinadorValidaciones([self.validador1, self.validador2])

    def test_validar_sin_errores(self):
        self.validador1.validar.return_value = []
        self.validador2.validar.return_value = []

        errores = self.coordinador.validar("producto")

        self.validador1.validar.assert_called_once_with("producto")
        self.validador2.validar.assert_called_once_with("producto")
        self.assertEqual(errores, [])

    def test_validar_con_errores(self):
        self.validador1.validar.return_value = ["error1"]
        self.validador2.validar.return_value = ["error2"]

        errores = self.coordinador.validar("producto")

        self.assertEqual(errores, ["error1", "error2"])