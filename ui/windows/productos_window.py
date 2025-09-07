from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QMainWindow, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt6 import QtCore
from PyQt6.QtGui import QIcon
from PyQt6.uic import loadUi

from controllers.producto_popup_controller import ProductoPopupController
from ui.windows.productos_popup import ProductoPopup
    
class ProductosWindow(QMainWindow):
    def __init__(self, controller, usuario_logeado):
        super().__init__()
        self.controller = controller
        self.usuario_logeado = usuario_logeado
        self.inicializarUI()

    def inicializarUI(self):
        loadUi("ui/designer/productos.ui", self)

        self.configurar()

        self.btnAgregar.clicked.connect(self.agregar_producto)
        self.buscarProducto.textChanged.connect(self.buscar_producto)
        self.btnImprimir.clicked.connect(self.imprimir_productos)

        self.cargar_productos()
        self.show()


    def configurar(self):
        self.tabla_productos.verticalHeader().setVisible(False)
        self.tabla_productos.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.setMinimumSize(self.geometry().width(), self.geometry().height())
        self.setMaximumSize(self.geometry().width(), self.geometry().height())
        

    def cargar_productos(self):
        try:
            productos = self.controller.obtener_productos(self.usuario_logeado.id_usuario)
            self.poblar_tabla(productos)
            self.actualizar_label_modificacion()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al cargar productos: {e}")

    def agregar_producto(self):
        popup_controller = ProductoPopupController(
            producto_service=self.controller.service,
            categorias_service=self.controller.categorias_service,
            validador=self.controller.validador
        )
        popup = ProductoPopup(popup_controller, self.usuario_logeado)
        if popup.exec():
            self.controller.registrar_modificacion(self.usuario_logeado.id_usuario)
            self.actualizar_label_modificacion()
            self.cargar_productos()

    def editar_producto(self, producto):
        popup_controller = ProductoPopupController(
            producto_service=self.controller.service,
            categorias_service=self.controller.categorias_service,
            validador=self.controller.validador
        )
        popup = ProductoPopup(popup_controller, self.usuario_logeado, producto)
        if popup.exec():
            self.controller.registrar_modificacion(self.usuario_logeado.id_usuario)
            self.actualizar_label_modificacion()
            self.cargar_productos()
    

    def eliminar_producto(self, producto):
        confirmacion = QMessageBox.question(
            self,
            "Confirmar eliminación",
            f"¿Estás seguro de que querés eliminar '{producto.nombre}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirmacion == QMessageBox.StandardButton.Yes:
            try:
                self.controller.eliminar_producto(producto.id_producto)
                self.controller.registrar_modificacion(self.usuario_logeado.id_usuario) # Registro la modificaicon para actualizar el label
                self.actualizar_label_modificacion()
                self.cargar_productos()  # Recargo la tabla
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar el producto: {e}")


    def _crear_item(self, texto):
        item = QTableWidgetItem(str(texto) if texto is not None else "")
        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        return item
    
    def _crear_acciones(self, producto):
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        btn_editar = self._crear_boton("resources/icons/edit.png", "Editar producto", lambda: self.editar_producto(producto))
        btn_borrar = self._crear_boton("resources/icons/delete.png", "Eliminar producto", lambda: self.eliminar_producto(producto))

        layout.addWidget(btn_editar)
        layout.addWidget(btn_borrar)
        widget.setLayout(layout)
        return widget 
    

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
        productos_con_categoria = []

        for producto in productos:
            nombre_categoria = self.controller.obtener_nombre_categoria(producto.categoria_id)
            productos_con_categoria.append((nombre_categoria, producto))

        productos_con_categoria.sort(key=lambda x: x[0] or "")

        self.tabla_productos.setRowCount(len(productos))
        
        for fila, (nombre_categoria, producto) in enumerate(productos_con_categoria):
            total = producto.cantidad * producto.precio_unitario  

            # Si la ubicación o medida son None o "--- Seleccionar ---", muestro vacio
            ubicacion = "" if producto.ubicacion in (None, "--- Seleccionar ---") else producto.ubicacion
            medida = "" if producto.medida in (None, "--- Seleccionar ---") else producto.medida

            datos = [
                producto.id_producto,
                producto.nombre,
                nombre_categoria, 
                ubicacion,
                medida,
                producto.cantidad,
                producto.precio_unitario,
                round(total, 2)
            ]

            for col, dato in enumerate(datos):
                self.tabla_productos.setItem(fila, col, self._crear_item(dato))

            acciones = self._crear_acciones(producto)
            self.tabla_productos.setCellWidget(fila, len(datos), acciones)
            self.tabla_productos.setRowHeight(fila, 36)

        header = self.tabla_productos.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)


    def buscar_producto(self):
        nombre = self.buscarProducto.text()
        id_usuario = self.usuario_logeado.id_usuario
        productos = self.controller.obtener_productos(id_usuario, nombre)
        self.poblar_tabla(productos)

    def imprimir_productos(self):
        productos = self.controller.obtener_productos(self.usuario_logeado.id_usuario)
        self.controller.imprimir(productos, self)

    def actualizar_label_modificacion(self):
        try:
            fecha = self.controller.obtener_ultima_modificacion(self.usuario_logeado.id_usuario)
            if fecha:
                self.lbl_ultima_modificacion.setText(f"Última modificación: {fecha.strftime('%d/%m/%Y %H:%M:%S')}")
            else:
                self.lbl_ultima_modificacion.setText("Última modificación: No disponible")
        except Exception as e:
            print(f"[ERROR actualizar_label_modificacion] {e}")
            self.lbl_ultima_modificacion.setText("Última modificación: Error al obtener")