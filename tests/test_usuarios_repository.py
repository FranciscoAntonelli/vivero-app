from unittest import TestCase
from unittest.mock import Mock
from repositories.usuarios_repository import UsuarioRepository
from models.usuario import Usuario

class TestUsuarioRepository(TestCase):

    def setUp(self):
        # --- Mock de cursor y conexión ---
        self.mock_cursor = Mock()
        self.mock_conexion = Mock()
        # El repo usará self.mock_conexion.cursor() y devolverá self.mock_cursor
        self.mock_conexion.cursor.return_value = self.mock_cursor

        self.repo = UsuarioRepository(self.mock_conexion)

    def test_mapear_a_usuario_devuelve_none(self):
        fila = None
        usuario = self.repo.mapear_a_usuario(fila)
        assert usuario is None

    def test_mapear_a_usuario_devuelve_usuario(self):
        fila = (1, "usuario1", "clave123")
        usuario = self.repo.mapear_a_usuario(fila)
        assert isinstance(usuario, Usuario)
        assert usuario.id_usuario == 1
        assert usuario.nombre_usuario == "usuario1"
        assert usuario.clave == "clave123"

    def test_obtener_por_nombre_existente(self):
        # Hacemos que fetchone devuelva la tupla real
        self.mock_cursor.fetchone.return_value = (1, "usuario1", "clave123")
        usuario = self.repo.obtener_por_nombre("usuario1")
        assert isinstance(usuario, Usuario)
        assert usuario.id_usuario == 1
        assert usuario.nombre_usuario == "usuario1"
        assert usuario.clave == "clave123"
        self.mock_cursor.execute.assert_called_once_with(
            "SELECT id_usuario, nombre_usuario, contraseña FROM usuarios WHERE nombre_usuario = %s",
            ("usuario1",)
        )

    def test_obtener_por_nombre_inexistente(self):
        # fetchone devuelve None
        self.mock_cursor.fetchone.return_value = None
        usuario = self.repo.obtener_por_nombre("usuarioX")
        assert usuario is None
        self.mock_cursor.execute.assert_called_once_with(
            "SELECT id_usuario, nombre_usuario, contraseña FROM usuarios WHERE nombre_usuario = %s",
            ("usuarioX",)
        )