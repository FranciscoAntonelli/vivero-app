from validators.validador import Validador


class RangoFechasValidador(Validador):
  
    def validar(self, fecha_inicio, fecha_fin):
        if fecha_inicio is None or fecha_fin is None:
            return None  # no se validan si alguna de las fechas es None, se asume que no se filtrará por fecha

        if fecha_fin < fecha_inicio:
            return "La fecha final no puede ser menor a la fecha inicial."
        return None