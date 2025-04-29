from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QInputDialog, QMessageBox, QCompleter, QDialog, QVBoxLayout, QCompleter, QLineEdit, QDialogButtonBox, QLabel
from PyQt5.QtCore import Qt
from controllers import obtener_recetas_por_producto, agregar_receta, editar_receta, eliminar_receta, obtener_todos_los_ingredientes

class GestionarRecetasDialog(QDialog):
    def __init__(self, producto_id, nombre_producto, parent=None):
        super().__init__(parent)
        self.producto_id = producto_id
        self.setWindowTitle(f"Gestionar Recetas - {nombre_producto}")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setRowCount(0)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Ingrediente", "Cantidad Necesaria", "Unidad"])
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
            self.table.setItem(row, 0, QTableWidgetItem(str(receta[0])))
            self.table.setItem(row, 1, QTableWidgetItem(receta[2]))
            self.table.setItem(row, 2, QTableWidgetItem(str(receta[3])))
            self.table.setItem(row, 3, QTableWidgetItem(receta[4]))

    def agregar_ingrediente(self):
        ingredientes = obtener_todos_los_ingredientes()  # Esta función debe devolver una lista de tuplas (id, nombre)
        nombres_ingredientes = [ingrediente[1] for ingrediente in ingredientes]

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
            ingrediente_id = next((ingrediente[0] for ingrediente in ingredientes if ingrediente[1] == nombre_ingrediente), None)

            if ingrediente_id is None:
                QMessageBox.warning(self, "Ingrediente no encontrado", "El ingrediente ingresado no existe.")
                return

            cantidad_necesaria, ok = QInputDialog.getDouble(self, "Agregar Ingrediente", "Ingrese la cantidad necesaria:")
            if not ok:
                return

            agregar_receta(self.producto_id, ingrediente_id, cantidad_necesaria)
            self.actualizar_recetas()
            dialog.accept()
        
        button_box.accepted.connect(aceptar)
        button_box.rejected.connect(dialog.reject)

        dialog.exec_()


    def editar_ingrediente(self):
        fila_seleccionada = self.table.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Editar Ingrediente", "Por favor, seleccione un ingrediente para editar.")
            return

        receta_id = int(self.table.item(fila_seleccionada, 0).text())
        cantidad_actual = float(self.table.item(fila_seleccionada, 2).text())

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

        receta_id = int(self.table.item(fila_seleccionada, 0).text())
        eliminar_receta(receta_id)
        self.actualizar_recetas()
    