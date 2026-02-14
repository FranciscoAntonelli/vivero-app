from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.uic import loadUi


class RegistrarUsuarioPopup(QDialog):

    def __init__(self, registrar_usuario_use_case, parent=None):
        super().__init__(parent)
        loadUi("ui/designer/registrar_usuario.ui", self)

        self.registrar_usuario_use_case = registrar_usuario_use_case

        self.btnRegistrar.clicked.connect(self._registrar)
        self.btnCancelar.clicked.connect(self.reject)

    def _registrar(self):
        try:
            resultado = self.registrar_usuario_use_case.ejecutar(
                nombre_usuario=self.inputUsuario.text(),
                password=self.inputPassword.text(),
                password_confirm=self.inputConfirmar.text()
            )

            if resultado.exito:
                QMessageBox.information(self, "Éxito", "Usuario registrado correctamente")
                self.accept()
            else:
                errores_str = "\n".join(resultado.errores)
                QMessageBox.warning(self, "Validación", errores_str)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
