class LoginService:
    def __init__(self, usuario_repository):
        self.usuario_repository = usuario_repository


    def verificar_credenciales(self, nombre_usuario, clave):
        usuario = self.usuario_repository.obtener_por_nombre(nombre_usuario)
        if usuario and usuario.clave == clave:
            return usuario  
        return False
