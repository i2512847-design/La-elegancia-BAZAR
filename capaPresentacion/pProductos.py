import sys, os, uuid
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from conexion import supabase
from capaLogica.lProductos import *


st.set_page_config(
    page_title="Bazar | Productos",
    page_icon="🛍️",
    layout="wide"
)


st.markdown("""
<style>
.card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}
.price {
    color: #27ae60;
    font-size: 20px;
    font-weight: bold;
}
.img-box {
    width: 100%;
    height: 220px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    border-radius: 10px;
    background: #f5f5f5;
    margin-bottom: 10px;
}
.img-box img {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
}
</style>
""", unsafe_allow_html=True)


def subir_imagen_storage(file):
    ext = file.name.split(".")[-1]
    nombre = f"{uuid.uuid4()}.{ext}"
    ruta = f"productos/{nombre}"

    supabase.storage.from_("productos").upload(
        ruta,
        file.getvalue(),
        {"content-type": file.type}
    )

    return supabase.storage.from_("productos").get_public_url(ruta)

def imagen_valida(url):
    return url and (url.startswith("http://") or url.startswith("https://"))

def mostrar_imagen(url):
    if imagen_valida(url):
        st.markdown(
            f"""
            <div class="img-box">
                <img src="{url}">
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.info("📷 Sin imagen")


with st.sidebar:
    st.title("🛒 Bazar Admin")
    menu = st.radio("Menú", ["📦 Productos", "➕ Nuevo Producto"])

st.title("Gestión de Productos")
st.divider()


if menu == "📦 Productos":
    productos = listar_productos()

    if not productos:
        st.info("No hay productos registrados.")
    else:
        cols = st.columns(3)
        for i, p in enumerate(productos):
            with cols[i % 3]:
                st.markdown('<div class="card">', unsafe_allow_html=True)

                mostrar_imagen(p.get("foto"))

                st.subheader(p["nombre"])
                st.write(f"**Código:** {p['codigo']}")
                st.write(f"**Categoría:** {p['categoria']}")
                st.write(f"**Marca:** {p['marca']}")
                st.markdown(f"<div class='price'>S/. {p['precio']}</div>", unsafe_allow_html=True)

                with st.expander("✏️ Editar / 🗑️ Eliminar"):
                    nombre = st.text_input("Nombre", p["nombre"], key=f"n{p['id_producto']}")
                    categoria = st.text_input("Categoría", p["categoria"], key=f"c{p['id_producto']}")
                    marca = st.text_input("Marca", p["marca"], key=f"m{p['id_producto']}")
                    modelo = st.text_input("Modelo", p["modelo"], key=f"mo{p['id_producto']}")
                    descripcion = st.text_area("Descripción", p["descripcion"], key=f"d{p['id_producto']}")
                    precio = st.number_input("Precio", value=float(p["precio"]), key=f"p{p['id_producto']}")
                    stock = st.number_input("Stock", value=int(p["stock"]), key=f"s{p['id_producto']}")
                    estado = st.selectbox(
                        "Estado",
                        ["Activo", "Inactivo"],
                        index=0 if p["estado"] == "Activo" else 1,
                        key=f"e{p['id_producto']}"
                    )

                    st.markdown("### 🖼️ Imagen")
                    tipo_img = st.radio(
                        "Cambiar imagen",
                        ["Mantener", "Subir archivo", "URL"],
                        key=f"img{p['id_producto']}"
                    )

                    nueva_foto = p.get("foto")

                    if tipo_img == "Subir archivo":
                        file = st.file_uploader(
                            "Nueva imagen",
                            type=["jpg", "png", "jpeg"],
                            key=f"file{p['id_producto']}"
                        )
                        if file:
                            nueva_foto = subir_imagen_storage(file)

                    elif tipo_img == "URL":
                        url = st.text_input(
                            "URL de imagen",
                            key=f"url{p['id_producto']}"
                        )
                        if imagen_valida(url):
                            nueva_foto = url

                    if st.button("💾 Actualizar", key=f"u{p['id_producto']}"):
                        editar_producto(p["id_producto"], {
                            "nombre": nombre,
                            "categoria": categoria,
                            "marca": marca,
                            "modelo": modelo,
                            "descripcion": descripcion,
                            "precio": precio,
                            "stock": stock,
                            "estado": estado,
                            "foto": nueva_foto
                        })
                        st.session_state["mensaje"] = "✅ Producto actualizado"
                        st.rerun()

                    if st.button("🗑️ Eliminar", key=f"x{p['id_producto']}"):
                        borrar_producto(p["id_producto"])
                        st.session_state["mensaje"] = "🗑️ Producto eliminado"
                        st.rerun()

                st.markdown('</div>', unsafe_allow_html=True)


else:
    st.subheader("➕ Nuevo producto")

    contenedor = st.container()

    with contenedor:

        
        st.markdown("### 🖼️ Imagen")

        tipo_img = st.radio(
            "Tipo de imagen",
            ["Subir archivo", "URL"],
            horizontal=True,
            key="tipo_img_nuevo"
        )

        foto_url = None

        if tipo_img == "Subir archivo":
            file = st.file_uploader(
                "Selecciona una imagen",
                type=["jpg", "png", "jpeg"],
                key="file_nuevo"
            )
            if file:
                foto_url = subir_imagen_storage(file)
                st.image(foto_url, width=200)

        else:
            foto_url = st.text_input(
                "URL de la imagen",
                key="url_nuevo"
            )
            if foto_url:
                st.image(foto_url, width=200)

        
        with st.form("form_crear", clear_on_submit=True):
            nombre = st.text_input("Nombre")
            categoria = st.text_input("Categoría")
            marca = st.text_input("Marca")
            modelo = st.text_input("Modelo")
            descripcion = st.text_area("Descripción")
            precio = st.number_input("Precio", min_value=0.0)
            stock = st.number_input("Stock", min_value=0)
            estado = st.selectbox("Estado", ["Activo", "Inactivo"])

            guardar = st.form_submit_button("Guardar")

        
        if guardar:
            crear_producto({
                "nombre": nombre,
                "categoria": categoria,
                "marca": marca,
                "modelo": modelo,
                "descripcion": descripcion,
                "precio": precio,
                "stock": stock,
                "estado": estado,
                "foto": foto_url
            })
            st.success("✅ Producto registrado correctamente")

