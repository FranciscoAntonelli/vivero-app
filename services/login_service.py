class LoginService:
    def __init__(self, usuario_repository, password_hasher):
        self.usuario_repository = usuario_repository
        self.password_hasher = password_hasher


    def verificar_credenciales(self, nombre_usuario, clave):
        usuario = self.usuario_repository.obtener_por_nombre(nombre_usuario)
        if not usuario:
            return None
        
        if self.password_hasher.verificar(clave, usuario.clave):
            return usuario
        
        return None
    