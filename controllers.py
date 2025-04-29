from models import Mesa, Producto, Comanda, DetalleComanda, Ingrediente
from db import conectar_db

def obtener_todas_las_mesas():
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, numero, estado, pos_x, pos_y, reservada_a FROM Mesas")
        return [Mesa(*fila) for fila in cursor.fetchall()]

def obtener_comandas_por_mesa(mesa_id):
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, mesa_id, fecha_hora, estado, tipo, metodo_pago
            FROM Comandas
            WHERE mesa_id = ? AND estado != 'Pagado'
        """, (mesa_id,))
        comandas = []
        for row in cursor.fetchall():
            comanda = Comanda(*row)
            cursor.execute("""
                SELECT d.id, d.comanda_id, d.producto_id, p.nombre, d.cantidad, d.estado, 
                       d.notas, d.ingredientes_excluidos, d.ingredientes_agregados, d.subtotal
                FROM DetallesComanda d
                JOIN Productos p ON d.producto_id = p.id
                WHERE d.comanda_id = ?
            """, (comanda.id,))
            detalles = []
            for detalle_row in cursor.fetchall():
                detalles.append(DetalleComanda(*detalle_row))
            comanda.detalles = detalles
            comandas.append(comanda)
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

def agregar_producto_a_comanda(comanda_id, producto_id, cantidad, notas=""):
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO DetallesComanda (comanda_id, producto_id, cantidad, subtotal, notas)
            VALUES (?, ?, ?, (SELECT precio FROM Productos WHERE id = ?) * ?, ?)
        """, (comanda_id, producto_id, cantidad, producto_id, cantidad, notas))
        conn.commit()

def crear_comanda(mesa_id):
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Comandas (mesa_id, estado, tipo) VALUES (?, 'Pendiente', 'Comer en el lugar')",
            (mesa_id,)
        )
        conn.commit()
        return cursor.lastrowid

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
            SELECT dc.id, dc.comanda_id, dc.producto_id, p.nombre, dc.cantidad, dc.estado, dc.notas, 
                   dc.ingredientes_excluidos, dc.ingredientes_agregados, dc.subtotal
            FROM DetallesComanda dc
            JOIN Productos p ON dc.producto_id = p.id
            WHERE dc.comanda_id = ?
        """, (comanda_id,))
        return [DetalleComanda(*fila) for fila in cursor.fetchall()]
    

def obtener_detalles_comanda_cocina(comanda_id):
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT dc.id, dc.comanda_id, dc.producto_id, p.nombre, dc.cantidad, dc.estado, dc.notas, 
                   dc.ingredientes_excluidos, dc.ingredientes_agregados, dc.subtotal
            FROM DetallesComanda dc
            JOIN Productos p ON dc.producto_id = p.id
            WHERE dc.comanda_id = ? AND p.categoria NOT IN ('Alchohol', 'No alcoholico') AND dc.estado != 'Listo'
        """, (comanda_id,))
        return [DetalleComanda(*fila) for fila in cursor.fetchall()]

def cambiar_estado_comanda(comanda_id, nuevo_estado, metodo_pago=None):
    with conectar_db() as conn:
        cursor = conn.cursor()
        if metodo_pago:
            cursor.execute(
                "UPDATE Comandas SET estado = ?, metodo_pago = ? WHERE id = ?",
                (nuevo_estado, metodo_pago, comanda_id)
            )
        else:
            cursor.execute(
                "UPDATE Comandas SET estado = ? WHERE id = ?",
                (nuevo_estado, comanda_id)
            )
        conn.commit()

def cambiar_estado_detalle_comanda(detalle_id, nuevo_estado):
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE DetallesComanda SET estado = ? WHERE id = ?",
            (nuevo_estado, detalle_id)
        )
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

def actualizar_estado_comanda(comanda_id):
    with conectar_db() as conn:
        cursor = conn.cursor()

        # Verificar los estados de los detalles
        cursor.execute("""
            SELECT estado
            FROM DetallesComanda
            WHERE comanda_id = ?
        """, (comanda_id,))
        estados = [row[0] for row in cursor.fetchall()]

        # Determinar el estado de la comanda
        if all(estado == "Listo" for estado in estados):
            nuevo_estado = "Listo"
        elif any(estado == "En preparación" for estado in estados):
            nuevo_estado = "En preparación"
        else:
            nuevo_estado = "Pendiente"

        # Actualizar el estado de la comanda
        cursor.execute("""
            UPDATE Comandas
            SET estado = ?
            WHERE id = ?
        """, (nuevo_estado, comanda_id))
        conn.commit()
    
def obtener_ingredientes():
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, stock, stock_minimo, unidad FROM Ingredientes")
        return [Ingrediente(*row) for row in cursor.fetchall()]
    
