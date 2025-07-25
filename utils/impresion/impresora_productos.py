from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtGui import QPainter

class ImpresoraProductos:
    def imprimir(self, productos, parent=None):
        printer = QPrinter()
        dialog = QPrintDialog(printer, parent)
        if dialog.exec() == QPrintDialog.DialogCode.Accepted:
            painter = QPainter()
            painter.begin(printer)
            y = 100
            painter.drawText(100, y, "Listado de Productos")
            y += 40
            for producto in productos:
                texto = f"{producto.nombre} - {producto.precio_unitario} - {producto.cantidad}"
                painter.drawText(100, y, texto)
                y += 30
            painter.end()