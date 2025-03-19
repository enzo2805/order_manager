from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QDialog, QTabWidget, QWidget, QGridLayout
from PyQt5.QtCore import QByteArray, QSize
from PyQt5.QtGui import QPixmap, QIcon
from controllers import obtener_todos_los_productos


class SeleccionarProductoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Seleccionar Producto")
        self.setGeometry(100, 100, 800, 600)
        layout = QVBoxLayout()

        # Crear un QTabWidget para organizar los productos por categorías
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Obtener los productos y organizarlos por categorías
        productos = obtener_todos_los_productos()
        categorias = ["Entrada", "Plato principal", "Desayuno/Merienda", "Postre", "Alcohol", "No alcoholico", "Extra"]

        for categoria in categorias:
            tab = QWidget()
            grid_layout = QGridLayout()
            tab.setLayout(grid_layout)

            # Filtrar productos por categoría
            productos_categoria = [p for p in productos if p.categoria == categoria]

            # Agregar productos a la cuadrícula
            for i, producto in enumerate(productos_categoria):
                # Crear un botón con la imagen y el nombre del producto
                boton = QPushButton()
                boton.setText(producto.nombre)

                # Crear un QPixmap y cargar los datos de la imagen
                pixmap = QPixmap()
                if producto.imagen:
                    pixmap.loadFromData(QByteArray(producto.imagen))

                # Configurar el ícono del botón
                if not pixmap.isNull():  # Verificar que el QPixmap se cargó correctamente
                    boton.setIcon(QIcon(pixmap))
                else:
                    boton.setIcon(QIcon())  # Configurar un ícono vacío si no hay imagen

                boton.setIconSize(QSize(100, 100))  # Ajustar el tamaño del ícono
                boton.setStyleSheet("text-align: center;")  # Centrar el texto debajo del ícono
                boton.clicked.connect(lambda checked, p=producto: self.seleccionar_producto(p))

                # Agregar el botón a la cuadrícula
                row, col = divmod(i, 3)  # 3 columnas por fila
                grid_layout.addWidget(boton, row, col)

            self.tabs.addTab(tab, categoria)

        self.setLayout(layout)

    def seleccionar_producto(self, producto):
        self.selected_producto = producto
        self.accept()

    def obtener_producto_seleccionado(self):
        return getattr(self, "selected_producto", None)