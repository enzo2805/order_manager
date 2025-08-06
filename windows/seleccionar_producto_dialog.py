from PyQt5.QtWidgets import QWidget, QVBoxLayout, QToolButton, QTabWidget, QGridLayout
from PyQt5.QtCore import QByteArray, QSize, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QIcon
from api_client import obtener_productos

class WidgetSeleccionarProducto(QWidget):
    producto_seleccionado = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.setStyleSheet("""
            QTabBar::tab {
                font-size: 18px;
                min-width: 100px;
                min-height: 40px;
            }
            QTabBar::tab:selected {
                background: #388e3c;
                color: #fff;
            }
            QTabBar::tab:hover {
                background: #1565c0;
            }
            QTabWidget::pane {
                border: 2px solid #1976d2;
                border-radius: 8px;
                margin-top: 2px;
            }
            QPushButton[clase="highlight1_btn"] {
                font-size: 20px;
                padding: 10px;
            }
        """)

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
                boton = QToolButton()
                boton.setText(producto["nombre"])
                boton.setProperty("clase", "highlight1_btn")
                boton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

                pixmap = QPixmap()
                if producto["imagen"]:
                    imagen_bytes = QByteArray.fromBase64(producto["imagen"].encode('utf-8'))
                    pixmap.loadFromData(imagen_bytes)

                if not pixmap.isNull():
                    boton.setIcon(QIcon(pixmap))
                else:
                    boton.setIcon(QIcon())

                boton.setIconSize(QSize(250, 250))
                boton.setStyleSheet("text-align: center;")
                boton.clicked.connect(lambda checked, p=producto: self.seleccionar_producto(p))

                row, col = divmod(i, 3)
                grid_layout.addWidget(boton, row, col)

            self.tabs.addTab(tab, categoria)

    def seleccionar_producto(self, producto):
        self.producto_seleccionado.emit(producto)