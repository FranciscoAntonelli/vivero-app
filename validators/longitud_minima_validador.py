from validators.validador import Validador


class LongitudMinimaValidador(Validador):
    def __init__(self, campo, minimo):
        self.campo = campo
        self.minimo = minimo

    def validar(self, data):
        valor = data.get(self.campo)
        if valor and len(valor) < self.minimo:
            return [f"La contraseña debe tener al menos {self.minimo} caracteres."]
        return []