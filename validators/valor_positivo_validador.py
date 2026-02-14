from validators.validador import Validador

class ValorPositivoValidador(Validador):
    def __init__(self, campo, mensaje=None):
        self.campo = campo
        self.mensaje = mensaje or f"El campo '{campo}' debe ser mayor a cero."

    def validar(self, data):
        errores = []
        valor = data.get(self.campo)
        if valor <= 0:
            errores.append(self.mensaje)
        return errores