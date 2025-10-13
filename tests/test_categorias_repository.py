from unittest import TestCase
from unittest.mock import MagicMock
from models.categoria import Categoria
from repositories.categorias_repository import CategoriasRepository

class TestCategoriasRepository(TestCase):

    def setUp(self):
        # --- Mocks de conexión y cursor con soporte para 'with' ---
        self.mock_cursor = MagicMock()
        self.mock_conexion = MagicMock()
        # Configuro el cursor para usar el context manager
        self.mock_conexion.cursor.return_value.__enter__.return_value = self.mock_cursor
        self.mock_conexion.cursor.return_value.__exit__.return_value = None

        # Repositorio a testear
        self.repo = CategoriasRepository(self.mock_conexion)

    def test_obtener_todas(self):
        self.mock_cursor.fetchall.return_value = [
            (1, "Plantas"),
            (2, "Macetas")
        ]

        categorias = self.repo.obtener_todas()

        assert len(categorias) == 2
        assert categorias[0].id_categoria == 1
        assert categorias[0].nombre == "Plantas"
        assert categorias[1].id_categoria == 2
        assert categorias[1].nombre == "Macetas"
        self.mock_cursor.execute.assert_called_once_with(
            "SELECT id_categoria, nombre FROM categorias ORDER BY nombre"
        )

    def test_mapear_a_categoria(self):
        fila = (5, "Suculentas")
        categoria = self.repo.mapear_a_categoria(fila)

        assert isinstance(categoria, Categoria)
        assert categoria.id_categoria == 5
        assert categoria.nombre == "Suculentas"

    def test_obtener_por_id_existente(self):
        self.mock_cursor.fetchone.return_value = (3, "Orquídeas")

        categoria = self.repo.obtener_por_id(3)

        assert isinstance(categoria, Categoria)
        assert categoria.id_categoria == 3
        assert categoria.nombre == "Orquídeas"
        self.mock_cursor.execute.assert_called_once_with(
            "SELECT id_categoria, nombre FROM categorias WHERE id_categoria = %s",
            (3,)
        )

    def test_obtener_por_id_inexistente(self):
        self.mock_cursor.fetchone.return_value = None

        categoria = self.repo.obtener_por_id(99)

        assert categoria is None
        self.mock_cursor.execute.assert_called_once_with(
            "SELECT id_categoria, nombre FROM categorias WHERE id_categoria = %s",
            (99,)
        )