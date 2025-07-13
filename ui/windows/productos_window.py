from PyQt6.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from PyQt6 import QtCore
from PyQt6.uic import loadUi

from models.producto import Producto
    
class ProductosWindow(QMainWindow):
    def __init__(self, service, usuario_logeado):
        super().__init__()
        self.service = service
        self.usuario_logeado = usuario_logeado
        loadUi("ui/designer/productos.ui", self)
        self.configurar()
        
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


    def limpiar_campos(self):
        self.inputNombre.clear()
        self.inputUbicacion.setCurrentIndex(0)
        self.inputCantidad.clear()
        self.inputPrecio.clear()
        self.inputCategoria.setCurrentIndex(0)
        self.inputMedida.clear()

    def agregar_producto(self):
        try:
            nombre = self.inputNombre.text().strip()
            categoria = self.inputCategoria.currentText().strip()
            ubicacion = self.inputUbicacion.currentText().strip()
            medida_texto = self.inputMedida.text().strip()

            if medida_texto == '':
                medida = None
            else:
                try:
                    medida = float(medida_texto)
                    if medida < 0:
                        QMessageBox.warning(self, "Error", "La medida no puede ser negativa.")
                        return
                except ValueError:
                    QMessageBox.warning(self, "Error", "Medida debe ser un número válido.")
                    return

            if not nombre:
                QMessageBox.warning(self, "Error", "El nombre no puede estar vacío.")
                return
            
            try:
                cantidad = int(self.inputCantidad.text())
                if cantidad <= 0:
                    QMessageBox.warning(self, "Error", "La cantidad debe ser un número mayor que cero.")
                    return
                
                precio = float(self.inputPrecio.text())
                if precio <= 0:
                    QMessageBox.warning(self, "Error", "El precio debe ser un número mayor que cero.")
                    return
            except ValueError:
                QMessageBox.warning(self, "Error", "Cantidad debe ser un número entero y precio un número decimal.")
                return

            producto = Producto(
                nombre=nombre,
                categoria=categoria,
                ubicacion=ubicacion,
                medida=medida,
                cantidad=cantidad,
                precio_unitario=precio,
                creado_por=self.usuario_logeado.id_usuario
            )
            print("Medida:", repr(medida))

            if self.service.existe_producto(nombre, ubicacion):
                QMessageBox.warning(self, "Error", "Ya existe un producto con ese nombre y ubicación.")
                return
            
            self.service.agregar(producto)
            QMessageBox.information(self, "Éxito", "Producto agregado correctamente.")
            self.limpiar_campos()
            self.cargar_productos()

        except Exception as e:
           QMessageBox.critical(self, "Error", str(e))


    def editar_producto(self):
        fila = self.tabla_productos.currentRow()
        if fila == -1:
            QMessageBox.warning(self, "Error", "Seleccioná una fila para editar.")
            return

        try:
            id_producto = int(self.tabla_productos.item(fila, 0).text())
            nombre = self.tabla_productos.item(fila, 1).text().strip()
            if not nombre:
                QMessageBox.warning(self, "Error", "El nombre no puede estar vacío.")
                return

            categoria = self.tabla_productos.item(fila, 2).text().strip()
            categorias_validas = ['Planta', 'Maceta', 'Tierra']

            if categoria not in categorias_validas:
                QMessageBox.warning(self, "Error", f"La categoría debe ser una de: {', '.join(categorias_validas)}")
                return
            
            ubicacion = self.tabla_productos.item(fila, 3).text().strip() 
            ubicaciones_validas = ['', 'Exterior', 'Interior', 'Ambos']

            if ubicacion not in ubicaciones_validas:
                QMessageBox.warning(self, "Error", f"La ubicación debe ser una de: {', '.join(ubicaciones_validas)}")
                return

            medida_text = self.tabla_productos.item(fila, 4).text().strip()
            if medida_text == '' or medida_text.lower() == 'none':
                medida = None
            else:
                try:
                    medida = float(medida_text)
                    if medida < 0:
                        QMessageBox.warning(self, "Error", "La medida no puede ser negativa.")
                        return
                except ValueError:
                    QMessageBox.warning(self, "Error", "La medida debe ser un número válido.")
                    return
                
            cantidad_text = self.tabla_productos.item(fila, 5).text().strip()
            precio_text = self.tabla_productos.item(fila, 6).text().strip()
            if not cantidad_text:
                QMessageBox.warning(self, "Error", "La cantidad no puede estar vacía.")
                return

            if not precio_text:
                QMessageBox.warning(self, "Error", "El precio no puede estar vacío.")
                return
            
            try:
                cantidad = int(cantidad_text)
                if cantidad <= 0:
                    QMessageBox.warning(self, "Error", "La cantidad debe ser un número mayor que cero.")
                    return
            except ValueError:
                QMessageBox.warning(self, "Error", "La cantidad debe ser un número entero válido.")
                return

            try:
                precio = float(precio_text)
                if precio <= 0:
                    QMessageBox.warning(self, "Error", "El precio debe ser un número mayor que cero.")
                    return
            except ValueError:
                QMessageBox.warning(self, "Error", "El precio debe ser un número decimal válido.")
                return

            producto = Producto(
                id_producto=id_producto,
                nombre=nombre,
                categoria=categoria,
                ubicacion=ubicacion,
                medida=medida,
                cantidad=cantidad,
                precio_unitario=precio,
                creado_por=self.usuario_logeado
            )
            print(f"Medida: {repr(producto.medida)}")

            if self.service.existe_producto(nombre, ubicacion, id_excluir=id_producto):
                QMessageBox.warning(self, "Error", "Ya existe un producto con ese nombre y ubicación.")
                return

            self.service.editar(producto)
            QMessageBox.information(self, "Éxito", "Producto editado correctamente.")
            self.cargar_productos()

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
            self.cargar_productos()
            self.limpiar_campos()


    def poblar_tabla(self, productos):
        self.tabla_productos.setRowCount(len(productos))
        for fila, producto in enumerate(productos):
            datos = [
                producto.id_producto,
                producto.nombre,
                producto.categoria,
                producto.ubicacion,
                producto.medida,
                producto.cantidad,
                producto.precio_unitario
            ]
            for col, dato in enumerate(datos):
                texto = '' if dato is None else str(dato)
                item = QTableWidgetItem(str(texto))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.tabla_productos.setItem(fila, col, item)



    def buscar_producto(self):
        nombre = self.buscarProducto.text()
        id_usuario = self.usuario_logeado.id_usuario
        productos = self.service.buscar(nombre, id_usuario)
        self.poblar_tabla(productos)
