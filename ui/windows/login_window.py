from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.uic import loadUi
from PyQt6.QtCore import pyqtSignal

class LoginWindow(QMainWindow):
    login_exitoso = pyqtSignal(object)

    def __init__(self, login_service, validador_login, on_login_success):
        super().__init__()
        loadUi("ui/designer/login.ui", self)
        self.configurar()

        self.login_service = login_service
        self.validador_login = validador_login
        self.on_login_success = on_login_success

        self.boton_login.clicked.connect(self.autenticar) 
        self.login_exitoso.connect(self.on_login_success)

    def configurar(self):
        print(self.geometry())
        self.setMinimumSize(self.geometry().width(), self.geometry().height())
        self.setMaximumSize(self.geometry().width(), self.geometry().height())
        
    def autenticar(self):
        usuario = self.usuario_input.text()
        clave = self.clave_input.text()

        errores = self.validador_login.validar(usuario, clave)
        if errores:
            QMessageBox.warning(self, "Error de validación", "\n".join(errores))
            return

        try:
            usuario_obj = self.login_service.verificar_credenciales(usuario, clave)
            if not usuario_obj:
                QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos.")
                return
            self.login_exitoso.emit(usuario_obj)
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", "Error al conectar con el servicio, intente más tarde.")
            