from PyQt5.QtWidgets import QApplication
from windows.gestionar_comandas_cocina_dialog import GestionarComandasCocinaDialog

def iniciar_cocina():
    app = QApplication([])
    ventana = GestionarComandasCocinaDialog()
    ventana.show()
    app.exec_()

if __name__ == "__main__":
    iniciar_cocina()