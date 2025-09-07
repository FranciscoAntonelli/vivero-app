from validators.productos.validacion_producto import IValidacionProducto


class ValidacionCategoria(IValidacionProducto):
    def __init__(self, categorias):
        self.categorias = categorias

    def validar(self, producto_data):
        errores = []
        categoria = producto_data.get("categoria")
        categoria_id = None
        if categoria is None or categoria == "":
            categoria_id = None
        elif isinstance(categoria, int):
            if not any(c.id_categoria == categoria for c in self.categorias):
                errores.append("ID de categoría inválido.")
            else:
                categoria_id = categoria
        else:
            errores.append("Formato de categoría inválido.")

        producto_data["categoria_id"] = categoria_id
        return errores