from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QGridLayout, QToolButton, QHBoxLayout,
    QMessageBox, QSizePolicy
)
from PyQt5.QtCore import Qt, QSize, QByteArray
from PyQt5.QtGui import QPixmap, QIcon
from api_client import obtener_productos, agregar_producto, editar_producto, eliminar_producto
from windows.detalle_menu import DetalleMenu

class WidgetMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        self.setStyleSheet("""
            QTabBar::tab {
                font-size: 18px;
                min-width: 150px;
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
        """)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        botones_layout = QVBoxLayout()
        self.boton_agregar = QToolButton()
        self.boton_agregar.setText("Agregar Producto")
        self.boton_agregar.clicked.connect(self.agregar_producto)
        self.boton_agregar.setProperty("clase", "highlight1_btn")
        self.boton_agregar.setToolTip("Agregar un nuevo producto al menú")
        botones_layout.addWidget(self.boton_agregar)

        self.boton_eliminar = QToolButton()
        self.boton_eliminar.setText("Eliminar Producto")
        self.boton_eliminar.clicked.connect(self.eliminar_producto)
        self.boton_eliminar.setProperty("clase", "highlight1_btn")
        self.boton_eliminar.setToolTip("Eliminar el producto seleccionado")
        botones_layout.addWidget(self.boton_eliminar)

        layout.addLayout(botones_layout)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        self.producto_seleccionado = None
        self.botones_productos = {}

        self.actualizar_menu()

    def actualizar_menu(self):
        self.tabs.clear()
        self.producto_seleccionado = None
        self.botones_productos = {}

        productos = obtener_productos()
        categorias = ["Entrada", "Plato principal", "Desayuno/Merienda", "Postre", "Alcohol", "No alcoholico", "Extra"]

        for categoria in categorias:
            tab = QWidget()
            grid_layout = QGridLayout(tab)
            productos_categoria = [p for p in productos if p["categoria"] == categoria]
            for i, producto in enumerate(productos_categoria):
                boton = QToolButton()
                boton.setText(f"{producto['nombre']}\n${producto['precio']:.2f}")
                boton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
                boton.setToolTip(f"{producto['nombre']}")
                boton.setFixedSize(200, 220)
                pixmap = QPixmap()
                if producto["imagen"]:
                    imagen_bytes = QByteArray.fromBase64(producto["imagen"].encode('utf-8'))
                    pixmap.loadFromData(imagen_bytes)
                if not pixmap.isNull():
                    boton.setIcon(QIcon(pixmap))
                else:
                    boton.setIcon(QIcon())
                boton.setIconSize(QSize(150, 150))
                boton.clicked.connect(lambda checked, p=producto: self.seleccionar_producto(p))
                row, col = divmod(i, 3)
                grid_layout.addWidget(boton, row, col)
                self.botones_productos[producto["id"]] = boton
            self.tabs.addTab(tab, categoria)
            self.tabs.setTabToolTip(self.tabs.indexOf(tab), categoria)

    def seleccionar_producto(self, producto):
        self.producto_seleccionado = producto
        self.tabs.setVisible(False)
        if hasattr(self, "detalle_widget") and self.detalle_widget:
            self.layout().removeWidget(self.detalle_widget)
            self.detalle_widget.deleteLater()
        self.detalle_widget = DetalleMenu(
            producto,
            on_guardar=self.guardar_detalle_producto,
            on_cancelar=self.cancelar_detalle_producto,
            parent=self
        )
        self.layout().addWidget(self.detalle_widget)

    def agregar_producto(self):
        self.tabs.setVisible(False)
        if hasattr(self, "detalle_widget") and self.detalle_widget:
            self.layout().removeWidget(self.detalle_widget)
            self.detalle_widget.deleteLater()
        self.detalle_widget = DetalleMenu(
            producto={},
            on_guardar=self.guardar_nuevo_producto,
            on_cancelar=self.cancelar_detalle_producto,
            modo="agregar",
            parent=self
        )
        self.layout().addWidget(self.detalle_widget)

    def guardar_nuevo_producto(self, datos):
        agregar_producto(datos["nombre"], datos["precio"], datos["categoria"], datos["imagen"])
        self.cancelar_detalle_producto()
        self.actualizar_menu()

    def eliminar_producto(self):
        if not self.producto_seleccionado:
            QMessageBox.warning(self, "Eliminar Producto", "Por favor, seleccione un producto para eliminar.")
            return
        producto_id = self.producto_seleccionado["id"]
        respuesta = QMessageBox.question(self, "Eliminar Producto", "¿Está seguro de que desea eliminar este producto?", QMessageBox.Yes | QMessageBox.No)
        if respuesta == QMessageBox.Yes:
            eliminar_producto(producto_id)
            self.actualizar_menu()

    def guardar_detalle_producto(self, datos):
        editar_producto(datos["id"], datos["nombre"], datos["precio"], datos["categoria"], datos["imagen"])
        self.cancelar_detalle_producto()
        self.actualizar_menu()

    def cancelar_detalle_producto(self):
        if hasattr(self, "detalle_widget") and self.detalle_widget:
            self.layout().removeWidget(self.detalle_widget)
            self.detalle_widget.deleteLater()
            self.detalle_widget = None
        self.tabs.setVisible(True)