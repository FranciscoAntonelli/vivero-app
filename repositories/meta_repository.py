from models.producto_meta import ProductoMeta

class MetaRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def obtener_fecha_modificacion(self, usuario_id):
        cursor = self.conexion.cursor()
        cursor.execute("""
                       SELECT ultima_modificacion
                       FROM productos_meta
                       WHERE usuario_id = %s
                    """, (usuario_id,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None
    
    def actualizar_fecha_modificacion(self, usuario_id):
        cursor = self.conexion.cursor()
        cursor.execute("""
            INSERT INTO productos_meta (usuario_id, ultima_modificacion)
            VALUES (%s, NOW())
            ON CONFLICT (usuario_id) DO UPDATE
            SET ultima_modificacion = EXCLUDED.ultima_modificacion
        """, (usuario_id,))

    def obtener_meta(self, usuario_id):
        cursor = self.conexion.cursor()
        cursor.execute("""
            SELECT usuario_id, ultima_modificacion
            FROM productos_meta
            WHERE usuario_id = %s
        """, (usuario_id,))
        resultado = cursor.fetchone()
        return ProductoMeta(*resultado) if resultado else None