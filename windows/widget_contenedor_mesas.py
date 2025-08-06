from PyQt5.QtWidgets import QWidget, QPushButton, QMenu, QAction, QInputDialog, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QPalette, QColor
from api_client import (
    crear_mesa,
    eliminar_mesa,
    guardar_posicion_mesa,
    obtener_mesas,
    cambiar_estado_mesa,
    obtener_comandas_por_mesa,
    cambiar_mesa_comanda,
    obtener_todas_las_comandas_para_mesas
)

class WidgetContenedorMesas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.autoFillBackground = True
        self.modo_edicion = False
        self.mesas_widgets = {}
        self.on_mostrar_detalle = None
        self.actualizar_mesas()
    
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("teal"))
        self.setPalette(palette)

    def actualizar_mesas(self):
        self.limpiar_layout()
        self.mesas_widgets = {}

        mesas = obtener_mesas()
        comandas = obtener_todas_las_comandas_para_mesas()

        comandas_por_mesa = {}
        for comanda in comandas:
            mesa_id = comanda["mesa_id"]
            if mesa_id not in comandas_por_mesa:
                comandas_por_mesa[mesa_id] = []
            comandas_por_mesa[mesa_id].append(comanda)

        for mesa in mesas:
            mesa_comandas = comandas_por_mesa.get(mesa["id"], [])
            if any(comanda["estado"] != 'Pagado' for comanda in mesa_comandas):
                mesa["estado"] = "Ocupada"

            btn = self.crear_boton_mesa(mesa)
            self.mesas_widgets[mesa["id"]] = btn
            btn.setParent(self)
            btn.move(mesa["pos_x"], mesa["pos_y"])
            btn.show()

    def limpiar_layout(self):
        for child in self.children():
            if isinstance(child, QWidget):
                child.setParent(None)

    def crear_boton_mesa(self, mesa):
        btn = QPushButton(f"Mesa {mesa['numero']}\n{mesa['estado']}")
        btn.setProperty("clase", "mesa_btn")
        if mesa["estado"] == "Reservada":
            btn.setText(f"Mesa {mesa['numero']}\n{mesa['estado']}\nReservada a: {mesa['reservada_a']}")
        btn.setStyleSheet(self.obtener_color_estado(mesa["estado"]))
        btn.setFixedSize(80, 80)
        btn.setCheckable(self.modo_edicion)
        
        self.configurar_boton_edicion(btn, mesa)
        
        btn.clicked.connect(lambda: self.mostrar_detalle_mesa(mesa))
        
        return btn

    def configurar_boton_edicion(self, btn, mesa):
        btn.setContextMenuPolicy(Qt.CustomContextMenu)
        btn.customContextMenuRequested.connect(lambda pos, b=btn, m=mesa: self.mostrar_menu_contextual(pos, b, m))
        if self.modo_edicion:
            btn.setStyleSheet("border: 2px dashed blue;")
            btn.mousePressEvent = lambda event, b=btn: self.iniciar_mover(event, b)
            btn.mouseMoveEvent = lambda event, b=btn: self.mover_mesa(event, b)
            btn.mouseReleaseEvent = lambda event, b=btn: self.finalizar_mover(event, b)
            btn.setCursor(Qt.OpenHandCursor)
        else:
            btn.setStyleSheet(self.obtener_color_estado(mesa["estado"]))

    def obtener_color_estado(self, estado):
        estilos_estado = {
            "Libre": "background-color: green; color: white;",
            "Ocupada": "background-color: red; color: white;",
            "Reservada": "background-color: yellow; color: black;"
        }
        return estilos_estado.get(estado, "")

    def activar_modo_edicion(self, state):
        from PyQt5.QtCore import Qt
        self.modo_edicion = state == Qt.Checked
        self.actualizar_mesas()

    def mostrar_menu_contextual(self, pos, boton, mesa):
        menu = QMenu(self)
        cambiar_estado_libre = QAction("Libre", self)
        cambiar_estado_libre.triggered.connect(lambda: self.cambiar_estado(mesa, "Libre"))
        menu.addAction(cambiar_estado_libre)

        cambiar_estado_ocupada = QAction("Ocupada", self)
        cambiar_estado_ocupada.triggered.connect(lambda: self.cambiar_estado(mesa, "Ocupada"))
        menu.addAction(cambiar_estado_ocupada)

        cambiar_estado_reservada = QAction("Reservada", self)
        cambiar_estado_reservada.triggered.connect(lambda: self.reservar_mesa(mesa))
        menu.addAction(cambiar_estado_reservada)

        mover_comanda = QAction("Mover Comanda", self)
        mover_comanda.triggered.connect(lambda: self.mover_comanda(mesa))
        menu.addAction(mover_comanda)

        menu.exec_(QCursor.pos())

    def cambiar_estado(self, mesa, nuevo_estado):
        cambiar_estado_mesa(mesa["id"], nuevo_estado)
        self.actualizar_mesas()

    def reservar_mesa(self, mesa):
        nombre, ok = QInputDialog.getText(self, "Reservar Mesa", "Ingrese el nombre de la persona:")
        if ok and nombre:
            cambiar_estado_mesa(mesa["id"], "Reservada", nombre)
            self.actualizar_mesas()

    def mostrar_detalle_mesa(self, mesa_dict):
        if self.on_mostrar_detalle:
            self.on_mostrar_detalle(mesa_dict)

    def iniciar_mover(self, event, boton):
        if self.modo_edicion and event.button() == Qt.LeftButton:
            boton._moving = True
            boton.setCursor(Qt.ClosedHandCursor)
            boton._start_pos = event.globalPos()
            boton._start_widget_pos = boton.pos()

    def mover_mesa(self, event, boton):
        if hasattr(boton, '_moving') and boton._moving:
            delta = event.globalPos() - boton._start_pos
            boton.move(boton._start_widget_pos + delta)

    def finalizar_mover(self, event, boton):
        if hasattr(boton, '_moving'):
            boton._moving = False
            boton.setCursor(Qt.OpenHandCursor)

    def guardar_cambios(self):
        for mesa_id, boton in self.mesas_widgets.items():
            nueva_posicion = boton.pos()
            guardar_posicion_mesa(mesa_id, nueva_posicion.x(), nueva_posicion.y())
        QMessageBox.information(self, "Guardado", "Posiciones de las mesas guardadas correctamente.")

    def crear_mesa(self):
        crear_mesa()
        self.actualizar_mesas()
        
    def eliminar_mesa(self):
        mesa_id, ok = QInputDialog.getInt(self, "Eliminar Mesa", "Ingrese el ID de la mesa a eliminar:")
        if ok:
            eliminar_mesa(mesa_id)
            QMessageBox.information(self, "Mesa eliminada", f"Mesa con ID {mesa_id} eliminada correctamente.")
            self.actualizar_mesas()

    def mover_comanda(self, mesa_origen):
        mesas_libres = [mesa for mesa in obtener_mesas() if mesa["estado"] == "Libre"]

        if not mesas_libres:
            QMessageBox.warning(self, "Mover Comanda", "No hay mesas libres disponibles.")
            return

        opciones = [f"Mesa {mesa['numero']}" for mesa in mesas_libres]
        mesa_seleccionada, ok = QInputDialog.getItem(
            self,
            "Mover Comanda",
            "Seleccione una mesa libre para mover la comanda:",
            opciones,
            editable=False
        )

        if not ok or not mesa_seleccionada:
            return

        numero_mesa = int(mesa_seleccionada.split(" ")[1])
        mesa_destino = next((mesa for mesa in mesas_libres if mesa["numero"] == numero_mesa), None)

        if not mesa_destino:
            QMessageBox.warning(self, "Mover Comanda", "No se pudo encontrar la mesa seleccionada.")
            return

        for comanda in obtener_comandas_por_mesa(mesa_origen["id"]):
            cambiar_mesa_comanda(comanda["id"], mesa_destino["id"])

        cambiar_estado_mesa(mesa_origen["id"], "Libre")
        cambiar_estado_mesa(mesa_destino["id"], "Ocupada")

        QMessageBox.information(self, "Mover Comanda", f"Las comandas de la Mesa {mesa_origen['numero']} se han movido a la Mesa {mesa_destino['numero']}.")
        self.actualizar_mesas()