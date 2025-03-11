from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QDialog, QCheckBox, QMenu, QAction, QInputDialog, QLabel, QFormLayout, QTableWidget, QTableWidgetItem, QHBoxLayout, QLineEdit, QMessageBox, QComboBox, QSpinBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from controllers import obtener_todas_las_mesas, cambiar_estado_mesa, guardar_posicion_mesa, agregar_mesa, eliminar_mesa, obtener_comandas_por_mesa, obtener_todos_los_productos, agregar_producto, eliminar_producto, agregar_producto_a_comanda
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Comandas")
        self.setGeometry(100, 100, 400, 300)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout_principal = QVBoxLayout()

        self.boton_dine_in = QPushButton("Comer en el lugar")
        self.boton_dine_in.clicked.connect(self.dine_in)
        self.layout_principal.addWidget(self.boton_dine_in)

        self.boton_take_away = QPushButton("Para llevar")
        self.boton_take_away.clicked.connect(self.take_away)
        self.layout_principal.addWidget(self.boton_take_away)

        self.boton_ver_mesas = QPushButton("Ver Mesas")
        self.boton_ver_mesas.clicked.connect(self.ver_mesas)
        self.layout_principal.addWidget(self.boton_ver_mesas)

        self.boton_ver_comandas = QPushButton("Ver Comandas")
        self.boton_ver_comandas.clicked.connect(self.ver_comandas)
        self.layout_principal.addWidget(self.boton_ver_comandas)

        self.boton_gestionar_menu = QPushButton("Gestionar Menú")
        self.boton_gestionar_menu.clicked.connect(self.gestionar_menu)
        self.layout_principal.addWidget(self.boton_gestionar_menu)

        self.central_widget.setLayout(self.layout_principal)

        self.crear_menu()

    def crear_menu(self):
        menubar = self.menuBar()
        menu_opciones = menubar.addMenu("Opciones")

        accion_dine_in = QAction("Comer en el lugar", self)
        accion_dine_in.triggered.connect(self.dine_in)
        menu_opciones.addAction(accion_dine_in)

        accion_take_away = QAction("Para llevar", self)
        accion_take_away.triggered.connect(self.take_away)
        menu_opciones.addAction(accion_take_away)

        accion_ver_mesas = QAction("Ver Mesas", self)
        accion_ver_mesas.triggered.connect(self.ver_mesas)
        menu_opciones.addAction(accion_ver_mesas)

        accion_ver_comandas = QAction("Ver Comandas", self)
        accion_ver_comandas.triggered.connect(self.ver_comandas)
        menu_opciones.addAction(accion_ver_comandas)

        accion_gestionar_menu = QAction("Gestionar Menú", self)
        accion_gestionar_menu.triggered.connect(self.gestionar_menu)
        menu_opciones.addAction(accion_gestionar_menu)

    def dine_in(self):
        # Aquí puedes agregar la lógica para gestionar las comandas de "Comer en el lugar"
        print("Comer en el lugar seleccionado")

    def take_away(self):
        # Aquí puedes agregar la lógica para gestionar las comandas de "Para llevar"
        print("Para llevar seleccionado")

    def ver_mesas(self):
        self.ventana_mesas = InterfazMesas()
        self.ventana_mesas.show()

    def ver_comandas(self):
        # Aquí puedes agregar la lógica para ver las comandas
        print("Ver Comandas seleccionado")

    def gestionar_menu(self):
        self.ventana_menu = GestionarMenuDialog(self)
        self.ventana_menu.exec_()

class GestionarMenuDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gestionar Menú")
        self.setGeometry(100, 100, 600, 400)
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setRowCount(0)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Precio", "Categoría"])

        self.actualizar_menu()

        layout.addWidget(self.table)

        botones_layout = QHBoxLayout()
        self.boton_agregar = QPushButton("Agregar Producto")
        self.boton_agregar.clicked.connect(self.agregar_producto)
        botones_layout.addWidget(self.boton_agregar)

        self.boton_eliminar = QPushButton("Eliminar Producto")
        self.boton_eliminar.clicked.connect(self.eliminar_producto)
        botones_layout.addWidget(self.boton_eliminar)

        layout.addLayout(botones_layout)
        self.setLayout(layout)

    def actualizar_menu(self):
        productos = obtener_todos_los_productos()
        self.table.setRowCount(len(productos))
        for row, producto in enumerate(productos):
            self.table.setItem(row, 0, QTableWidgetItem(str(producto.id)))
            self.table.setItem(row, 1, QTableWidgetItem(producto.nombre))
            self.table.setItem(row, 2, QTableWidgetItem(f"${producto.precio:.2f}"))
            self.table.setItem(row, 3, QTableWidgetItem(producto.categoria))

    def agregar_producto(self):
        nombre, ok = QInputDialog.getText(self, "Agregar Producto", "Ingrese el nombre del producto:")
        if ok and nombre:
            precio, ok = QInputDialog.getDouble(self, "Agregar Producto", "Ingrese el precio del producto:")
            if ok:
                categorias = ["entrada", "principal", "extra", "postre", "alcohol", "soft drink"]
                categoria, ok = QInputDialog.getItem(self, "Agregar Producto", "Seleccione la categoría del producto:", categorias, 0, False)
                if ok and categoria:
                    agregar_producto(nombre, precio, categoria)
                    self.actualizar_menu()

    def eliminar_producto(self):
        producto_id, ok = QInputDialog.getInt(self, "Eliminar Producto", "Ingrese el ID del producto a eliminar:")
        if ok:
            eliminar_producto(producto_id)
            self.actualizar_menu()

