from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QMainWindow, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt6 import QtCore
from PyQt6.QtGui import QIcon
from PyQt6.uic import loadUi

from use_cases.productos.producto_popup_use_case import ProductoPopupUseCase
from ui.windows.productos_popup_window import ProductoPopup
    
class ProductosWindow(QMainWindow):
    def __init__(self, producto_use_case, producto_popup_use_case, usuario_logeado):
        super().__init__()
        self.inicializarUI(producto_use_case, producto_popup_use_case, usuario_logeado)

    def inicializarUI(self, producto_use_case, producto_popup_use_case, usuario_logeado):
        self.producto_use_case = producto_use_case # Para la ventana completa
        self.producto_popup_use_case = producto_popup_use_case # Para los popups
        self.usuario_logeado = usuario_logeado
        self._cargar_ui()
        self._configurar_ventana()
        self._conectar_signales()
        self.cargar_productos()
        self._mostrar()

    def _cargar_ui(self):
        loadUi("ui/designer/productos.ui", self)


    def _configurar_ventana(self):
        self.tabla_productos.verticalHeader().setVisible(False)
        self.tabla_productos.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setMinimumSize(self.geometry().width(), self.geometry().height())
        self.setMaximumSize(self.geometry().width(), self.geometry().height())

    def _conectar_signales(self):
        self.btnAgregar.clicked.connect(self.agregar_producto)
        self.buscarProducto.textChanged.connect(self.buscar_producto)
        self.btnImprimir.clicked.connect(self.imprimir_productos)

    def _cargar_datos_iniciales(self):
        self.cargar_productos()
        
    def _mostrar(self):
        self.show()

    def cargar_productos(self):
        try:
            productos = self._obtener_productos()
            self._actualizar_ui_productos(productos)
        except Exception as e:
            self._mostrar_error(f"Ocurrió un error al cargar productos: {e}")

    # Metodo para obtener productos
    def _obtener_productos(self):
        return self.producto_use_case.obtener_productos(self.usuario_logeado.id_usuario)

    # Método para actualizar la UI
    def _actualizar_ui_productos(self, productos):
        self.poblar_tabla(productos)
        self.actualizar_label_modificacion()

    # Metodo solo para mostrar errores
    def _mostrar_error(self, mensaje):
        QMessageBox.critical(self, "Error", mensaje)

    def agregar_producto(self):
        resultado = self._abrir_popup_producto()
        if resultado and resultado.exito:
            self._actualizar_productos_despues_de_guardar()

    # abre el popup y devuelve el resultado
    def _abrir_popup_producto(self):
        popup = ProductoPopup(self.producto_popup_use_case, self.usuario_logeado)
        if popup.exec():
            return popup.resultado_guardado
        return None
    
    # Actualizo la UI despues de guardar un producto
    def _actualizar_productos_despues_de_guardar(self):
        self.producto_use_case.registrar_modificacion(self.usuario_logeado.id_usuario)
        self.actualizar_label_modificacion()
        self.cargar_productos()
               

    def editar_producto(self, producto):
        resultado = self._abrir_popup_editar_producto(producto)
        if resultado and resultado.exito:
            self._actualizar_productos_despues_de_guardar()

    # abre el popup de edicion y devuelve el resultado
    def _abrir_popup_editar_producto(self, producto):
        popup = ProductoPopup(self.producto_popup_use_case, self.usuario_logeado, producto)
        if popup.exec():
            return popup.resultado_guardado
        return None
    

    def eliminar_producto(self, producto):
        confirmacion = QMessageBox.question(
            self,
            "Confirmar eliminación",
            f"¿Estás seguro de que querés eliminar '{producto.nombre}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirmacion == QMessageBox.StandardButton.Yes:
            try:
                self.producto_use_case.eliminar_producto(producto.id_producto)
                self.producto_use_case.registrar_modificacion(self.usuario_logeado.id_usuario) # Registro la modificaicon para actualizar el label
                self.actualizar_label_modificacion()
                self.cargar_productos()  # Recargo la tabla
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar el producto: {e}")


    def _crear_item(self, texto):
        item = QTableWidgetItem(str(texto) if texto is not None else "")
        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        return item
    
    def _crear_acciones(self, producto):
        layout = self._crear_layout_acciones()
        botones = self._crear_botones_acciones(producto)
        
        for btn in botones:
            layout.addWidget(btn)

        widget = QWidget()
        widget.setLayout(layout)
        return widget
    
    def _crear_layout_acciones(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        return layout
    
    def _crear_botones_acciones(self, producto):
        return [
            self._crear_boton("resources/icons/edit.png", "Editar producto", lambda: self.editar_producto(producto)),
            self._crear_boton("resources/icons/delete.png", "Eliminar producto", lambda: self.eliminar_producto(producto))
        ]
    
    def _crear_boton(self, icon_path, tooltip, callback):
        btn = QPushButton()
        btn.setIcon(QIcon(icon_path))
        btn.setIconSize(QtCore.QSize(24, 24))
        btn.setFixedSize(32, 32)
        btn.setStyleSheet("QPushButton { border: none; background: transparent; }")
        btn.setToolTip(tooltip)
        btn.clicked.connect(callback)
        return btn


    def poblar_tabla(self, productos):
        productos_ordenados = self._preparar_productos_con_categoria(productos)
        self._llenar_tabla(productos_ordenados)
            
    # recorre los productos con el nombre de su categoria y los ordena
    def _preparar_productos_con_categoria(self, productos):
        productos_con_categoria = [
            (self.producto_use_case.obtener_nombre_categoria(p.categoria_id), p)
            for p in productos
        ]
        return sorted(productos_con_categoria, key=lambda x: x[0] or "")

    # Llena la tabla con los productos 
    def _llenar_tabla(self, productos_con_categoria):
        self.tabla_productos.setRowCount(len(productos_con_categoria))

        for fila, (nombre_categoria, producto) in enumerate(productos_con_categoria):
            datos = self._mapear_producto_a_datos_tabla(producto, nombre_categoria)
            for col, dato in enumerate(datos):
                self.tabla_productos.setItem(fila, col, self._crear_item(dato))

            acciones = self._crear_acciones(producto)
            self.tabla_productos.setCellWidget(fila, len(datos), acciones)
            self.tabla_productos.setRowHeight(fila, 36)

        header = self.tabla_productos.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    # Mapea un producto con los datos que se muestran en la tabla
    def _mapear_producto_a_datos_tabla(self, producto, nombre_categoria):
        total = producto.cantidad * producto.precio_unitario
        ubicacion = "" if producto.ubicacion in (None, "--- Seleccionar ---") else producto.ubicacion
        medida = "" if producto.medida in (None, "--- Seleccionar ---") else producto.medida

        return [
            producto.id_producto,
            producto.nombre,
            nombre_categoria,
            ubicacion,
            medida,
            producto.cantidad,
            producto.precio_unitario,
            round(total, 2)
        ]

    def buscar_producto(self):
        nombre = self.buscarProducto.text()
        id_usuario = self.usuario_logeado.id_usuario
        productos = self.producto_use_case.obtener_productos(id_usuario, nombre)
        self.poblar_tabla(productos)

    def imprimir_productos(self):
        productos = self.producto_use_case.obtener_productos(self.usuario_logeado.id_usuario)
        self.producto_use_case.imprimir(productos, self)

    def actualizar_label_modificacion(self):
        try:
            fecha = self.producto_use_case.obtener_ultima_modificacion(self.usuario_logeado.id_usuario)
            if fecha:
                self.lbl_ultima_modificacion.setText(f"Última modificación: {fecha.strftime('%d/%m/%Y %H:%M:%S')}")
            else:
                self.lbl_ultima_modificacion.setText("Última modificación: No disponible")
        except Exception as e:
            print(f"[ERROR actualizar_label_modificacion] {e}")
            self.lbl_ultima_modificacion.setText("Última modificación: Error al obtener")