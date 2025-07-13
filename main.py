from db.db import get_connection
from PyQt6.QtWidgets import QApplication
import sys
from services.login_service import LoginService
from ui.windows.login_window import LoginWindow
from repositories.productos_repository import ProductosRepository
from services.productos_service import ProductosService
from ui.windows.productos_window import ProductosWindow
from repositories.usuario_repository import UsuarioRepository

app = QApplication(sys.argv)

def iniciar_aplicacion(usuario_logeado, conexion):
    print(f"Bienvenido, {usuario_logeado.nombre_usuario}")

    productos_repo = ProductosRepository(conexion)  
    productos_service = ProductosService(productos_repo)

    productos_window = ProductosWindow(productos_service, usuario_logeado)
    productos_window.show()

    app.productos_window = productos_window

def crear_usuario_por_defecto(conexion):
    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    cantidad = cursor.fetchone()[0]
    if cantidad == 0:
        cursor.execute(
            "INSERT INTO usuarios (nombre_usuario, contraseña) VALUES (%s, %s)",
            ('admin', 'admin123')
        )
        conexion.commit()

def crear_usuario_prueba(conexion):
    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*) FROM usuarios WHERE nombre_usuario = %s", ('usuario2',))
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO usuarios (nombre_usuario, contraseña) VALUES (%s, %s)",
            ('usuario2', 'clave456')
        )
        conexion.commit()

if __name__ == "__main__":
    conexion = get_connection()
    crear_usuario_por_defecto(conexion)
    crear_usuario_prueba(conexion)
    
    usuario_repo = UsuarioRepository(conexion)
    login_service = LoginService(usuario_repo)

    login = LoginWindow(login_service, lambda usuario: iniciar_aplicacion(usuario, conexion))
    login.show()
   
    sys.exit(app.exec())