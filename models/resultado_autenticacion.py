class ResultadoAutenticacion:
    def __init__(self, exito, usuario=None, errores=None):
        self.exito = exito
        self.usuario = usuario
        self.errores = errores