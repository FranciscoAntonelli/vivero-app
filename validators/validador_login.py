class ValidadorLogin:
    def __init__(self, min_longitud_usuario=3):
        self.min_longitud_usuario = min_longitud_usuario

    def validar(self, usuario, clave):
        errores = []

        if not usuario or not clave:
            errores.append("Debe ingresar usuario y contraseña.")
            return errores

        if len(usuario.strip()) < self.min_longitud_usuario:
            errores.append(f"El nombre de usuario debe tener al menos {self.min_longitud_usuario} caracteres.")

        return errores