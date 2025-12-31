from conexion import supabase

def obtener_productos():
    return (
        supabase
        .table("productos")
        .select("*")
        .order("id_producto")
        .execute()
        .data
    )

def agregar_producto(data):
    return supabase.table("productos").insert(data).execute().data

def actualizar_producto(id_producto, data):
    return (
        supabase
        .table("productos")
        .update(data)
        .eq("id_producto", id_producto)
        .execute()
        .data
    )

def eliminar_producto(id_producto):
    return (
        supabase
        .table("productos")
        .delete()
        .eq("id_producto", id_producto)
        .execute()
        .data
    )
