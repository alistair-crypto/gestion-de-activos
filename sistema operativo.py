import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gestión de Activos", layout="wide")

# Inicializamos la memoria
if 'inventario' not in st.session_state:
    st.session_state.inventario = pd.DataFrame(columns=['Libro', 'Costo', 'Venta', 'Stock'])
if 'ventas_realizadas' not in st.session_state:
    st.session_state.ventas_realizadas = 0.0
if 'costos_recuperados' not in st.session_state:
    st.session_state.costos_recuperados = 0.0

st.title("⚖️ Mi Tablero de Control")

menu = st.sidebar.radio("Navegación", ["Registrar Activos", "Estado Financiero"])

if menu == "Registrar Activos":
    st.subheader("📚 Entrada de Mercancía")
    nombre = st.text_input("Nombre del Libro")
    c = st.number_input("Costo unitario", min_value=0.0)
    v = st.number_input("Precio de venta", min_value=0.0)
    
    if st.button("GUARDAR EN INVENTARIO"):
        nuevo = pd.DataFrame([[nombre, c, v, 1]], columns=['Libro', 'Costo', 'Venta', 'Stock'])
        st.session_state.inventario = pd.concat([st.session_state.inventario, nuevo], ignore_index=True)
        st.success(f"Libro {nombre} añadido.")

elif menu == "Estado Financiero":
    st.subheader("📊 Resumen de Ganancias y Pérdidas")
    
    # Cálculos
    total_en_inventario = st.session_state.inventario['Costo'].sum()
    ganancia_potencial = (st.session_state.inventario['Venta'].sum() - total_en_inventario)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("CAPITAL INVERTIDO", f"${total_en_inventario:.2f}")
        st.caption("Dinero que 'salió' de tu bolsa y está en libros.")
        
    with col2:
        st.metric("INGRESOS ESTIMADOS", f"${st.session_state.inventario['Venta'].sum():.2f}")
        st.caption("Lo que recibirás al vender todo.")
        
    with col3:
        st.metric("UTILIDAD PROYECTADA", f"${ganancia_potencial:.2f}", delta=f"{ganancia_potencial:.2f}")
        st.caption("Lo que te 'quedará' de ganancia neta.")

    st.write("---")
    st.write("### Detalle de Activos")
    st.table(st.session_state.inventario)
