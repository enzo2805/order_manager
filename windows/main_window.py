from PyQt5.QtWidgets import QMainWindow, QLabel, QStackedWidget, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import QTimer, QTime, Qt, QDate

from windows.gestionar_menu_dialog import WidgetMenu
from windows.interfaz_mesas import WidgetMesas
from windows.ver_comandas_dialog import WidgetComandas

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestión")
        self.setObjectName("mainWindow")
        self.setStyleSheet("""
            #mainWindow {
                background-color: white;
            }
            QToolButton {
                font-size: 14px;
            }        
            QPushButton[clase = "highlight1_btn"] {
                font-size: 28px;
                padding: 20px 40px;
                min-width: 200px;
                min-height: 60px;
            }
            QToolButton[clase = "highlight1_btn"] {
                font-size: 28px;
                padding: 20px 40px;
                min-width: 200px;
                max-width: 200px;
                min-height: 60px;
            }
            QPushButton[clase = "highlight2_btn"] {
                font-size: 22px;
                padding: 10px 20px;
                min-width: 100px;
                min-height: 30px;
            }
            QToolButton[clase = "highlight2_btn"] {
                font-size: 22px;
                padding: 10px 20px;
                min-width: 100px;
                min-height: 30px;
            }
            QPushButton[clase = "mesa_btn"] {
                font-size: 14px;
                min-width: 40px;
                min-height: 40px;
                padding: 5px;
            }
            QCheckBox, QLineEdit {
                font-size: 26px;
                padding: 10px;
            }
            QLabel {
                font-size: 26px;
                padding: 8px;
            }
            QTableWidget {
                font-size: 16px;
            }
            QHeaderView::section {
                font-size: 18px;
                font-weight: bold;
                border: 1px solid #1565c0;
            }
            QSpinBox {
                font-size: 22px;
                padding: 5px;
            }
            QFormLayout {
                font-size: 22px;
                margin: 10px;
                padding: 10px;
            }
            QDoubleSpinBox {
                font-size: 22px;
                padding: 5px;
            }
            QComboBox {
                font-size: 22px;
                padding: 5px;
            }
            QFileDialog {
                font-size: 22px;
                padding: 10px;
            }
        """)
        self.showMaximized()

        self.stacked = QStackedWidget()
        self.stacked.showFullScreen()
        self.setCentralWidget(self.stacked)

        self.widget_mesas = WidgetMesas()
        self.widget_menu = WidgetMenu()
        self.widget_comandas = WidgetComandas()

        self.stacked.addWidget(self.widget_mesas)
        self.stacked.addWidget(self.widget_menu)
        self.stacked.addWidget(self.widget_comandas)

        nav = QWidget()
        nav_layout = QHBoxLayout(nav)
        btn_mesas = QPushButton("Mesas")
        btn_mesas.setProperty("clase", "highlight1_btn")
        btn_menu = QPushButton("Menú")
        btn_menu.setProperty("clase", "highlight1_btn")
        btn_comandas = QPushButton("Comandas")
        btn_comandas.setProperty("clase", "highlight1_btn")
        nav_layout.addWidget(btn_mesas)
        nav_layout.addWidget(btn_menu)
        nav_layout.addWidget(btn_comandas)
        nav_layout.addStretch()

        btn_mesas.clicked.connect(lambda: self.stacked.setCurrentWidget(self.widget_mesas))
        btn_menu.clicked.connect(lambda: self.stacked.setCurrentWidget(self.widget_menu))
        btn_comandas.clicked.connect(lambda: self.stacked.setCurrentWidget(self.widget_comandas))

        main_layout = QVBoxLayout()
        main_layout.addWidget(nav)
        main_layout.addWidget(self.stacked, stretch=1)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.reloj_label = QLabel(self)
        self.reloj_label.setStyleSheet("font-size: 18px; padding: 5px;")
        self.reloj_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        main_layout.addWidget(self.reloj_label)

        self.timer_reloj = QTimer(self)
        self.timer_reloj.timeout.connect(self.actualizar_reloj)
        self.timer_reloj.start(1000)

        self.actualizar_reloj()

    def actualizar_reloj(self):
        hora_actual = QTime.currentTime().toString("hh:mm:ss")
        fecha_actual = QDate.currentDate().toString("dd/MM/yyyy")
        self.reloj_label.setText(f"{hora_actual} - {fecha_actual}")