from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtGui import QPainter, QFont

from utils.impresion.impresora import Impresora


class ImpresoraReportes(Impresora):

    def imprimir(self, reportes):
        printer = QPrinter()
        dialog = QPrintDialog(printer)

        if dialog.exec() != QPrintDialog.DialogCode.Accepted:
            return

        painter = QPainter(printer)
        painter.setFont(QFont("Courier", 10))

        y = 100
        line_height = 30
        total_general = 0

        painter.drawText(100, y, "REPORTE DIARIO DE VENTAS")
        y += line_height * 2

        header = f"{'Fecha':<15}{'Cantidad':>12}{'Total':>15}"
        painter.drawText(100, y, header)
        y += 20
        painter.drawLine(100, y, 800, y)
        y += 20

        for fecha, cantidad, total in reportes:
            total_general += total
            texto = f"{str(fecha):<12}{cantidad:>11}{f'${total:.2f}':>22}"
            painter.drawText(100, y, texto)
            y += line_height

        y += 20
        painter.drawLine(100, y, 800, y)
        y += line_height

        total_texto = f"{'TOTAL GENERAL:':<22}{f'${total_general:.2f}':>23}"
        painter.drawText(100, y, total_texto)

        painter.end()