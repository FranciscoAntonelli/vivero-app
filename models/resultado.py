class Resultado:
    def __init__(self, exito, valor=None, errores=None):
        self.exito = exito
        self.valor = valor
        self.errores = errores

    @property
    def fallo(self):
        return not self.exito