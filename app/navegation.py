from ui.windows.productos_window import ProductosWindow
from ui.windows.ventas_window import VentasWindow
from ui.windows.login_window import LoginWindow
from ui.windows.reportes_window import ReportesWindow
from ui.windows.inicio_window import InicioWindow

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

        reportes_window = ReportesWindow(
            self.container["reportes_use_case"],
            self.container["imprimir_reportes_use_case"],
            usuario,
            self.container["grafico_renderer"]   
        )

        self.app.inicio_window = InicioWindow(
            productos_window,
            ventas_window,
            reportes_window,
            usuario,
            on_logout=self.show_login
        )

        self.app.inicio_window.show()
