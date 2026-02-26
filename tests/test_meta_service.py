import unittest
from unittest.mock import Mock
from services.meta_service import MetaService


class TestMetaService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = Mock()
        self.service = MetaService(self.mock_repo)

    def test_obtener_ultima_modificacion_existente(self):
        self.mock_repo.obtener_fecha_modificacion.return_value = "2025-10-13"

        resultado = self.service.obtener_ultima_modificacion("fran")

        self.assertEqual(resultado, "2025-10-13")
        self.mock_repo.obtener_fecha_modificacion.assert_called_once_with("fran")

    def test_obtener_ultima_modificacion_no_registrada(self):
        self.mock_repo.obtener_fecha_modificacion.return_value = None

        resultado = self.service.obtener_ultima_modificacion("fran")

        self.assertEqual(resultado, None)
        self.mock_repo.obtener_fecha_modificacion.assert_called_once_with("fran")

    def test_registrar_modificacion(self):
        self.service.registrar_modificacion("fran")

        self.mock_repo.actualizar_fecha_modificacion.assert_called_once_with("fran")