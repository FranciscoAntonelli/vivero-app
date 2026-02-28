from exceptions.usuario_ya_existe_error import UsuarioYaExisteError
from domain.models.resultado import Resultado
from domain.models.usuario import Usuario
from use_cases.auth.iregistrar_usuario_use_case import IRegistrarUsuarioUseCase


class RegistrarUsuarioUseCase(IRegistrarUsuarioUseCase):
    def __init__(self, usuario_repository, password_hasher, validador):
        self.usuario_repository = usuario_repository
        self.password_hasher = password_hasher
        self.validador = validador

    def ejecutar(self, nombre_usuario, password, password_confirm):

        # Limpiar espacios en blanco
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
            password_hash = self.password_hasher.hash(password)
            usuario = Usuario(None, nombre_usuario, password_hash)
            self.usuario_repository.crear(usuario)
            return Resultado(True)

        except UsuarioYaExisteError:
            return Resultado(
                False,
                None,
                ["El nombre de usuario ya está en uso."]
            )