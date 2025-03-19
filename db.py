import sqlite3

def conectar_db():
    return sqlite3.connect("comedor.db")

def crear_tablas():
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.executescript("""
        CREATE TABLE IF NOT EXISTS Mesas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero INTEGER UNIQUE NOT NULL,
            estado TEXT CHECK(estado IN ('Libre', 'Ocupada', 'Reservada')) NOT NULL,
            reservada_a TEXT,
            pos_x INTEGER DEFAULT 0,
            pos_y INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS Ingredientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            stock INTEGER NOT NULL,
            stock_minimo INTEGER NOT NULL DEFAULT 5,
            unidad TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            imagen TEXT,
            categoria TEXT NOT NULL CHECK(categoria IN ('Entrada', 'Plato principal', 'Desayuno/Merienda', 'Postre', 'Alchohol', 'No alcoholico', 'Extra')),
        );

        CREATE TABLE IF NOT EXISTS Comandas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mesa_id INTEGER NOT NULL,
            fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            estado TEXT CHECK(estado IN ('Pendiente', 'En preparación', 'Servido', 'Pagado')) NOT NULL,
            FOREIGN KEY (mesa_id) REFERENCES Mesas(id)
        );

        CREATE TABLE IF NOT EXISTS DetallesComanda (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            comanda_id INTEGER NOT NULL,
            producto_id INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            subtotal REAL NOT NULL,
            notas TEXT,
            ingredientes_excluidos TEXT,
            ingredientes_agregados TEXT,
            FOREIGN KEY (comanda_id) REFERENCES Comandas(id),
            FOREIGN KEY (producto_id) REFERENCES Productos(id)
        );

        CREATE TABLE IF NOT EXISTS MovimientosStock (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ingrediente_id INTEGER NOT NULL,
            tipo TEXT CHECK(tipo IN ('Ingreso', 'Salida')) NOT NULL,
            cantidad REAL NOT NULL,
            fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            motivo TEXT,
            FOREIGN KEY (ingrediente_id) REFERENCES Ingredientes(id)
        );
        """)
        conn.commit()

def insertar_mesa(numero, estado):
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Mesas (numero, estado) VALUES (?, ?)", (numero, estado))
        conn.commit()

def insertar_producto(nombre, precio):
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Productos (nombre, precio) VALUES (?, ?)", (nombre, precio))
        conn.commit()

def insertar_ingrediente(nombre, stock, stock_minimo, unidad):
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Ingredientes (nombre, stock, stock_minimo, unidad) VALUES (?, ?, ?, ?)", 
                       (nombre, stock, stock_minimo, unidad))
        conn.commit()

def obtener_productos():
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Productos")
        return cursor.fetchall()

def obtener_mesas():
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Mesas")
        return cursor.fetchall()

def obtener_ingredientes():
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Ingredientes")
        return cursor.fetchall()

if __name__ == "__main__":
    crear_tablas()
    print("Base de datos inicializada correctamente.")