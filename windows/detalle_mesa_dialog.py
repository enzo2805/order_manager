from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox, QFormLayout, QInputDialog

from api_client import (
    cambiar_estado_comanda,
    cambiar_estado_mesa,
    obtener_comandas_por_mesa,
    crear_comanda,
    agregar_producto_a_comanda
)
from models import Comanda, DetalleComanda
from windows.agregar_producto_comanda_dialog import AgregarProductoComandaDialog

class DetalleMesaDialog(QDialog):
    def __init__(self, mesa, comandas, parent=None):
        super().__init__(parent)
        self.mesa = mesa
        self.comandas = []  # Inicializar como una lista vacía
        self.setWindowTitle(f"Detalle de Mesa {mesa.numero}")
        self.setGeometry(100, 100, 600, 400)
        layout = QVBoxLayout()
        
        info_layout = QFormLayout()
        info_layout.addRow("Número:", QLabel(str(mesa.numero)))
        info_layout.addRow("Estado:", QLabel(mesa.estado))
        if mesa.estado == "Reservada":
            info_layout.addRow("Reservada a:", QLabel(mesa.reservada_a))
        layout.addLayout(info_layout)
        
        botones_layout = QHBoxLayout()
        self.boton_libre = QPushButton("Libre")
        self.boton_libre.clicked.connect(lambda: self.cambiar_estado("Libre"))
        botones_layout.addWidget(self.boton_libre)

        self.boton_ocupada = QPushButton("Ocupada")
        self.boton_ocupada.clicked.connect(lambda: self.cambiar_estado("Ocupada"))
        botones_layout.addWidget(self.boton_ocupada)

        self.boton_reservada = QPushButton("Reservada")
        self.boton_reservada.clicked.connect(lambda: self.cambiar_estado("Reservada"))
        botones_layout.addWidget(self.boton_reservada)

        layout.addLayout(botones_layout)
        
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["ID Comanda", "Producto", "Cantidad", "Estado", "Notas", "Ing. Excluidos", "Ing. Agregados", "Subtotal"])
        
        # Llamar a actualizar_comandas para inicializar self.comandas
        self.actualizar_comandas()

        layout.addWidget(self.table)

        botones_cobrar_layout = QHBoxLayout()
        self.boton_agregar_producto = QPushButton("Agregar Producto")
        self.boton_agregar_producto.clicked.connect(self.agregar_producto)
        botones_cobrar_layout.addWidget(self.boton_agregar_producto)

        self.boton_cobrar = QPushButton("Cobrar")
        self.boton_cobrar.clicked.connect(self.cobrar)
        botones_cobrar_layout.addWidget(self.boton_cobrar)

        layout.addLayout(botones_cobrar_layout)

        self.setLayout(layout)

    def cambiar_estado(self, nuevo_estado):
        if nuevo_estado == "Reservada":
            nombre, ok = QInputDialog.getText(self, "Reservar Mesa", "Ingrese el nombre de la persona:")
            if ok and nombre:
                cambiar_estado_mesa(self.mesa.id, nuevo_estado, nombre)
        else:
            cambiar_estado_mesa(self.mesa.id, nuevo_estado)
        self.accept()

    def agregar_producto(self):
        dialog = AgregarProductoComandaDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            producto, cantidad, notas = dialog.obtener_seleccion()
            if producto:
                comanda_activa = next((comanda for comanda in self.comandas if comanda.estado == "Pendiente"), None)

                if not comanda_activa:
                    comanda_id = crear_comanda(self.mesa.id)
                    comanda_activa = Comanda(comanda_id, self.mesa.id, None, "Pendiente", "Comer en el lugar", None)
                    self.comandas.append(comanda_activa)

                agregar_producto_a_comanda(comanda_activa.id, producto["id"], cantidad, notas)

                self.actualizar_comandas()

    def actualizar_comandas(self):
        # Obtener las comandas desde la API
        comandas_dict = obtener_comandas_por_mesa(self.mesa.id)
        
        # Convertir los diccionarios en objetos Comanda
        self.comandas = []
        for comanda_dict in comandas_dict:
            comanda = Comanda(
                id=comanda_dict["id"],
                mesa_id=comanda_dict["mesa_id"],
                fecha_hora=comanda_dict["fecha_hora"],
                estado=comanda_dict["estado"],
                tipo=comanda_dict["tipo"],
                metodo_pago=comanda_dict.get("metodo_pago", None)
            )
            
            # Convertir los detalles de la comanda
            comanda.detalles = [
                DetalleComanda(
                    id=detalle["id"],
                    comanda_id=detalle["comanda_id"],
                    producto_id=detalle["producto_id"],
                    producto_nombre=detalle["producto_nombre"],
                    cantidad=detalle["cantidad"],
                    estado=detalle["estado"],
                    notas=detalle.get("notas", ""),
                    ingredientes_excluidos=detalle.get("ingredientes_excluidos", ""),
                    ingredientes_agregados=detalle.get("ingredientes_agregados", ""),
                    subtotal=detalle["subtotal"]
                )
                for detalle in comanda_dict.get("detalles", [])
            ]
            
            self.comandas.append(comanda)

        # Actualizar la tabla de comandas
        self.actualizar_tabla_comandas()

    def actualizar_tabla_comandas(self):
        detalles = []
        for comanda in self.comandas:
            detalles.extend(comanda.detalles)
        
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

        self.accept()