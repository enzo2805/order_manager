from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QDialog, QTabWidget, QWidget, QGridLayout
from PyQt5.QtCore import QByteArray, QSize
from PyQt5.QtGui import QPixmap, QIcon
from api_client import obtener_productos


class SeleccionarProductoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Seleccionar Producto")
        self.setGeometry(100, 100, 800, 600)
        layout = QVBoxLayout()

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        productos = obtener_productos()
        categorias = ["Entrada", "Plato principal", "Desayuno/Merienda", "Postre", "Alcohol", "No alcoholico", "Extra"]

        for categoria in categorias:
            tab = QWidget()
            grid_layout = QGridLayout()
            tab.setLayout(grid_layout)

            productos_categoria = [p for p in productos if p["categoria"] == categoria]

            for i, producto in enumerate(productos_categoria):
                boton = QPushButton()
                boton.setText(producto["nombre"])

                pixmap = QPixmap()
                if producto["imagen"]:
                    imagen_bytes = QByteArray.fromBase64(producto["imagen"].encode('utf-8'))
                    pixmap.loadFromData(imagen_bytes)

                if not pixmap.isNull():
                    boton.setIcon(QIcon(pixmap))
                else:
                    boton.setIcon(QIcon())

                boton.setIconSize(QSize(100, 100))
                boton.setStyleSheet("text-align: center;") 
                boton.clicked.connect(lambda checked, p=producto: self.seleccionar_producto(p))

                row, col = divmod(i, 3) 
                grid_layout.addWidget(boton, row, col)

            self.tabs.addTab(tab, categoria)

        self.setLayout(layout)

    def seleccionar_producto(self, producto):
        self.selected_producto = producto
        self.accept()

    def obtener_producto_seleccionado(self):
        return getattr(self, "selected_producto", None)