from flask import Flask, jsonify, request
from flask_cors import CORS
from controllers import (
    agregar_ingrediente,
    agregar_mesa,
    agregar_receta,
    cambiar_estado_comanda,
    cambiar_estado_detalle_comanda,
    cambiar_mesa_comanda,
    editar_ingrediente,
    editar_receta,
    eliminar_ingrediente,
    eliminar_ingrediente_de_receta,
    eliminar_mesa,
    guardar_posicion_mesa,
    obtener_comandas_pendientes_y_en_preparacion,
    obtener_detalles_comanda,
    obtener_ingredientes,
    obtener_recetas_por_producto,
    obtener_todas_las_comandas_para_mesas,
    obtener_todas_las_mesas,
    cambiar_estado_mesa,
    obtener_comandas_por_mesa,
    crear_comanda,
    crear_comanda_para_llevar,
    agregar_producto_a_comanda,
    obtener_todos_los_productos,
    agregar_producto,
    editar_producto,
    eliminar_producto,
    obtener_todas_las_comandas,
)

app = Flask(__name__)
CORS(app)

app = Flask(__name__)
CORS(app)

@app.route('/mesas', methods=['GET'])
def obtener_mesas_endpoint():
    try:
        mesas = obtener_todas_las_mesas()
        return ([mesa.to_dict() for mesa in mesas]), 200
    except Exception as e:
        print(f"Error al obtener mesas: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/mesas/<int:id>/estado', methods=['PUT'])
def cambiar_estado_mesa_endpoint(id):
    datos = request.json
    nuevo_estado = datos.get("estado")
    reservada_a = datos.get("reservada_a", None)
    try:
        cambiar_estado_mesa(id, nuevo_estado, reservada_a)
        return jsonify({"id": id, "estado": nuevo_estado, "reservada_a": reservada_a})
    except Exception as e:
        print(f"Error al cambiar el estado de la mesa {id}: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/mesas/<int:id>/comandas', methods=['GET'])
def obtener_comandas_por_mesa_endpoint(id):
    try:
        comandas = obtener_comandas_por_mesa(id)
        return jsonify([comanda.to_dict() for comanda in comandas])
    except Exception as e:
        print(f"Error al obtener comandas para la mesa {id}: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/comandas', methods=['POST'])
def crear_comanda_endpoint():
    datos = request.json
    mesa_id = datos["mesa_id"]
    comanda_id = crear_comanda(mesa_id)
    return jsonify({"id": comanda_id, "mesa_id": mesa_id, "estado": "Pendiente"}), 201

@app.route('/comandas/para_llevar', methods=['POST'])
def crear_comanda_para_llevar_endpoint():
    try:
        comanda_id = crear_comanda_para_llevar()
        return jsonify({"id": comanda_id, "tipo": "Para llevar", "estado": "Pendiente"}), 201
    except Exception as e:
        print(f"Error al crear comanda para llevar: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/comandas/<int:id>/productos', methods=['POST'])
def agregar_producto_a_comanda_endpoint(id):
    datos = request.json
    producto_id = datos["producto_id"]
    cantidad = datos["cantidad"]
    notas = datos.get("notas", "")
    agregar_producto_a_comanda(id, producto_id, cantidad, notas)
    return jsonify({"comanda_id": id, "producto_id": producto_id, "cantidad": cantidad, "notas": notas})

@app.route('/productos', methods=['GET'])
def obtener_productos_endpoint():
    productos = obtener_todos_los_productos()
    if not productos:
        return jsonify([]), 200
    return jsonify([producto.to_dict() for producto in productos])

@app.route('/productos', methods=['POST'])
def agregar_producto_endpoint():
    datos = request.json
    nombre = datos["nombre"]
    precio = datos["precio"]
    categoria = datos["categoria"]
    imagen = datos.get("imagen", None)
    agregar_producto(nombre, precio, categoria, imagen)
    return jsonify({"nombre": nombre, "precio": precio, "categoria": categoria}), 201

@app.route('/productos/<int:id>', methods=['PUT'])
def editar_producto_endpoint(id):
    datos = request.json
    nombre = datos["nombre"]
    precio = datos["precio"]
    categoria = datos["categoria"]
    imagen = datos.get("imagen", None)
    editar_producto(id, nombre, precio, categoria, imagen)
    return jsonify({"id": id, "nombre": nombre, "precio": precio, "categoria": categoria})

@app.route('/productos/<int:id>', methods=['DELETE'])
def eliminar_producto_endpoint(id):
    eliminar_producto(id)
    return jsonify({"id": id, "mensaje": "Producto eliminado"})

@app.route('/comandas_cocina', methods=['GET'])
def obtener_comandas_pendientes_y_en_preparacion_endopoint():
    try:
        comandas = obtener_comandas_pendientes_y_en_preparacion()
        if not comandas:
            return jsonify([]), 200
        return jsonify([comanda.to_dict() for comanda in comandas]), 200
    except Exception as e:
        print(f"Error al obtener comandas pendientes y en preparación: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500
    
@app.route('/comandas/<int:id>', methods=['GET'])
def obtener_detalles_comanda_endpoint(id):
    try:
        comanda = obtener_detalles_comanda(id)
        return jsonify(comanda.to_dict())
    except Exception as e:
        print(f"Error al obtener comanda con ID {id}: {e}")

@app.route('/ingredientes', methods=['GET'])
def obtener_ingredientes_endpoint():
    try:
        ingredientes = obtener_ingredientes()
        return jsonify([ingrediente.to_dict() for ingrediente in ingredientes])
    except Exception as e:
        print(f"Error al obtener ingredientes: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500
    
@app.route('/ingredientes', methods=['POST'])
def agregar_ingrediente_endpoint():
    datos = request.json
    nombre = datos["nombre"]
    stock = datos["stock"]
    stock_minimo = datos["stock_minimo"]
    unidad = datos["unidad"]
    try:
        nuevo_ingrediente_id = agregar_ingrediente(nombre, stock, stock_minimo, unidad)
        return jsonify({"id": nuevo_ingrediente_id, "nombre": nombre, "stock": stock, "stock_minimo": stock_minimo, "unidad": unidad}), 201
    except Exception as e:
        print(f"Error al agregar ingrediente: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/ingredientes/<int:id>', methods=['PUT'])
def editar_ingrediente_endpoint(id):
    datos = request.json
    nombre = datos["nombre"]
    stock = datos["stock"]
    stock_minimo = datos["stock_minimo"]
    unidad = datos["unidad"]
    try:
        editar_ingrediente(id, nombre, stock, stock_minimo, unidad)
        return jsonify({"id": id, "nombre": nombre, "stock": stock, "stock_minimo": stock_minimo, "unidad": unidad})
    except Exception as e:
        print(f"Error al editar ingrediente con ID {id}: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/ingredientes/<int:id>', methods=['DELETE'])
def eliminar_ingrediente_endpoint(id):
    try:
        eliminar_ingrediente(id)
        return jsonify({"id": id, "mensaje": "Ingrediente eliminado"})
    except Exception as e:
        print(f"Error al eliminar ingrediente con ID {id}: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/productos/<int:producto_id>/recetas', methods=['GET'])
def obtener_recetas_por_producto_endpoint(producto_id):
    try:
        recetas = obtener_recetas_por_producto(producto_id)
        return jsonify([receta.to_dict() for receta in recetas])
    except Exception as e:
        print(f"Error al obtener recetas para el producto {producto_id}: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500
    
@app.route('/recetas', methods=['POST'])
def agregar_receta_endpoint():
    datos = request.json
    producto_id = datos["producto_id"]
    ingrediente_id = datos["ingrediente_id"]
    cantidad_necesaria = datos["cantidad_necesaria"]
    try:
        nueva_receta_id = agregar_receta(producto_id, ingrediente_id, cantidad_necesaria)
        return jsonify({"id": nueva_receta_id, "producto_id": producto_id, "ingrediente_id": ingrediente_id, "cantidad_necesaria": cantidad_necesaria}), 201
    except Exception as e:
        print(f"Error al agregar receta: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/recetas/<int:receta_id>', methods=['PUT'])
def editar_receta_endpoint(receta_id):
    datos = request.json
    cantidad_necesaria = datos["cantidad_necesaria"]
    try:
        editar_receta(receta_id, cantidad_necesaria)
        return jsonify({"id": receta_id, "cantidad_necesaria": cantidad_necesaria})
    except Exception as e:
        print(f"Error al editar receta con ID {receta_id}: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/recetas/<int:receta_id>', methods=['DELETE'])
def eliminar_ingrediente_de_receta_endpoint(receta_id):
    try:
        eliminar_ingrediente_de_receta(receta_id)
        return jsonify({"id": receta_id, "mensaje": "Receta eliminada"})
    except Exception as e:
        print(f"Error al eliminar receta con ID {receta_id}: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/mesas', methods=['POST'])
def crear_mesa_endpoint():
    try:
        nueva_mesa_id = agregar_mesa()
        return jsonify({"id": nueva_mesa_id}), 201
    except Exception as e:
        print(f"Error al crear una nueva mesa: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/mesas/<int:id>', methods=['DELETE'])
def eliminar_mesa_endpoint(id):
    try:
        eliminar_mesa(id)
        return jsonify({"id": id, "eliminado": True})
    except Exception as e:
        print(f"Error al eliminar la mesa {id}: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/mesas/<int:id>/posicion', methods=['PUT'])
def actualizar_posicion_mesa_endpoint(id):
    datos = request.json
    pos_x = datos.get("pos_x")
    pos_y = datos.get("pos_y")
    try:
        guardar_posicion_mesa(id, pos_x, pos_y)
        return jsonify({"id": id, "pos_x": pos_x, "pos_y": pos_y})
    except Exception as e:
        print(f"Error al actualizar la posición de la mesa {id}: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/comandas/<int:comanda_id>/mover', methods=['PUT'])
def cambiar_mesa_comanda_endpoint(comanda_id):
    datos = request.json
    nueva_mesa_id = datos["nueva_mesa_id"]
    try:
        cambiar_mesa_comanda(comanda_id, nueva_mesa_id)
        return jsonify({"comanda_id": comanda_id, "nueva_mesa_id": nueva_mesa_id})
    except Exception as e:
        print(f"Error al mover la comanda {comanda_id} a la mesa {nueva_mesa_id}: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/comandas', methods=['GET'])
def obtener_todas_las_comandas_endpoint():
    try:
        comandas = obtener_todas_las_comandas()
        if not comandas:
            return jsonify([]), 200
        return jsonify([comanda.to_dict() for comanda in comandas]), 200
    except Exception as e:
        print(f"Error al obtener todas las comandas: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/detalle_comanda/<int:id>/estado', methods=['PUT'])
def cambiar_estado_detalle_comanda_endpoint(id):
    datos = request.json
    nuevo_estado = datos.get("estado")
    try:
        cambiar_estado_detalle_comanda(id, nuevo_estado)
        return jsonify({"id": id, "estado": nuevo_estado})
    except Exception as e:
        print(f"Error al cambiar el estado del detalle de comanda {id}: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/comanda/<int:id>/estado', methods=['PUT'])
def cambiar_estado_comanda_endpoint(id):
    datos = request.json
    nuevo_estado = datos.get("estado")
    metodo_pago = datos.get("metodo_pago")
    try:
        cambiar_estado_comanda(id, nuevo_estado, metodo_pago)
        return jsonify({"id": id, "estado": nuevo_estado, "metodo_pago": metodo_pago})
    except Exception as e:
        print(f"Error al cambiar el estado de la comanda {id}: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/comandas_mesas', methods=['GET'])
def obtener_todas_las_comandas_para_mesas_endpoint():
    try:
        comandas = obtener_todas_las_comandas_para_mesas()
        if not comandas:
            return jsonify([]), 200
        return jsonify([comanda.to_dict() for comanda in comandas]), 200
    except Exception as e:
        print(f"Error al obtener todas las comandas: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 