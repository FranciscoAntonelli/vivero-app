class CoordinadorValidaciones:
    def __init__(self, validadores):
        self.validadores = validadores

    def validar(self, data):
        errores = []
        for validador in self.validadores:
            errores.extend(validador.validar(data))
        return errores