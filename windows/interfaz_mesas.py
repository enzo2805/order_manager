from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from api_client import agregar_producto_a_comanda, crear_comanda, obtener_comandas_por_mesa
from models import Mesa
from windows.agregar_producto_comanda_dialog import WidgetAgregarProductoComanda
from windows.widget_contenedor_mesas import WidgetContenedorMesas
from windows.widget_botonera_mesas import WidgetBotoneraMesas
from windows.detalle_mesa_dialog import WidgetDetalleMesa
from models import Mesa
class WidgetMesas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout_principal = QHBoxLayout(self)

        self.botonera = WidgetBotoneraMesas(self)
        self.layout_principal.addWidget(self.botonera)

        self.central_area = QWidget(self)
        self.central_layout = QVBoxLayout(self.central_area)
        self.layout_principal.addWidget(self.central_area)

        self.mesas_container = WidgetContenedorMesas(self)
        self.central_layout.addWidget(self.mesas_container)
        self.detalle_widget = None
        self.agregar_producto_widget = None

        self.botonera.check_edicion.stateChanged.connect(self.mesas_container.activar_modo_edicion)
        self.botonera.boton_guardar.clicked.connect(self.mesas_container.guardar_cambios)
        self.botonera.boton_crear.clicked.connect(self.mesas_container.crear_mesa)
        self.botonera.boton_eliminar.clicked.connect(self.mesas_container.eliminar_mesa)
        self.mesas_container.on_mostrar_detalle = self.mostrar_detalle_mesa

    def mostrar_detalle_mesa(self, mesa):
        if self.mesas_container is not None:
            self.central_layout.removeWidget(self.mesas_container)
            self.mesas_container.setParent(None)
            self.mesas_container = None
        if self.agregar_producto_widget:
            self.central_layout.removeWidget(self.agregar_producto_widget)
            self.agregar_producto_widget.deleteLater()
            self.agregar_producto_widget = None
        if self.detalle_widget:
            self.central_layout.removeWidget(self.detalle_widget)
            self.detalle_widget.deleteLater()
        if isinstance(mesa, dict):
            mesa_obj = Mesa(
                id=mesa["id"],
                numero=mesa["numero"],
                estado=mesa["estado"],
                reservada_a=mesa.get("reservada_a", None),
                pos_x=mesa.get("pos_x", 0),
                pos_y=mesa.get("pos_y", 0)
            )
        else:
            mesa_obj = mesa
        self.detalle_widget = WidgetDetalleMesa(mesa_obj, self)
        self.detalle_widget.on_agregar_producto = self.mostrar_agregar_producto
        self.detalle_widget.on_volver = self.mostrar_mesas
        self.central_layout.addWidget(self.detalle_widget)

    def mostrar_mesas(self):
        if self.detalle_widget:
            self.central_layout.removeWidget(self.detalle_widget)
            self.detalle_widget.deleteLater()
            self.detalle_widget = None
        if self.agregar_producto_widget:
            self.central_layout.removeWidget(self.agregar_producto_widget)
            self.agregar_producto_widget.deleteLater()
            self.agregar_producto_widget = None
        if self.mesas_container is None:
            self.mesas_container = WidgetContenedorMesas(self)
            self.mesas_container.on_mostrar_detalle = self.mostrar_detalle_mesa
            self.botonera.check_edicion.stateChanged.connect(self.mesas_container.activar_modo_edicion)
            self.botonera.boton_guardar.clicked.connect(self.mesas_container.guardar_cambios)
            self.botonera.boton_crear.clicked.connect(self.mesas_container.crear_mesa)
            self.botonera.boton_eliminar.clicked.connect(self.mesas_container.eliminar_mesa)
        self.central_layout.addWidget(self.mesas_container)

    def mostrar_agregar_producto(self, mesa):
        if self.detalle_widget:
            self.central_layout.removeWidget(self.detalle_widget)
            self.detalle_widget.deleteLater()
            self.detalle_widget = None
        if self.agregar_producto_widget:
            self.central_layout.removeWidget(self.agregar_producto_widget)
            self.agregar_producto_widget.deleteLater()
        self.agregar_producto_widget = WidgetAgregarProductoComanda(self)
        self.agregar_producto_widget.on_aceptar = lambda datos: self.finalizar_agregar_producto(mesa, datos)
        self.agregar_producto_widget.on_cancelar = lambda: self.cancelar_agregar_producto(mesa)
        self.central_layout.addWidget(self.agregar_producto_widget)

    def finalizar_agregar_producto(self, mesa, datos):
        producto, cantidad, notas = datos
        if producto:
            comandas = obtener_comandas_por_mesa(mesa.id)
            comanda_activa = next((c for c in comandas if c["estado"] == "Pendiente"), None)
            if not comanda_activa:
                comanda_resp = crear_comanda(mesa.id)
                comanda_id = comanda_resp["id"]
                comanda_activa = {"id": comanda_id, "mesa_id": mesa.id, "estado": "Pendiente"}
            agregar_producto_a_comanda(comanda_activa["id"], producto["id"], cantidad, notas)
        self.mostrar_detalle_mesa(mesa)

    def cancelar_agregar_producto(self, mesa):
        self.mostrar_detalle_mesa(mesa)

    def ocultar_detalle_mesa(self):
        if self.detalle_widget is not None:
            self.layout_principal.removeWidget(self.detalle_widget)
            self.detalle_widget.deleteLater()
            self.detalle_widget = None