def agregar_ingrediente(nombre, stock, stock_minimo, unidad):
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute( "INSERT INTO Ingredientes (nombre, stock, stock_minimo, unidad) VALUES (?, ?, ?, ?)",
            (nombre, stock, stock_minimo, unidad)
        )
        conn.commit()

def editar_ingrediente(ingrediente_id, nombre, stock, stock_minimo, unidad):
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Ingredientes SET nombre = ?, stock = ?, stock_minimo = ?, unidad = ? WHERE id = ?",
            (nombre, stock, stock_minimo, unidad, ingrediente_id)
        )
        conn.commit()

def eliminar_ingrediente(ingrediente_id):
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Ingredientes WHERE id = ?", (ingrediente_id,))
        conn.commit()

def obtener_comandas_pendientes_y_en_preparacion():
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, mesa_id, fecha_hora, estado, tipo
            FROM Comandas
            WHERE estado IN ('Pendiente', 'En preparación')
        """)
        comandas = []
        for row in cursor.fetchall():
            comanda = Comanda(*row)
            cursor.execute("""
                SELECT d.id, d.comanda_id, d.producto_id, p.nombre, d.cantidad, d.estado, d.notas, 
                       d.ingredientes_excluidos, d.ingredientes_agregados, d.subtotal
                FROM DetallesComanda d
                JOIN Productos p ON d.producto_id = p.id
                WHERE d.comanda_id = ? AND p.categoria NOT IN ('Alchohol', 'No alcoholico')
            """, (comanda.id,))
            detalles = [DetalleComanda(*detalle_row) for detalle_row in cursor.fetchall()]
            comanda.detalles = detalles
            comandas.append(comanda)
        return comandas
    
def descontar_ingredientes(comanda_id):
    with conectar_db() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT producto_id, cantidad
            FROM DetallesComanda
            WHERE comanda_id = ?
        """, (comanda_id,))
        productos = cursor.fetchall()

        for producto_id, cantidad in productos:
            cursor.execute("""
                SELECT ingrediente_id, cantidad_necesaria
                FROM Receta
                WHERE producto_id = ?
            """, (producto_id,))
            ingredientes = cursor.fetchall()

            for ingrediente_id, cantidad_necesaria in ingredientes:
                cursor.execute("""
                    UPDATE Ingredientes
                    SET stock = stock - ?
                    WHERE id = ?
                """, (cantidad * cantidad_necesaria, ingrediente_id))

        conn.commit()

def agregar_receta(producto_id, ingrediente_id, cantidad_necesaria):
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Receta (producto_id, ingrediente_id, cantidad_necesaria)
            VALUES (?, ?, ?)
        """, (producto_id, ingrediente_id, cantidad_necesaria))
        conn.commit()

def editar_receta(receta_id, cantidad_necesaria):
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Receta
            SET cantidad_necesaria = ?
            WHERE id = ?
        """, (cantidad_necesaria, receta_id))
        conn.commit()

def eliminar_receta(receta_id):
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM Receta
            WHERE id = ?
        """, (receta_id,))
        conn.commit()

def obtener_recetas_por_producto(producto_id):
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.id, r.ingrediente_id, i.nombre, r.cantidad_necesaria, i.unidad
            FROM Receta r
            JOIN Ingredientes i ON r.ingrediente_id = i.id
            WHERE r.producto_id = ?
        """, (producto_id,))
        return cursor.fetchall()
    
def verificar_stock(producto_id, cantidad_producto):
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT i.nombre, i.stock, r.cantidad_necesaria * ?
            FROM Receta r
            JOIN Ingredientes i ON r.ingrediente_id = i.id
            WHERE r.producto_id = ?
        """, (cantidad_producto, producto_id))
        ingredientes = cursor.fetchall()

        faltantes = []
        for nombre, stock, cantidad_requerida in ingredientes:
            if stock < cantidad_requerida:
                faltantes.append((nombre, stock, cantidad_requerida))
        return faltantes

def descontar_ingredientes(producto_id, cantidad_producto):
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.ingrediente_id, r.cantidad_necesaria * ?
            FROM Receta r
            WHERE r.producto_id = ?
        """, (cantidad_producto, producto_id))
        ingredientes = cursor.fetchall()

        for ingrediente_id, cantidad_a_descontar in ingredientes:
            cursor.execute("""
                UPDATE Ingredientes
                SET stock = stock - ?
                WHERE id = ?
            """, (cantidad_a_descontar, ingrediente_id))
        conn.commit()

def obtener_todos_los_ingredientes():
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre FROM Ingredientes")
        return cursor.fetchall()