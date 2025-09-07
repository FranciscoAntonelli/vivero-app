from validators.login.validador_login_base import ValidadorLoginBase


class ValidacionCamposObligatorios(ValidadorLoginBase):
    def validar(self, usuario, clave):
        errores = []
        if not usuario or usuario.strip() == "":
            errores.append("El usuario no puede estar vacío.")
        if not clave or clave.strip() == "":
            errores.append("La contraseña no puede estar vacía.")
        return errores