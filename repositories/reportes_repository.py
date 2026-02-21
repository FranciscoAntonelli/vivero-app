class ReportesRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def obtener_stock_por_producto(self, usuario_id):
        with self.conexion.cursor() as cur:
            cur.execute("""
                SELECT nombre, SUM(cantidad) AS total_stock
                FROM productos
                WHERE creado_por = %s
                GROUP BY nombre
                ORDER BY nombre
            """, (usuario_id,))
            return cur.fetchall()

    def obtener_ventas_mensuales(self, usuario_id):
        with self.conexion.cursor() as cur:
            cur.execute("""
                SELECT TO_CHAR(fecha, 'YYYY-MM') AS mes, SUM(total)
                FROM ventas
                WHERE id_usuario = %s
                GROUP BY mes
                ORDER BY mes
            """, (usuario_id,))
            return cur.fetchall()
        
    def obtener_reporte_diario(self, usuario_id, fecha_desde=None, fecha_hasta=None):
        query = """
            SELECT 
                DATE(fecha) AS dia,
                COUNT(*) AS cantidad,
                SUM(total) AS total
            FROM ventas
            WHERE id_usuario = %s
        """
        condiciones = []
        params = [usuario_id]


        if fecha_desde:
            condiciones.append("fecha >= %s")
            params.append(fecha_desde)
        if fecha_hasta:
            condiciones.append("fecha <= %s")
            params.append(fecha_hasta)

        if condiciones:
            query += " AND " + " AND ".join(condiciones)

        query += " GROUP BY dia ORDER BY dia"

        with self.conexion.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()


    def obtener_stock_por_categoria(self, usuario_id):
        with self.conexion.cursor() as cur:
            cur.execute("""
                SELECT c.nombre, SUM(p.cantidad) AS total_stock
                FROM productos p
                JOIN categorias c ON p.categoria_id = c.id_categoria
                WHERE p.creado_por = %s
                GROUP BY c.nombre
                ORDER BY c.nombre
            """, (usuario_id,))
            return cur.fetchall()
        

    def obtener_productos_mas_vendidos(self, usuario_id, top_n=10):
        query = """
            SELECT p.nombre, SUM(dv.cantidad_vendida) as total_vendido
            FROM detalle_ventas dv
            JOIN productos p ON dv.id_producto = p.id_producto
            JOIN ventas v ON dv.id_venta = v.id_venta
            WHERE v.id_usuario = %s
            GROUP BY p.nombre
            ORDER BY total_vendido DESC
            LIMIT %s
        """
        with self.conexion.cursor() as cursor:
            cursor.execute(query, (usuario_id, top_n))
            return cursor.fetchall() 