import unittest
from unittest.mock import Mock
from services.productos_service import ProductosService


class TestProductosService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = Mock()
        self.service = ProductosService(self.mock_repo)

    # --- buscar ---
    def test_buscar_con_parametros(self):
        self.mock_repo.buscar.return_value = ["producto1", "producto2"]

        resultado = self.service.buscar(nombre="flor", id_usuario=1)

        self.mock_repo.buscar.assert_called_once_with("flor", 1)
        self.assertEqual(resultado, ["producto1", "producto2"])

    # --- eliminar ---
    def test_eliminar_producto(self):
        self.service.eliminar(10)
        self.mock_repo.eliminar.assert_called_once_with(10)

    # --- agregar ---
    def test_agregar_producto(self):
        producto_mock = Mock()
        self.service.agregar(producto_mock)
        self.mock_repo.agregar.assert_called_once_with(producto_mock)

    # --- editar ---
    def test_editar_producto(self):
        producto_mock = Mock()
        self.service.editar(producto_mock)
        self.mock_repo.editar.assert_called_once_with(producto_mock)
