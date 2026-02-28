from matplotlib.figure import Figure
from infrastructure.graficos.grafico_renderer import GraficoRenderer
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class MatplotlibGraficoRenderer(GraficoRenderer):
    def render_stock_producto(self, datos):
        productos = [d[0] for d in datos]
        cantidades = [d[1] for d in datos]

        fig = Figure(figsize=(8, max(6, len(productos) * 0.45)))
        ax = fig.add_subplot(111)

        ax.barh(productos, cantidades)
        ax.set_xlabel("Cantidad")
        ax.set_title("Stock por producto")

        fig.subplots_adjust(left=0.3)

        return FigureCanvas(fig)
    
    def render_stock_categoria(self, datos):
            categorias = [d[0] for d in datos]
            cantidades = [d[1] for d in datos]

            fig = Figure(figsize=(6, 4))
            ax = fig.add_subplot(111)

            ax.pie(cantidades, labels=categorias, autopct="%1.1f%%")
            ax.set_title("Stock por categoría")

            return FigureCanvas(fig)
    
    def render_ventas_mensuales(self, datos):
        meses = [d[0] for d in datos]
        totales = [d[1] for d in datos]

        fig = Figure(figsize=(6, 4))
        ax = fig.add_subplot(111)

        ax.plot(meses, totales, marker="o")
        ax.set_title("Ventas mensuales")
        ax.set_ylabel("Total vendido")

        return FigureCanvas(fig)
    

    def render_productos_mas_vendidos(self, datos):
        # Extrae nombres y cantidades de los datos
        nombres = [x[0] for x in datos]
        cantidades = [x[1] for x in datos]

        # Crea la figura y el eje
        fig = Figure(figsize=(8, max(6, len(nombres) * 0.45)))
        ax = fig.add_subplot(111)

        ax.barh(nombres, cantidades, color="#3498db")
        ax.set_xlabel("Cantidad vendida")
        ax.set_title("Productos más vendidos")
        ax.invert_yaxis()  # Invierte el eje Y para mostrar el más vendido arriba

        fig.subplots_adjust(left=0.3)  # Ajusta el margen izquierdo

        return FigureCanvas(fig)