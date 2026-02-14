from validators.validador import Validador

class LongitudMaximaValidador(Validador):
    def __init__(self, campo, maximo):
        self.campo = campo
        self.maximo = maximo

    def validar(self, data):
        valor = data.get(self.campo)
        if valor and len(valor.strip()) > self.maximo:
            return [f"El campo '{self.campo}' es demasiado largo."]
        return []