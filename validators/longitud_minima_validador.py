from validators.validador import Validador


class LongitudMinimaValidador(Validador):
    def __init__(self, campo, minimo, nombre_mostrable=None):
        self.campo = campo
        self.minimo = minimo
        self.nombre_mostrable = nombre_mostrable or campo

    def validar(self, data):
        valor = data.get(self.campo)
        if valor and len(valor) < self.minimo:
            return [f"{self.nombre_mostrable} debe tener al menos {self.minimo} caracteres."]
        return []