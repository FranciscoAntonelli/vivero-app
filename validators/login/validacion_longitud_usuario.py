from validators.login.validador_login_base import ValidadorLoginBase


class ValidacionLongitudUsuario(ValidadorLoginBase):
    def __init__(self, min_longitud):
        self.min_longitud = min_longitud

    def validar(self, usuario, clave):
        errores = []
        if usuario and len(usuario.strip()) < self.min_longitud:
            errores.append(f"El nombre de usuario debe tener al menos {self.min_longitud} caracteres.")
        return errores