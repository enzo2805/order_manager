from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QInputDialog, QMessageBox, QCompleter, QLineEdit, QDialogButtonBox, QLabel
from PyQt5.QtCore import Qt
from api_client import (
    eliminar_ingrediente_de_receta,
    obtener_recetas_por_producto,
    agregar_receta,
    editar_receta,
    obtener_ingredientes
)

class GestionarRecetasDialog(QDialog):
    def __init__(self, producto_id, nombre_producto, parent=None):
        super().__init__(parent)
        self.producto_id = producto_id
        self.setWindowTitle(f"Gestionar Recetas - {nombre_producto}")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;  /* Color de fondo claro */
                border: 1px solid #ccc;  /* Borde sutil */
                border-radius: 8px;  /* Bordes redondeados */
            }
            QTableWidget {
                background-color: #ffffff;  /* Fondo blanco para la tabla */
                border: 1px solid #ccc;  /* Borde de la tabla */
                border-radius: 4px;  /* Bordes redondeados para la tabla */
            }  
            QTableWidget::item {
                border-bottom: 1px solid #ddd;  /* Línea divisoria entre filas */
                font-size: 14px;  /* Tamaño de fuente de los items */
            }
            QTablePanel {
                background-color: #f9f9f9;  /* Color de fondo del panel
                border: 1px solid #ddd;  /* Borde del panel */
            }
            QTableWidget::item:selected {
                background-color: #d0e7ff;  /* Color de fondo al seleccionar */
                color: #000;  /* Color de texto al seleccionar */
            }
            QPushButton {
                background-color: #4CAF50;  /* Color de fondo verde */
                color: white;  /* Color de texto blanco */
                border: none;  /* Sin borde */
                border-radius: 4px;  /* Bordes redondeados */
                padding: 10px 20px;  /* Espaciado interno */
                font-size: 16px;  /* Tamaño de fuente */
            }
            QPushButton:hover {
                background-color: #45a049;  /* Color de fondo verde más oscuro al pasar
                por encima */
            }
            
        """)

        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setRowCount(0)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Ingrediente", "Cant. Necesaria", "Unidad"])
        self.actualizar_recetas()

        layout.addWidget(self.table)

        botones_layout = QHBoxLayout()
        self.boton_agregar = QPushButton("Agregar Ingrediente")
        self.boton_agregar.clicked.connect(self.agregar_ingrediente)
        botones_layout.addWidget(self.boton_agregar)

        self.boton_editar = QPushButton("Editar Ingrediente")
        self.boton_editar.clicked.connect(self.editar_ingrediente)
        botones_layout.addWidget(self.boton_editar)

        self.boton_eliminar = QPushButton("Eliminar Ingrediente")
        self.boton_eliminar.clicked.connect(self.eliminar_ingrediente)
        botones_layout.addWidget(self.boton_eliminar)

        layout.addLayout(botones_layout)
        self.setLayout(layout)

    def actualizar_recetas(self):
        recetas = obtener_recetas_por_producto(self.producto_id)
        self.table.setRowCount(len(recetas))
        for row, receta in enumerate(recetas):
            item_nombre = QTableWidgetItem(receta["nombre"])
            item_nombre.setData(Qt.UserRole, receta["id"])
            self.table.setItem(row, 0, item_nombre)
            self.table.setItem(row, 1, QTableWidgetItem(str(receta["cantidad_necesaria"])))
            self.table.setItem(row, 2, QTableWidgetItem(receta["unidad"]))

    def agregar_ingrediente(self):
        ingredientes = obtener_ingredientes()
        nombres_ingredientes = [ingrediente["nombre"] for ingrediente in ingredientes]

        dialog = QDialog(self)
        dialog.setWindowTitle("Agregar Ingrediente")
        layout = QVBoxLayout(dialog)

        label_nombre = QLabel("Ingrese el nombre del ingrediente:")
        layout.addWidget(label_nombre)

        line_edit = QLineEdit(dialog)
        completer = QCompleter(nombres_ingredientes, self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        line_edit.setCompleter(completer)
        layout.addWidget(line_edit)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
        layout.addWidget(button_box)

        def aceptar():
            nombre_ingrediente = line_edit.text()
            ingrediente = next((ing for ing in ingredientes if ing["nombre"] == nombre_ingrediente), None)

            if ingrediente is None:
                QMessageBox.warning(self, "Ingrediente no encontrado", "El ingrediente ingresado no existe.")
                return

            cantidad_necesaria, ok = QInputDialog.getDouble(self, "Agregar Ingrediente", "Ingrese la cantidad necesaria:")
            if not ok:
                return

            agregar_receta(self.producto_id, ingrediente["id"], cantidad_necesaria)
            self.actualizar_recetas()
            dialog.accept()

        button_box.accepted.connect(aceptar)
        button_box.rejected.connect(dialog.reject)

        dialog.exec_()

    def editar_ingrediente(self):
        fila_seleccionada = self.table.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Eliminar Ingrediente", "Por favor, seleccione un ingrediente para eliminar.")
            return

        item_nombre = self.table.item(fila_seleccionada, 0)
        receta_id = item_nombre.data(Qt.UserRole)
        cantidad_actual = float(self.table.item(fila_seleccionada, 1).text())

        cantidad_necesaria, ok = QInputDialog.getDouble(self, "Editar Ingrediente", "Ingrese la nueva cantidad necesaria:", value=cantidad_actual)
        if not ok:
            return

        editar_receta(receta_id, cantidad_necesaria)
        self.actualizar_recetas()

    def eliminar_ingrediente(self):
        fila_seleccionada = self.table.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Eliminar Ingrediente", "Por favor, seleccione un ingrediente para eliminar.")
            return

        item_nombre = self.table.item(fila_seleccionada, 0)
        receta_id = item_nombre.data(Qt.UserRole)
        eliminar_ingrediente_de_receta(receta_id)
        self.actualizar_recetas()