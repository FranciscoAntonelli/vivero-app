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

            total_general = 0  # Acumulador del total

            for producto in productos:
                subtotal = producto.precio_unitario * producto.cantidad
                total_general += subtotal

                texto = (f"{producto.nombre} - {producto.cantidad} x ${producto.precio_unitario:.2f} "
                         f"= ${subtotal:.2f}")
                painter.drawText(100, y, texto)
                y += 30
            
            # Línea final con el total general
            y += 20
            painter.drawText(100, y, f"TOTAL GENERAL: ${total_general:.2f}")
            painter.end()