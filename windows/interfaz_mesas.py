from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QCheckBox, QMenu, QAction, QInputDialog, QWidget, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from controllers import cambiar_mesa_comanda, obtener_todas_las_mesas, cambiar_estado_mesa, guardar_posicion_mesa, agregar_mesa, eliminar_mesa, obtener_comandas_por_mesa
from windows.detalle_mesa_dialog import DetalleMesaDialog


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
            comandas = obtener_comandas_por_mesa(mesa.id)
            if any(comanda.estado != 'Pagado' for comanda in comandas):
                mesa.estado = "Ocupada"
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
            btn.setStyleSheet(self.obtener_color_estado(mesa.estado))

    def obtener_color_estado(self, estado):
        estilos_estado = {
            "Libre": "background-color: green; color: white;",
            "Ocupada": "background-color: red; color: white;",
            "Reservada": "background-color: yellow; color: black;"
        }
        return estilos_estado.get(estado, "")

    def activar_modo_edicion(self, estado):
        self.modo_edicion = estado == Qt.Checked
        self.actualizar_mesas()

    def mostrar_menu_contextual(self, pos, boton, mesa):
        menu = QMenu(self)
        forma_menu = QMenu("Cambiar Forma", self)
        
        estilos_forma = {
            "Cuadrada": "background-color: lightgray;",
            "Redonda": "border-radius: 40px; background-color: lightgray;",
            "Rectangular": "width: 100px; background-color: lightgray;"
        }
        
        for forma, estilo in estilos_forma.items():
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

        mover_comanda = QAction("Mover Comanda", self)
        mover_comanda.triggered.connect(lambda: self.mover_comanda(mesa))
        menu.addAction(mover_comanda)

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
        self.actualizar_mesas()

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
    
    def mover_comanda(self, mesa_origen):
        mesas_libres = [mesa for mesa in obtener_todas_las_mesas() if mesa.estado == "Libre"]

        if not mesas_libres:
            QMessageBox.warning(self, "Mover Comanda", "No hay mesas libres disponibles.")
            return

        opciones = [f"Mesa {mesa.numero}" for mesa in mesas_libres]
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
        mesa_destino = next((mesa for mesa in mesas_libres if mesa.numero == numero_mesa), None)

        if not mesa_destino:
            QMessageBox.warning(self, "Mover Comanda", "No se pudo encontrar la mesa seleccionada.")
            return

        for comanda in obtener_comandas_por_mesa(mesa_origen.id):
            cambiar_mesa_comanda(comanda.id, mesa_destino.id)

        cambiar_estado_mesa(mesa_origen.id, "Libre")
        cambiar_estado_mesa(mesa_destino.id, "Ocupada")

        QMessageBox.information(self, "Mover Comanda", f"Las comandas de la Mesa {mesa_origen.numero} se han movido a la Mesa {mesa_destino.numero}.")
        self.actualizar_mesas()