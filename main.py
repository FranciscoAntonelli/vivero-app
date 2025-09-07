from controllers.login_controller import LoginController
from db.db import get_connection
from PyQt6.QtWidgets import QApplication
import sys

from repositories.productos_repository import ProductosRepository
from repositories.categorias_repository import CategoriasRepository
from repositories.usuarios_repository import UsuarioRepository
from repositories.meta_repository import MetaRepository

from services.productos_service import ProductosService
from services.login_service import LoginService
from services.categorias_service import CategoriasService
from services.meta_service import MetaService

from ui.windows.productos_window import ProductosWindow
from ui.windows.login_window import LoginWindow

from validators.login.coordinador_validaciones_login import CoordinadorValidacionesLogin
from validators.login.validacion_campos_obligatorios import ValidacionCamposObligatorios
from validators.login.validacion_longitud_usuario import ValidacionLongitudUsuario
from validators.productos.coordinador_validaciones_productos import CoordinadorValidaciones
from validators.productos.validacion_nombre import ValidacionNombre
from validators.productos.validacion_categoria import ValidacionCategoria
from validators.productos.validacion_ubicacion import ValidacionUbicacion
from validators.productos.validacion_cantidad import ValidacionCantidad
from validators.productos.validacion_precio import ValidacionPrecio
from validators.productos.validacion_medida import ValidacionMedida


from controllers.productos_controller import ProductosController

from models.ubicacion import Ubicacion

from utils.impresion.impresora_productos import ImpresoraProductos

def iniciar_aplicacion(usuario_logeado):
    ventana = ProductosWindow(
        productos_controller,
        usuario_logeado
    )
    app.productos_window = ventana

# ==================== Inicio ====================
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # DB
    conexion = get_connection()
    
    # Repositories
    productos_repo = ProductosRepository(conexion)
    usuario_repo = UsuarioRepository(conexion)
    categorias_repo = CategoriasRepository(conexion)
    productos_meta_repo = MetaRepository(conexion)

    # Services
    productos_service = ProductosService(productos_repo)
    login_service = LoginService(usuario_repo)
    categorias_service = CategoriasService(categorias_repo)
    productos_meta_service = MetaService(productos_meta_repo)

    # Validadores
    categorias = categorias_service.listar_categorias()  # Objetos de categoria
    ubicaciones_validas = [u.value for u in Ubicacion]

    validador_login = CoordinadorValidacionesLogin([
        ValidacionCamposObligatorios(),
        ValidacionLongitudUsuario(3)
    ])

    validadores = [
        ValidacionNombre(),
        ValidacionCategoria(categorias),
        ValidacionUbicacion(ubicaciones_validas),
        ValidacionCantidad(),
        ValidacionPrecio(),
        ValidacionMedida()
    ]
    validador_producto = CoordinadorValidaciones(validadores)

    impresora = ImpresoraProductos()

    # Controllers
    login_controller = LoginController(login_service, validador_login)
    productos_controller = ProductosController(
        productos_service,
        categorias_service,
        productos_meta_service,
        validador_producto,
        impresora  
    )

    # Login UI
    login = LoginWindow(
        login_controller,
        on_login_success=lambda usuario: iniciar_aplicacion(usuario)
    )
   
    # Arranca y termina el Qt
    sys.exit(app.exec())