from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QMessageBox, QInputDialog
from api_client import agregar_producto_a_comanda, crear_comanda_para_llevar, cambiar_estado_comanda
from windows.agregar_producto_comanda_dialog import AgregarProductoComandaDialog


class DetalleComandaParaLlevarDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Comanda Para Llevar")
        self.setGeometry(100, 100, 600, 400)

        self.productos = []

        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Producto", "Cantidad", "Notas", "Subtotal"])
        layout.addWidget(self.table)

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
        self.table.setRowCount(len(self.productos))
        for row, detalle in enumerate(self.productos):
            self.table.setItem(row, 0, QTableWidgetItem(detalle["nombre"]))
            self.table.setItem(row, 1, QTableWidgetItem(str(detalle["cantidad"])))
            self.table.setItem(row, 2, QTableWidgetItem(detalle["notas"]))
            subtotal = detalle.get("subtotal", 0)
            self.table.setItem(row, 3, QTableWidgetItem(f"${subtotal:.2f}"))

    def agregar_producto(self):
        dialog = AgregarProductoComandaDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            producto, cantidad, notas = dialog.obtener_seleccion()
            if producto:
                subtotal = producto.get("precio", 0) * cantidad
                self.productos.append({
                    "id": producto["id"],
                    "nombre": producto["nombre"],
                    "cantidad": cantidad,
                    "notas": notas,
                    "subtotal": subtotal
                })
                self.actualizar_tabla()
                QMessageBox.information(self, "Producto Agregado", f"Producto '{producto['nombre']}' agregado a la comanda.")

    def finalizar_comanda(self):
        if not self.productos:
            QMessageBox.warning(self, "Sin productos", "Debes agregar al menos un producto.")
            return

        comanda = crear_comanda_para_llevar()
        comanda_id = comanda["id"]

        for detalle in self.productos:
            agregar_producto_a_comanda(
                comanda_id=comanda_id,
                producto_id=detalle["id"],
                cantidad=detalle["cantidad"],
                notas=detalle.get("notas", "")
            )

        cambiar_estado_comanda(comanda_id, "Pendiente")

        QMessageBox.information(
            self,
            "Comanda Finalizada",
            "La comanda ha sido creada y marcada como 'Pendiente'. Ahora está lista para ser tomada por un cocinero."
        )

        self.accept()