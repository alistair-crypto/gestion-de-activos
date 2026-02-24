import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gestión de Activos Pro", layout="wide")

# Inicializamos la memoria
if 'inventario' not in st.session_state:
    st.session_state.inventario = pd.DataFrame(columns=['Libro', 'Costo Unit.', 'Venta Unit.', 'Cantidad', 'Costo Total', 'Venta Total'])

st.title("⚖️ Tablero de Control de Activos")

menu = st.sidebar.radio("Navegación", ["Registrar Activos", "Estado Financiero"])

if menu == "Registrar Activos":
    st.subheader("📚 Entrada de Mercancía")
    with st.container():
        nombre = st.text_input("Nombre del Libro")
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            c = st.number_input("Costo unitario", min_value=0.0, step=0.1)
        with col_b:
            v = st.number_input("Precio de venta", min_value=0.0, step=0.1)
        with col_c:
            cant = st.number_input("Cantidad", min_value=1, step=1)
    
    if st.button("GUARDAR EN INVENTARIO"):
        costo_t = c * cant
        venta_t = v * cant
        nuevo = pd.DataFrame([[nombre, c, v, cant, costo_t, venta_t]], 
                            columns=['Libro', 'Costo Unit.', 'Venta Unit.', 'Cantidad', 'Costo Total', 'Venta Total'])
        st.session_state.inventario = pd.concat([st.session_state.inventario, nuevo], ignore_index=True)
        st.success(f"Has registrado {cant} unidades de '{nombre}'")

elif menu == "Estado Financiero":
    st.subheader("📊 Resumen General de Activos")
    
    if st.session_state.inventario.empty:
        st.info("Registra libros en el inventario para ver los estados financieros.")
    else:
        # Cálculos basados en cantidad
        total_invertido = st.session_state.inventario['Costo Total'].sum()
        total_proyectado = st.session_state.inventario['Venta Total'].sum()
        ganancia_neta = total_proyectado - total_invertido
        total_unidades = st.session_state.inventario['Cantidad'].sum()
        
        col1, col2, col3, col4 = st.columns(4)
        
        col1.metric("UNIDADES TOTALES", int(total_unidades))
        col2.metric("CAPITAL SALIÓ", f"${total_invertido:.2f}")
        col3.metric("ESPERO QUE ENTRE", f"${total_proyectado:.2f}")
        col4.metric("LO QUE QUEDARÁ", f"${ganancia_neta:.2f}", delta=f"{ganancia_neta:.2f}")

        st.write("---")
        st.write("### Detalle del Inventario")
        st.dataframe(st.session_state.inventario, use_container_width=True)
