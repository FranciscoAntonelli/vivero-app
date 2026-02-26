from PyQt6.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QHeaderView, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.uic import loadUi
from PyQt6.QtCore import pyqtSignal

class ReportesWindow(QWidget):
    volver_inicio = pyqtSignal()

    def __init__(self, reportes_use_case, imprimir_reportes_use_case, usuario_logeado, grafico_renderer):
        super().__init__()
        self.reportes_use_case = reportes_use_case
        self.imprimir_reportes_use_case = imprimir_reportes_use_case
        self.usuario_logeado = usuario_logeado
        self.grafico_renderer = grafico_renderer
        self.canvas_stock_producto = None
        self.canvas_stock_categoria = None
        self.canvas_ventas_mensuales = None
        self.canvas_productos_mas_vendidos = None
        loadUi("ui/designer/reportes.ui", self)
        self._configurar_ventana()
        self._configurar_tabs()
        self._conectar_signales()

    def _configurar_ventana(self):
        self.tabla_reportes.verticalHeader().setVisible(False)

        self.tabla_reportes.horizontalHeader().setStretchLastSection(True)
        self.tabla_reportes.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

    def _conectar_signales(self):
        self.boton_imprimir.clicked.connect(self.imprimir_resumen)
        self.botonBuscar.clicked.connect(self.buscar_por_fechas)
        self.btn_volver.clicked.connect(self._volver)


    # -------------------------
    #       FUNCIONALIDADES
    # -------------------------
    def cargar_reportes(self):
        resultado = self.reportes_use_case.obtener_reporte_diario(self.usuario_logeado.id_usuario)

        if not resultado.exito:
            self._mostrar_error("\n".join(resultado.errores))
            return

        self._poblar_tabla(resultado.valor)
        self.grafico_stock_producto()
        self.grafico_stock_categoria()
        self.grafico_ventas_mensuales()
        self.grafico_productos_mas_vendidos()
          

    def _poblar_tabla(self, reportes):
        self.tabla_reportes.setRowCount(len(reportes))

        for fila, r in enumerate(reportes):
            dia, cantidad, total = r

            item_fecha = QTableWidgetItem(str(dia))
            item_fecha.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            item_cantidad = QTableWidgetItem(str(cantidad))
            item_cantidad.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            item_total = QTableWidgetItem(f"$ {total:.2f}")
            item_total.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.tabla_reportes.setItem(fila, 0, item_fecha)
            self.tabla_reportes.setItem(fila, 1, item_cantidad)
            self.tabla_reportes.setItem(fila, 2, item_total)



    def _volver(self):
        self.volver_inicio.emit()


    def imprimir_resumen(self):
        self.imprimir_reportes_use_case.ejecutar(self.usuario_logeado.id_usuario)
        

    # -------------------------
    #       UTILES
    # -------------------------
    def _mostrar_error(self, mensaje):
        QMessageBox.critical(self, "Error", mensaje)

    def buscar_por_fechas(self):
        
        fecha_desde = self.fechaDesde.date().toPyDate()
        fecha_hasta = self.fechaHasta.date().toPyDate()

        resultado = self.reportes_use_case.obtener_reporte_diario(
            self.usuario_logeado.id_usuario, fecha_desde, fecha_hasta
        )

        if not resultado.exito:
            self._mostrar_error("\n".join(resultado.errores))
            return

        if not resultado.valor:
            self.tabla_reportes.setRowCount(0)
            # opcional: mostrar label informativo
            QMessageBox.information(
                self,
                "Información",
                "No hay datos en el rango seleccionado."
            )
            return
        self._poblar_tabla(resultado.valor)

           
        

    def _configurar_tabs(self):

        # ---------- STOCK ----------
        self.scrollArea.setWidgetResizable(True)

        self.layout_stock = QVBoxLayout(self.scrollAreaWidgetContents)
        self.layout_stock.setContentsMargins(0, 0, 0, 0)
        self.layout_stock.setSpacing(0)

        # ---------- TAB CATEGORIA ----------
        self.scrollArea_2.setWidgetResizable(True)

        self.layout_categoria = QVBoxLayout(self.scrollAreaWidgetContents_categoria)
        self.layout_categoria.setContentsMargins(0, 0, 0, 0)
        self.layout_categoria.setSpacing(0)

        # ---------- TAB VENTAS ----------
        self.scrollArea_3.setWidgetResizable(True)

        self.layout_ventas = QVBoxLayout(self.scrollAreaWidgetContents_ventas)
        self.layout_ventas.setContentsMargins(0, 0, 0, 0)
        self.layout_ventas.setSpacing(0)

        # ---------- TAB PRODUCTOS MAS VENDIDOS ----------
        self.scrollArea_productos_mas_vendidos.setWidgetResizable(True)

        self.layout_productos_mas_vendidos = QVBoxLayout(
            self.scrollAreaWidgetContents_productos_mas_vendidos
        )
        self.layout_productos_mas_vendidos.setContentsMargins(0, 0, 0, 0)
        self.layout_productos_mas_vendidos.setSpacing(0)

    def grafico_stock_producto(self):
        usuario_id = self.usuario_logeado.id_usuario
        datos = self.reportes_use_case.obtener_stock_por_producto(usuario_id)

        if not datos:
            return

        canvas = self.grafico_renderer.render_stock_producto(datos)
        altura = len(datos) * 35 + 150

        self.canvas_stock_producto = self._mostrar_canvas(self.layout_stock, canvas, 
                                                          self.canvas_stock_producto, 
                                                          min_height=altura)


    def grafico_stock_categoria(self):
        usuario_id = self.usuario_logeado.id_usuario
        datos = self.reportes_use_case.obtener_stock_por_categoria(usuario_id)

        if not datos:
            return

        canvas = self.grafico_renderer.render_stock_categoria(datos)
        self.canvas_stock_categoria = self._mostrar_canvas(self.layout_categoria, canvas, self.canvas_stock_categoria)


    def grafico_ventas_mensuales(self):
        usuario_id = self.usuario_logeado.id_usuario
        datos = self.reportes_use_case.obtener_ventas_mensuales(usuario_id)

        if not datos:
            return

        canvas = self.grafico_renderer.render_ventas_mensuales(datos)
        self.canvas_ventas_mensuales = self._mostrar_canvas(self.layout_ventas, canvas, self.canvas_ventas_mensuales)

    def grafico_productos_mas_vendidos(self):
        usuario_id = self.usuario_logeado.id_usuario
        datos = self.reportes_use_case.obtener_productos_mas_vendidos(usuario_id, top_n=10)

        if not datos:
            return  

        canvas = self.grafico_renderer.render_productos_mas_vendidos(datos)
        self.canvas_productos_mas_vendidos = self._mostrar_canvas(self.layout_productos_mas_vendidos, canvas, self.canvas_productos_mas_vendidos)

    def _mostrar_canvas(self, layout, nuevo_canvas, canvas_anterior=None, min_height=None):
        if canvas_anterior:
            layout.removeWidget(canvas_anterior)
            canvas_anterior.deleteLater()

        nuevo_canvas.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )

        if min_height:
            nuevo_canvas.setMinimumHeight(min_height)

        layout.addWidget(nuevo_canvas)
        return nuevo_canvas

    