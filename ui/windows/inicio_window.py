from PyQt6.QtWidgets import QMainWindow
from PyQt6.uic import loadUi
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt

class InicioWindow(QMainWindow):
    def __init__(self, productos_window, ventas_window, reportes_window, usuario, on_logout):
        super().__init__()
        loadUi("ui/designer/inicio.ui", self)

        self.productos_window = productos_window
        self.ventas_window = ventas_window
        self.reportes_window = reportes_window
        self.usuario = usuario
        self.on_logout = on_logout

        self._configurar_ventana()
        self._configurar_usuario()

        self.stack = self.stackedWidget

        self.idx_inicio = self.stack.currentIndex()
        self.idx_productos = self.stack.addWidget(self.productos_window)
        self.idx_ventas = self.stack.addWidget(self.ventas_window)
        self.idx_reportes = self.stack.addWidget(self.reportes_window)

        self.productos_window.volver_inicio.connect(self.ir_inicio)
        self.ventas_window.volver_inicio.connect(self.ir_inicio)
        self.reportes_window.volver_inicio.connect(self.ir_inicio)

        self.btn_productos.clicked.connect(self.ir_productos)
        self.btn_ventas.clicked.connect(self.ir_ventas)
        self.btn_reportes.clicked.connect(self.ir_reportes)
        self.btnCerrarSesion.clicked.connect(self.cerrar_sesion)

    # -------------------------
    #       CONFIGURACION

    def _configurar_ventana(self):
        self.resize(1100, 500)
        self.setMinimumSize(self.geometry().width(), self.geometry().height())
        self.setMaximumSize(self.geometry().width(), self.geometry().height())

    def _configurar_usuario(self):
        font = QFont("Arial", 12)
        font.setBold(True)

        self.labelUsuario.setFont(font) 
        self.labelUsuario.setText(f"{self.usuario.nombre_usuario}")

        # icono
        pixmap = QPixmap("resources/icons/user.png")
        pixmap = pixmap.scaled(
            40, 40,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.labelIconoUsuario.setPixmap(pixmap)

    # -------------------------
    #       FUNCIONALIDADES

    def ir_productos(self):
        self.productos_window.cargar_productos()
        self.stack.setCurrentIndex(self.idx_productos)
        self.setWindowTitle("Productos")

    def ir_ventas(self):
        self.stack.setCurrentIndex(self.idx_ventas)
        self.setWindowTitle("Ventas")
        self.ventas_window.cargar_ventas()

    def ir_reportes(self):
        self.stack.setCurrentIndex(self.idx_reportes)
        self.setWindowTitle("Reportes")
        self.reportes_window.cargar_reportes()

    def ir_inicio(self):
        self.stack.setCurrentIndex(self.idx_inicio)
        self.setWindowTitle("Inicio")

    def cerrar_sesion(self):
        self.close() # cierra la ventana
        self.on_logout() # llama a la funcion de logout