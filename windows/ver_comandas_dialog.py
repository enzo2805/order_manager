from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout
from controllers import obtener_todas_las_comandas, obtener_detalles_comanda

class VerComandasDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ver Comandas")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Tipo", "Estado", "Mesa", "Fecha/Hora"])
        layout.addWidget(self.table)

        botones_layout = QHBoxLayout()
        self.boton_cerrar = QPushButton("Cerrar")
        self.boton_cerrar.clicked.connect(self.close)
        botones_layout.addWidget(self.boton_cerrar)

        layout.addLayout(botones_layout)
        self.setLayout(layout)

        self.cargar_comandas()

    def cargar_comandas(self):
        comandas = obtener_todas_las_comandas()
        self.table.setRowCount(len(comandas))
        for row, comanda in enumerate(comandas):
            self.table.setItem(row, 0, QTableWidgetItem(str(comanda.id)))
            self.table.setItem(row, 1, QTableWidgetItem(comanda.tipo))
            self.table.setItem(row, 2, QTableWidgetItem(comanda.estado))
            self.table.setItem(row, 3, QTableWidgetItem(str(comanda.mesa_id) if comanda.mesa_id else "N/A"))
            self.table.setItem(row, 4, QTableWidgetItem(comanda.fecha_hora))