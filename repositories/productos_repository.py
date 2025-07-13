from models.producto import Producto

class ProductosRepository:

    def __init__(self, conexion):
        self.conexion = conexion

    def buscar(self, nombre="", id_usuario=None):
        productos = []
        with self.conexion.cursor() as cursor:
            columnas = "id_producto, nombre, categoria, ubicacion, medida, cantidad, precio_unitario, creado_por"

            condiciones = ["creado_por = %s"]
            parametros = [id_usuario]

            if nombre:
                condiciones.append("nombre ILIKE %s")
                parametros.append(f"%{nombre}%")

            where_clause = " AND ".join(condiciones)
            
            cursor.execute(
                f"""SELECT {columnas} 
                    FROM productos 
                    WHERE {where_clause} 
                    ORDER BY nombre""",
                tuple(parametros)
            )

            for fila in cursor.fetchall():
                producto = Producto(
                    id_producto=fila[0],
                    nombre=fila[1],
                    categoria=fila[2],
                    ubicacion=fila[3],
                    medida=fila[4],
                    cantidad=fila[5],
                    precio_unitario=fila[6],
                    creado_por=fila[7]
                )
                productos.append(producto)

            return productos
    

    def eliminar(self, id_producto):
        with self.conexion.cursor() as cursor:
            cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id_producto,))
            self.conexion.commit()

    def agregar(self, producto):
        with self.conexion.cursor() as cursor:
            cursor.execute("""
                INSERT INTO productos (nombre, ubicacion, medida, cantidad, categoria, precio_unitario, creado_por)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                producto.nombre,
                producto.ubicacion,
                producto.medida,
                producto.cantidad,
                producto.categoria,
                producto.precio_unitario,
                producto.creado_por
            ))
        self.conexion.commit()


    def editar(self, producto):
        try:
            with self.conexion.cursor() as cursor:
                consulta = """
                    UPDATE productos
                    SET nombre = %s,
                        categoria = %s,
                        ubicacion = %s,
                        medida = %s,
                        cantidad = %s,
                        precio_unitario = %s
                    WHERE id_producto = %s
                """
                valores = (
                    producto.nombre,
                    producto.categoria,
                    producto.ubicacion,
                    producto.medida, 
                    producto.cantidad,
                    producto.precio_unitario,
                    producto.id_producto
                )
                cursor.execute(consulta, valores)
                self.conexion.commit()
        except Exception as e:
            self.conexion.rollback()
            raise Exception(f"No se pudo editar el producto: {e}")

    def obtener_nombre_por_id(self, id_producto):
        with self.conexion.cursor() as cursor:
            cursor.execute("SELECT nombre FROM productos WHERE id_producto = %s", (id_producto,))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else "Desconocido"
        
    def existe_producto(self, nombre, ubicacion, id_excluir=None):
        cursor = self.conexion.cursor()
        if id_excluir:
            cursor.execute(
                "SELECT COUNT(*) FROM productos WHERE nombre = %s AND ubicacion = %s AND id_producto != %s",
                (nombre, ubicacion, id_excluir)
            )
        else:
            cursor.execute(
                "SELECT COUNT(*) FROM productos WHERE nombre = %s AND ubicacion = %s",
                (nombre, ubicacion)
            )
        return cursor.fetchone()[0] > 0