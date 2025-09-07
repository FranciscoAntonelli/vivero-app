from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.uic import loadUi

from models.producto import Producto
from models.ubicacion import Ubicacion

class ProductoPopup(QDialog):
    def __init__(self, popup_controller, usuario_logeado, producto=None):
        super().__init__()
        self.inicializarUI(popup_controller, usuario_logeado, producto)

    def inicializarUI(self, popup_controller, usuario_logeado, producto):
        loadUi("ui/designer/producto_popup.ui", self)
        self.controller = popup_controller   
        self.usuario_logeado = usuario_logeado
        self.producto = producto
        self.configurar()
        self.cargar_categorias()
        self.cargar_ubicaciones()

        # Cambia el titulo segun lo que aprete el usuario
        if producto:
            self.setWindowTitle("Editar producto")
            self.cargar_datos(producto)
        else:
            self.setWindowTitle("Agregar producto")

        
        self.btnGuardar.clicked.connect(self.guardar_productos)

    def configurar(self):
        self.setMinimumSize(self.geometry().width(), self.geometry().height())
        self.setMaximumSize(self.geometry().width(), self.geometry().height())

    def cargar_datos(self, producto):
        self.inputNombre.setText(producto.nombre)
        self.inputUbicacion.setCurrentText(producto.ubicacion or "")
        self.inputMedida.setText(producto.medida or "")
        self.inputCantidad.setValue(producto.cantidad or 0)
        self.inputPrecio.setValue(producto.precio_unitario or 0.0)

        # Selecciona categoria usando el controller
        for i in range(self.inputCategoria.count()):
            nombre_categoria = self.controller.categorias_service.obtener_nombre_por_id(producto.categoria_id)
            if self.inputCategoria.itemText(i) == nombre_categoria:
                self.inputCategoria.setCurrentIndex(i)
                break


    def cargar_categorias(self):
        self.inputCategoria.clear()
        self.inputCategoria.addItem("--- Seleccionar ---", None)
        for categoria in self.controller.listar_categorias():  
            self.inputCategoria.addItem(categoria.nombre, categoria.id_categoria)

    def cargar_ubicaciones(self): 
        self.inputUbicacion.clear()
        #Opcion vacio al inicio
        self.inputUbicacion.addItem("--- Seleccionar ---", None) 
        for ubicacion in Ubicacion: 
            self.inputUbicacion.addItem(ubicacion.value, ubicacion.name)

    def guardar_productos(self):
        producto_dict = {
            "id_producto": self.producto.id_producto if self.producto else None,
            "nombre": self.inputNombre.text().strip(),
            "categoria": self.inputCategoria.currentData(),
            "ubicacion": self.inputUbicacion.currentText(),
            "medida": self.inputMedida.text().strip() or None,
            "cantidad": int(self.inputCantidad.text()) if self.inputCantidad.text() else 0,
            "precio_unitario": float(self.inputPrecio.text().replace(",", ".")) if self.inputPrecio.text() else 0.0,
            "creado_por": self.usuario_logeado.id_usuario
        }

        ok, errores = self.controller.validar_y_guardar(producto_dict, self.producto)
        if not ok:
            QMessageBox.warning(self, "Error", "\n".join(errores))
            return

        self.accept()  # cierra el popup

