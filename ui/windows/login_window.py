from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.uic import loadUi
from PyQt6.QtCore import pyqtSignal, QObject

class LoginWindow(QMainWindow):
    login_exitoso = pyqtSignal(object)

    def __init__(self, login_service, on_login_success):
        super().__init__()
        loadUi("ui/designer/login.ui", self)
        self.configurar()

        self.login_service = login_service
        self.on_login_success = on_login_success

        # Conectar botón de login a la función autenticar
        self.boton_login.clicked.connect(self.autenticar) 

        # Conectar la señal al callback externo
        self.login_exitoso.connect(self.on_login_success)

    def configurar(self):
        print(self.geometry())
        self.setMinimumSize(self.geometry().width(), self.geometry().height())
        self.setMaximumSize(self.geometry().width(), self.geometry().height())
        
    def autenticar(self):
        usuario = self.usuario_input.text()
        clave = self.clave_input.text()

        if not usuario or not clave:
            QMessageBox.warning(self, "Error", "Por favor, ingrese usuario y contraseña.")
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
            