import requests

BASE_URL = "http://localhost:5000"  # Cambia esto si el servidor está en otra dirección o puerto

def obtener_mesas():
    response = requests.get(f"{BASE_URL}/mesas")
    response.raise_for_status()
    return response.json()

def cambiar_estado_mesa(id, estado, reservada_a=None):
    payload = {"estado": estado}
    if reservada_a:
        payload["reservada_a"] = reservada_a
    response = requests.put(f"{BASE_URL}/mesas/{id}/estado", json=payload)
    response.raise_for_status()
    return response.json()

def obtener_comandas_por_mesa(id):
    response = requests.get(f"{BASE_URL}/mesas/{id}/comandas")
    response.raise_for_status()
    return response.json()

def crear_mesa():
    response = requests.post(f"{BASE_URL}/mesas")
    response.raise_for_status()
    return response.json()

def eliminar_mesa(mesa_id):
    response = requests.delete(f"{BASE_URL}/mesas/{mesa_id}")
    response.raise_for_status()
    return response.json()

def cambiar_mesa_comanda(comanda_id, nueva_mesa_id):
    payload = {"nueva_mesa_id": nueva_mesa_id}
    response = requests.put(f"{BASE_URL}/comandas/{comanda_id}/mover", json=payload)
    response.raise_for_status()
    return response.json()

def obtener_comandas_pendientes_y_en_preparacion():
    response = requests.get(f"{BASE_URL}/comandas_cocina")
    response.raise_for_status()
    return response.json()

def crear_comanda(mesa_id):
    payload = {"mesa_id": mesa_id}
    response = requests.post(f"{BASE_URL}/comandas", json=payload)
    response.raise_for_status()
    return response.json()

def crear_comanda_para_llevar():
    response = requests.post(f"{BASE_URL}/comandas/para_llevar")
    response.raise_for_status()
    return response.json()

def agregar_producto_a_comanda(comanda_id, producto_id, cantidad, notas=""):
    payload = {"producto_id": producto_id, "cantidad": cantidad, "notas": notas}
    response = requests.post(f"{BASE_URL}/comandas/{comanda_id}/productos", json=payload)
    response.raise_for_status()
    return response.json()

def cambiar_estado_detalle_comanda(comanda_id, estado):
    payload = {"estado": estado}
    response = requests.put(f"{BASE_URL}/detalle_comanda/{comanda_id}/estado", json=payload)
    response.raise_for_status()
    return response.json()

def cambiar_estado_comanda(comanda_id, estado, metodo_pago=None):
    payload = {"estado": estado, "metodo_pago": metodo_pago}
    response = requests.put(f"{BASE_URL}/comanda/{comanda_id}/estado", json=payload)
    response.raise_for_status()
    return response.json()

def obtener_productos():
    response = requests.get(f"{BASE_URL}/productos")
    response.raise_for_status()
    return response.json()

def agregar_producto(nombre, precio, categoria, imagen=None):
    payload = {"nombre": nombre, "precio": precio, "categoria": categoria, "imagen": imagen}
    response = requests.post(f"{BASE_URL}/productos", json=payload)
    response.raise_for_status()
    return response.json()

def editar_producto(id, nombre, precio, categoria, imagen=None):
    payload = {"nombre": nombre, "precio": precio, "categoria": categoria, "imagen": imagen}
    response = requests.put(f"{BASE_URL}/productos/{id}", json=payload)
    response.raise_for_status()
    return response.json()

def eliminar_producto(id):
    response = requests.delete(f"{BASE_URL}/productos/{id}")
    response.raise_for_status()
    return response.json()

def obtener_detalles_comanda(comanda_id):
    response = requests.get(f"{BASE_URL}/comandas/{comanda_id}")
    response.raise_for_status()
    return response.json()

def obtener_ingredientes():
    response = requests.get(f"{BASE_URL}/ingredientes")
    response.raise_for_status()
    return response.json()

def agregar_ingrediente(nombre, stock, stock_minimo, unidad):
    payload = {
        "nombre": nombre,
        "stock": stock,
        "stock_minimo": stock_minimo,
        "unidad": unidad
    }
    response = requests.post(f"{BASE_URL}/ingredientes", json=payload)
    response.raise_for_status()
    return response.json()

def editar_ingrediente(id, nombre, stock, stock_minimo, unidad):
    payload = {
        "nombre": nombre,
        "stock": stock,
        "stock_minimo": stock_minimo,
        "unidad": unidad
    }
    response = requests.put(f"{BASE_URL}/ingredientes/{id}", json=payload)
    response.raise_for_status()
    return response.json()

def eliminar_ingrediente(id):
    response = requests.delete(f"{BASE_URL}/ingredientes/{id}")
    response.raise_for_status()
    return response.json()

def obtener_recetas_por_producto(producto_id):
    response = requests.get(f"{BASE_URL}/productos/{producto_id}/recetas")
    response.raise_for_status()
    return response.json()

def agregar_receta(producto_id, ingrediente_id, cantidad_necesaria):
    payload = {
        "producto_id": producto_id,
        "ingrediente_id": ingrediente_id,
        "cantidad_necesaria": cantidad_necesaria
    }
    response = requests.post(f"{BASE_URL}/recetas", json=payload)
    response.raise_for_status()
    return response.json()

def editar_receta(receta_id, cantidad_necesaria):
    payload = {"cantidad_necesaria": cantidad_necesaria}
    response = requests.put(f"{BASE_URL}/recetas/{receta_id}", json=payload)
    response.raise_for_status()
    return response.json()

def eliminar_ingrediente_de_receta(receta_id):
    response = requests.delete(f"{BASE_URL}/recetas/{receta_id}")
    response.raise_for_status()
    return response.json()

def obtener_todas_las_comandas():
    response = requests.get(f"{BASE_URL}/comandas")
    response.raise_for_status()
    return response.json()

def obtener_todas_las_comandas_para_mesas():
    response = requests.get(f"{BASE_URL}/comandas_mesas")
    response.raise_for_status()
    return response.json()

def guardar_posicion_mesa(mesa_id, pos_x, pos_y):
    payload = {"pos_x": pos_x, "pos_y": pos_y}
    response = requests.put(f"{BASE_URL}/mesas/{mesa_id}/posicion", json=payload)
    response.raise_for_status()
    return response.json()