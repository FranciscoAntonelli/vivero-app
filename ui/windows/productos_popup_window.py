from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.uic import loadUi
import psycopg

from models.ubicacion import Ubicacion

class ProductoPopup(QDialog):
    def __init__(self, popup_use_case, usuario_logeado, producto=None):
        super().__init__()
        self.inicializarUI(popup_use_case, usuario_logeado, producto)

    def inicializarUI(self, popup_use_case, usuario_logeado, producto):
        self._use_case = popup_use_case
        self.usuario_logeado = usuario_logeado
        self.producto = producto
        self.resultado_guardado = None

        self._cargar_ui()
        self._configurar_ventana()
        self._cargar_datos_iniciales()
        self._conectar_signales()

    def _cargar_ui(self):
        loadUi("ui/designer/producto_popup.ui", self)

    def _configurar_ventana(self):
        self.setMinimumSize(self.geometry().width(), self.geometry().height())
        self.setMaximumSize(self.geometry().width(), self.geometry().height())

    def _cargar_datos_iniciales(self):
        self.cargar_categorias()
        self.cargar_ubicaciones()
        if self.producto:
            self.setWindowTitle("Editar producto")
            self.cargar_datos(self.producto)
        else:
            self.setWindowTitle("Agregar producto")

    def _conectar_signales(self):
        self.btnGuardar.clicked.connect(self.guardar_productos)

    def cargar_datos(self, producto):
        self.inputNombre.setText(producto.nombre)
        self.inputUbicacion.setCurrentText(producto.ubicacion or "")
        self.inputMedida.setText(producto.medida or "")
        self.inputCantidad.setValue(producto.cantidad or 0)
        self.inputPrecio.setValue(producto.precio_unitario or 0.0)

        nombre_categoria = self._use_case.categorias_service.obtener_nombre_por_id(producto.categoria_id)
        for i in range(self.inputCategoria.count()):
            if self.inputCategoria.itemText(i) == nombre_categoria:
                self.inputCategoria.setCurrentIndex(i)
                break


    def cargar_categorias(self):
        self.inputCategoria.clear()
        self.inputCategoria.addItem("--- Seleccionar ---", None)
        for categoria in self._use_case.listar_categorias():
            self.inputCategoria.addItem(categoria.nombre, categoria.id_categoria)

    def cargar_ubicaciones(self): 
        self.inputUbicacion.clear()
        self.inputUbicacion.addItem("--- Seleccionar ---", None) 
        for ubicacion in Ubicacion: 
            self.inputUbicacion.addItem(ubicacion.value, ubicacion.name)

    def _mostrar_errores(self, errores):
        """Muestra los errores en la interfaz"""
        QMessageBox.warning(self, "Error", "\n".join(errores))

    def _obtener_datos_producto(self):
        nombre = self.inputNombre.text().strip()
        categoria = self.inputCategoria.currentData()
        
        ubicacion_raw = self.inputUbicacion.currentText().strip()
        ubicacion = '' if ubicacion_raw == "--- seleccionar ---" else ubicacion_raw

        medida = self.inputMedida.text().strip() or ''
        cantidad = int(self.inputCantidad.text()) if self.inputCantidad.text() else 0
        precio_unitario = float(self.inputPrecio.text().replace(",", ".")) if self.inputPrecio.text() else 0.0
        creado_por = self.usuario_logeado.id_usuario

        return {
            "id_producto": self.producto.id_producto if self.producto else None,
            "nombre": nombre,
            "categoria": categoria,
            "ubicacion": ubicacion,
            "medida": medida,
            "cantidad": cantidad,
            "precio_unitario": precio_unitario,
            "creado_por": creado_por
        }

    def guardar_productos(self):
        producto_dict = self._obtener_datos_producto()
        resultado = self._use_case.guardar_producto(producto_dict, self.producto)
        
        if not resultado.exito:
            self._mostrar_errores(resultado.errores)
            return
        
        self.resultado_guardado = resultado 
        self.accept()

