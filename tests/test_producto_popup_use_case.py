from unittest import TestCase
from unittest.mock import MagicMock, Mock
from models.resultado_guardado import ResultadoGuardado
from use_cases.productos.producto_popup_use_case import ProductoPopupUseCase
from models.producto import Producto

class TestProductoPopupUseCase(TestCase):

    def setUp(self):
        # Mocks de dependencias
        self.mock_validador = MagicMock()
        self.mock_saver = MagicMock()
        self.mock_categorias_service = MagicMock()

        # Instancia del caso de uso
        self.use_case = ProductoPopupUseCase(
            self.mock_validador,
            self.mock_saver,
            self.mock_categorias_service
        )

    def test_listar_categorias(self):
        # Arrange
        categorias = [("1", "Plantas"), ("2", "Macetas")]
        self.mock_categorias_service.listar_categorias.return_value = categorias

        # Act
        resultado = self.use_case.listar_categorias()

        # Assert
        self.assertEqual(resultado, categorias)
        self.mock_categorias_service.listar_categorias.assert_called_once()

    def test_guardar_producto_con_errores_devuelve_resultado_falso(self):
        # Arrange
        producto_dict = {"nombre": "", "precio_unitario": 500}
        errores = {"nombre": "El nombre es obligatorio"}
        self.mock_validador.validar.return_value = errores

        # Act
        resultado = self.use_case.guardar_producto(producto_dict)

        # Assert
        self.assertFalse(resultado.exito)
        self.assertEqual(resultado.errores, errores)
        self.mock_saver.guardar.assert_not_called()

    def test_guardar_producto_valido_llama_saver_y_retorna_exito(self):
        # Arrange
        producto_dict = {"nombre": "Ficus", "precio_unitario": 500}
        producto = Producto(
            id_producto=1,
            nombre="Ficus",
            categoria_id=1,
            ubicacion="Interior",
            medida="Grande",
            cantidad=10,
            precio_unitario=500,
            creado_por=1
        )

        self.mock_validador.validar.return_value = {}  # sin errores
        self.mock_saver.guardar.return_value = producto

        # Act
        resultado = self.use_case.guardar_producto(producto_dict)

        # Assert
        self.assertTrue(resultado.exito)
        self.assertIsInstance(resultado, ResultadoGuardado)
        self.assertEqual(resultado.producto, producto)
        self.mock_saver.guardar.assert_called_once_with(producto_dict, None)

    def test_guardar_producto_existente_actualiza_en_saver(self):
        # Arrange
        producto_dict = {"nombre": "Cactus", "precio_unitario": 200}
        producto_existente = Producto(
            id_producto=5,
            nombre="Cactus Viejo",
            categoria_id=2,
            ubicacion="Exterior",
            medida="Pequeña",
            cantidad=3,
            precio_unitario=150,
            creado_por=1
        )
        self.mock_validador.validar.return_value = {}
        self.mock_saver.guardar.return_value = producto_existente

        # Act
        resultado = self.use_case.guardar_producto(producto_dict, producto_existente)

        # Assert
        self.assertTrue(resultado.exito)
        self.mock_saver.guardar.assert_called_once_with(producto_dict, producto_existente)
