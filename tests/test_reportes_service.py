import unittest
from unittest.mock import Mock
from services.reportes_service import ReportesService


class TestReportesService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = Mock()
        self.service = ReportesService(self.mock_repo)

    def test_obtener_reporte_diario_sin_filtros(self):
        # Arrange
        usuario_id = 1
        expected_data = [
            ('2023-01-01', 5, 100.50),
            ('2023-01-02', 3, 75.25)
        ]
        self.mock_repo.obtener_reporte_diario.return_value = expected_data

        # Act
        result = self.service.obtener_reporte_diario(usuario_id)

        # Assert
        self.mock_repo.obtener_reporte_diario.assert_called_once_with(usuario_id, None, None)
        self.assertEqual(result, expected_data)
        self.assertIsInstance(result, list)
        for item in result:
            self.assertIsInstance(item, tuple)
            self.assertEqual(len(item), 3)  # dia, cantidad, total

    def test_obtener_reporte_diario_con_filtros_fecha(self):
        # Arrange
        usuario_id = 1
        fecha_desde = '2023-01-01'
        fecha_hasta = '2023-01-31'
        expected_data = [
            ('2023-01-15', 2, 50.00)
        ]
        self.mock_repo.obtener_reporte_diario.return_value = expected_data

        # Act
        result = self.service.obtener_reporte_diario(usuario_id, fecha_desde, fecha_hasta)

        # Assert
        self.mock_repo.obtener_reporte_diario.assert_called_once_with(usuario_id, fecha_desde, fecha_hasta)
        self.assertEqual(result, expected_data)
        self.assertIsInstance(result, list)
        for item in result:
            self.assertIsInstance(item, tuple)
            self.assertEqual(len(item), 3)

    def test_obtener_stock_por_categoria(self):
        # Arrange
        usuario_id = 1
        expected_data = [
            ('Flores', 150),
            ('Plantas', 200),
            ('Herramientas', 50)
        ]
        self.mock_repo.obtener_stock_por_categoria.return_value = expected_data

        # Act
        result = self.service.obtener_stock_por_categoria(usuario_id)

        # Assert
        self.mock_repo.obtener_stock_por_categoria.assert_called_once_with(usuario_id)
        self.assertEqual(result, expected_data)
        self.assertIsInstance(result, list)
        for item in result:
            self.assertIsInstance(item, tuple)
            self.assertEqual(len(item), 2)  # nombre_categoria, total_stock
            self.assertIsInstance(item[0], str)
            self.assertIsInstance(item[1], int)

    def test_obtener_stock_por_producto(self):
        # Arrange
        usuario_id = 1
        expected_data = [
            ('Rosa Roja', 50),
            ('Tulipán Amarillo', 30),
            ('Maceta Grande', 20)
        ]
        self.mock_repo.obtener_stock_por_producto.return_value = expected_data

        # Act
        result = self.service.obtener_stock_por_producto(usuario_id)

        # Assert
        self.mock_repo.obtener_stock_por_producto.assert_called_once_with(usuario_id)
        self.assertEqual(result, expected_data)
        self.assertIsInstance(result, list)
        for item in result:
            self.assertIsInstance(item, tuple)
            self.assertEqual(len(item), 2)  # nombre_producto, total_stock
            self.assertIsInstance(item[0], str)
            self.assertIsInstance(item[1], int)

    def test_obtener_ventas_mensuales(self):
        # Arrange
        usuario_id = 1
        expected_data = [
            ('2023-01', 500.00),
            ('2023-02', 750.50),
            ('2023-03', 600.25)
        ]
        self.mock_repo.obtener_ventas_mensuales.return_value = expected_data

        # Act
        result = self.service.obtener_ventas_mensuales(usuario_id)

        # Assert
        self.mock_repo.obtener_ventas_mensuales.assert_called_once_with(usuario_id)
        self.assertEqual(result, expected_data)
        self.assertIsInstance(result, list)
        for item in result:
            self.assertIsInstance(item, tuple)
            self.assertEqual(len(item), 2)  # mes, total
            self.assertIsInstance(item[0], str)
            self.assertIsInstance(item[1], float)