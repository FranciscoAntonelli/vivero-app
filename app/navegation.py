from ui.windows.productos_window import ProductosWindow
from ui.windows.ventas_window import VentasWindow
from ui.windows.login_window import LoginWindow

class Navigation:

    def __init__(self, app, container):
        self.app = app
        self.container = container

    def show_login(self):
        self.app.login = LoginWindow(
            self.container["login_use_case"],
            self.container["registrar_usuario_use_case"],
            on_login_success=self.start_app
        )

    def start_app(self, usuario):
        productos_window = ProductosWindow(
            self.container["productos_use_case"],
            self.container["categorias_use_case"],
            self.container["productos_meta_use_case"],
            self.container["imprimir_productos_use_case"],
            self.container["producto_popup_use_case"],
            usuario
        )

        ventas_window = VentasWindow(
            self.container["venta_use_case"],
            self.container["productos_use_case"],
            usuario
        )
