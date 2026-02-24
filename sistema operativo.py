import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gestión de Activos", page_icon="📈")

st.title("📈 Sistema de Gestión de Activos")
st.markdown("---")

# Sidebar para navegación
menu = st.sidebar.radio("Navegación", ["Panel de Control", "Inventario Libros", "Estado Financiero"])

if menu == "Panel de Control":
    st.subheader("Bienvenido al Centro de Estrategia")
    st.write("Aquí verás el resumen de tus activos.")
    st.metric(label="Valor Total del Inventario", value="$0.00", delta="0%")

elif menu == "Inventario Libros":
    st.subheader("📚 Control de Inventario")
    # Aquí es donde conectaremos tu base de datos después
    st.info("Listo para registrar nuevos activos.")

elif menu == "Estado Financiero":
    st.subheader("💸 Flujo de Caja")
    st.write("Diferencia entre Activos y Pasivos.")