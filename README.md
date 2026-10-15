# Proyectos de Luis Miguel Quintana Gil

Hola, soy Luis Miguel, estudiante de Ingeniería en Ciencia de Datos en el ITESO (Zapopan, Jalisco). Este repositorio reúne los proyectos que voy desarrollando durante mi vida universitaria y personal, enfocados en análisis y visualización de datos.

**Herramientas con las que trabajo:** Python, Power BI, R, Java y Excel.

**Contacto:** luisquintanta2006@gmail.com

---

## Proyectos

| Proyecto | Descripción | Herramientas |
| --- | --- | --- |
| [Ventas de videojuegos](./videojuegos-dashboard) | Análisis exploratorio y dashboard interactivo de ventas de videojuegos (1980–2024) | Python, pandas, Streamlit, Plotly, Seaborn |
| [Dashboard de fútbol](./dashboard-futbol) | Reporte de estadísticas y comparativas de equipos de fútbol | Power BI, DAX |
| [Fut Draft](./fut-draft) | Simulador por consola del modo draft de FIFA | Python, pandas |

---

## 1. Ventas de videojuegos (1980–2024)

Análisis exploratorio de un dataset de ventas globales de videojuegos por consola, género, publisher y región, junto con un dashboard interactivo.

**Qué incluye**

- Limpieza de datos: manejo de valores nulos, conversión de fechas, reconstrucción de ventas totales y eliminación de registros sin ventas.
- Notebook con el análisis exploratorio: ventas por año, género, consola y publisher, distribución regional, evolución de géneros, relación entre puntuación de la crítica y ventas, y mapa de calor consola × género.
- Dashboard en Streamlit con filtros por rango de años, género y consola, indicadores clave (KPIs), un explorador de datos y la opción de cargar un CSV propio.

**Archivos**

- `app.py`: dashboard en Streamlit.
- `videogames_eda.ipynb`: notebook del análisis exploratorio.
- `videogames.csv`: datos utilizados.
- `requirements.txt`: librerías necesarias.

**Cómo ejecutarlo**

```bash
cd videojuegos-dashboard
pip install -r requirements.txt
streamlit run app.py
```

---

## 2. Dashboard de fútbol

Reporte en Power BI para analizar el rendimiento de equipos de fútbol.

**Qué incluye**

- Cuatro páginas: datos generales, comparativa equipo vs equipo, tabla general y próximos partidos.
- Modelo de datos con tablas de dimensiones (equipo, liga, fecha y estadio) conectadas a tablas de partidos, eventos y estadísticas.
- Medidas calculadas de rendimiento, como puntos, partidos ganados, empatados y perdidos, diferencia de goles, goles por partido y promedios de tiros, corners y tarjetas amarillas.
- Segmentadores por liga, temporada y equipo.

**Archivos**

- `Proyecto_chido.pbix`: reporte de Power BI.

**Cómo abrirlo:** descarga el archivo y ábrelo con Power BI Desktop.

---

## 3. Fut Draft

Programa en consola que imita la mecánica del Fut Draft de FIFA: el usuario arma una alineación de 11 jugadores eligiendo entre 4 opciones aleatorias por cada posición.

**Qué incluye**

- Carga de la base de jugadores desde un archivo de Excel con pandas.
- Selección por posición sin repetir jugadores, con validación de las entradas del usuario.
- Cálculo de la valoración media, la química del equipo (por nacionalidad, liga y club) y un puntaje final.

**Archivos**

- `finaldef.py`: código del juego.
- `jugadores para futdraft.xlsx`: base de datos de jugadores.

**Cómo ejecutarlo**

```bash
cd fut-draft
pip install pandas openpyxl
python finaldef.py
```
