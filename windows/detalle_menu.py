from PyQt5.QtWidgets import (
    QWidget, QFormLayout, QLineEdit, QDoubleSpinBox, QComboBox, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog
)
from PyQt5.QtCore import Qt, QByteArray
from PyQt5.QtGui import QPixmap
import base64
import os

from windows.gestionar_recetas_dialog import GestionarRecetasDialog

class DetalleMenu(QWidget):
    def __init__(self, producto, on_guardar, on_cancelar, modo="editar", parent=None):
        super().__init__(parent)
        self.producto = producto or {}
        self.on_guardar = on_guardar
        self.on_cancelar = on_cancelar
        self.modo = modo

        layout = QVBoxLayout(self)
        form = QFormLayout()
        self.nombre_edit = QLineEdit(self.producto.get("nombre", ""))
        form.addRow("Nombre:", self.nombre_edit)

        self.precio_edit = QDoubleSpinBox()
        self.precio_edit.setMaximum(999999)
        self.precio_edit.setValue(float(self.producto.get("precio", 0)))
        form.addRow("Precio:", self.precio_edit)

        self.categoria_combo = QComboBox()
        categorias = ["Entrada", "Plato principal", "Desayuno/Merienda", "Postre", "Alcohol", "No alcoholico", "Extra"]
        self.categoria_combo.addItems(categorias)
        if self.producto.get("categoria") in categorias:
            self.categoria_combo.setCurrentText(self.producto["categoria"])
        form.addRow("Categoría:", self.categoria_combo)

        self.imagen_label = QLabel()
        self.imagen_label.setFixedSize(150, 150)
        self.imagen_label.setAlignment(Qt.AlignCenter)
        if self.producto.get("imagen"):
            pixmap = QPixmap()
            pixmap.loadFromData(QByteArray.fromBase64(self.producto["imagen"].encode('utf-8')))
            self.imagen_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio))
        form.addRow("Imagen:", self.imagen_label)

        self.boton_cambiar_imagen = QPushButton("Cambiar Imagen")
        self.boton_cambiar_imagen.clicked.connect(self.cambiar_imagen)
        self.boton_cambiar_imagen.setProperty("clase", "highlight2_btn")
        self.boton_cambiar_imagen.setToolTip("Seleccionar una nueva imagen para el producto")
        form.addRow("", self.boton_cambiar_imagen)

        layout.addLayout(form)
        
        if self.modo != "agregar":
            self.boton_recetas = QPushButton("Gestionar Receta")
            self.boton_recetas.clicked.connect(self.gestionar_recetas)
            self.boton_recetas.setProperty("clase", "highlight2_btn")
            self.boton_recetas.setToolTip("Gestionar la receta del producto seleccionado")
            layout.addWidget(self.boton_recetas)

        botones = QHBoxLayout()
        self.boton_guardar = QPushButton("Agregar" if self.modo == "agregar" else "Guardar")
        self.boton_guardar.clicked.connect(self.guardar)
        self.boton_guardar.setProperty("clase", "highlight2_btn")
        self.boton_guardar.setToolTip("Guardar los cambios del producto")
        botones.addWidget(self.boton_guardar)
        self.boton_cancelar = QPushButton("Cancelar")
        self.boton_cancelar.clicked.connect(self.cancelar)
        self.boton_cancelar.setProperty("clase", "highlight2_btn")
        self.boton_cancelar.setToolTip("Cancelar la operación y volver al menú")
        botones.addWidget(self.boton_cancelar)
        layout.addLayout(botones)

        self.nueva_imagen = None

    def cambiar_imagen(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar Imagen", "", "Imágenes (*.png *.jpg *.jpeg *.bmp)")
        if archivo:
            pixmap = QPixmap(archivo)
            self.imagen_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio))
            self.nueva_imagen = archivo

    def guardar(self):
        imagen = self.nueva_imagen
        if imagen and os.path.isfile(imagen):
            with open(imagen, "rb") as f:
                imagen = base64.b64encode(f.read()).decode("utf-8")
        else:
            imagen = self.producto.get("imagen")

        datos = {
            "id": self.producto.get("id"),
            "nombre": self.nombre_edit.text(),
            "precio": self.precio_edit.value(),
            "categoria": self.categoria_combo.currentText(),
            "imagen": imagen
        }
        self.on_guardar(datos)

    def cancelar(self):
        self.on_cancelar()

    def gestionar_recetas(self):
        producto_id = self.producto["id"]
        nombre_producto = self.producto["nombre"]
        dialog = GestionarRecetasDialog(producto_id, nombre_producto, self)
        dialog.exec_()