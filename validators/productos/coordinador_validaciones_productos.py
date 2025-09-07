class CoordinadorValidaciones:
    def __init__(self, validadores):
        self.validadores = validadores
 
    def validar(self, producto):
        errores = []
        for validador in self.validadores:
            errores.extend(validador.validar(producto))
        return errores

