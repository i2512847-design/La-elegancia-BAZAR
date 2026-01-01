from capaDatos.dProductos import *

def listar_productos():
    return obtener_productos()

def crear_producto(data):
    if not data["nombre"]:
        raise ValueError("nombre es obligatorio")
    if data["precio"] < 0 or data["stock"] < 0:
        raise ValueError("Precio y stock no pueden ser negativos")

    return agregar_producto(data)

def editar_producto(id_producto, data):
    if not data["nombre"]:
        raise ValueError("El nombre no puede estar vacío")

    return actualizar_producto(id_producto, data)

def borrar_producto(id_producto):
    return eliminar_producto(id_producto)
