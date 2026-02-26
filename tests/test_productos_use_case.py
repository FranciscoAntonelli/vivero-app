import unittest
from unittest.mock import Mock
from use_cases.productos.productos_use_case import ProductosUseCase
from models.producto import Producto


class TestProductosUseCase(unittest.TestCase):
    def setUp(self):
        self.mock_service = Mock()
        self.use_case = ProductosUseCase(self.mock_service)
        self.producto = Producto(
            id_producto=1,
            nombre="Producto 1",
            categoria_id=2,
            ubicacion="Estante 1",
            medida="Unidad",
            cantidad=5,
            precio_unitario=100.0,
            creado_por=1
        )

  
    def test_obtener_productos_devuelve_lista(self):
        self.mock_service.buscar.return_value = [self.producto]

        resultado = self.use_case.obtener_productos(id_usuario=1)

        self.mock_service.buscar.assert_called_once_with(None, 1)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].nombre, "Producto 1")

    def test_eliminar_producto_llama_service(self):
        self.use_case.eliminar_producto(5)
        self.mock_service.eliminar.assert_called_once_with(5)

    def test_eliminar_producto_lanza_excepcion_si_falla(self):
        self.mock_service.eliminar.side_effect = Exception("DB Error")

        with self.assertRaises(Exception) as context:
            self.use_case.eliminar_producto(5)

        self.assertIn("No se pudo eliminar el producto", str(context.exception))