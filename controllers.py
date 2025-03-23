from models import Mesa, Producto, Comanda, DetalleComanda
from db import conectar_db

def obtener_todas_las_mesas():
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, numero, estado, pos_x, pos_y, reservada_a FROM Mesas")
        return [Mesa(*fila) for fila in cursor.fetchall()]

def obtener_comandas_por_mesa(mesa_id):
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, mesa_id, fecha_hora, estado FROM Comandas WHERE mesa_id = ? AND estado != 'cerrada'", (mesa_id,))
        comandas = [Comanda(*fila) for fila in cursor.fetchall()]
        for comanda in comandas:
            comanda.detalles = obtener_detalles_comanda(comanda.id)
        return comandas

def obtener_detalles_comanda(comanda_id):
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT dc.id, dc.comanda_id, dc.producto_id, p.nombre, dc.cantidad, dc.subtotal, dc.notas, dc.ingredientes_excluidos, dc.ingredientes_agregados
            FROM DetallesComanda dc
            JOIN Productos p ON dc.producto_id = p.id
            WHERE dc.comanda_id = ?
        """, (comanda_id,))
        return [DetalleComanda(*fila) for fila in cursor.fetchall()]

def cambiar_estado_mesa(mesa_id, nuevo_estado, reservada_a=None):
    with conectar_db() as conn:
        cursor = conn.cursor()
        if nuevo_estado == "Reservada":
            cursor.execute("UPDATE Mesas SET estado = ?, reservada_a = ? WHERE id = ?", (nuevo_estado, reservada_a, mesa_id))
        else:
            cursor.execute("UPDATE Mesas SET estado = ?, reservada_a = NULL WHERE id = ?", (nuevo_estado, mesa_id))
        conn.commit()

def guardar_posicion_mesa(mesa_id, pos_x, pos_y):
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE Mesas SET pos_x = ?, pos_y = ? WHERE id = ?", (pos_x, pos_y, mesa_id))
        conn.commit()

def agregar_mesa():
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Mesas (numero, estado) VALUES ((SELECT COALESCE(MAX(numero), 0) + 1 FROM Mesas), 'Libre')")
        conn.commit()

def eliminar_mesa(mesa_id):
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Mesas WHERE id = ?", (mesa_id,))
        conn.commit()

def obtener_todos_los_productos():
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, precio, categoria, imagen FROM Productos")
        productos = []
        for fila in cursor.fetchall():
            productos.append(Producto(*fila))
        return productos

def agregar_producto(nombre, precio, categoria, imagen=None):
    with conectar_db() as conn:
        cursor = conn.cursor()
        # Leer la imagen como binario si se proporciona
        imagen_blob = None
        if imagen:
            with open(imagen, "rb") as file:
                imagen_blob = file.read()
        cursor.execute(
            "INSERT INTO Productos (nombre, precio, categoria, imagen) VALUES (?, ?, ?, ?)",
            (nombre, precio, categoria, imagen_blob),
        )
        conn.commit()

def editar_producto(producto_id, nombre, precio, categoria, imagen=None):
    with conectar_db() as conn:
        cursor = conn.cursor()
        # Leer la imagen como binario si se proporciona
        imagen_blob = None
        if imagen:
            with open(imagen, "rb") as file:
                imagen_blob = file.read()
        cursor.execute(
            """
            UPDATE Productos
            SET nombre = ?, precio = ?, categoria = ?, imagen = ?
            WHERE id = ?
            """,
            (nombre, precio, categoria, imagen_blob, producto_id),
        )
        conn.commit()

def eliminar_producto(producto_id):
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Productos WHERE id = ?", (producto_id,))
        conn.commit()

def agregar_producto_a_comanda(comanda_id=None, mesa_id=None, producto_id=None, cantidad=1, notas="", ingredientes_excluidos="", ingredientes_agregados=""):
    with conectar_db() as conn:
        cursor = conn.cursor()

        # Si no se proporciona un comanda_id, buscar o crear una comanda asociada a la mesa
        if comanda_id is None:
            if mesa_id is None:
                raise ValueError("Debe proporcionarse un comanda_id o una mesa_id.")
            
            # Buscar una comanda pendiente para la mesa
            cursor.execute("SELECT id FROM Comandas WHERE mesa_id = ? AND estado = 'Pendiente'", (mesa_id,))
            comanda = cursor.fetchone()
            if comanda is None:
                # Crear una nueva comanda si no existe una comanda pendiente
                cursor.execute("INSERT INTO Comandas (mesa_id, estado, tipo) VALUES (?, 'Pendiente', 'Comer en el lugar')", (mesa_id,))
                comanda_id = cursor.lastrowid
            else:
                comanda_id = comanda[0]

        # Agregar el producto a la comanda
        cursor.execute("""
            INSERT INTO DetallesComanda (comanda_id, producto_id, cantidad, subtotal, notas, ingredientes_excluidos, ingredientes_agregados)
            VALUES (?, ?, ?, (SELECT precio FROM Productos WHERE id = ?) * ?, ?, ?, ?)
        """, (comanda_id, producto_id, cantidad, producto_id, cantidad, notas, ingredientes_excluidos, ingredientes_agregados))
        conn.commit()

def crear_comanda_para_llevar():
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Comandas (mesa_id, estado, tipo) VALUES (NULL, 'Pendiente', 'Para llevar')"
        )
        conn.commit()
        return cursor.lastrowid

def obtener_detalles_comanda(comanda_id):
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT d.id, d.comanda_id, d.producto_id, p.nombre, d.cantidad, d.subtotal, d.notas, d.ingredientes_excluidos, d.ingredientes_agregados
            FROM DetallesComanda d
            JOIN Productos p ON d.producto_id = p.id
            WHERE d.comanda_id = ?
        """, (comanda_id,))
        detalles = []
        for row in cursor.fetchall():
            detalles.append(DetalleComanda(*row))
        return detalles

def cambiar_estado_comanda(comanda_id, nuevo_estado):
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE Comandas SET estado = ? WHERE id = ?", (nuevo_estado, comanda_id))
        conn.commit()

def obtener_todas_las_comandas():
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, mesa_id, fecha_hora, estado, tipo
            FROM Comandas
        """)
        comandas = []
        for row in cursor.fetchall():
            comandas.append(Comanda(*row))
        return comandas