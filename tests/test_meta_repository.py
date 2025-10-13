from unittest import TestCase
from unittest.mock import Mock
from datetime import datetime
from repositories.meta_repository import MetaRepository
from models.producto_meta import ProductoMeta


class TestMetaRepository(TestCase):

    def setUp(self):
        # Mock de cursor y conexión
        self.mock_cursor = Mock()
        self.mock_conexion = Mock()
        self.mock_conexion.cursor.return_value = self.mock_cursor

        self.repo = MetaRepository(self.mock_conexion)

    def test_obtener_fecha_modificacion_existente(self):
        fecha = datetime(2025, 10, 10, 12, 0, 0)
        self.mock_cursor.fetchone.return_value = (fecha,)

        resultado = self.repo.obtener_fecha_modificacion(1)

        assert resultado == fecha
        self.mock_cursor.execute.assert_called_once_with("""
                       SELECT ultima_modificacion
                       FROM productos_meta
                       WHERE usuario_id = %s
                    """, (1,))

    def test_obtener_fecha_modificacion_inexistente(self):
        self.mock_cursor.fetchone.return_value = None

        resultado = self.repo.obtener_fecha_modificacion(99)

        assert resultado is None

    def test_actualizar_fecha_modificacion(self):
        self.repo.actualizar_fecha_modificacion(2)

        self.mock_cursor.execute.assert_called_once_with("""
            INSERT INTO productos_meta (usuario_id, ultima_modificacion)
            VALUES (%s, NOW())
            ON CONFLICT (usuario_id) DO UPDATE
            SET ultima_modificacion = EXCLUDED.ultima_modificacion
        """, (2,))

    def test_mapear_a_producto_meta(self):
        fecha = datetime(2025, 10, 10, 18, 0, 0)
        fila = (7, fecha)

        meta = self.repo.mapear_a_producto_meta(fila)

        assert isinstance(meta, ProductoMeta)
        assert meta.usuario_id == 7
        assert meta.ultima_modificacion == fecha

    def test_obtener_meta_existente(self):
        fecha = datetime(2025, 10, 10, 15, 30, 0)
        self.mock_cursor.fetchone.return_value = (3, fecha)

        resultado = self.repo.obtener_meta(3)

        assert isinstance(resultado, ProductoMeta)
        assert resultado.usuario_id == 3
        assert resultado.ultima_modificacion == fecha

    def test_obtener_meta_inexistente(self):
        self.mock_cursor.fetchone.return_value = None

        resultado = self.repo.obtener_meta(99)

        assert resultado is None