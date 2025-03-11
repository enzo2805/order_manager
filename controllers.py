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
        cursor.execute("SELECT id, nombre, precio, categoria FROM Productos")
        return [Producto(*fila) for fila in cursor.fetchall()]

def agregar_producto(nombre, precio, categoria):
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Productos (nombre, precio, categoria) VALUES (?, ?, ?)", (nombre, precio, categoria))
        conn.commit()

def eliminar_producto(producto_id):
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Productos WHERE id = ?", (producto_id,))
        conn.commit()

def agregar_producto_a_comanda(mesa_id, producto_id, cantidad, notas="", ingredientes_excluidos="", ingredientes_agregados=""):
    with conectar_db() as conn:
        cursor = conn.cursor()
        # Verificar si hay una comanda Pendiente para la mesa
        cursor.execute("SELECT id FROM Comandas WHERE mesa_id = ? AND estado = 'Pendiente'", (mesa_id,))
        comanda = cursor.fetchone()
        if comanda is None:
            # Crear una nueva comanda si no existe una comanda Pendiente
            cursor.execute("INSERT INTO Comandas (mesa_id, estado) VALUES (?, 'Pendiente')", (mesa_id,))
            comanda_id = cursor.lastrowid
        else:
            comanda_id = comanda[0]
        
        # Agregar el producto a la comanda
        cursor.execute("""
            INSERT INTO DetallesComanda (comanda_id, producto_id, cantidad, subtotal, notas, ingredientes_excluidos, ingredientes_agregados)
            VALUES (?, ?, ?, (SELECT precio FROM Productos WHERE id = ?) * ?, ?, ?, ?)
        """, (comanda_id, producto_id, cantidad, producto_id, cantidad, notas, ingredientes_excluidos, ingredientes_agregados))
        conn.commit()