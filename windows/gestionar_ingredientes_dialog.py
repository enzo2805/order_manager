from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QMessageBox, QInputDialog
from api_client import obtener_ingredientes, agregar_ingrediente, editar_ingrediente, eliminar_ingrediente

class GestionarIngredientesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gestionar Ingredientes")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Stock", "Stock Mínimo", "Unidad"])
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

        self.cargar_ingredientes()

    def cargar_ingredientes(self):
        # Llama a la API para obtener los ingredientes
        ingredientes = obtener_ingredientes()
        self.table.setRowCount(len(ingredientes))
        for row, ingrediente in enumerate(ingredientes):
            self.table.setItem(row, 0, QTableWidgetItem(str(ingrediente["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(ingrediente["nombre"]))
            self.table.setItem(row, 2, QTableWidgetItem(str(ingrediente["stock"])))
            self.table.setItem(row, 3, QTableWidgetItem(str(ingrediente["stock_minimo"])))
            self.table.setItem(row, 4, QTableWidgetItem(ingrediente["unidad"]))

    def agregar_ingrediente(self):
        nombre, ok = QInputDialog.getText(self, "Agregar Ingrediente", "Ingrese el nombre del ingrediente:")
        if not ok or not nombre:
            return

        stock, ok = QInputDialog.getInt(self, "Agregar Ingrediente", "Ingrese el stock inicial:")
        if not ok:
            return

        stock_minimo, ok = QInputDialog.getInt(self, "Agregar Ingrediente", "Ingrese el stock mínimo:")
        if not ok:
            return

        unidad, ok = QInputDialog.getText(self, "Agregar Ingrediente", "Ingrese la unidad (e.g., kg, litros):")
        if not ok or not unidad:
            return

        # Llama a la API para agregar el ingrediente
        agregar_ingrediente(nombre, stock, stock_minimo, unidad)
        self.cargar_ingredientes()

    def editar_ingrediente(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Editar Ingrediente", "Seleccione un ingrediente para editar.")
            return

        ingrediente_id = int(self.table.item(row, 0).text())
        nombre, ok = QInputDialog.getText(self, "Editar Ingrediente", "Ingrese el nuevo nombre del ingrediente:", text=self.table.item(row, 1).text())
        if not ok or not nombre:
            return

        stock, ok = QInputDialog.getInt(self, "Editar Ingrediente", "Ingrese el nuevo stock:", value=int(self.table.item(row, 2).text()))
        if not ok:
            return

        stock_minimo, ok = QInputDialog.getInt(self, "Editar Ingrediente", "Ingrese el nuevo stock mínimo:", value=int(self.table.item(row, 3).text()))
        if not ok:
            return

        unidad, ok = QInputDialog.getText(self, "Editar Ingrediente", "Ingrese la nueva unidad:", text=self.table.item(row, 4).text())
        if not ok or not unidad:
            return

        # Llama a la API para editar el ingrediente
        editar_ingrediente(ingrediente_id, nombre, stock, stock_minimo, unidad)
        self.cargar_ingredientes()

    def eliminar_ingrediente(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Eliminar Ingrediente", "Seleccione un ingrediente para eliminar.")
            return

        ingrediente_id = int(self.table.item(row, 0).text())
        respuesta = QMessageBox.question(self, "Eliminar Ingrediente", "¿Está seguro de que desea eliminar este ingrediente?", QMessageBox.Yes | QMessageBox.No)
        if respuesta == QMessageBox.Yes:
            # Llama a la API para eliminar el ingrediente
            eliminar_ingrediente(ingrediente_id)
            self.cargar_ingredientes()