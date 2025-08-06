from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QCheckBox

class WidgetBotoneraMesas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.check_edicion = QCheckBox("Modo Edición")
        self.check_edicion.setProperty("clase", "highlight1_btn")
        self.boton_guardar = QPushButton("Guardar")
        self.boton_guardar.setProperty("clase", "highlight1_btn")
        self.boton_crear = QPushButton("Crear Mesa")
        self.boton_crear.setProperty("clase", "highlight1_btn")
        self.boton_eliminar = QPushButton("Eliminar Mesa")
        self.boton_eliminar.setProperty("clase", "highlight1_btn")
        layout.addWidget(self.check_edicion)
        layout.addWidget(self.boton_guardar)
        layout.addWidget(self.boton_crear)
        layout.addWidget(self.boton_eliminar)
        layout.addStretch()
        self.setFixedWidth(300)