import unittest
from unittest.mock import Mock
from use_cases.auth.registrar_usuario_use_case import RegistrarUsuarioUseCase
from domain.models.resultado import Resultado
from domain.models.usuario import Usuario
from exceptions.usuario_ya_existe_error import UsuarioYaExisteError


class TestRegistrarUsuarioUseCase(unittest.TestCase):
    def setUp(self):
        self.mock_login_service = Mock()
        self.mock_validador = Mock()

        self.use_case = RegistrarUsuarioUseCase(
            self.mock_login_service,
            self.mock_validador
        )

    def test_registro_exitoso_devuelve_resultado_valido(self):
        nombre_usuario = "juan"
        password = "123456"
        password_confirm = "123456"

        self.mock_validador.validar.return_value = []
        self.mock_login_service.registrar.return_value = None

        resultado = self.use_case.ejecutar(nombre_usuario, password, password_confirm)

        self.assertTrue(resultado.exito)

        self.mock_validador.validar.assert_called_once()
        self.mock_login_service.registrar.assert_called_once_with(
            nombre_usuario.strip(),
            password.strip()
        )

    def test_registro_fallido_lanza_excepcion_si_falla(self):
        nombre_usuario = "juan"
        password = "123"
        password_confirm = "123"
        self.mock_validador.validar.return_value = ["Usuario o contraseña incorrecta"]

        resultado = self.use_case.ejecutar(nombre_usuario, password, password_confirm)

        self.assertIsInstance(resultado, Resultado)
        self.assertFalse(resultado.exito)
        self.assertIn("Usuario o contraseña incorrecta", resultado.errores)

    def test_registro_fallido_usuario_ya_existe(self):
        nombre_usuario = "juan"
        password = "123456"
        password_confirm = "123456"
        self.mock_validador.validar.return_value = []
        self.mock_login_service.registrar.side_effect = UsuarioYaExisteError()

        resultado = self.use_case.ejecutar(nombre_usuario, password, password_confirm)

        self.assertIsInstance(resultado, Resultado)
        self.assertFalse(resultado.exito)
        self.assertIn("El nombre de usuario ya está en uso.", resultado.errores)