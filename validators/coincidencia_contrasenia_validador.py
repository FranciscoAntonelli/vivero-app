from validators.validador import Validador


class CoincidenciaContraseniaValidador(Validador):
    def validar(self, data):
        if data.get("password") != data.get("password_confirm"):
            return ["Las contraseñas no coinciden."]
        return []