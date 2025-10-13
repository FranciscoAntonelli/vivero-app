import unittest
from unittest.mock import Mock
from services.login_service import LoginService
from models.usuario import Usuario


class TestLoginService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = Mock()
        self.service = LoginService(self.mock_repo)

    def test_verificar_credenciales_correctas(self):
        usuario = Usuario(id_usuario=1, nombre_usuario="fran", clave="1234")
        self.mock_repo.obtener_por_nombre.return_value = usuario

        resultado = self.service.verificar_credenciales("fran", "1234")

        self.assertEqual(resultado, usuario)
        self.mock_repo.obtener_por_nombre.assert_called_once_with("fran")

    def test_verificar_credenciales_incorrectas(self):
        usuario = Usuario(id_usuario=1, nombre_usuario="fran", clave="1234")
        self.mock_repo.obtener_por_nombre.return_value = usuario

        resultado = self.service.verificar_credenciales("fran", "9999")

        self.assertIsNone(resultado)
        self.mock_repo.obtener_por_nombre.assert_called_once_with("fran")

    def test_usuario_inexistente(self):
        self.mock_repo.obtener_por_nombre.return_value = None

        resultado = self.service.verificar_credenciales("no_existe", "1234")

        self.assertIsNone(resultado)
        self.mock_repo.obtener_por_nombre.assert_called_once_with("no_existe")