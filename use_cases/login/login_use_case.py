from models.resultado_autenticacion import ResultadoAutenticacion


class LoginUseCase:
    def __init__(self, login_service, validador):
        self.login_service = login_service
        self.validador = validador

    def autenticar(self, usuario, clave):
        errores = self.validador.validar(usuario, clave)
        if errores:
            return ResultadoAutenticacion(exito=False, errores=errores)
        
        usuario_obj = self.login_service.verificar_credenciales(usuario, clave)
        if not usuario_obj:
            return ResultadoAutenticacion(exito=False, errores=["Usuario o contraseña incorrectos."])
        
        return ResultadoAutenticacion(exito=True, usuario=usuario_obj)