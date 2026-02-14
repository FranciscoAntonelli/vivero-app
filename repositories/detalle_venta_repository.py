from models.detalle_venta import DetalleVenta


class DetalleVentaRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def mapear_a_detalle_venta(self, fila):
        print(fila)
        return DetalleVenta(
            id_detalle=fila[0],
            id_venta=fila[1],
            id_producto=fila[2],
            cantidad=fila[3],
            subtotal=fila[4]
        )

    def buscar_detalles_por_venta(self, id_venta):
        query = "SELECT id_detalle, id_venta, id_producto, cantidad_vendida, subtotal FROM detalle_ventas WHERE id_venta = %s"
        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (id_venta,))
            filas = cursor.fetchall()
        return [self.mapear_a_detalle_venta(fila) for fila in filas]

    def agregar_detalle_venta(self, detalle_venta):
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO detalle_ventas (id_venta, id_producto, cantidad_vendida, subtotal)
                    VALUES (%s, %s, %s, %s)
                """, (
                    detalle_venta.id_venta,
                    detalle_venta.id_producto,
                    detalle_venta.cantidad,
                    detalle_venta.subtotal
                ))
            self.db_connection.commit()
        except Exception:
            self.db_connection.rollback()
            raise

