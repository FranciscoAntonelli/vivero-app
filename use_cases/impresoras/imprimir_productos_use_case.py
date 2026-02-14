from use_cases.impresoras.iimprimir_productos_use_case import IImprimirProductosUseCase


class ImprimirProductosUseCase(IImprimirProductosUseCase):
    def __init__(self, impresora):
        self.impresora = impresora

    def ejecutar(self, datos):
        self.impresora.imprimir(datos)