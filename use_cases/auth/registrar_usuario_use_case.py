from exceptions.usuario_ya_existe_error import UsuarioYaExisteError
from domain.models.resultado import Resultado
from use_cases.auth.iregistrar_usuario_use_case import IRegistrarUsuarioUseCase


class RegistrarUsuarioUseCase(IRegistrarUsuarioUseCase):
    def __init__(self, usuario_service, validador):
        self.usuario_service = usuario_service
        self.validador = validador

    def ejecutar(self, nombre_usuario, password, password_confirm):
        nombre_usuario = nombre_usuario.strip()
        password = password.strip()
        password_confirm = password_confirm.strip()

        data = {
            "usuario": nombre_usuario,
            "password": password,
            "password_confirm": password_confirm
        }

        errores = self.validador.validar(data)
        if errores:
            return Resultado(False, None, errores)
        
        try:
            self.usuario_service.registrar(nombre_usuario, password)
            return Resultado(True)

        except UsuarioYaExisteError:
            return Resultado(False, None, ["El nombre de usuario ya está en uso."])