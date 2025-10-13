from unittest import TestCase
from unittest.mock import Mock
from services.categorias_service import CategoriasService
from models.categoria import Categoria

class TestCategoriasService(TestCase):

    def setUp(self):
        # Mock del repo que vamos a inyectar en el service
        self.mock_repo = Mock()
        self.service = CategoriasService(self.mock_repo)

    def test_listar_categorias(self):
        # Configuramos el mock para que devuelva una lista de categorías
        self.mock_repo.obtener_todas.return_value = [
            Categoria(id_categoria=1, nombre="Plantas"),
            Categoria(id_categoria=2, nombre="Macetas")
        ]

        resultado = self.service.listar_categorias()

        assert len(resultado) == 2
        assert resultado[0].nombre == "Plantas"
        assert resultado[1].nombre == "Macetas"
        self.mock_repo.obtener_todas.assert_called_once()

    def test_obtener_nombre_por_id_existente(self):
        self.mock_repo.obtener_por_id.return_value = Categoria(id_categoria=1, nombre="Plantas")

        nombre = self.service.obtener_nombre_por_id(1)

        assert nombre == "Plantas"
        self.mock_repo.obtener_por_id.assert_called_once_with(1)

    def test_obtener_nombre_por_id_inexistente(self):
        self.mock_repo.obtener_por_id.return_value = None

        nombre = self.service.obtener_nombre_por_id(99)

        assert nombre == ""
        self.mock_repo.obtener_por_id.assert_called_once_with(99)