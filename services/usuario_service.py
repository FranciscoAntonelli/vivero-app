from exceptions.usuario_ya_existe_error import UsuarioYaExisteError
from domain.models.usuario import Usuario


class UsuarioService:
    def __init__(self, usuario_repository, password_hasher):
        self.usuario_repository = usuario_repository
        self.password_hasher = password_hasher

    def registrar(self, nombre_usuario, password):
        if self.usuario_repository.obtener_por_nombre(nombre_usuario):
            raise UsuarioYaExisteError()

        password_hash = self.password_hasher.hash(password)
        usuario = Usuario(None, nombre_usuario, password_hash)
        self.usuario_repository.crear(usuario)

        return usuario