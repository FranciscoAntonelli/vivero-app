from models.categoria import Categoria


class CategoriasRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def obtener_todas(self):
        with self.conexion.cursor() as cursor:
            cursor.execute("SELECT id_categoria, nombre FROM categorias ORDER BY nombre")
            filas = cursor.fetchall()
            return [Categoria(id_categoria=fila[0], nombre=fila[1]) for fila in filas]