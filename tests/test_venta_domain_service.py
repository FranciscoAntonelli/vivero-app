from unittest.mock import Mock
from services.venta_domain_service import VentaDomainService
from models.venta import Venta

class TestVentaDomainService:
    def setup_method(self):
        self.mock_ventas_service = Mock()
        self.mock_detalle_service = Mock()
        self.mock_productos_service = Mock()
        self.domain_service = VentaDomainService(
            self.mock_ventas_service,
            self.mock_detalle_service,
            self.mock_productos_service
        )

    def test_procesar_venta_actualiza_stock_correctamente(self):
        # Arrange
        mock_venta = Venta(id_usuario=1, total=50.0)
        mock_carrito = Mock()
        mock_carrito.items = [
            Mock(producto=Mock(id_producto=1), cantidad=2, subtotal=20.0),
            Mock(producto=Mock(id_producto=2), cantidad=1, subtotal=30.0)
        ]
        self.mock_ventas_service.agregar.return_value = 123

        # Act
        resultado = self.domain_service.procesar_venta(mock_venta, mock_carrito)

        # Assert
        self.mock_ventas_service.agregar.assert_called_once_with(mock_venta)

        # Verificar que se agregaron los detalles de venta
        assert self.mock_detalle_service.agregar.call_count == 2

        llamadas = self.mock_detalle_service.agregar.call_args_list

        detalle_1 = llamadas[0][0][0]
        detalle_2 = llamadas[1][0][0]

        assert detalle_1.id_venta == 123
        assert detalle_1.id_producto == 1
        assert detalle_1.cantidad == 2
        assert detalle_1.subtotal == 20.0

        assert detalle_2.id_venta == 123
        assert detalle_2.id_producto == 2
        assert detalle_2.cantidad == 1
        assert detalle_2.subtotal == 30.0

        # Verificar que se actualizó el stock de los productos
        self.mock_productos_service.descontar_stock.assert_any_call(1, 2)
        self.mock_productos_service.descontar_stock.assert_any_call(2, 1)

        assert resultado == 123