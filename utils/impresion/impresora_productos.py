from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtGui import QPainter, QFont

class ImpresoraProductos:
    def preparar_datos_productos(self, productos):
        lineas = []
        total_general = 0
        for p in productos:
            subtotal = p.precio_unitario * p.cantidad
            total_general += subtotal
            lineas.append({
                "nombre": p.nombre,
                "precio": p.precio_unitario,
                "cantidad": p.cantidad,
                "subtotal": subtotal
            })
        return lineas, total_general

    def dibujar_productos(self, painter, lineas, total_general):
        y = 100
        painter.drawText(100, y, "Listado de Productos")
        y += 30

        header = f"{'Nombre':<25}{'Precio':>15}{'Cantidad':>14}{'Subtotal':>14}"
        painter.drawText(100, y, header)
        y += 20
        painter.drawLine(100, y, 800, y)
        y += 20

        for linea in lineas:
            texto = f"{linea['nombre']:<25}{linea['precio']:>15.2f}{linea['cantidad']:>10}{linea['subtotal']:>18.2f}"
            painter.drawText(100, y, texto)
            y += 30

        y += 20
        painter.drawLine(100, y, 800, y)
        y += 30
        total_texto = f"{'TOTAL GENERAL:':<60}${total_general:>.2f}"
        painter.drawText(100, y, total_texto)

    def imprimir(self, productos, parent=None):
        printer = QPrinter()
        dialog = QPrintDialog(printer, parent)

        if dialog.exec() == QPrintDialog.DialogCode.Accepted:
            painter = QPainter()
            painter.begin(printer)
            painter.setFont(QFont("Courier", 10))

            lineas, total_general = self.preparar_datos_productos(productos)
            self.dibujar_productos(painter, lineas, total_general)

            painter.end()