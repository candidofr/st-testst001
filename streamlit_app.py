import streamlit as st
import altair as alt
from vega_datasets import data

# Cargar el dataset
cars = data.cars()

# Título de la aplicación
st.title("Explorador Interactivo del Dataset Cars")

# Descripción
st.markdown(
    """
    Usa los controles a la izquierda para visualizar relaciones entre diferentes variables
    del dataset de automóviles. Este conjunto de datos incluye información como el consumo,
    cilindrada, caballos de fuerza, entre otros.
    """
)

# Barra lateral con controles
st.sidebar.header("Opciones de visualización")

x_axis = st.sidebar.selectbox("Selecciona variable para el eje X", cars.columns, index=5)
y_axis = st.sidebar.selectbox("Selecciona variable para el eje Y", cars.columns, index=0)
color_by = st.sidebar.selectbox("Color por", ["None"] + list(cars.columns), index=6)

# Filtrado por año
year_range = st.sidebar.slider(
    "Selecciona rango de año", 
    int(cars['Year'].min()), 
    int(cars['Year'].max()), 
    (int(cars['Year'].min()), int(cars['Year'].max()))
)
filtered_data = cars[(cars['Year'] >= year_range[0]) & (cars['Year'] <= year_range[1])]

# Gráfico interactivo con Altair
chart = alt.Chart(filtered_data).mark_circle(size=60).encode(
    x=alt.X(x_axis, type='quantitative'),
    y=alt.Y(y_axis, type='quantitative'),
    tooltip=['Name', x_axis, y_axis],
    color=alt.Color(color_by) if color_by != "None" else alt.value("steelblue")
).interactive()

# Mostrar gráfico
st.altair_chart(chart, use_container_width=True)

# Mostrar el dataframe si el usuario quiere
if st.checkbox("Mostrar datos"):
    st.write(filtered_data)
