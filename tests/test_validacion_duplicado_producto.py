import unittest
from unittest.mock import Mock
from validators.productos.validacion_duplicado_producto import ValidadorDuplicadoProducto


class TestValidadorDuplicadoProducto(unittest.TestCase):
    def setUp(self):
        self.mock_service = Mock()
        self.validador = ValidadorDuplicadoProducto(self.mock_service)

    def test_producto_duplicado_devuelve_error(self):
        self.mock_service.existe_producto.return_value = True
        producto_data = {
            "nombre": "Planta",
            "ubicacion": "Estante A",
            "medida": "Maceta chica",
            "id_producto": 1
        }

        errores = self.validador.validar(producto_data)

        self.mock_service.existe_producto.assert_called_once_with(
            "Planta", "Estante A", "Maceta chica", id_excluir=1
        )
        self.assertIn("Ya existe un producto con ese nombre y ubicación.", errores)

    def test_producto_no_duplicado_no_devuelve_errores(self):
        self.mock_service.existe_producto.return_value = False
        producto_data = {
            "nombre": "Planta nueva",
            "ubicacion": "Estante B",
            "medida": "Maceta grande"
        }

        errores = self.validador.validar(producto_data)

        self.mock_service.existe_producto.assert_called_once_with(
            "Planta nueva", "Estante B", "Maceta grande", id_excluir=None
        )
        self.assertEqual(errores, [])