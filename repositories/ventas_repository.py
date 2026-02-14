class VentasRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def mapear_a_venta(self, fila):
        return {
            "id_venta": fila[0],
            "fecha": fila[1],
            "total": fila[2]
        }
    
    def buscar_ventas(self, usuario_id, fecha_inicio=None, fecha_fin=None):
        query = """
            SELECT id_venta, fecha, total
            FROM ventas
            WHERE id_usuario = %s
        """
        parametros = [usuario_id]

        if fecha_inicio:
            query += " AND fecha >= %s"
            parametros.append(fecha_inicio)

        if fecha_fin:
            query += " AND fecha <= %s"
            parametros.append(fecha_fin)

        query += " ORDER BY fecha DESC"

        with self.conexion.cursor() as cursor:
            cursor.execute(query, parametros)
            filas = cursor.fetchall()

        return [self.mapear_a_venta(fila) for fila in filas]
    
    def registrar_venta(self, venta):
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO ventas (id_usuario, fecha, total)
                    VALUES (%s, %s, %s)
                    RETURNING id_venta
                """, (
                    venta.id_usuario,
                    venta.fecha,
                    venta.total
                ))
                id_venta = cursor.fetchone()[0]  # Obtener el ID generado
            self.conexion.commit()
            return id_venta
        except Exception:
            self.conexion.rollback()
            raise
