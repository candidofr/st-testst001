import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import os

# Configuración inicial
st.set_page_config(page_title="Explorador de Autos (Datos Sintéticos)", layout="wide")
st.title("Explorador Interactivo de Datos de Autos (Sintéticos)")

# Generar datos sintéticos
# np.random.seed(42)
# n = 200
# df = pd.DataFrame({
# 'Horsepower': np.random.normal(150, 40, n).clip(50, 300),
#     'Miles_per_Gallon': np.random.normal(25, 5, n).clip(10, 50),
#     'Weight': np.random.normal(3000, 500, n).clip(1500, 5000),
#     'Acceleration': np.random.normal(15, 2, n).clip(8, 25),
#     'Year': np.random.randint(1970, 1983, n),
#     'Origin': np.random.choice(['USA', 'Europe', 'Japan'], size=n)
# })
# df['Name'] = ['Car ' + str(i) for i in range(n)]

csv_path = "data/autos_sinteticos.csv"

if os.path.exists(csv_path):
    st.sidebar.success(f"📁 Archivo encontrado: {csv_path}")
    try:
        df = pd.read_csv(csv_path)
        st.sidebar.info(f"✅ Archivo cargado con {df.shape[0]} filas.")
    except Exception as e:
        st.sidebar.error(f"❌ Error al leer el CSV: {e}")
        st.stop()
else:
    st.sidebar.error(f"❌ El archivo CSV no se encuentra en: `{csv_path}`")
    st.stop()

# --- Controles globales ---
st.sidebar.header("Opciones de visualización")

# Ejes y color
x_axis = st.sidebar.selectbox("Eje X", df.select_dtypes(include=np.number).columns, index=0)
y_axis = st.sidebar.selectbox("Eje Y", df.select_dtypes(include=np.number).columns, index=1)
color_by = st.sidebar.selectbox("Color por", ["None"] + df.columns.tolist(), index=6)

# Filtro por año
year_min, year_max = int(df["Year"].min()), int(df["Year"].max())
year_range = st.sidebar.slider("Rango de Año", year_min, year_max, (year_min, year_max))

# Filtro por origen
origins = df['Origin'].unique().tolist()
selected_origins = st.sidebar.multiselect("Filtrar por Origen", origins, default=origins)

# Aplicar filtros globales
filtered_df = df[
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1]) &
    (df["Origin"].isin(selected_origins))
]

# Crear pestañas
tab1, tab2 = st.tabs(["Explorador principal", "Análisis adicional"])

# --- PESTAÑA 1 ---
with tab1:
    st.subheader("Gráfico Interactivo")

    chart = alt.Chart(filtered_df).mark_circle(size=60).encode(
        x=alt.X(x_axis, title=x_axis),
        y=alt.Y(y_axis, title=y_axis),
        tooltip=['Name', x_axis, y_axis, 'Year', 'Origin'],
        color=alt.Color(color_by) if color_by != "None" else alt.value("steelblue")
    ).interactive()

    st.altair_chart(chart, use_container_width=True)

    if st.checkbox("Mostrar datos"):
        st.dataframe(filtered_df)

# --- PESTAÑA 2 ---
with tab2:
    st.subheader("Análisis adicional")

    # Filtro local: Horsepower
    st.markdown("#### Filtro adicional: Rango de Caballos de Fuerza")
    hp_min = int(filtered_df["Horsepower"].min())
    hp_max = int(filtered_df["Horsepower"].max())
    hp_range = st.slider("Selecciona el rango de Horsepower", hp_min, hp_max, (hp_min, hp_max))

    # Aplicar filtro local
    filtered_hp_df = filtered_df[
        (filtered_df["Horsepower"] >= hp_range[0]) & 
        (filtered_df["Horsepower"] <= hp_range[1])
    ]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Distribución de Caballos de Fuerza")
        hist_hp = alt.Chart(filtered_hp_df).mark_bar().encode(
            alt.X("Horsepower", bin=alt.Bin(maxbins=30)),
            y='count()',
            color='Origin'
        )
        st.altair_chart(hist_hp, use_container_width=True)

    with col2:
        st.markdown("### Boxplot de MPG por Región")
        box_mpg = alt.Chart(filtered_hp_df).mark_boxplot().encode(
            x='Origin',
            y='Miles_per_Gallon',
            color='Origin'
        )
        st.altair_chart(box_mpg, use_container_width=True)

    st.markdown("### Evolución del Peso Promedio por Año (Filtrado)")
    avg_weight = filtered_hp_df.groupby('Year')['Weight'].mean().reset_index()
    line_chart = alt.Chart(avg_weight).mark_line(point=True).encode(
        x='Year:O',
        y='Weight',
        tooltip=['Year', 'Weight']
    )
    st.altair_chart(line_chart, use_container_width=True)
