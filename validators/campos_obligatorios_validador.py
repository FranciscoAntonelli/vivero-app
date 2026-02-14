from validators.validador import Validador

class CamposObligatoriosValidador(Validador):
    def __init__(self, campos_con_mensaje):
        self.campos = campos_con_mensaje

    def validar(self, data):
        errores = []
        for campo, mensaje in self.campos.items():
            valor = data.get(campo)
            if not valor.strip():
                errores.append(mensaje)
        return errores