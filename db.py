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
                             
        CREATE TABLE IF NOT EXISTS Receta (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER NOT NULL,
            ingrediente_id INTEGER NOT NULL,
            cantidad_necesaria REAL NOT NULL,
            FOREIGN KEY (producto_id) REFERENCES Productos(id),
            FOREIGN KEY (ingrediente_id) REFERENCES Ingredientes(id)
        );

        CREATE TABLE IF NOT EXISTS Comandas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mesa_id INTEGER,
            fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            tipo TEXT DEFAULT 'Comer en el lugar',
            estado TEXT CHECK(estado IN ('Pendiente', 'En preparación', 'Listo', 'Pagado')) NOT NULL,
            metodo_pago TEXT DEFAULT NULL,
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
            estado TEXT CHECK(estado IN ('Pendiente', 'En preparación', 'Listo')) DEFAULT 'Pendiente',
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

if __name__ == "__main__":
    crear_tablas()
    print("Base de datos inicializada correctamente.")