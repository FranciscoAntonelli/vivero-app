from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtGui import QPainter, QFont

class ImpresoraProductos:
    def imprimir(self, productos, parent=None):
        printer = QPrinter()
        dialog = QPrintDialog(printer, parent)
        if dialog.exec() == QPrintDialog.DialogCode.Accepted:
            painter = QPainter()
            painter.begin(printer)

            painter.setFont(QFont("Courier", 10))

            y = 100
            painter.drawText(100, y, "Listado de Productos")
            y += 30

            # Encabezados con ancho fijo
            header = f"{'Nombre':<25}{'Precio':>15}{'Cantidad':>14}{'Subtotal':>14}"
            painter.drawText(100, y, header)
            y += 20

            # Línea superior
            painter.drawLine(100, y, 800, y)
            y += 20

            total_general = 0  

            for producto in productos:
                subtotal = producto.precio_unitario * producto.cantidad
                total_general += subtotal

                linea = f"{producto.nombre:<25}{producto.precio_unitario:>15.2f}{producto.cantidad:>10}{subtotal:>18.2f}"
                painter.drawText(100, y, linea)
                y += 30
            
            y += 20

            # Línea inferior
            painter.drawLine(100, y, 800, y)
            y += 30
            total_line = f"{'TOTAL GENERAL:':<60}${total_general:>.2f}"
            painter.drawText(100, y, total_line)

            painter.end()