import base64


class Mesa:
    def __init__(self, id, numero, estado, pos_x, pos_y, reservada_a=None):
        self.id = id
        self.numero = numero
        self.estado = estado
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.reservada_a = reservada_a

    def __repr__(self):
        reservada_info = f" - Reservada a: {self.reservada_a}" if self.reservada_a else ""
        return f"Mesa {self.numero} ({self.estado}) - Posición: ({self.pos_x}, {self.pos_y}){reservada_info}"
    
    def __dict__(self):
        return {
            "id": self.id,
            "numero": self.numero,
            "estado": self.estado,
            "pos_x": self.pos_x,
            "pos_y": self.pos_y,
            "reservada_a": self.reservada_a
        }
    
    def to_dict(self):
        return {
            "id": self.id,
            "numero": self.numero,
            "estado": self.estado,
            "pos_x": self.pos_x,
            "pos_y": self.pos_y,
            "reservada_a": self.reservada_a
        }


class Producto:
    def __init__(self, id, nombre, precio, categoria, imagen=None):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        self.imagen = imagen

    def __repr__(self):
        return f"{self.nombre} - ${self.precio:.2f} ({self.categoria})"
    
    def __dict__(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio,
            "categoria": self.categoria,
            "imagen": self.imagen
        }
    
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio,
            "categoria": self.categoria,
            "imagen": base64.b64encode(self.imagen).decode('utf-8') if self.imagen else None
        }

class Ingrediente:
    def __init__(self, id, nombre, stock, stock_minimo, unidad):
        self.id = id
        self.nombre = nombre
        self.stock = stock
        self.stock_minimo = stock_minimo
        self.unidad = unidad

    def __repr__(self):
        return f"{self.nombre}: {self.stock} {self.unidad} (Mín: {self.stock_minimo})"
    
    def __dict__(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "stock": self.stock,
            "stock_minimo": self.stock_minimo,
            "unidad": self.unidad
        }

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "stock": self.stock,
            "stock_minimo": self.stock_minimo,
            "unidad": self.unidad
        }

class Comanda:
    def __init__(self, id, mesa_id, fecha_hora, estado, tipo, metodo_pago):
        self.id = id
        self.mesa_id = mesa_id
        self.fecha_hora = fecha_hora
        self.estado = estado
        self.tipo = tipo
        self.metodo_pago = metodo_pago
        self.detalles = []

    def __dict__(self):
        return {
            "id": self.id,
            "mesa_id": self.mesa_id,
            "fecha_hora": self.fecha_hora,
            "estado": self.estado,
            "tipo": self.tipo,
            "metodo_pago": self.metodo_pago,
            "detalles": [detalle.__dict__() for detalle in self.detalles]
        }
    
    def to_dict(self):
        return {
            "id": self.id,
            "mesa_id": self.mesa_id,
            "fecha_hora": self.fecha_hora,
            "estado": self.estado,
            "tipo": self.tipo,
            "metodo_pago": self.metodo_pago,
            "detalles": [detalle.to_dict() for detalle in self.detalles]
        }
    
    def __repr__(self):
        return f"Comanda {self.id} - Mesa {self.mesa_id} - Estado: {self.estado} - Tipo: {self.tipo} - Método de Pago: {self.metodo_pago} - Fecha/Hora: {self.fecha_hora} - Detalles: {len(self.detalles)}"

class DetalleComanda:
    def __init__(self, id, comanda_id, producto_id, producto_nombre, cantidad, estado, notas, ingredientes_excluidos, ingredientes_agregados, subtotal):
        self.id = id
        self.comanda_id = comanda_id
        self.producto_id = producto_id
        self.producto_nombre = producto_nombre
        self.cantidad = cantidad
        self.estado = estado
        self.notas = notas
        self.ingredientes_excluidos = ingredientes_excluidos
        self.ingredientes_agregados = ingredientes_agregados
        self.subtotal = subtotal

    def __dict__(self):
        return {
            "id": self.id,
            "comanda_id": self.comanda_id,
            "producto_id": self.producto_id,
            "producto_nombre": self.producto_nombre,
            "cantidad": self.cantidad,
            "estado": self.estado,
            "notas": self.notas,
            "ingredientes_excluidos": self.ingredientes_excluidos,
            "ingredientes_agregados": self.ingredientes_agregados,
            "subtotal": self.subtotal
        }

    def to_dict(self):
        return {
            "id": self.id,
            "comanda_id": self.comanda_id,
            "producto_id": self.producto_id,
            "producto_nombre": self.producto_nombre,
            "cantidad": self.cantidad,
            "estado": self.estado,
            "notas": self.notas,
            "ingredientes_excluidos": self.ingredientes_excluidos,
            "ingredientes_agregados": self.ingredientes_agregados,
            "subtotal": self.subtotal
        }

    def __repr__(self):
        return f"{self.producto_nombre} x{self.cantidad} - ${self.subtotal:.2f}"
    
class Receta:
    def __init__(self, id, ingrediente_id, nombre, cantidad_necesaria, unidad):
        self.id = id
        self.ingrediente_id = ingrediente_id
        self.nombre = nombre
        self.cantidad_necesaria = cantidad_necesaria
        self.unidad = unidad

    def __repr__(self):
        return f"Receta {self.id} - Ingrediente ID: {self.ingrediente_id}, Ingrediente ID: {self.nombre}, Cantidad: {self.cantidad_necesaria}, Unidad: {self.unidad}"
    
    def __dict__(self):
        return {
            "id": self.id,
            "ingrediente_id": self.ingrediente_id,
            "nombre": self.nombre,
            "cantidad_necesaria": self.cantidad_necesaria,
            "unidad": self.unidad
        }

    def to_dict(self):
        return {
            "id": self.id,
            "ingrediente_id": self.ingrediente_id,
            "nombre": self.nombre,
            "cantidad_necesaria": self.cantidad_necesaria,
            "unidad": self.unidad
        }