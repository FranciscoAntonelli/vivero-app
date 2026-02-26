from PyQt6.QtWidgets import QMainWindow, QMessageBox, QLineEdit
from PyQt6.uic import loadUi
from PyQt6.QtCore import pyqtSignal
from ui.popups.registrar_usuario_popup import RegistrarUsuarioPopup

class LoginWindow(QMainWindow):
    login_exitoso = pyqtSignal(object)

    def __init__(self, login_use_case, registrar_usuario_use_case, on_login_success):
        super().__init__()
        self.inicializar_ui(login_use_case, registrar_usuario_use_case, on_login_success)

    def inicializar_ui(self, login_use_case, registrar_usuario_use_case, on_login_success):
        self.login_use_case = login_use_case
        self.registrar_usuario_use_case = registrar_usuario_use_case
        self.on_login_success = on_login_success

        self._cargar_ui()
        self._configurar_ventana()
        self._conectar_signales()
        self._mostrar()

    def _cargar_ui(self):
        loadUi("ui/designer/login.ui", self)

    def _configurar_ventana(self):
        self.setMinimumSize(self.geometry().width(), self.geometry().height())
        self.setMaximumSize(self.geometry().width(), self.geometry().height())
        

    def _conectar_signales(self):
        self.boton_login.clicked.connect(self.autenticar)
        self.login_exitoso.connect(self.on_login_success)
        self.checkbox_mostrar_clave.stateChanged.connect(
            self.mostrar_clave
        )
        self.boton_registrarse.clicked.connect(self.abrir_registro)

    def abrir_registro(self):
        dialog = RegistrarUsuarioPopup(self.registrar_usuario_use_case, self)
        dialog.exec()

    def mostrar_clave(self, estado):
        if estado:  # checkbox tildado
            self.clave_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:       # checkbox destildado
            self.clave_input.setEchoMode(QLineEdit.EchoMode.Password)

    def _mostrar(self):
        self.show()
        
    def autenticar(self):
        usuario, clave = self.obtener_credenciales()
        resultado = self.login_use_case.autenticar(usuario, clave)
        self.procesar_resultado_autenticacion(resultado)

    def obtener_credenciales(self):
        """Devuelve los datos ingresados por el usuario."""
        return self.usuario_input.text(), self.clave_input.text()
            
    def procesar_resultado_autenticacion(self, resultado):
        """muestra errores o cierra la ventana."""
        if not resultado.exito:
            self.mostrar_errores(resultado.errores)
            return

        self.login_exitoso.emit(resultado.valor)
        self.close()

    def mostrar_errores(self, errores):
        """Muestra los errores de validacion."""
        QMessageBox.warning(self, "Error de validación", "\n".join(errores))