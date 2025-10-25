from unittest import TestCase
from unittest.mock import MagicMock, Mock
from models.producto import Producto
from repositories.productos_repository import ProductosRepository

class TestProductosRepository(TestCase):

    def setUp(self):
        self.mock_conexion = MagicMock()
        self.mock_cursor = MagicMock()
        # Importante: simular el contexto del cursor
        self.mock_conexion.cursor.return_value.__enter__.return_value = self.mock_cursor
        self.mock_conexion.cursor.return_value.__exit__.return_value = None


    def test_buscar(self):
        self.mock_cursor.fetchall.return_value = [
            (1, "Planta Ficus", 1, "Invernadero", "Grande", 10, 500, 1)
        ]
        repo = ProductosRepository(self.mock_conexion)

        resultado = repo.buscar(nombre="Ficus", id_usuario=1)

        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].nombre, "Planta Ficus")
        self.mock_cursor.execute.assert_called_once()

    def test_eliminar(self):
        repo = ProductosRepository(self.mock_conexion)

        repo.eliminar(1)

        self.mock_cursor.execute.assert_called_once_with(
            "DELETE FROM productos WHERE id_producto = %s", (1,)
        )
        self.mock_conexion.commit.assert_called_once()

    def test_agregar(self):
        repo = ProductosRepository(self.mock_conexion)
        producto = Producto(
            id_producto=None,
            nombre="Planta Rosa",
            categoria_id=2,
            ubicacion="Exterior",
            medida="Mediana",
            cantidad=5,
            precio_unitario=300,
            creado_por=1
        )

        repo.agregar(producto)

        self.mock_cursor.execute.assert_called_once()
        self.mock_conexion.commit.assert_called_once()

    def test_editar(self):
        repo = ProductosRepository(self.mock_conexion)
        producto = Producto(
            id_producto=1,
            nombre="Planta Rosa",
            categoria_id=2,
            ubicacion="Exterior",
            medida="Mediana",
            cantidad=5,
            precio_unitario=300,
            creado_por=1
        )

        repo.editar(producto)

        self.mock_cursor.execute.assert_called_once()
        self.mock_conexion.commit.assert_called_once()

   