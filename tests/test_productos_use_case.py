import unittest
from unittest.mock import Mock
from use_cases.productos.productos_use_case import ProductosUseCase
from models.producto import Producto


class TestProductosUseCase(unittest.TestCase):
    def setUp(self):
        self.mock_service = Mock()
        self.mock_categorias_service = Mock()
        self.mock_meta_service = Mock()
        self.mock_validador = Mock()
        self.mock_impresora = Mock()

        self.use_case = ProductosUseCase(
            self.mock_service,
            self.mock_categorias_service,
            self.mock_meta_service,
            self.mock_validador,
            self.mock_impresora
        )

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

    # --- TESTS ---

    def test_obtener_productos_devuelve_lista(self):
        self.mock_service.buscar.return_value = [self.producto]

        resultado = self.use_case.obtener_productos(id_usuario=1)

        self.mock_service.buscar.assert_called_once_with(None, 1)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].nombre, "Producto 1")

    def test_obtener_nombre_categoria(self):
        self.mock_categorias_service.obtener_nombre_por_id.return_value = "Plantas"

        nombre = self.use_case.obtener_nombre_categoria(2)

        self.mock_categorias_service.obtener_nombre_por_id.assert_called_once_with(2)
        self.assertEqual(nombre, "Plantas")

    def test_registrar_modificacion(self):
        self.use_case.registrar_modificacion(1)
        self.mock_meta_service.registrar_modificacion.assert_called_once_with(1)

    def test_obtener_ultima_modificacion(self):
        self.mock_meta_service.obtener_ultima_modificacion.return_value = "2025-10-10 12:00"

        fecha = self.use_case.obtener_ultima_modificacion(1)

        self.mock_meta_service.obtener_ultima_modificacion.assert_called_once_with(1)
        self.assertEqual(fecha, "2025-10-10 12:00")

    def test_eliminar_producto_llama_service(self):
        self.use_case.eliminar_producto(5)
        self.mock_service.eliminar.assert_called_once_with(5)

    def test_eliminar_producto_lanza_excepcion_si_falla(self):
        self.mock_service.eliminar.side_effect = Exception("DB Error")

        with self.assertRaises(Exception) as context:
            self.use_case.eliminar_producto(5)

        self.assertIn("No se pudo eliminar el producto", str(context.exception))

    def test_imprimir_llama_a_impresora(self):
        productos = [self.producto]
        ventana = Mock()

        self.use_case.imprimir(productos, ventana)

        self.mock_impresora.imprimir.assert_called_once_with(productos, ventana)

    def test_agregar_producto_valida_y_agrega(self):
        self.mock_service.existe_producto.return_value = False

        self.use_case.agregar_producto(self.producto)

        self.mock_service.existe_producto.assert_called_once()
        self.mock_service.agregar.assert_called_once_with(self.producto)

    def test_agregar_producto_lanza_excepcion_si_duplicado(self):
        self.mock_service.existe_producto.return_value = True

        with self.assertRaises(Exception) as context:
            self.use_case.agregar_producto(self.producto)

        self.assertIn("Ya existe un producto", str(context.exception))
        self.mock_service.agregar.assert_not_called()

    def test_editar_producto_valida_y_edita(self):
        self.mock_service.existe_producto.return_value = False

        self.use_case.editar_producto(self.producto)

        self.mock_service.existe_producto.assert_called_once()
        self.mock_service.editar.assert_called_once_with(self.producto)

    def test_editar_producto_lanza_excepcion_si_duplicado(self):
        self.mock_service.existe_producto.return_value = True

        with self.assertRaises(Exception):
            self.use_case.editar_producto(self.producto)

        self.mock_service.editar.assert_not_called()
