import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QAction, QMessageBox, QDialog
from windows.gestionar_menu_dialog import GestionarMenuDialog
from windows.interfaz_mesas import InterfazMesas
from controllers import crear_comanda_para_llevar
from windows.detalle_comanda_para_llevar_dialog import DetalleComandaParaLlevarDialog
from windows.ver_comandas_dialog import VerComandasDialog
from windows.gestionar_ingredientes_dialog import GestionarIngredientesDialog
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Comandas")
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout_principal = QVBoxLayout()

        self.boton_take_away = QPushButton("Para llevar")
        self.boton_take_away.clicked.connect(self.take_away)
        self.layout_principal.addWidget(self.boton_take_away)

        self.boton_ver_mesas = QPushButton("Ver Mesas")
        self.boton_ver_mesas.clicked.connect(self.ver_mesas)
        self.layout_principal.addWidget(self.boton_ver_mesas)

        self.boton_ver_comandas = QPushButton("Ver Comandas")
        self.boton_ver_comandas.clicked.connect(self.ver_comandas)
        self.layout_principal.addWidget(self.boton_ver_comandas)
        
        self.boton_gestionar_ingredientes = QPushButton("Gestionar Ingredientes")
        self.boton_gestionar_ingredientes.clicked.connect(self.gestionar_ingredientes)
        self.layout_principal.addWidget(self.boton_gestionar_ingredientes)

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
        self.ventana_mesas = InterfazMesas()
        self.ventana_mesas.show()

    def take_away(self):
        comanda_id = crear_comanda_para_llevar()

        dialog = DetalleComandaParaLlevarDialog(comanda_id, self)
        dialog.exec_()

    def ver_mesas(self):
        self.ventana_mesas = InterfazMesas()
        self.ventana_mesas.show()

    def ver_comandas(self):
        dialog = VerComandasDialog(self)
        dialog.exec_()

    def gestionar_menu(self):
        self.ventana_menu = GestionarMenuDialog(self)
        self.ventana_menu.exec_()
    
    def gestionar_ingredientes(self):
        dialog = GestionarIngredientesDialog(self)
        dialog.exec_()


def iniciar_interfaz():
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec_())