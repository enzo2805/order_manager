from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QMessageBox, QInputDialog
from PyQt5.QtGui import QColor
from controllers import cambiar_estado_comanda, descontar_ingredientes, obtener_comandas_pendientes_y_en_preparacion, obtener_detalles_comanda_cocina, cambiar_estado_detalle_comanda, actualizar_estado_comanda

class GestionarComandasCocinaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gestionar Comandas - Cocina")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Mesa", "Estado", "Tipo"])
        layout.addWidget(self.table)

        self.setLayout(layout)

        self.cargar_comandas()

    def cargar_comandas(self):
        comandas = obtener_comandas_pendientes_y_en_preparacion()
        filas = []

        for comanda in comandas:
            detalles = obtener_detalles_comanda_cocina(comanda.id)
            for detalle in detalles:
                filas.append({
                    "id": detalle.id,
                    "mesa": str(comanda.mesa_id) if comanda.mesa_id else "Para llevar",
                    "estado": str(detalle.estado),
                    "tipo": comanda.tipo,
                    "producto": detalle.producto_nombre,
                    "cantidad": detalle.cantidad,
                    "notas": detalle.notas if detalle.notas else "",
                    "ingredientes_excluidos": detalle.ingredientes_excluidos if detalle.ingredientes_excluidos else "",
                    "ingredientes_agregados": detalle.ingredientes_agregados if detalle.ingredientes_agregados else ""
                })

        self.table.setRowCount(len(filas))
        self.table.setColumnCount(10)  # Cambiar a 10 columnas para incluir el botón
        self.table.setHorizontalHeaderLabels([
            "ID", "Mesa", "Estado", "Tipo", "Producto", "Cantidad", 
            "Notas", "Ing. Excluidos", "Ing. Agregados", "Acción"
        ])

        for row, fila in enumerate(filas):
            item_id = QTableWidgetItem(str(fila["id"]))
            item_mesa = QTableWidgetItem(fila["mesa"])
            item_estado = QTableWidgetItem(fila["estado"])
            item_tipo = QTableWidgetItem(fila["tipo"])
            item_producto = QTableWidgetItem(fila["producto"])
            item_cantidad = QTableWidgetItem(str(fila["cantidad"]))
            item_notas = QTableWidgetItem(fila["notas"])
            item_ingredientes_excluidos = QTableWidgetItem(fila["ingredientes_excluidos"])
            item_ingredientes_agregados = QTableWidgetItem(fila["ingredientes_agregados"])

            # Aplicar colores según el estado
            if fila["estado"] == "Pendiente":
                color = QColor("yellow")
            elif fila["estado"] == "En preparación":
                color = QColor("lightblue")
            elif fila["estado"] == "Listo":
                color = QColor("green")
            else:
                color = QColor("white")

            for item in [item_id, item_mesa, item_estado, item_tipo, item_producto, item_cantidad, item_notas, item_ingredientes_excluidos, item_ingredientes_agregados]:
                item.setBackground(color)

            # Crear botón con texto y acción dinámicos según el estado
            if fila["estado"] == "Pendiente":
                btn_accion = QPushButton("Tomar Comanda")
                btn_accion.clicked.connect(lambda _, detalle_id=fila["id"]: self.tomar_comanda_producto(detalle_id))
            elif fila["estado"] == "En preparación":
                btn_accion = QPushButton("Marcar Listo")
                btn_accion.clicked.connect(lambda _, detalle_id=fila["id"]: self.marcar_producto_listo(detalle_id))
            else:
                btn_accion = QPushButton("Acción no disponible")
                btn_accion.setEnabled(False)

            self.table.setItem(row, 0, item_id)
            self.table.setItem(row, 1, item_mesa)
            self.table.setItem(row, 2, item_estado)
            self.table.setItem(row, 3, item_tipo)
            self.table.setItem(row, 4, item_producto)
            self.table.setItem(row, 5, item_cantidad)
            self.table.setItem(row, 6, item_notas)
            self.table.setItem(row, 7, item_ingredientes_excluidos)
            self.table.setItem(row, 8, item_ingredientes_agregados)
            self.table.setCellWidget(row, 9, btn_accion)  # Agregar el botón a la última columna
  
    def tomar_comanda_producto(self, detalle_id):
        cambiar_estado_detalle_comanda(detalle_id, "En preparación")  # Cambia el estado a "En preparación"
        self.cargar_comandas()  # Recarga la tabla para reflejar los cambios
        QMessageBox.information(self, "Producto Tomado", "El producto ha sido marcado como 'En preparación'.")

    def marcar_producto_listo(self, detalle_id):
        cambiar_estado_detalle_comanda(detalle_id, "Listo")  # Cambia el estado a "Listo"
        self.cargar_comandas()  # Recarga la tabla para reflejar los cambios
        QMessageBox.information(self, "Producto Listo", "El producto ha sido marcado como 'Listo'.")