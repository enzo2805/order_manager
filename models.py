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


class Producto:
    def __init__(self, id, nombre, precio, categoria, imagen=None):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        self.imagen = imagen

    def __repr__(self):
        return f"{self.nombre} - ${self.precio:.2f} ({self.categoria})"

class Ingrediente:
    def __init__(self, id, nombre, stock, stock_minimo, unidad):
        self.id = id
        self.nombre = nombre
        self.stock = stock
        self.stock_minimo = stock_minimo
        self.unidad = unidad

    def __repr__(self):
        return f"{self.nombre}: {self.stock} {self.unidad} (Mín: {self.stock_minimo})"

class Comanda:
    def __init__(self, id, mesa_id, fecha_hora, estado):
        self.id = id
        self.mesa_id = mesa_id
        self.fecha_hora = fecha_hora
        self.estado = estado
        self.detalles = []

    def agregar_detalle(self, detalle):
        self.detalles.append(detalle)

    def calcular_total(self):
        return sum(detalle.subtotal for detalle in self.detalles)

    def __repr__(self):
        return f"Comanda {self.id} - Mesa {self.mesa_id} ({self.estado})"

class DetalleComanda:
    def __init__(self, id, comanda_id, producto_id, producto_nombre, cantidad, subtotal, notas, ingredientes_excluidos, ingredientes_agregados):
        self.id = id
        self.comanda_id = comanda_id
        self.producto_id = producto_id
        self.producto_nombre = producto_nombre
        self.cantidad = cantidad
        self.subtotal = subtotal
        self.notas = notas
        self.ingredientes_excluidos = ingredientes_excluidos
        self.ingredientes_agregados = ingredientes_agregados

    def __repr__(self):
        return f"{self.producto_nombre} x{self.cantidad} - ${self.subtotal:.2f}"