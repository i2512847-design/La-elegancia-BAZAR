# 🛍️ Bazar – Sistema de Gestión de Productos

Aplicación web desarrollada en **Python** usando **Streamlit** como interfaz gráfica y **Supabase** como backend (base de datos y almacenamiento de imágenes).  
Permite gestionar productos de un bazar mediante operaciones **CRUD** (crear, listar, actualizar y eliminar), incluyendo la carga de imágenes por **URL** o **archivo local**.

---

## 🚀 Tecnologías utilizadas

- **Python 3.13+**
- **Streamlit** – interfaz web
- **Supabase** – base de datos PostgreSQL y Storage
- **python-dotenv** – manejo de variables de entorno
- **Git & GitHub** – control de versiones
- **Streamlit Cloud** – despliegue en la nube

---

## 📂 Estructura del proyecto

BAZAR/
│
├── capaDatos/
│ └── dProductos.py # Acceso a datos (Supabase)
│
├── capaLogica/
│ └── lProductos.py # Lógica de negocio
│
├── capaPresentacion/
│ └── pProductos.py # Interfaz Streamlit
│
├── conexion.py # Conexión a Supabase
├── main.py # Punto de entrada
├── .gitignore
├── pyproject.toml # Dependencias
└── README.md