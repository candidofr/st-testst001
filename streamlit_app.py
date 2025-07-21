import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

# Configuración inicial de Streamlit
st.set_page_config(page_title="Explorador de Autos (Datos Sintéticos)", layout="wide")

st.title("Explorador Interactivo de Datos de Autos (Sintéticos)")

# Generar datos sintéticos
np.random.seed(42)
n = 200

df = pd.DataFrame({
    'Horsepower': np.random.normal(150, 40, n).clip(50, 300),
    'Miles_per_Gallon': np.random.normal(25, 5, n).clip(10, 50),
    'Weight': np.random.normal(3000, 500, n).clip(1500, 5000),
    'Acceleration': np.random.normal(15, 2, n).clip(8, 25),
    'Year': np.random.randint(1970, 1983, n),
    'Origin': np.random.choice(['USA', 'Europe', 'Japan'], size=n)
})
df['Name'] = ['Car ' + str(i) for i in range(n)]

# Sidebar
st.sidebar.header("Opciones de visualización")
x_axis = st.sidebar.selectbox("Eje X", df.select_dtypes(include=np.number).columns, index=0)
y_axis = st.sidebar.selectbox("Eje Y", df.select_dtypes(include=np.number).columns, index=1)
color_by = st.sidebar.selectbox("Color por", ["None"] + df.columns.tolist(), index=6)

# Filtrado por año
year_min, year_max = int(df["Year"].min()), int(df["Year"].max())
year_range = st.sidebar.slider("Rango de Año", year_min, year_max, (year_min, year_max))
filtered_df = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]

# Gráfico
chart = alt.Chart(filtered_df).mark_circle(size=60).encode(
    x=alt.X(x_axis, title=x_axis),
    y=alt.Y(y_axis, title=y_axis),
    tooltip=['Name', x_axis, y_axis, 'Year', 'Origin'],
    color=alt.Color(color_by) if color_by != "None" else alt.value("steelblue")
).interactive()

st.altair_chart(chart, use_container_width=True)

# Mostrar tabla si se desea
if st.checkbox("Mostrar datos"):
    st.dataframe(filtered_df)
