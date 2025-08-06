from PyQt5.QtWidgets import QSizePolicy, QWidget, QHeaderView, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt
from api_client import obtener_todas_las_comandas

class WidgetComandas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setHorizontalHeaderLabels(["ID", "Tipo", "Estado", "Mesa", "Fecha/Hora"])
        
        self.table.setSortingEnabled(True)
        self.table.sortByColumn(4, Qt.DescendingOrder)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        layout.addWidget(self.table)

        botones_layout = QHBoxLayout()
        self.boton_actualizar = QPushButton("Actualizar")
        self.boton_actualizar.setProperty("clase", "highlight2_btn")
        self.boton_actualizar.setToolTip("Actualizar la lista de comandas")
        self.boton_actualizar.clicked.connect(self.cargar_comandas)
        botones_layout.addWidget(self.boton_actualizar)

        layout.addLayout(botones_layout)

        self.cargar_comandas()

    def cargar_comandas(self):
        self.table.setRowCount(0)
        self.table.clearContents()
        comandas = obtener_todas_las_comandas()
        self.table.setRowCount(len(comandas))
        for row, comanda in enumerate(comandas):
            self.table.setItem(row, 0, QTableWidgetItem(str(comanda["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(comanda.get("tipo", "")))
            self.table.setItem(row, 2, QTableWidgetItem(comanda.get("estado", "")))
            self.table.setItem(row, 3, QTableWidgetItem(str(comanda.get("mesa_id", "")) if comanda.get("mesa_id") else "N/A"))
            self.table.setItem(row, 4, QTableWidgetItem(comanda.get("fecha_hora", "")))