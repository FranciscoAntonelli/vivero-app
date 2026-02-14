from exceptions.usuario_ya_existe_error import UsuarioYaExisteError
from models.resultado_registrar_usuario import ResultadoRegistroUsuario
from models.usuario import Usuario
from use_cases.auth.iregistrar_usuario_use_case import IRegistrarUsuarioUseCase


class RegistrarUsuarioUseCase(IRegistrarUsuarioUseCase):
    def __init__(self, usuario_repository, password_hasher, validador):
        self.usuario_repository = usuario_repository
        self.password_hasher = password_hasher
        self.validador = validador

    def ejecutar(self, nombre_usuario, password, password_confirm):
        data = {
            "usuario": nombre_usuario,
            "password": password,
            "password_confirm": password_confirm
        }

        errores = self.validador.validar(data)
        if errores:
            return ResultadoRegistroUsuario(False, errores)
        
        try:
            password_hash = self.password_hasher.hash(password)
            usuario = Usuario(None, nombre_usuario, password_hash)
            self.usuario_repository.crear(usuario)
            return ResultadoRegistroUsuario(True)

        except UsuarioYaExisteError:
            return ResultadoRegistroUsuario(
                False,
                ["El nombre de usuario ya está en uso."]
            )