class DetalleMesaDialog(QDialog):
    def __init__(self, mesa, comandas, parent=None):
        super().__init__(parent)
        self.mesa = mesa
        self.comandas = comandas
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
        
        # Botones para cambiar el estado de la mesa
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
        
        # Tabla de comandas
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID Comanda", "Producto", "Cantidad", "Estado", "Subtotal"])
        
        self.actualizar_tabla_comandas()

        layout.addWidget(self.table)

        # Botones para agregar productos y cobrar
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
            # Aquí debes agregar la lógica para actualizar la comanda con el producto, la cantidad y las notas seleccionados
            # Por ejemplo, podrías llamar a una función en el controlador para agregar el producto a la comanda
            # y luego actualizar la tabla de comandas en el diálogo
            self.actualizar_comanda(producto, cantidad, notas)

    def actualizar_comanda(self, producto, cantidad, notas):
        # Lógica para actualizar la comanda con el producto, la cantidad y las notas seleccionados
        # Aquí puedes agregar el producto a la comanda y actualizar la tabla de comandas
        agregar_producto_a_comanda(self.mesa.id, producto.id, cantidad, notas)
        # Volver a obtener las comandas y sus detalles
        self.comandas = obtener_comandas_por_mesa(self.mesa.id)
        self.actualizar_tabla_comandas()

    def actualizar_tabla_comandas(self):
        detalles = []
        for comanda in self.comandas:
            detalles.extend(comanda.detalles)
        
        self.table.setRowCount(len(detalles))
        row = 0
        for detalle in detalles:
            self.table.setItem(row, 0, QTableWidgetItem(str(detalle.comanda_id)))
            self.table.setItem(row, 1, QTableWidgetItem(detalle.producto_nombre))
            self.table.setItem(row, 2, QTableWidgetItem(str(detalle.cantidad)))
            self.table.setItem(row, 3, QTableWidgetItem(detalle.notas))
            self.table.setItem(row, 4, QTableWidgetItem(f"${detalle.subtotal:.2f}"))
            row += 1

    def cobrar(self):
        total = sum(float(self.table.item(row, 4).text().replace('$', '')) for row in range(self.table.rowCount()))
        QMessageBox.information(self, "Cobrar", f"El total a cobrar es: ${total:.2f}")
        cambiar_estado_mesa(self.mesa.id, "Libre")
        self.accept()

class AgregarProductoComandaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar Producto a Comanda")
        self.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout()

        self.productos = obtener_todos_los_productos()
        self.producto_combo = QComboBox()
        self.producto_combo.addItems([producto.nombre for producto in self.productos])
        layout.addWidget(QLabel("Seleccione el producto:"))
        layout.addWidget(self.producto_combo)

        self.cantidad_input = QSpinBox()
        self.cantidad_input.setRange(1, 100)
        layout.addWidget(QLabel("Cantidad:"))
        layout.addWidget(self.cantidad_input)

        self.notas_input = QLineEdit()
        layout.addWidget(QLabel("Notas:"))
        layout.addWidget(self.notas_input)

        botones_layout = QHBoxLayout()
        self.boton_aceptar = QPushButton("Aceptar")
        self.boton_aceptar.clicked.connect(self.accept)
        botones_layout.addWidget(self.boton_aceptar)

        self.boton_cancelar = QPushButton("Cancelar")
        self.boton_cancelar.clicked.connect(self.reject)
        botones_layout.addWidget(self.boton_cancelar)

        layout.addLayout(botones_layout)
        self.setLayout(layout)

    def obtener_seleccion(self):
        producto = self.productos[self.producto_combo.currentIndex()]
        cantidad = self.cantidad_input.value()
        notas = self.notas_input.text()
        return producto, cantidad, notas

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

def iniciar_interfaz():
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec_())