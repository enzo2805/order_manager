from models import Mesa, Producto, Ingrediente, Comanda, DetalleComanda
from db import conectar_db

def obtener_todas_las_mesas():
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, numero, estado, pos_x, pos_y, reservada_a FROM Mesas")
        return [Mesa(*fila) for fila in cursor.fetchall()]

def obtener_todos_los_productos():
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, precio FROM Productos")
        return [Producto(*fila) for fila in cursor.fetchall()]

def obtener_todos_los_ingredientes():
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, stock, stock_minimo, unidad FROM Ingredientes")
        return [Ingrediente(*fila) for fila in cursor.fetchall()]

def obtener_comandas_por_mesa(mesa_id):
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, mesa_id, fecha_hora, estado FROM Comandas WHERE mesa_id = ? AND estado = 'servido'", (mesa_id,))
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

def cambiar_estado_comanda(comanda_id, nuevo_estado):
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE Comandas SET estado = ? WHERE id = ?", (nuevo_estado, comanda_id))
        conn.commit()

def obtener_estado_mesa(mesa_id):
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT estado FROM Mesas WHERE id = ?", (mesa_id,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None

def obtener_estado_comanda(comanda_id):
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT estado FROM Comandas WHERE id = ?", (comanda_id,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None

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

def obtener_total_cuenta(mesa_id):
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT SUM(subtotal) FROM DetallesComanda 
            WHERE comanda_id IN (SELECT id FROM Comandas WHERE mesa_id = ?)
        """, (mesa_id,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado and resultado[0] is not None else 0.0

def guardar_posicion_mesa(mesa_id, pos_x, pos_y):
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE Mesas SET pos_x = ?, pos_y = ? WHERE id = ?", (pos_x, pos_y, mesa_id))
        conn.commit()