import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ── Configuración de página ───────────────────────────────────────────────────
st.set_page_config(
    page_title="🎮 Video Games Sales Dashboard",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Estilos ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=Syne:wght@700;800&display=swap');

    html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }
    h1, h2, h3 { font-family: 'Syne', sans-serif; }

    .stApp { background-color: #0e0e1a; color: #e8e8f0; }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #13132b 0%, #1a1a3a 100%);
        border-right: 1px solid #2a2a5a;
    }

    .metric-card {
        background: linear-gradient(135deg, #1e1e40 0%, #252550 100%);
        border: 1px solid #3a3a70;
        border-radius: 12px;
        padding: 20px 24px;
        text-align: center;
    }
    .metric-value {
        font-family: 'Syne', sans-serif;
        font-size: 2rem;
        font-weight: 800;
        color: #a78bfa;
        line-height: 1;
    }
    .metric-label {
        font-size: 0.78rem;
        color: #9090c0;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 6px;
    }
    .section-title {
        font-family: 'Syne', sans-serif;
        font-size: 1.15rem;
        font-weight: 700;
        color: #c4b5fd;
        border-left: 3px solid #7c3aed;
        padding-left: 10px;
        margin-bottom: 12px;
    }
    div[data-testid="stSelectbox"] label,
    div[data-testid="stMultiSelect"] label,
    div[data-testid="stSlider"] label { color: #b0b0d8 !important; font-size: 0.85rem; }
</style>
""", unsafe_allow_html=True)

PLOTLY_TEMPLATE = "plotly_dark"
ACCENT = "#a78bfa"
PALETTE = px.colors.qualitative.Vivid

# ── Carga y limpieza de datos ─────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("videogames.csv")

    # Limpiar
    df.drop(columns=["img", "last_update"], inplace=True)
    df["release_date"] = pd.to_datetime(df["release_date"], format="%d/%m/%Y", errors="coerce")
    df["year"] = df["release_date"].dt.year.astype("Int64")
    df = df[df["year"].between(1980, 2024)]

    sales_cols = ["na_sales", "jp_sales", "pal_sales", "other_sales"]
    df[sales_cols] = df[sales_cols].fillna(0)

    mask = df["total_sales"].isna()
    df.loc[mask, "total_sales"] = df.loc[mask, sales_cols].sum(axis=1)
    df = df[df["total_sales"] > 0].copy()
    df["developer"] = df["developer"].fillna("Unknown")

    return df

df = load_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎮 Filtros")
    st.markdown("---")

    year_min, year_max = int(df["year"].min()), int(df["year"].max())
    year_range = st.slider("Rango de años", year_min, year_max, (1990, 2020))

    all_genres = sorted(df["genre"].dropna().unique().tolist())
    genres_sel = st.multiselect("Géneros", all_genres, default=all_genres)

    all_consoles = sorted(df["console"].dropna().unique().tolist())
    consoles_sel = st.multiselect("Consolas", all_consoles, default=all_consoles)

    st.markdown("---")
    st.markdown("### 📁 Usar tu propio CSV")
    uploaded = st.file_uploader("Sube un CSV limpio", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
        df["year"] = pd.to_numeric(df.get("year", pd.Series(dtype=float)), errors="coerce")
        st.success("✅ Archivo cargado")

# ── Aplicar filtros ───────────────────────────────────────────────────────────
mask = (
    df["year"].between(*year_range) &
    df["genre"].isin(genres_sel) &
    df["console"].isin(consoles_sel)
)
dff = df[mask].copy()

if dff.empty:
    st.warning("⚠️ No hay datos con los filtros seleccionados. Ajusta los filtros del sidebar.")
    st.stop()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<h1 style='font-family:Syne,sans-serif; font-size:2.4rem; margin-bottom:0;'>
    🎮 Video Games Sales Dashboard
</h1>
<p style='color:#7070a0; margin-top:4px; margin-bottom:24px;'>
    Análisis exploratorio · 1980–2024 · Ventas en millones de unidades
</p>
""", unsafe_allow_html=True)

# ── KPI Cards ─────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
kpis = [
    (k1, f"{len(dff):,}", "Juegos"),
    (k2, f"{dff['total_sales'].sum():,.0f}M", "Ventas totales"),
    (k3, f"{dff['console'].nunique()}", "Consolas"),
    (k4, f"{dff['genre'].nunique()}", "Géneros"),
    (k5, f"{dff['publisher'].nunique()}", "Publishers"),
]
for col, val, label in kpis:
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{val}</div>
            <div class="metric-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Sección 1: Ventas por año ─────────────────────────────────────────────────
st.markdown('<div class="section-title">📈 Evolución de ventas por año</div>', unsafe_allow_html=True)
c1, c2 = st.columns([2, 1])

with c1:
    ventas_anio = dff.groupby("year")["total_sales"].sum().reset_index()
    fig = px.area(
        ventas_anio, x="year", y="total_sales",
        labels={"year": "Año", "total_sales": "Ventas (M)"},
        template=PLOTLY_TEMPLATE, color_discrete_sequence=[ACCENT]
    )
    fig.update_layout(margin=dict(t=10, b=10), height=280, hovermode="x unified")
    fig.update_traces(fillcolor="rgba(167,139,250,0.15)")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    top_year = ventas_anio.loc[ventas_anio["total_sales"].idxmax()]
    st.markdown(f"""
    <div class="metric-card" style="margin-top:10px;">
        <div class="metric-value">{int(top_year['year'])}</div>
        <div class="metric-label">Año con más ventas</div>
        <div style="color:#a78bfa; font-size:1.1rem; margin-top:8px;">{top_year['total_sales']:,.1f}M unidades</div>
    </div>
    """, unsafe_allow_html=True)

    num_juegos_anio = dff.groupby("year").size().reset_index(name="juegos")
    fig2 = px.bar(
        num_juegos_anio, x="year", y="juegos",
        labels={"year": "Año", "juegos": "Juegos lanzados"},
        template=PLOTLY_TEMPLATE, color_discrete_sequence=["#4ade80"]
    )
    fig2.update_layout(margin=dict(t=10, b=10), height=180, showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

# ── Sección 2: Géneros y Consolas ─────────────────────────────────────────────
st.markdown('<div class="section-title">🎯 Géneros & Consolas</div>', unsafe_allow_html=True)
col_a, col_b = st.columns(2)

with col_a:
    top_n_genre = st.select_slider("Top géneros", options=list(range(5, 21)), value=10)
    generos = dff.groupby("genre")["total_sales"].sum().nlargest(top_n_genre).reset_index()
    fig = px.bar(
        generos.sort_values("total_sales"), x="total_sales", y="genre", orientation="h",
        color="total_sales", color_continuous_scale="Purples",
        labels={"total_sales": "Ventas (M)", "genre": ""},
        template=PLOTLY_TEMPLATE
    )
    fig.update_layout(margin=dict(t=10, b=10), height=350, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

with col_b:
    top_n_con = st.select_slider("Top consolas", options=list(range(5, 21)), value=10)
    consolas = dff.groupby("console")["total_sales"].sum().nlargest(top_n_con).reset_index()
    fig = px.bar(
        consolas, x="console", y="total_sales",
        color="total_sales", color_continuous_scale="Blues",
        labels={"total_sales": "Ventas (M)", "console": ""},
        template=PLOTLY_TEMPLATE
    )
    fig.update_layout(margin=dict(t=10, b=10), height=350, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

# ── Sección 3: Regiones y Publishers ─────────────────────────────────────────
st.markdown('<div class="section-title">🌍 Distribución regional & Publishers</div>', unsafe_allow_html=True)
col_c, col_d = st.columns(2)

with col_c:
    regiones = {
        "Norteamérica": dff["na_sales"].sum(),
        "Europa/PAL": dff["pal_sales"].sum(),
        "Japón": dff["jp_sales"].sum(),
        "Otras": dff["other_sales"].sum(),
    }
    fig = px.pie(
        names=list(regiones.keys()), values=list(regiones.values()),
        hole=0.45, color_discrete_sequence=PALETTE,
        template=PLOTLY_TEMPLATE
    )
    fig.update_layout(margin=dict(t=20, b=10), height=320, legend=dict(orientation="h", y=-0.1))
    st.plotly_chart(fig, use_container_width=True)

with col_d:
    top_pub = (
        dff[dff["publisher"] != "Unknown"]
        .groupby("publisher")["total_sales"].sum()
        .nlargest(10).reset_index()
    )
    fig = px.pie(
        top_pub, names="publisher", values="total_sales",
        hole=0.45, color_discrete_sequence=PALETTE,
        template=PLOTLY_TEMPLATE
    )
    fig.update_layout(margin=dict(t=20, b=10), height=320, legend=dict(orientation="h", y=-0.15))
    st.plotly_chart(fig, use_container_width=True)

# ── Sección 4: Evolución géneros + Heatmap ───────────────────────────────────
st.markdown('<div class="section-title">📊 Tendencias de géneros · Heatmap consola×género</div>', unsafe_allow_html=True)
col_e, col_f = st.columns([3, 2])

with col_e:
    top6 = dff.groupby("genre")["total_sales"].sum().nlargest(6).index.tolist()
    evol = dff[dff["genre"].isin(top6)].groupby(["year", "genre"])["total_sales"].sum().reset_index()
    fig = px.line(
        evol, x="year", y="total_sales", color="genre",
        labels={"year": "Año", "total_sales": "Ventas (M)", "genre": "Género"},
        template=PLOTLY_TEMPLATE, color_discrete_sequence=PALETTE
    )
    fig.update_layout(margin=dict(t=10, b=10), height=320, hovermode="x unified",
                      legend=dict(orientation="h", y=-0.2))
    st.plotly_chart(fig, use_container_width=True)

with col_f:
    top_con_hm = dff.groupby("console")["total_sales"].sum().nlargest(8).index
    hm_data = (
        dff[dff["console"].isin(top_con_hm)]
        .groupby(["console", "genre"])["total_sales"].sum()
        .unstack(fill_value=0)
    )
    fig = px.imshow(
        hm_data, color_continuous_scale="Purples",
        labels={"color": "Ventas (M)"},
        template=PLOTLY_TEMPLATE, aspect="auto"
    )
    fig.update_layout(margin=dict(t=10, b=10), height=320,
                      xaxis=dict(tickangle=-40))
    st.plotly_chart(fig, use_container_width=True)

# ── Sección 5: Crítica vs Ventas ─────────────────────────────────────────────
df_scored = dff[dff["critic_score"].notna()].copy()
if not df_scored.empty:
    st.markdown('<div class="section-title">⭐ Puntuación crítica vs Ventas</div>', unsafe_allow_html=True)
    fig = px.scatter(
        df_scored, x="critic_score", y="total_sales",
        color="genre", hover_data=["title", "console", "publisher", "year"],
        opacity=0.65, trendline="ols",
        labels={"critic_score": "Puntuación crítica", "total_sales": "Ventas (M)", "genre": "Género"},
        template=PLOTLY_TEMPLATE, color_discrete_sequence=PALETTE
    )
    fig.update_layout(margin=dict(t=10, b=10), height=380,
                      legend=dict(orientation="h", y=-0.2))
    st.plotly_chart(fig, use_container_width=True)
    corr = df_scored[["critic_score", "total_sales"]].corr().iloc[0, 1]
    st.caption(f"📌 Correlación de Pearson: **{corr:.3f}** · Basado en {len(df_scored):,} juegos con puntuación")

# ── Sección 6: Top juegos ─────────────────────────────────────────────────────
st.markdown('<div class="section-title">🏆 Top juegos más vendidos</div>', unsafe_allow_html=True)
top_n_games = st.slider("Número de juegos", 5, 50, 20)
top_games = dff.nlargest(top_n_games, "total_sales")[
    ["title", "console", "genre", "publisher", "year", "total_sales",
     "na_sales", "jp_sales", "pal_sales", "other_sales"]
]
fig = px.bar(
    top_games.sort_values("total_sales"), x="total_sales", y="title", orientation="h",
    color="genre", hover_data=["console", "publisher", "year"],
    labels={"total_sales": "Ventas (M)", "title": ""},
    template=PLOTLY_TEMPLATE, color_discrete_sequence=PALETTE
)
fig.update_layout(margin=dict(t=10, b=10), height=max(300, top_n_games * 22),
                  legend=dict(orientation="h", y=-0.15))
st.plotly_chart(fig, use_container_width=True)

# ── Sección 7: Explorador de datos ───────────────────────────────────────────
st.markdown('<div class="section-title">🔍 Explorador de datos</div>', unsafe_allow_html=True)
with st.expander("Ver tabla filtrada", expanded=False):
    cols_show = ["title", "console", "genre", "publisher", "developer",
                 "year", "total_sales", "na_sales", "jp_sales", "pal_sales",
                 "other_sales", "critic_score"]
    cols_show = [c for c in cols_show if c in dff.columns]
    st.dataframe(
        dff[cols_show].sort_values("total_sales", ascending=False).reset_index(drop=True),
        use_container_width=True, height=400
    )
    csv = dff[cols_show].to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Descargar datos filtrados (CSV)", csv,
                       "videogames_filtrado.csv", "text/csv")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<hr style='border-color:#2a2a5a; margin-top:40px;'>
<p style='text-align:center; color:#4a4a7a; font-size:0.78rem;'>
    Video Games Sales Dashboard · 1980–2024 · Datos en millones de unidades vendidas
</p>
""", unsafe_allow_html=True)
