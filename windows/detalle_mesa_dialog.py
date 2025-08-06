from PyQt5.QtWidgets import QWidget, QHeaderView, QSizePolicy, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox, QFormLayout, QInputDialog

from api_client import (
    cambiar_estado_comanda,
    cambiar_estado_mesa,
    obtener_comandas_por_mesa,
    crear_comanda,
    agregar_producto_a_comanda
)
from models import Comanda, DetalleComanda
from windows.agregar_producto_comanda_dialog import WidgetAgregarProductoComanda

class WidgetDetalleMesa(QWidget):
    def __init__(self, mesa, parent=None):
        super().__init__(parent)
        self.mesa = mesa
        self.comandas = []
        self.on_volver = None
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        layout = QVBoxLayout(self)
        
        info_layout = QFormLayout()
        detalle_layout = QHBoxLayout()
        detalle_layout.addWidget(QLabel(f"Mesa número: {str(mesa.numero)}"))
        detalle_layout.addWidget(QLabel(f"Estado: {mesa.estado}"))
        if mesa.estado == "Reservada":
            detalle_layout.addWidget(QLabel(f"Reservada a: {mesa.reservada_a}"))
        fila = QWidget()
        fila.setLayout(detalle_layout)

        info_layout.addRow(fila)
        layout.addLayout(info_layout)
        
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setHorizontalHeaderLabels(["ID", "Producto", "Cant.", "Estado", "Notas", "Ing. Excluidos", "Ing. Agregados", "Subtotal"])
        
        self.table.setColumnWidth(0, 40)
        self.table.setColumnWidth(1, 300)
        self.table.setColumnWidth(2, 40)
        self.table.setColumnWidth(3, 110)
        self.table.setColumnWidth(7, QHeaderView.Stretch)

        self.actualizar_comandas()
        layout.addWidget(self.table)

        botones_cobrar_layout = QHBoxLayout()
        self.boton_agregar_producto = QPushButton("Agregar Producto")
        self.boton_agregar_producto.clicked.connect(self.agregar_producto)
        self.boton_agregar_producto.setProperty("clase", "highlight2_btn")
        botones_cobrar_layout.addWidget(self.boton_agregar_producto)

        self.boton_cobrar = QPushButton("Cobrar")
        self.boton_cobrar.clicked.connect(self.cobrar)
        self.boton_cobrar.setProperty("clase", "highlight2_btn")
        botones_cobrar_layout.addWidget(self.boton_cobrar)

        layout.addLayout(botones_cobrar_layout)
        
        self.boton_volver = QPushButton("Volver")
        self.boton_volver.clicked.connect(self.volver)
        self.boton_volver.setProperty("clase", "highlight2_btn")
        layout.addWidget(self.boton_volver)

    def cambiar_estado(self, nuevo_estado):
        if nuevo_estado == "Reservada":
            nombre, ok = QInputDialog.getText(self, "Reservar Mesa", "Ingrese el nombre de la persona:")
            if ok and nombre:
                cambiar_estado_mesa(self.mesa.id, nuevo_estado, nombre)
        else:
            cambiar_estado_mesa(self.mesa.id, nuevo_estado)
        self.actualizar_comandas()

    def agregar_producto(self):
        if self.on_agregar_producto:
            self.on_agregar_producto(self.mesa)

    def procesar_agregado_producto(self, seleccion):
        producto, cantidad, notas = seleccion
        if producto:
            comanda_activa = next((comanda for comanda in self.comandas if comanda.estado == "Pendiente"), None)
            if not comanda_activa:
                comanda_id = crear_comanda(self.mesa.id)
                comanda_activa = Comanda(comanda_id, self.mesa.id, None, "Pendiente", "Comer en el lugar", None)
                self.comandas.append(comanda_activa)
            agregar_producto_a_comanda(comanda_activa.id, producto["id"], cantidad, notas)
            self.actualizar_comandas()
        self.ocultar_widget_agregar_producto()

    def ocultar_widget_agregar_producto(self):
        if hasattr(self, "widget_agregar") and self.widget_agregar is not None:
            self.layout().removeWidget(self.widget_agregar)
            self.widget_agregar.deleteLater()
            self.widget_agregar = None

    def actualizar_comandas(self):
        comandas_dict = obtener_comandas_por_mesa(self.mesa.id)
        self.comandas = []
        for c in comandas_dict:
            comanda = Comanda(
                c["id"],
                c["mesa_id"],
                c.get("fecha_hora"),
                c["estado"],
                c.get("tipo"),
                c.get("metodo_pago")
            )
            if "detalles" in c:
                comanda.detalles = [
                    DetalleComanda(
                        d["id"],
                        d["comanda_id"],
                        d["producto_id"],
                        d["producto_nombre"],
                        d["cantidad"],
                        d["estado"],
                        d.get("notas", ""),
                        d.get("ingredientes_excluidos", ""),
                        d.get("ingredientes_agregados", ""),
                        d["subtotal"]
                    )
                    for d in c["detalles"]
                ]
            self.comandas.append(comanda)

        detalles = []
        for comanda in self.comandas:
            for detalle in comanda.detalles:
                detalles.append((
                    comanda.id,
                    detalle.producto_nombre,
                    detalle.cantidad,
                    detalle.estado,
                    detalle.notas,
                    detalle.ingredientes_excluidos,
                    detalle.ingredientes_agregados,
                    detalle.subtotal
                ))

        self.table.setUpdatesEnabled(False)
        self.table.setSortingEnabled(False)
        self.table.clearContents()
        self.table.setRowCount(len(detalles))
        for row, d in enumerate(detalles):
            productoName = QTableWidgetItem(str(d[1]))
            productoName.setToolTip(d[1])
            self.table.setItem(row, 0, QTableWidgetItem(str(d[0])))
            self.table.setItem(row, 1, productoName)
            self.table.setItem(row, 2, QTableWidgetItem(str(d[2])))
            self.table.setItem(row, 3, QTableWidgetItem(d[3]))
            self.table.setItem(row, 4, QTableWidgetItem(d[4] if d[4] else ""))
            self.table.setItem(row, 5, QTableWidgetItem(d[5] if d[5] else ""))
            self.table.setItem(row, 6, QTableWidgetItem(d[6] if d[6] else ""))
            self.table.setItem(row, 7, QTableWidgetItem(f"${d[7]:.2f}"))
        self.table.setUpdatesEnabled(True)
        self.table.setSortingEnabled(True)

    def actualizar_tabla_comandas(self):
        detalles = []
        for comanda in self.comandas:
            detalles.extend(comanda.detalles)

        self.table.setUpdatesEnabled(False)
        self.table.setSortingEnabled(False)
        self.table.clearContents()
        self.table.setRowCount(len(detalles))
        for row, detalle in enumerate(detalles):
            self.table.setItem(row, 0, QTableWidgetItem(str(detalle.comanda_id)))
            self.table.setItem(row, 1, QTableWidgetItem(detalle.producto_nombre))
            self.table.setItem(row, 2, QTableWidgetItem(str(detalle.cantidad)))
            self.table.setItem(row, 3, QTableWidgetItem(detalle.estado))
            self.table.setItem(row, 4, QTableWidgetItem(detalle.notas if detalle.notas else ""))
            self.table.setItem(row, 5, QTableWidgetItem(detalle.ingredientes_excluidos if detalle.ingredientes_excluidos else ""))
            self.table.setItem(row, 6, QTableWidgetItem(detalle.ingredientes_agregados if detalle.ingredientes_agregados else ""))
            self.table.setItem(row, 7, QTableWidgetItem(f"${detalle.subtotal:.2f}"))
        self.table.setUpdatesEnabled(True)
        self.table.setSortingEnabled(True)

    def cobrar(self):
        total = sum(float(self.table.item(row, 7).text().replace('$', '')) for row in range(self.table.rowCount()))

        metodos_pago = ["Efectivo", "Tarjeta", "Mercado Pago"]
        metodo_pago, ok = QInputDialog.getItem(
            self,
            "Método de Pago",
            "Seleccione el método de pago:",
            metodos_pago,
            editable=False
        )

        if not ok:
            return

        if metodo_pago == "Efectivo":
            monto_pagado, ok = QInputDialog.getDouble(
                self,
                "Cobrar",
                f"El total a cobrar es: ${total:.2f}\nIngrese el monto pagado:",
                decimals=2
            )

            if not ok:
                return 

            if monto_pagado < total:
                QMessageBox.warning(self, "Monto Insuficiente", "El monto ingresado es menor que el total a cobrar.")
                return
            
            vuelto = monto_pagado - total

            QMessageBox.information(
                self,
                "Cobro Exitoso",
                f"Método de Pago: {metodo_pago}\nTotal: ${total:.2f}\nMonto Pagado: ${monto_pagado:.2f}\nVuelto: ${vuelto:.2f}"
            )
        else:
            QMessageBox.information(
                self,
                "Cobro Exitoso",
                f"Método de Pago: {metodo_pago}\nTotal: ${total:.2f}"
            )

        for comanda in self.comandas:
            cambiar_estado_comanda(comanda.id, "Pagado", metodo_pago)

        cambiar_estado_mesa(self.mesa.id, "Libre")

        self.actualizar_comandas()

        self.volver()
    
    def volver(self):
        if self.on_volver:
            self.on_volver()
        else:
            self.setParent(None)