from models.resultado_guardado import ResultadoGuardado
from exceptions.error_violacion_unica import ErrorViolacionUnica
from use_cases.productos.iproducto_popup_use_case import IProductoPopupUseCase


class ProductoPopupUseCase(IProductoPopupUseCase):
    """coordina la validacion, el saver y el service del producto."""
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

        try:
            producto = self.saver.guardar(producto_dict, producto_existente)

        except ErrorViolacionUnica: 
            return ResultadoGuardado(
                exito=False,
                errores=["Ya existe un producto con el mismo nombre, medida y ubicación."]
            ) 
        except Exception as e:
            return ResultadoGuardado(
                exito=False,
                errores=[f"Ocurrió un error inesperado al guardar el producto: {e}"]
            )

        return ResultadoGuardado(exito=True, producto=producto)