from models.producto import Producto


class ValidadorProducto:
    def __init__(self, categorias, ubicaciones_validas):
        self.categorias_dict = {c.nombre: c.id_categoria for c in categorias}
        self.categorias_validas = list(self.categorias_dict.keys())
        self.ubicaciones_validas = ubicaciones_validas


    def validar(self, nombre, categoria, ubicacion, cantidad_text, precio_text, medida=None, creado_por=None, id_producto=None):
        errores = []

        if not nombre:
            errores.append("El nombre no puede estar vacío.")

        if categoria and categoria not in self.categorias_dict:
            errores.append(f"La categoría debe ser una de: {', '.join(self.categorias_validas)} o dejarla vacía.")

        if ubicacion and ubicacion not in self.ubicaciones_validas:
            errores.append(f"La ubicación debe ser una de: {', '.join(self.ubicaciones_validas)}")

        try:
            cantidad = int(cantidad_text)
            if cantidad <= 0:
                errores.append("La cantidad debe ser mayor que cero.")
        except ValueError:
            errores.append("La cantidad debe ser un número entero válido.")
            cantidad = None

        try:
            precio = float(precio_text)
            if precio <= 0:
                errores.append("El precio debe ser mayor que cero.")
        except:
            errores.append("El precio debe ser un número decimal válido.")
            precio = None

        if medida:
            if len(medida.strip()) > 30:
                errores.append("La medida es demasiado larga.")

        if errores:
            return errores, None
        
        categoria_id = self.categorias_dict.get(categoria)
        
        producto = Producto(
            id_producto=id_producto,
            nombre=nombre,
            categoria_id=categoria_id,  
            ubicacion=ubicacion,
            medida=medida,
            cantidad=cantidad,
            precio_unitario=precio,
            creado_por=creado_por
        )

        return [], producto

