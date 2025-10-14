class ResultadoGuardado:
    def __init__(self, exito, producto=None, errores=None):
        self.exito = exito
        self.producto = producto
        self.errores = errores