from PyQt6.QtWidgets import QDialog, QMessageBox, QTableWidgetItem, QPushButton, QHeaderView, QWidget, QHBoxLayout
from PyQt6.uic import loadUi
from decimal import Decimal
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFont


class VentaPopup(QDialog):
    def __init__(self, ventas_use_case, productos_use_case, carrito_venta, usuario_logeado, parent=None):
        super().__init__(parent)

        loadUi("ui/designer/registrar_venta.ui", self)

        self.ventas_use_case = ventas_use_case
        self.productos_use_case = productos_use_case
        self.usuario_logeado = usuario_logeado

        self.carrito = carrito_venta
        self.total_venta = Decimal("0.00")

        self._setup_ui()
        self._conectar_signales()

    # ---------------- UI ----------------

    def _setup_ui(self):
        self.setWindowTitle("Registrar Venta")
        self._cargar_productos_disponibles()
        self._actualizar_label_precio_producto()

        font = QFont()
        font.setPointSize(14)  
        font.setBold(True)

        self.labelTotal.setFont(font)
        self.labelTotal.setText("Total: $0.00")

        self.tabla_carrito.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_carrito.verticalHeader().setVisible(False)

    def _conectar_signales(self):
        self.btnAgregar.clicked.connect(self.agregar_producto_al_carrito)
        self.btnConfirmar.accepted.connect(self.registrar_venta)
        self.btnConfirmar.rejected.connect(self.reject)
        self.comboProductos.currentIndexChanged.connect(
            self._actualizar_label_precio_producto
        )

    # ---------------- Productos ----------------

    def _cargar_productos_disponibles(self):
        productos = self.productos_use_case.obtener_productos(
            self.usuario_logeado.id_usuario
        )

        self.comboProductos.clear()

        for producto in productos:
            if producto.medida:
                texto = f"{producto.nombre} - {producto.medida}"
            else:
                texto = producto.nombre

            self.comboProductos.addItem(texto, producto)

    def _actualizar_label_precio_producto(self):
        producto = self.comboProductos.currentData()

        if not producto:
            self.labelPrecio.setText("Precio: $0.00")
            return

        self.labelPrecio.setText(f"Precio: ${producto.precio_unitario}")

    # ---------------- Carrito ----------------

    def agregar_producto_al_carrito(self):
        producto = self.comboProductos.currentData()
        cantidad = self.inputCantidad.value()

        if not producto:
            QMessageBox.warning(self, "Advertencia", "Seleccione un producto.")
            return

        try:
            self.carrito.agregar(producto, cantidad)
            self._actualizar_ui_carrito()
        except ValueError as e:
            QMessageBox.warning(self, "Advertencia", str(e))

            self._actualizar_ui_carrito()

    def _actualizar_ui_carrito(self):
        items = self.carrito.items
        self.tabla_carrito.setRowCount(len(items))

        for fila, item in enumerate(items):
            producto = item.producto

            self._set_item(fila, 0, producto.nombre)
            self._set_item(fila, 1, str(item.cantidad))
            self._set_item(fila, 2, f"${item.precio_unitario}")
            self._set_item(fila, 3, f"${item.subtotal}")

            btn = QPushButton()
            btn.setIcon(QIcon("resources/icons/delete.PNG"))

            # tamaño del ícono
            btn.setIconSize(QSize(24, 24))

            # tamaño fijo para el botón
            btn.setFixedSize(36, 36)

            # estilo para el botón
            btn.setStyleSheet("""
                QPushButton {
                    border: none;
                }
                QPushButton:hover {
                    background-color: #ffe5e5;
                    border-radius: 6px;
                }
            """)
            btn.setToolTip("Eliminar del carrito")

            # centrar el botón en la celda
            container = QWidget()
            layout = QHBoxLayout(container)
            layout.addWidget(btn)
            layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
            layout.setContentsMargins(0, 0, 0, 0)

            btn.clicked.connect(
                lambda _, pid=producto.id_producto: self._eliminar_producto(pid)
            )
            self.tabla_carrito.setCellWidget(fila, 4, container)
            self.tabla_carrito.setRowHeight(fila, btn.height())

        self.labelTotal.setText(f"Total: ${self.carrito.total()}")

    def _set_item(self, fila, col, texto):
        item = QTableWidgetItem(texto)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tabla_carrito.setItem(fila, col, item)

    def _eliminar_producto(self, id_producto):
        self.carrito.eliminar(id_producto)
        self._actualizar_ui_carrito()


    # ---------------- Venta ----------------

    def registrar_venta(self):
        if self.carrito.vacio():
            QMessageBox.warning(self, "Advertencia", "El carrito está vacío.")
            return

        try:
            self.ventas_use_case.registrar_venta(
                self.carrito,
                self.usuario_logeado.id_usuario
            )

            QMessageBox.information(self, "Éxito", "Venta registrada correctamente.")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))