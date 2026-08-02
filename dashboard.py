"""
Dashboard interactivo para explorar el dataset Superstore Sales.

Ejecutar con: streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Configuracion de la pagina ---
st.set_page_config(page_title="🛒Superstore Sales Dashboard", page_icon="", layout="wide")

# --- Carga de datos ---
@st.cache_data
def cargar_datos():
    df = pd.read_csv('data/superstore_procesado.csv', encoding='ISO-8859-1')
    df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
    return df

df = cargar_datos()

# --- Titulo ---
st.title("🛒 Dashboard de Superstore Sales")
st.markdown("Explora el dataset limpio de forma interactiva. Datos originales de [Kaggle - Superstore Dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final).")

# --- Filtros en la barra lateral ---
st.sidebar.header("Filtros")

region = st.sidebar.multiselect(
    "Region",
    options=sorted(df['Region'].unique()),
    default=sorted(df['Region'].unique())
)

category = st.sidebar.multiselect(
    "Category",
    options=sorted(df['Category'].unique()),
    default=sorted(df['Category'].unique())
)

segment = st.sidebar.multiselect(
    "Segment",
    options=sorted(df['Segment'].unique()),
    default=sorted(df['Segment'].unique())
)

# --- Aplicar filtros ---
df_filtrado = df[
    (df['Region'].isin(region)) &
    (df['Category'].isin(category)) &
    (df['Segment'].isin(segment))
]


# --- Metricas principales ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("No. Transacciones", f"{df_filtrado.shape[0]:,}")
col2.metric("Ventas totales", f"${df_filtrado['Sales'].sum():,.2f}")
col3.metric("Ganancia total", f"${df_filtrado['Profit'].sum():,.2f}")

margen = (df_filtrado['Profit'].sum() / df_filtrado['Sales'].sum() * 100) if not df_filtrado.empty and df_filtrado['Sales'].sum() != 0 else 0
col4.metric("Margen promedio", f"{margen:.2f}%")

st.divider()

# --- Graficas en dos columnas ---
col_izq, col_der = st.columns(2)

with col_izq:
    st.subheader("Margen de ganancia por categoria")
    
    if df_filtrado.empty:
        st.warning("No hay datos para los filtros seleccionados.")
    else:
        margen_cat = (df_filtrado.groupby('Category').apply(
            lambda x: (x['Profit'].sum() / x['Sales'].sum()) * 100
        ).sort_values())
        
        fig, ax = plt.subplots(figsize=(7, 5))
        colores = ['firebrick' if v < 0 else 'forestgreen' for v in margen_cat.values]
        ax.bar(margen_cat.index, margen_cat.values, color=colores)
        ax.axhline(0, color='black', linewidth=1)
        ax.set_ylabel('Margen (%)')
        ax.set_xlabel('Categoria')
        st.pyplot(fig, use_container_width=True)

with col_der:
    st.subheader("Ventas totales por mes")
    
    if df_filtrado.empty:
        st.warning("No hay datos para los filtros seleccionados.")
    else:
        df_filtrado['Mes'] = df_filtrado['Order Date'].dt.month
        ventas_mes = df_filtrado.groupby('Mes')['Sales'].sum()
        
        fig2, ax2 = plt.subplots(figsize=(7, 5))
        ax2.plot(ventas_mes.index, ventas_mes.values, marker='o')
        ax2.set_xlabel('Mes')
        ax2.set_ylabel('Ventas ($)')
        ax2.set_xticks(range(1, 13))
        st.pyplot(fig2, use_container_width=True)


st.divider()
st.subheader("Datos filtrados")
st.dataframe(df_filtrado, use_container_width=True)