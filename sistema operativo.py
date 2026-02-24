import streamlit as st
import pandas as pd
import datetime

# Configuración inicial
st.set_page_config(page_title="Control de Activos", layout="wide")

# Inicializar estados si no existen
if 'inventario' not in st.session_state:
    st.session_state.inventario = pd.DataFrame(columns=['Libro', 'Costo', 'Precio Venta', 'Stock'])
if 'ventas' not in st.session_state:
    st.session_state.ventas = pd.DataFrame(columns=['Fecha', 'Libro', 'Ingreso', 'Costo_Unitario', 'Ganancia'])

st.title("📈 Mi Tablero de Control Financiero")
menu = st.sidebar.radio("Menú", ["Panel Financiero", "Inventario", "Nueva Venta"])

# --- PANEL FINANCIERO (LO QUE ENTRÓ, SALIÓ Y QUEDÓ) ---
if menu == "Panel Financiero":
    st.subheader("📊 Balance de Resultados")
    
    ingreso_total = st.session_state.ventas['Ingreso'].sum()
    costo_total = st.session_state.ventas['Costo_Unitario'].sum()
    ganancia_neta = st.session_state.ventas['Ganancia'].sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("DINERO QUE ENTRÓ", f"${ingreso_total:.2f}")
    col2.metric("DINERO QUE SALIÓ (Costo)", f"${costo_total:.2f}", delta_color="inverse")
    col3.metric("LO QUE QUEDÓ (Ganancia)", f"${ganancia_neta:.2f}")

    st.write("---")
    st.write("### Historial de Transacciones")
    st.table(st.session_state.ventas)

# --- INVENTARIO ---
elif menu == "Inventario":
    st.subheader("📚 Gestión de Stock")
    with st.form("registro_libro"):
        nombre = st.text_input("Nombre del Libro")
        costo = st.number_input("¿Cuánto te costó a ti?", min_value=0.0)
        venta = st.number_input("¿A cuánto lo vendes?", min_value=0.0)
        cantidad = st.number_input("Cantidad inicial", min_value=1)
        if st.form_submit_button("Añadir al Inventario"):
            nuevo = pd.DataFrame([[nombre, costo, venta, cantidad]], columns=['Libro', 'Costo', 'Precio Venta', 'Stock'])
            st.session_state.inventario = pd.concat([st.session_state.inventario, nuevo], ignore_index=True)
            st.success(f"Activo '{nombre}' registrado.")
    
    st.dataframe(st.session_state.inventario)

# --- REGISTRAR VENTA ---
elif menu == "Nueva Venta":
    st.subheader("💸 Registrar una Venta")
    if st.session_state.inventario.empty:
        st.warning("No hay libros en el inventario.")
    else:
        libro_sel = st.selectbox("Selecciona el libro vendido", st.session_state.inventario['Libro'])
        if st.button("Confirmar Venta de 1 unidad"):
            # Buscar datos del libro
            idx = st.session_state.inventario[st.session_state.inventario['Libro'] == libro_sel].index[0]
            costo_u = st.session_state.inventario.at[idx, 'Costo']
            precio_v = st.session_state.inventario.at[idx, 'Precio Venta']
            
            # Registrar Venta
            nueva_v = pd.DataFrame([[datetime.date.today(), libro_sel, precio_v, costo_u, (precio_v - costo_u)]], 
                                  columns=['Fecha', 'Libro', 'Ingreso', 'Costo_Unitario', 'Ganancia'])
            st.session_state.ventas = pd.concat([st.session_state.ventas, nueva_v], ignore_index=True)
            
            # Restar del Stock
            st.session_state.inventario.at[idx, 'Stock'] -= 1
            st.success(f"Venta de {libro_sel} registrada. ¡Dinero en caja!")
