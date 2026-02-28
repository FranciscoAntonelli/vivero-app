from domain.models.categoria import Categoria


class CategoriasRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def obtener_todas(self):
        with self.conexion.cursor() as cursor:
            cursor.execute("SELECT id_categoria, nombre FROM categorias ORDER BY nombre")
            filas = cursor.fetchall()
            return [self.mapear_a_categoria(fila) for fila in filas]

    def mapear_a_categoria(self, fila):
        return Categoria(id_categoria=fila[0], nombre=fila[1])
    
    def obtener_por_id(self, id_categoria):
        with self.conexion.cursor() as cursor:
            cursor.execute(
                "SELECT id_categoria, nombre FROM categorias WHERE id_categoria = %s",
                (id_categoria,)
            )
            fila = cursor.fetchone()
            if fila:
                return self.mapear_a_categoria(fila)
            return None