from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.uic import loadUi
from PyQt6.QtCore import pyqtSignal

class LoginWindow(QMainWindow):
    login_exitoso = pyqtSignal(object)

    def __init__(self, login_controller, on_login_success):
        super().__init__()
        self.inicializarUI(login_controller, on_login_success)

    def inicializarUI(self, login_controller, on_login_success):
        loadUi("ui/designer/login.ui", self)
        self.configurar()

        self.login_controller = login_controller
        self.on_login_success = on_login_success

        self.boton_login.clicked.connect(self.autenticar) 
        self.login_exitoso.connect(self.on_login_success)
        self.show()

    def configurar(self):
        self.setMinimumSize(self.geometry().width(), self.geometry().height())
        self.setMaximumSize(self.geometry().width(), self.geometry().height())
        
    def autenticar(self):
        usuario = self.usuario_input.text()
        clave = self.clave_input.text()

        usuario_obj, errores = self.login_controller.autenticar(usuario, clave)
        if errores:
            QMessageBox.warning(self, "Error de validación", "\n".join(errores))
            return

        self.login_exitoso.emit(usuario_obj)
        self.close()
            