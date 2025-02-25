# Esquema inicial de la base de datos (usando SQL)

CREATE TABLE Mesas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero INTEGER UNIQUE NOT NULL,
    pos_x INTEGER NOT NULL DEFAULT 0,
    pos_y INTEGER NOT NULL DEFAULT 0,
    estado TEXT CHECK(estado IN ('Libre', 'Ocupada', 'Reservada')) NOT NULL
);

CREATE TABLE Ingredientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    stock INTEGER NOT NULL,
    stock_minimo INTEGER NOT NULL DEFAULT 5,
    unidad TEXT NOT NULL  -- Ejemplo: gramos, unidades, litros
);

CREATE TABLE Productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL
);

CREATE TABLE Recetas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_id INTEGER NOT NULL,
    ingrediente_id INTEGER NOT NULL,
    cantidad REAL NOT NULL, -- Cantidad de ingrediente utilizada en la receta
    FOREIGN KEY (producto_id) REFERENCES Productos(id),
    FOREIGN KEY (ingrediente_id) REFERENCES Ingredientes(id)
);

CREATE TABLE Comandas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mesa_id INTEGER NOT NULL,
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado TEXT CHECK(estado IN ('Pendiente', 'En preparación', 'Servido', 'Pagado')) NOT NULL,
    FOREIGN KEY (mesa_id) REFERENCES Mesas(id)
);

CREATE TABLE DetallesComanda (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    comanda_id INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    subtotal REAL NOT NULL,
    notas TEXT, -- Para cambios en el plato por demanda del cliente
    ingredientes_excluidos TEXT, -- Ingredientes removidos de la receta original
    ingredientes_agregados TEXT, -- Ingredientes añadidos a la receta original
    FOREIGN KEY (comanda_id) REFERENCES Comandas(id),
    FOREIGN KEY (producto_id) REFERENCES Productos(id)
);

CREATE TABLE MovimientosStock (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ingrediente_id INTEGER NOT NULL,
    tipo TEXT CHECK(tipo IN ('Ingreso', 'Salida')) NOT NULL,
    cantidad REAL NOT NULL,
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    motivo TEXT,
    FOREIGN KEY (ingrediente_id) REFERENCES Ingredientes(id)
);

# Estructura de archivos del proyecto

app/
│-- main.py  # Archivo principal que ejecuta la aplicación
│-- db.py  # Manejo de la base de datos SQLite
│-- ui.py  # Interfaz gráfica (PyQt o Tkinter)
│-- models.py  # Clases y lógica de negocio (mesas, comandas, productos, ingredientes, stock)
│-- controllers.py  # Controladores para manejar la interacción entre la UI y la BD
│-- stock_manager.py  # Módulo para la gestión del stock y alertas
│-- reports.py  # Generación de reportes
│-- print_service.py  # Módulo para impresión de tickets
│-- assets/  # Recursos como imágenes o íconos
│-- docs/  # Documentación de uso
