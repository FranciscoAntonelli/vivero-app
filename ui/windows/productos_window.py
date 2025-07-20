from PyQt6.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt6 import QtCore
from PyQt6.uic import loadUi
    
class ProductosWindow(QMainWindow):
    def __init__(self, productos_service, categorias_service, usuario_logeado, validador):
        super().__init__()
        loadUi("ui/designer/productos.ui", self)
        self.service = productos_service
        self.categorias_service = categorias_service
        self.usuario_logeado = usuario_logeado
        self.validador = validador

        self.configurar()
        self.cargar_categorias()
        
        self.btnAgregar.clicked.connect(self.agregar_producto)
        self.btnEliminar.clicked.connect(self.eliminar_producto)
        self.btnEditar.clicked.connect(self.editar_producto)
        
        self.buscarProducto.textChanged.connect(self.buscar_producto)

        self.cargar_productos()

    def configurar(self):
        self.tabla_productos.verticalHeader().setVisible(False)
        self.tabla_productos.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        print(self.geometry())
        
        self.setMinimumSize(self.geometry().width(), self.geometry().height())
        self.setMaximumSize(self.geometry().width(), self.geometry().height())
        

    def cargar_productos(self):
        try:
            productos = self.service.buscar(id_usuario=self.usuario_logeado.id_usuario)
            self.poblar_tabla(productos)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al cargar productos: {e}")

    def cargar_categorias(self):
        self.inputCategoria.clear()
        self.inputCategoria.addItem("")
        categorias = self.categorias_service.listar_categorias()
        for categoria in categorias:
            self.inputCategoria.addItem(categoria.nombre, categoria.id_categoria)


    def limpiar_campos(self):
        self.inputNombre.clear()
        self.inputUbicacion.setCurrentIndex(0)
        self.inputCantidad.clear()
        self.inputPrecio.clear()
        self.inputCategoria.setCurrentIndex(0)
        self.inputMedida.clear()

    def restaurar_tabla_y_limpiar(self):
        self.cargar_productos()
        self.limpiar_campos()

    def agregar_producto(self):
        nombre = self.inputNombre.text().strip()
        categoria = self.inputCategoria.currentText()
        ubicacion = self.inputUbicacion.currentText().strip() or None
        medida_texto = self.inputMedida.text().strip()
        medida = medida_texto if medida_texto and medida_texto.lower() != "none" else None
        cantidad_text = self.inputCantidad.text().strip()
        precio_text = self.inputPrecio.text().strip()

        errores, producto = self.validador.validar(
            nombre=nombre,
            categoria=categoria,
            ubicacion=ubicacion,
            cantidad_text=cantidad_text,
            precio_text=precio_text,
            medida=medida,
            creado_por=self.usuario_logeado.id_usuario,
            id_producto=None 
        )

        if errores:
            QMessageBox.warning(self, "Error", "\n".join(errores))
            return

        if self.service.existe_producto(nombre, ubicacion, medida):
            QMessageBox.warning(self, "Error", "Ya existe un producto con ese nombre, ubicación y medida.")
            return

        try:
            self.service.agregar(producto)
            QMessageBox.information(self, "Éxito", "Producto agregado correctamente.")
            self.restaurar_tabla_y_limpiar()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {str(e)}")


    def editar_producto(self):
        fila = self.tabla_productos.currentRow()
        if fila == -1:
            QMessageBox.warning(self, "Error", "Seleccioná una fila para editar.")
            return

        id_producto = int(self.tabla_productos.item(fila, 0).text())
        nombre = self.tabla_productos.item(fila, 1).text().strip()
        categoria = self.tabla_productos.item(fila, 2).text().strip()
        ubicacion = self.tabla_productos.item(fila, 3).text().strip() or None
        medida_texto = self.tabla_productos.item(fila, 4).text().strip()
        medida = medida_texto if medida_texto.lower() != "none" else None
        cantidad_text = self.tabla_productos.item(fila, 5).text().strip()
        precio_text = self.tabla_productos.item(fila, 6).text().strip()

        errores, producto = self.validador.validar(
            nombre=nombre,
            categoria=categoria,
            ubicacion=ubicacion,
            cantidad_text=cantidad_text,
            precio_text=precio_text,
            medida=medida,
            creado_por=self.usuario_logeado,
            id_producto=id_producto
        )

        if errores:
            QMessageBox.warning(self, "Error", "\n".join(errores))
            self.restaurar_tabla_y_limpiar()
            return

        # Verificar duplicados
        if self.service.existe_producto(nombre, ubicacion, medida, id_excluir=id_producto):
            QMessageBox.warning(self, "Error", "Ya existe un producto con ese nombre y ubicación.")
            self.restaurar_tabla_y_limpiar()
            return

        # Editar
        try:
            self.service.editar(producto)
            QMessageBox.information(self, "Éxito", "Producto editado correctamente.")
            self.restaurar_tabla_y_limpiar()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Ocurrió un error: {str(e)}")
            self.cargar_productos()

    def eliminar_producto(self):
        fila = self.tabla_productos.currentRow()
        if fila == -1:
            QMessageBox.warning(self, "Error", "Seleccioná un producto para eliminar.")
            return

        id_producto = int(self.tabla_productos.item(fila, 0).text())

        confirmacion = QMessageBox.question(
            self,
            "Confirmar eliminación",
            "¿Estás seguro de que querés eliminar este producto?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirmacion == QMessageBox.StandardButton.Yes:
            self.service.eliminar(id_producto)
            QMessageBox.information(self, "Éxito", "Producto eliminado correctamente.")
            self.restaurar_tabla_y_limpiar()


    def poblar_tabla(self, productos):
        productos_con_categoria = []

        for producto in productos:
            nombre_categoria = self.categorias_service.obtener_nombre_por_id(producto.categoria_id)
            productos_con_categoria.append((nombre_categoria, producto))

        productos_con_categoria.sort(key=lambda x: x[0] or "")

        self.tabla_productos.setRowCount(len(productos))
        
        for fila, (nombre_categoria, producto) in enumerate(productos_con_categoria):
            total = producto.cantidad * producto.precio_unitario  

            datos = [
                producto.id_producto,
                producto.nombre,
                nombre_categoria, 
                producto.ubicacion,
                producto.medida,
                producto.cantidad,
                producto.precio_unitario,
                round(total, 2)
            ]

            for col, dato in enumerate(datos):
                texto = '' if dato is None else str(dato)
                item = QTableWidgetItem(texto)
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.tabla_productos.setItem(fila, col, item)

        header = self.tabla_productos.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)


    def buscar_producto(self):
        nombre = self.buscarProducto.text()
        id_usuario = self.usuario_logeado.id_usuario
        productos = self.service.buscar(nombre, id_usuario)
        self.poblar_tabla(productos)
