from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QMessageBox
from controllers import agregar_producto_a_comanda, obtener_detalles_comanda, cambiar_estado_comanda
from windows.agregar_producto_comanda_dialog import AgregarProductoComandaDialog

class DetalleComandaParaLlevarDialog(QDialog):
    def __init__(self, comanda_id, parent=None):
        super().__init__(parent)
        self.comanda_id = comanda_id
        self.setWindowTitle(f"Comanda Para Llevar - ID: {comanda_id}")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        # Tabla para mostrar los detalles de la comanda
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Producto", "Cantidad", "Notas", "Subtotal"])
        layout.addWidget(self.table)

        # Botones para agregar productos y finalizar la comanda
        botones_layout = QHBoxLayout()
        self.boton_agregar_producto = QPushButton("Agregar Producto")
        self.boton_agregar_producto.clicked.connect(self.agregar_producto)
        botones_layout.addWidget(self.boton_agregar_producto)

        self.boton_finalizar = QPushButton("Finalizar Comanda")
        self.boton_finalizar.clicked.connect(self.finalizar_comanda)
        botones_layout.addWidget(self.boton_finalizar)

        layout.addLayout(botones_layout)
        self.setLayout(layout)

        self.actualizar_tabla()

    def actualizar_tabla(self):
        detalles = obtener_detalles_comanda(self.comanda_id)
        self.table.setRowCount(len(detalles))
        for row, detalle in enumerate(detalles):
            self.table.setItem(row, 0, QTableWidgetItem(detalle.producto_nombre))
            self.table.setItem(row, 1, QTableWidgetItem(str(detalle.cantidad)))
            self.table.setItem(row, 2, QTableWidgetItem(detalle.notas))
            self.table.setItem(row, 3, QTableWidgetItem(f"${detalle.subtotal:.2f}"))

    def agregar_producto(self):
        dialog = AgregarProductoComandaDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            producto, cantidad, notas = dialog.obtener_seleccion()
            if producto:
                agregar_producto_a_comanda(comanda_id=self.comanda_id, producto_id=producto.id, cantidad=cantidad, notas=notas)
                self.actualizar_tabla()
                QMessageBox.information(self, "Producto Agregado", f"Producto '{producto.nombre}' agregado a la comanda.")

    def finalizar_comanda(self):
        cambiar_estado_comanda(self.comanda_id, "Pagado")
        QMessageBox.information(self, "Comanda Finalizada", "La comanda ha sido finalizada.")
        self.accept()