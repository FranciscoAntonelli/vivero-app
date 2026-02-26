import unittest
from unittest.mock import Mock
from use_cases.auth.registrar_usuario_use_case import RegistrarUsuarioUseCase
from models.resultado import Resultado
from models.usuario import Usuario
from exceptions.usuario_ya_existe_error import UsuarioYaExisteError


class TestRegistrarUsuarioUseCase(unittest.TestCase):
    def setUp(self):
        self.mock_usuario_repository = Mock()
        self.mock_password_hasher = Mock()
        self.mock_validador = Mock()
        self.use_case = RegistrarUsuarioUseCase(
            self.mock_usuario_repository,
            self.mock_password_hasher,
            self.mock_validador
        )

    def test_registro_exitoso_devuelve_resultado_valido(self):
        # Arrange
        nombre_usuario = "juan"
        password = "123456"
        password_confirm = "123456"
        hashed_password = "hashed123"
        self.mock_validador.validar.return_value = []
        self.mock_password_hasher.hash.return_value = hashed_password
        self.mock_usuario_repository.crear.return_value = None  # No exception

        # Act
        resultado = self.use_case.ejecutar(nombre_usuario, password, password_confirm)

        # Assert
        self.assertIsInstance(resultado, Resultado)
        self.assertTrue(resultado.exito)
        self.mock_validador.validar.assert_called_once_with({
            "usuario": nombre_usuario,
            "password": password,
            "password_confirm": password_confirm
        })
        self.mock_password_hasher.hash.assert_called_once_with(password)
        self.mock_usuario_repository.crear.assert_called_once()
        created_usuario = self.mock_usuario_repository.crear.call_args[0][0]
        self.assertIsInstance(created_usuario, Usuario)
        self.assertEqual(created_usuario.nombre_usuario, nombre_usuario)
        self.assertEqual(created_usuario.clave, hashed_password)

    def test_registro_fallido_lanza_excepcion_si_falla(self):
        # Arrange
        nombre_usuario = "juan"
        password = "123"
        password_confirm = "123"
        self.mock_validador.validar.return_value = ["Usuario o contraseña incorrecta"]

        # Act
        resultado = self.use_case.ejecutar(nombre_usuario, password, password_confirm)

        # Assert
        self.assertIsInstance(resultado, Resultado)
        self.assertFalse(resultado.exito)
        self.assertIn("Usuario o contraseña incorrecta", resultado.errores)
        self.mock_password_hasher.hash.assert_not_called()
        self.mock_usuario_repository.crear.assert_not_called()

    def test_registro_fallido_usuario_ya_existe(self):
        # Arrange
        nombre_usuario = "juan"
        password = "123456"
        password_confirm = "123456"
        self.mock_validador.validar.return_value = []
        self.mock_password_hasher.hash.return_value = "hashed"
        self.mock_usuario_repository.crear.side_effect = UsuarioYaExisteError()

        # Act
        resultado = self.use_case.ejecutar(nombre_usuario, password, password_confirm)

        # Assert
        self.assertIsInstance(resultado, Resultado)
        self.assertFalse(resultado.exito)
        self.assertIn("El nombre de usuario ya está en uso.", resultado.errores)