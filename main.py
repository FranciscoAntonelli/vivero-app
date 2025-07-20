from db.db import get_connection
from PyQt6.QtWidgets import QApplication
import sys

from repositories.productos_repository import ProductosRepository
from repositories.categorias_repository import CategoriasRepository
from repositories.usuario_repository import UsuarioRepository

from services.productos_service import ProductosService
from services.login_service import LoginService
from services.categorias_service import CategoriasService

from ui.windows.productos_window import ProductosWindow
from ui.windows.login_window import LoginWindow

from validators.validador_producto import ValidadorProducto
from validators.validador_login import ValidadorLogin

from models.ubicacion import Ubicacion

def iniciar_aplicacion(usuario_logeado):
    ventana = ProductosWindow(productos_service, categorias_service, usuario_logeado, validador_producto)
    ventana.show()
    app.productos_window = ventana

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

# ==================== Inicio ====================
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # DB
    conexion = get_connection()
    crear_usuario_por_defecto(conexion)
    crear_usuario_prueba(conexion)
    
    # Repositories
    productos_repo = ProductosRepository(conexion)
    usuario_repo = UsuarioRepository(conexion)
    categorias_repo = CategoriasRepository(conexion)

    # Services
    productos_service = ProductosService(productos_repo)
    login_service = LoginService(usuario_repo)
    categorias_service = CategoriasService(categorias_repo)

    # Validadores
    categorias = categorias_service.listar_categorias()  # Objetos de categoria
    ubicaciones_validas = [u.value for u in Ubicacion]
    validador_producto = ValidadorProducto(categorias, ubicaciones_validas)
    validador_login = ValidadorLogin()

    # Login UI
    login = LoginWindow(login_service, validador_login, lambda usuario: iniciar_aplicacion(usuario))
    login.show()
   
    # Arranca y termina el Qt
    sys.exit(app.exec())