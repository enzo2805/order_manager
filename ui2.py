from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QCheckBox, QMenu, QAction, QInputDialog, QDialog, QLabel, QFormLayout, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor
from controllers import obtener_todas_las_mesas, cambiar_estado_mesa, guardar_posicion_mesa, agregar_mesa, eliminar_mesa, obtener_comandas_por_mesa
import sys

# Constantes para estilos y tamaños
ESTILOS_ESTADO = {
    "Libre": "background-color: green; color: white;",
    "Ocupada": "background-color: red; color: white;",
    "Reservada": "background-color: yellow; color: black;"
}
ESTILO_EDICION = "border: 2px dashed blue;"
ESTILO_FORMA = {
    "Cuadrada": "background-color: lightgray;",
    "Redonda": "border-radius: 40px; background-color: lightgray;",
    "Rectangular": "width: 100px; background-color: lightgray;"
}
TAMANO_BOTON = (80, 80)

class DetalleMesaDialog(QDialog):
    def __init__(self, mesa, comandas, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Detalle de Mesa {mesa.numero}")
        self.setGeometry(100, 100, 600, 400)
        layout = QVBoxLayout()
        
        # Información de la mesa
        info_layout = QFormLayout()
        info_layout.addRow("Número:", QLabel(str(mesa.numero)))
        info_layout.addRow("Estado:", QLabel(mesa.estado))
        if mesa.estado == "Reservada":
            info_layout.addRow("Reservada a:", QLabel(mesa.reservada_a))
        layout.addLayout(info_layout)
        
        # Tabla de comandas
        self.table = QTableWidget()
        self.table.setRowCount(len(comandas))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID Comanda", "Producto", "Cantidad", "Estado", "Subtotal"])
        
        row = 0
        for comanda in comandas:
            for detalle in comanda.detalles:
                self.table.setItem(row, 0, QTableWidgetItem(str(comanda.id)))
                self.table.setItem(row, 1, QTableWidgetItem(detalle.producto_nombre))
                self.table.setItem(row, 2, QTableWidgetItem(str(detalle.cantidad)))
                self.table.setItem(row, 3, QTableWidgetItem(comanda.estado))
                self.table.setItem(row, 4, QTableWidgetItem(f"${detalle.subtotal:.2f}"))
                row += 1
        
        layout.addWidget(self.table)
        self.setLayout(layout)

class InterfazMesas(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Mesas")
        self.setGeometry(100, 100, 800, 600)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout_principal = QVBoxLayout()
        self.mesas_container = QWidget(self.central_widget)
        self.mesas_container.setGeometry(0, 0, 800, 600)
        self.mesas_container.setStyleSheet("background-color: white;")
        self.modo_edicion = False
        self.mesas_widgets = {}

        self.check_edicion = QCheckBox("Modo Edición")
        self.check_edicion.stateChanged.connect(self.activar_modo_edicion)
        self.layout_principal.addWidget(self.check_edicion)

        self.boton_guardar = QPushButton("Guardar")
        self.boton_guardar.clicked.connect(self.guardar_cambios)
        self.layout_principal.addWidget(self.boton_guardar)

        self.boton_crear = QPushButton("Crear Mesa")
        self.boton_crear.clicked.connect(self.crear_mesa)
        self.layout_principal.addWidget(self.boton_crear)

        self.boton_eliminar = QPushButton("Eliminar Mesa")
        self.boton_eliminar.clicked.connect(self.eliminar_mesa)
        self.layout_principal.addWidget(self.boton_eliminar)

        self.layout_principal.addWidget(self.mesas_container)
        self.central_widget.setLayout(self.layout_principal)

        self.actualizar_mesas()

    def actualizar_mesas(self):
        self.limpiar_layout(self.mesas_container)
        self.mesas_widgets = {}
        mesas = obtener_todas_las_mesas()
        for mesa in mesas:
            btn = self.crear_boton_mesa(mesa)
            self.mesas_widgets[mesa.id] = btn
            btn.setParent(self.mesas_container)
            btn.move(mesa.pos_x, mesa.pos_y)
            btn.show()

    def limpiar_layout(self, layout):
        for widget in layout.children():
            if isinstance(widget, QWidget):
                widget.setParent(None)

    def crear_boton_mesa(self, mesa):
        btn = QPushButton(f"Mesa {mesa.numero}\n{mesa.estado}")
        if mesa.estado == "Reservada":
            btn.setText(f"Mesa {mesa.numero}\n{mesa.estado}\nReservada a: {mesa.reservada_a}")
        btn.setStyleSheet(self.obtener_color_estado(mesa.estado))
        btn.setFixedSize(*TAMANO_BOTON)
        btn.setCheckable(self.modo_edicion)
        
        self.configurar_boton_edicion(btn, mesa)
        
        btn.clicked.connect(lambda: self.mostrar_detalle_mesa(mesa))
        
        return btn

    def configurar_boton_edicion(self, btn, mesa):
        btn.setContextMenuPolicy(Qt.CustomContextMenu)
        btn.customContextMenuRequested.connect(lambda pos, b=btn, m=mesa: self.mostrar_menu_contextual(pos, b, m))
        if self.modo_edicion:
            btn.setStyleSheet(ESTILO_EDICION)
            btn.mousePressEvent = lambda event, b=btn: self.iniciar_mover(event, b)
            btn.mouseMoveEvent = lambda event, b=btn: self.mover_mesa(event, b)
            btn.mouseReleaseEvent = lambda event, b=btn: self.finalizar_mover(event, b)
            btn.setCursor(Qt.OpenHandCursor)
        else:
            btn.setStyleSheet(self.obtener_color_estado(mesa.estado))

    def obtener_color_estado(self, estado):
        return ESTILOS_ESTADO.get(estado, "")

    def activar_modo_edicion(self, estado):
        self.modo_edicion = estado == Qt.Checked
        self.actualizar_mesas()

    def mostrar_menu_contextual(self, pos, boton, mesa):
        menu = QMenu(self)
        forma_menu = QMenu("Cambiar Forma", self)
        
        for forma, estilo in ESTILO_FORMA.items():
            accion = QAction(forma, self)
            accion.triggered.connect(lambda checked=False, s=estilo: boton.setStyleSheet(s))
            forma_menu.addAction(accion)
        
        menu.addMenu(forma_menu)

        cambiar_estado_libre = QAction("Libre", self)
        cambiar_estado_libre.triggered.connect(lambda: self.cambiar_estado(mesa, "Libre"))
        menu.addAction(cambiar_estado_libre)

        cambiar_estado_ocupada = QAction("Ocupada", self)
        cambiar_estado_ocupada.triggered.connect(lambda: self.cambiar_estado(mesa, "Ocupada"))
        menu.addAction(cambiar_estado_ocupada)

        cambiar_estado_reservada = QAction("Reservada", self)
        cambiar_estado_reservada.triggered.connect(lambda: self.reservar_mesa(mesa))
        menu.addAction(cambiar_estado_reservada)

        menu.exec_(QCursor.pos())

    def cambiar_estado(self, mesa, nuevo_estado):
        cambiar_estado_mesa(mesa.id, nuevo_estado)
        self.actualizar_mesas()

    def reservar_mesa(self, mesa):
        nombre, ok = QInputDialog.getText(self, "Reservar Mesa", "Ingrese el nombre de la persona:")
        if ok and nombre:
            cambiar_estado_mesa(mesa.id, "Reservada", nombre)
            self.actualizar_mesas()

    def mostrar_detalle_mesa(self, mesa):
        comandas = obtener_comandas_por_mesa(mesa.id)
        dialog = DetalleMesaDialog(mesa, comandas, self)
        dialog.exec_()

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
        print("Cambios guardados")

    def crear_mesa(self):
        agregar_mesa()
        self.actualizar_mesas()

    def eliminar_mesa(self):
        mesa_id, ok = QInputDialog.getInt(self, "Eliminar Mesa", "Ingrese el ID de la mesa a eliminar:")
        if ok:
            eliminar_mesa(mesa_id)
            self.actualizar_mesas()

def iniciar_interfaz():
    app = QApplication(sys.argv)
    ventana = InterfazMesas()
    ventana.show()
    sys.exit(app.exec_())