from models.categoria import Categoria


class CategoriasRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def obtener_nombres(self):
        with self.conexion.cursor() as cursor:
            cursor.execute("SELECT nombre FROM categorias ORDER BY nombre")
            return [fila[0] for fila in cursor.fetchall()]
        
    def existe_categoria(self, nombre_categoria):
        with self.conexion.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM categorias WHERE nombre = %s", (nombre_categoria,))
            return cursor.fetchone()[0] > 0
        
    def agregar_categoria(self, nombre_categoria):
        with self.conexion.cursor() as cursor:
            cursor.execute("INSERT INTO categorias (nombre) VALUES (%s)", (nombre_categoria,))
        self.conexion.commit()

    def obtener_todas(self):
        with self.conexion.cursor() as cursor:
            cursor.execute("SELECT id_categoria, nombre FROM categorias ORDER BY nombre")
            filas = cursor.fetchall()
            return [Categoria(id_categoria=fila[0], nombre=fila[1]) for fila in filas]