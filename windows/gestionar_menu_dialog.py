from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QDialog, QInputDialog, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt, QByteArray
from PyQt5.QtGui import QPixmap
from controllers import obtener_todos_los_productos, agregar_producto, eliminar_producto, editar_producto

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
            
            # Mostrar la imagen
            if producto.imagen:
                pixmap = QPixmap()
                pixmap.loadFromData(QByteArray(producto.imagen))
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
                    # Seleccionar imagen
                    imagen, _ = QFileDialog.getOpenFileName(self, "Seleccionar Imagen", "", "Imágenes (*.png *.jpg *.jpeg *.bmp)")
                    agregar_producto(nombre, precio, categoria, imagen)
                    self.actualizar_menu()

    def editar_producto(self):
        # Obtener el producto seleccionado
        fila_seleccionada = self.table.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Editar Producto", "Por favor, seleccione un producto para editar.")
            return

        # Obtener los datos del producto seleccionado
        producto_id = int(self.table.item(fila_seleccionada, 0).text())
        nombre_actual = self.table.item(fila_seleccionada, 1).text()
        precio_actual = float(self.table.item(fila_seleccionada, 2).text().replace("$", ""))
        categoria_actual = self.table.item(fila_seleccionada, 3).text()

        # Pedir nuevos datos al usuario
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

        # Seleccionar una nueva imagen (opcional)
        imagen, _ = QFileDialog.getOpenFileName(self, "Seleccionar Nueva Imagen (Opcional)", "", "Imágenes (*.png *.jpg *.jpeg *.bmp)")

        # Actualizar el producto en la base de datos
        editar_producto(producto_id, nombre, precio, categoria, imagen if imagen else None)

        # Actualizar la tabla
        self.actualizar_menu()

    def eliminar_producto(self):
        producto_id, ok = QInputDialog.getInt(self, "Eliminar Producto", "Ingrese el ID del producto a eliminar:")
        if ok:
            eliminar_producto(producto_id)
            self.actualizar_menu()
