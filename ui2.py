from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QCheckBox, QMenu, QAction
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor
from controllers import obtener_todas_las_mesas, cambiar_estado_mesa, guardar_posicion_mesa
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
        btn.setStyleSheet(self.obtener_color_estado(mesa.estado))
        btn.setFixedSize(*TAMANO_BOTON)
        btn.setCheckable(self.modo_edicion)
        btn.clicked.connect(lambda _, m=mesa: self.cambiar_estado(m))
        
        if self.modo_edicion:
            self.configurar_boton_edicion(btn, mesa)
        
        return btn

    def configurar_boton_edicion(self, btn, mesa):
        btn.setContextMenuPolicy(Qt.CustomContextMenu)
        btn.customContextMenuRequested.connect(lambda pos, b=btn, m=mesa: self.mostrar_menu_contextual(pos, b, m))
        btn.setStyleSheet(ESTILO_EDICION)
        btn.mousePressEvent = lambda event, b=btn: self.iniciar_mover(event, b)
        btn.mouseMoveEvent = lambda event, b=btn: self.mover_mesa(event, b)
        btn.mouseReleaseEvent = lambda event, b=btn: self.finalizar_mover(event, b)
        btn.setCursor(Qt.OpenHandCursor)

    def obtener_color_estado(self, estado):
        return ESTILOS_ESTADO.get(estado, "")

    def cambiar_estado(self, mesa):
        if not self.modo_edicion:
            nuevo_estado = "Libre" if mesa.estado != "Libre" else "Ocupada"
            cambiar_estado_mesa(mesa.id, nuevo_estado)
            self.actualizar_mesas()

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
        menu.exec_(QCursor.pos())

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

def iniciar_interfaz():
    app = QApplication(sys.argv)
    ventana = InterfazMesas()
    ventana.show()
    sys.exit(app.exec_())