from abc import ABC, abstractmethod


class IImprimirReportesUseCase(ABC):

    @abstractmethod
    def ejecutar(self, usuario_id, fecha_desde=None, fecha_hasta=None):
        pass