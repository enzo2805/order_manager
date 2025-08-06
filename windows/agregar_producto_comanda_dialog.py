from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSpinBox, QLineEdit, QHBoxLayout
from windows.seleccionar_producto_dialog import WidgetSeleccionarProducto

class WidgetAgregarProductoComanda(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        self.boton_seleccionar_producto = QPushButton("Seleccionar Producto")
        self.boton_seleccionar_producto.clicked.connect(self.seleccionar_producto)
        self.boton_seleccionar_producto.setProperty("clase", "highlight2_btn")
        self.boton_seleccionar_producto.setToolTip("Seleccionar un producto para agregar a la comanda")
        layout.addWidget(self.boton_seleccionar_producto)

        self.label_producto_seleccionado = QLabel("Producto seleccionado: Ninguno")
        layout.addWidget(self.label_producto_seleccionado)

        self.cantidad_input = QSpinBox()
        self.cantidad_input.setRange(1, 100)
        layout.addWidget(QLabel("Cantidad:"))
        layout.addWidget(self.cantidad_input)

        self.notas_input = QLineEdit()
        layout.addWidget(QLabel("Notas:"))
        layout.addWidget(self.notas_input)

        botones_layout = QHBoxLayout()
        self.boton_aceptar = QPushButton("Aceptar")
        self.boton_aceptar.clicked.connect(self.aceptar)
        self.boton_aceptar.setProperty("clase", "highlight2_btn")
        self.boton_aceptar.setToolTip("Aceptar y agregar el producto a la comanda")
        botones_layout.addWidget(self.boton_aceptar)

        self.boton_cancelar = QPushButton("Cancelar")
        self.boton_cancelar.clicked.connect(self.cancelar)
        self.boton_cancelar.setProperty("clase", "highlight2_btn")
        self.boton_cancelar.setToolTip("Cancelar la operación")
        botones_layout.addWidget(self.boton_cancelar)

        layout.addLayout(botones_layout)

        self.producto_seleccionado = None
        self.on_aceptar = None
        self.on_cancelar = None

    def seleccionar_producto(self):
        self.selector = WidgetSeleccionarProducto()
        self.selector.producto_seleccionado.connect(self.producto_seleccionado_callback)
        self.selector.setWindowModality(True)
        self.selector.setWindowTitle("Seleccionar producto")
        self.selector.resize(400, 400)
        self.selector.show()

    def producto_seleccionado_callback(self, producto):
        self.producto_seleccionado = producto
        self.label_producto_seleccionado.setText(f"Producto seleccionado: {producto['nombre']}")
        self.selector.close()

    def obtener_seleccion(self):
        return self.producto_seleccionado, self.cantidad_input.value(), self.notas_input.text()

    def aceptar(self):
        if self.on_aceptar:
            self.on_aceptar(self.obtener_seleccion())

    def cancelar(self):
        if self.on_cancelar:
            self.on_cancelar()