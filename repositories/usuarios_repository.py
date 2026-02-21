from models.usuario import Usuario
from psycopg import errors
from exceptions.usuario_ya_existe_error import UsuarioYaExisteError

class UsuarioRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def obtener_por_nombre(self, nombre_usuario):
        cursor = self.conexion.cursor()
        cursor.execute(
            "SELECT id_usuario, nombre_usuario, contraseña FROM usuarios WHERE nombre_usuario = %s",
            (nombre_usuario,)
        )
        fila = cursor.fetchone()
        return self.mapear_a_usuario(fila)  # devuelvo Usuario o None

    def mapear_a_usuario(self, fila):
        if fila is None:
            return None
        return Usuario(id_usuario=fila[0], nombre_usuario=fila[1], clave=fila[2])
    

    def crear(self, usuario):
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO usuarios (nombre_usuario, contraseña)
                    VALUES (%s, %s)
                    """,
                (usuario.nombre_usuario, usuario.clave)
            )
            self.conexion.commit()
        except errors.UniqueViolation:
            self.conexion.rollback()
            raise UsuarioYaExisteError("El nombre de usuario ya está en uso.")
        
        except Exception:
            self.conexion.rollback()
            raise