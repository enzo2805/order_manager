from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QDialog, QInputDialog, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt, QByteArray
from PyQt5.QtGui import QPixmap
from api_client import obtener_productos, agregar_producto, editar_producto, eliminar_producto
from windows.gestionar_recetas_dialog import GestionarRecetasDialog

class GestionarMenuDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gestionar Menú")
        self.setGeometry(100, 100, 600, 400)
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setRowCount(0)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Precio", "Categoría", "Imagen"])

        self.actualizar_menu()

        layout.addWidget(self.table)

        botones_layout = QHBoxLayout()
        self.boton_agregar = QPushButton("Agregar Producto")
        self.boton_agregar.clicked.connect(self.agregar_producto)
        botones_layout.addWidget(self.boton_agregar)

        self.boton_editar = QPushButton("Editar Producto")
        self.boton_editar.clicked.connect(self.editar_producto)
        botones_layout.addWidget(self.boton_editar)

        self.boton_eliminar = QPushButton("Eliminar Producto")
        self.boton_eliminar.clicked.connect(self.eliminar_producto)
        botones_layout.addWidget(self.boton_eliminar)

        self.boton_recetas = QPushButton("Gestionar Recetas")
        self.boton_recetas.clicked.connect(self.gestionar_recetas)
        botones_layout.addWidget(self.boton_recetas)

        layout.addLayout(botones_layout)
        self.setLayout(layout)

    def gestionar_recetas(self):
        fila_seleccionada = self.table.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Gestionar Recetas", "Por favor, seleccione un producto para gestionar sus recetas.")
            return

        producto_id = int(self.table.item(fila_seleccionada, 0).text())
        nombre_producto = self.table.item(fila_seleccionada, 1).text()

        dialog = GestionarRecetasDialog(producto_id, nombre_producto, self)
        dialog.exec_()
        
    def actualizar_menu(self):
        productos = obtener_productos()
        self.table.setRowCount(len(productos))
        for row, producto in enumerate(productos):
            self.table.setItem(row, 0, QTableWidgetItem(str(producto["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(producto["nombre"]))
            self.table.setItem(row, 2, QTableWidgetItem(f"${producto['precio']:.2f}"))
            self.table.setItem(row, 3, QTableWidgetItem(producto["categoria"]))
            
            if producto["imagen"]:
                pixmap = QPixmap()
                pixmap.loadFromData(QByteArray.fromBase64(producto["imagen"].encode('utf-8')))
                item_imagen = QTableWidgetItem()
                item_imagen.setData(Qt.DecorationRole, pixmap.scaled(50, 50, Qt.KeepAspectRatio))
                self.table.setItem(row, 4, item_imagen)
            else:
                self.table.setItem(row, 4, QTableWidgetItem("Sin imagen"))

    def agregar_producto(self):
        nombre, ok = QInputDialog.getText(self, "Agregar Producto", "Ingrese el nombre del producto:")
        if ok and nombre:
            precio, ok = QInputDialog.getDouble(self, "Agregar Producto", "Ingrese el precio del producto:")
            if ok:
                categorias = ["Entrada", "Plato principal", "Desayuno/Merienda", "Postre", "Alcohol", "No alcoholico", "Extra"]
                categoria, ok = QInputDialog.getItem(self, "Agregar Producto", "Seleccione la categoría del producto:", categorias, 0, False)
                if ok and categoria:
                    imagen, _ = QFileDialog.getOpenFileName(self, "Seleccionar Imagen", "", "Imágenes (*.png *.jpg *.jpeg *.bmp)")
                    agregar_producto(nombre, precio, categoria, imagen)
                    self.actualizar_menu()

    def editar_producto(self):
        fila_seleccionada = self.table.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Editar Producto", "Por favor, seleccione un producto para editar.")
            return

        producto_id = int(self.table.item(fila_seleccionada, 0).text())
        nombre_actual = self.table.item(fila_seleccionada, 1).text()
        precio_actual = float(self.table.item(fila_seleccionada, 2).text().replace("$", ""))
        categoria_actual = self.table.item(fila_seleccionada, 3).text()

        nombre, ok = QInputDialog.getText(self, "Editar Producto", "Ingrese el nuevo nombre del producto:", text=nombre_actual)
        if not ok or not nombre:
            return

        precio, ok = QInputDialog.getDouble(self, "Editar Producto", "Ingrese el nuevo precio del producto:", value=precio_actual)
        if not ok:
            return

        categorias = ["Entrada", "Plato principal", "Desayuno/Merienda", "Postre", "Alcohol", "No alcoholico", "Extra"]
        categoria, ok = QInputDialog.getItem(self, "Editar Producto", "Seleccione la nueva categoría del producto:", categorias, categorias.index(categoria_actual), False)
        if not ok:
            return

        imagen, _ = QFileDialog.getOpenFileName(self, "Seleccionar Nueva Imagen (Opcional)", "", "Imágenes (*.png *.jpg *.jpeg *.bmp)")

        editar_producto(producto_id, nombre, precio, categoria, imagen if imagen else None)

        self.actualizar_menu()

    def eliminar_producto(self):
        fila_seleccionada = self.table.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Eliminar Producto", "Por favor, seleccione un producto para eliminar.")
            return

        producto_id = int(self.table.item(fila_seleccionada, 0).text())
        respuesta = QMessageBox.question(self, "Eliminar Producto", "¿Está seguro de que desea eliminar este producto?", QMessageBox.Yes | QMessageBox.No)
        if respuesta == QMessageBox.Yes:
            eliminar_producto(producto_id)
            self.actualizar_menu()