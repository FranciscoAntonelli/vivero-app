from PyQt6.QtWidgets import QMessageBox, QWidget, QTableWidgetItem, QHeaderView, QHBoxLayout
from PyQt6.uic import loadUi
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, pyqtSignal

from domain.models.carrito_venta import CarritoVenta
from ui.popups.venta_popup import VentaPopup 

class VentasWindow(QWidget):
    volver_inicio = pyqtSignal()

    def __init__(self, ventas_use_case, productos_use_case, usuario_logeado):
        super().__init__()
        self.ventas_use_case = ventas_use_case
        self.productos_use_case = productos_use_case
        self.usuario_logeado = usuario_logeado

        loadUi("ui/designer/ventas.ui", self)
        self._configurar_ventana()
        self._conectar_signales()

    def _configurar_ventana(self):
        # Tabla ventas
        self.tabla_ventas.verticalHeader().setVisible(False)
        self.tabla_ventas.setAlternatingRowColors(True)
        self.tabla_ventas.verticalHeader().setDefaultSectionSize(36)

        # Tabla detalles
        self.tabla_detalle_venta.verticalHeader().setVisible(False)
        self.tabla_detalle_venta.setAlternatingRowColors(True)
        self.tabla_detalle_venta.verticalHeader().setDefaultSectionSize(36)

        # Configurar headers
        self.tabla_ventas.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.tabla_detalle_venta.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.contenedorDetalles.hide()
        self.contenedorDetalles.setMaximumWidth(0)

        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.labelTotal.setFont(font)

        self.tabla_ventas.setAlternatingRowColors(False)
        self.tabla_detalle_venta.setAlternatingRowColors(False)

    def _conectar_signales(self):
        self.botonRegistrarVenta.clicked.connect(self.abrir_popup_venta)
        self.botonBuscar.clicked.connect(self.buscar_por_fechas)
        self.tabla_ventas.itemSelectionChanged.connect(self.mostrar_detalles)
        self.btn_volver.clicked.connect(self._volver)
        self.tabla_ventas.setAlternatingRowColors(False)

    def _volver(self):
        self.volver_inicio.emit()

    def buscar_por_fechas(self):
        fecha_inicio = self.fechaDesde.date().toPyDate() 
        fecha_fin = self.fechaHasta.date().toPyDate() 
        resultado = self.ventas_use_case.obtener_ventas(
            self.usuario_logeado.id_usuario,
            fecha_inicio,
            fecha_fin
        )

        if not resultado.exito:
            self._mostrar_error("\n".join(resultado.errores))
            return
        
        if not resultado.valor:
            self.tabla_ventas.setRowCount(0)
            self.labelTotal.setText("Total general: $0.00")

            QMessageBox.information(self, "Información", "No hay ventas en el rango seleccionado.")
            return

        self._poblar_tabla(resultado.valor)

    
    def cargar_ventas(self):
        resultado = self.ventas_use_case.obtener_ventas(self.usuario_logeado.id_usuario)

        if not resultado.exito:
            self._mostrar_error("\n".join(resultado.errores))
            return

        ventas = resultado.valor
        if not ventas:
            self.tabla_ventas.setRowCount(0)
            self.labelTotal.setText("Total general: $0.00")
            return

        self._poblar_tabla(ventas)


    def _poblar_tabla(self, ventas):
        self.tabla_ventas.setRowCount(len(ventas))

        total_general = 0

        for fila, v in enumerate(ventas):
            self.tabla_ventas.setItem(
                fila, 0, self._item_centrado(str(v["id_venta"]))
            )
            self.tabla_ventas.setItem(
                fila, 1, self._item_centrado(str(v["fecha"]))
            )
            self.tabla_ventas.setItem(
                fila, 2, self._item_centrado(f"${v['total']:.2f}")
            )

            total_general += v["total"]

        font = QFont()
        font.setPointSize(14)
        font.setBold(True)

        self.labelTotal.setFont(font)
        self.labelTotal.setText(f"Total general: ${total_general:.2f}")

    # -----------------------------
    #   POPUP DE REGISTRAR VENTA
    # -----------------------------

    def abrir_popup_venta(self):
        carrito = CarritoVenta()

        popup = VentaPopup(
            self.ventas_use_case,
            self.productos_use_case,
            carrito,
            self.usuario_logeado,
            self
        )

        if popup.exec():
            self.cargar_ventas()



    def mostrar_detalles(self):
        fila = self.tabla_ventas.currentRow()
        if fila == -1:
            return

        self.contenedorDetalles.setMaximumWidth(0)
        self.contenedorDetalles.show()

        id_venta = int(self.tabla_ventas.item(fila, 0).text())
        detalles = self.ventas_use_case.obtener_detalles(id_venta)

        self.tabla_detalle_venta.setRowCount(len(detalles))

        for r, det in enumerate(detalles):
            nombre = self.productos_use_case.obtener_nombre(det.id_producto).nombre
            cantidad = det.cantidad
            subtotal = det.subtotal
            precio_unit = subtotal / cantidad if cantidad > 0 else 0

            self.tabla_detalle_venta.setItem(
                r, 0, self._item_centrado(str(det.id_detalle))
            )

            self.tabla_detalle_venta.setItem(
                r, 1, self._item_centrado(str(det.id_venta))
            )

            self.tabla_detalle_venta.setItem(
                r, 2, self._item_centrado(nombre)
            )

            self.tabla_detalle_venta.setItem(
                r, 3, self._item_centrado(str(cantidad))
            )

            self.tabla_detalle_venta.setItem(
                r, 4, self._item_centrado(f"${precio_unit:.2f}")
            )

            self.tabla_detalle_venta.setItem(
                r, 5, self._item_centrado(f"${subtotal:.2f}")
            )

    def _item_centrado(self, texto):
        item = QTableWidgetItem(texto)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        return item


    def _mostrar_error(self, mensaje):
        QMessageBox.critical(self, "Error", mensaje)