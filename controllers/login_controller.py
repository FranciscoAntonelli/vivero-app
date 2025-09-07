class LoginController:
    def __init__(self, login_service, validador):
        self.login_service = login_service
        self.validador = validador

    def autenticar(self, usuario, clave):
        # Validaciones
        errores = self.validador.validar(usuario, clave)
        if errores:
            return None, errores
        
        # Verifico credenciales
        usuario_obj = self.login_service.verificar_credenciales(usuario, clave)
        if not usuario_obj:
            return None, ["Usuario o contraseña incorrectos."]

        return usuario_obj, []