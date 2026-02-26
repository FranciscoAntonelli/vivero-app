import unittest
from unittest.mock import Mock
from services.login_service import LoginService
from models.usuario import Usuario


class TestLoginService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = Mock()
        self.mock_hasher = Mock()
        self.service = LoginService(self.mock_repo, self.mock_hasher)

    def test_verificar_credenciales_correctas(self):
        usuario = Usuario(id_usuario=1, nombre_usuario="fran", clave="HASH_GUARDADO")
        self.mock_repo.obtener_por_nombre.return_value = usuario
        self.mock_hasher.verificar.return_value = True

        resultado = self.service.verificar_credenciales("fran", "1234")

        self.assertEqual(resultado, usuario)
        self.mock_repo.obtener_por_nombre.assert_called_once_with("fran")
        self.mock_hasher.verificar.assert_called_once_with("1234", "HASH_GUARDADO")

    def test_verificar_credenciales_incorrectas(self):
        usuario = Usuario(id_usuario=1, nombre_usuario="fran", clave="HASH_GUARDADO")
        self.mock_repo.obtener_por_nombre.return_value = usuario
        self.mock_hasher.verificar.return_value = False

        resultado = self.service.verificar_credenciales("fran", "9999")

        self.assertIsNone(resultado)
        self.mock_hasher.verificar.assert_called_once_with("9999", "HASH_GUARDADO")

    def test_verificar_credenciales_usuario_no_existe(self):
        self.mock_repo.obtener_por_nombre.return_value = None

        resultado = self.service.verificar_credenciales("fran", "1234")

        self.assertIsNone(resultado)
        self.mock_hasher.verify.assert_not_called()