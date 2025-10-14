from models.producto import Producto
from models.resultado_guardado import ResultadoGuardado


class ProductoPopupUseCase:
    """coordina la validacion y el saver del producto."""
    def __init__(self, coordinador_validaciones, saver, categorias_service):
        self.coordinador_validaciones = coordinador_validaciones
        self.saver = saver
        self.categorias_service = categorias_service

    def listar_categorias(self):
        return self.categorias_service.listar_categorias()
    
    def guardar_producto(self, producto_dict, producto_existente=None):
        errores = self.coordinador_validaciones.validar(producto_dict)
        if errores:
            return ResultadoGuardado(exito=False, errores=errores)
        
        producto = self.saver.guardar(producto_dict, producto_existente)
        return ResultadoGuardado(exito=True, producto=producto)