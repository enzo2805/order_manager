from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QSpinBox, QLineEdit, QHBoxLayout
from windows.seleccionar_producto_dialog import SeleccionarProductoDialog

class AgregarProductoComandaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar Producto a Comanda")
        self.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout()

        # Botón para seleccionar un producto
        self.boton_seleccionar_producto = QPushButton("Seleccionar Producto")
        self.boton_seleccionar_producto.clicked.connect(self.seleccionar_producto)
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
        self.boton_aceptar.clicked.connect(self.accept)
        botones_layout.addWidget(self.boton_aceptar)

        self.boton_cancelar = QPushButton("Cancelar")
        self.boton_cancelar.clicked.connect(self.reject)
        botones_layout.addWidget(self.boton_cancelar)

        layout.addLayout(botones_layout)
        self.setLayout(layout)

        self.producto_seleccionado = None

    def seleccionar_producto(self):
        dialog = SeleccionarProductoDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.producto_seleccionado = dialog.obtener_producto_seleccionado()
            self.label_producto_seleccionado.setText(f"Producto seleccionado: {self.producto_seleccionado.nombre}")

    def obtener_seleccion(self):
        return self.producto_seleccionado, self.cantidad_input.value(), self.notas_input.text()
