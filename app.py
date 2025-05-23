# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from conexion_sqlserver import (
    obtener_videojuegos, obtener_videojuegos_ordenado,
    insertar_videojuego, actualizar_videojuego, eliminar_videojuego,
    obtener_plataformas, insertar_plataforma, actualizar_plataforma, eliminar_plataforma
)
import steam_streamlit
import steambd

st.set_page_config(page_title="PuertoGames CRUD", layout="wide")
st.title("PuertoGames 2025 – Gestión de Videojuegos y Plataformas")

menu = st.sidebar.radio(
    "Menú",
    ["Videojuegos", "Plataformas", "Estadísticas", "SteamBD Explorer", "Steam Analytics"],
)

# —————————————— Videojuegos ——————————————
if menu == "Videojuegos":
    st.header("CRUD Videojuegos")
    c1, c2 = st.columns([2, 1])

    with c1:
        filtro = st.text_input("🔍 Buscar título o plataforma")
        orden = st.radio("Ordenar precio", ["Ascendente", "Descendente"])
        asc = orden == "Ascendente"
        rows = obtener_videojuegos(filtro) if filtro else obtener_videojuegos_ordenado(asc)
        data = [tuple(r) for r in rows]
        df = pd.DataFrame(
            data,
            columns=["ID", "Título", "Precio", "Stock", "ID_Plataforma", "Plataforma"]
        )
        st.dataframe(df, use_container_width=True)

        if not df.empty:
            seleccionado = st.selectbox("Seleccionar ID", sorted(df["ID"].tolist()))
        else:
            seleccionado = None

    with c2:
        st.subheader("Formulario")
        vid = st.number_input("ID Videojuego", min_value=0, step=1, value=seleccionado if seleccionado else 0)
        tit = st.text_input("Título")
        pre = st.number_input("Precio", min_value=0.0, step=0.01, format="%.2f")
        stk = st.number_input("Stock", min_value=0, step=1)

        plats = obtener_plataformas()
        data_p = [tuple(p) for p in plats]
        m = {nombre: pid for pid, nombre in data_p}
        plat_sel = st.selectbox("Plataforma", list(m.keys()))

        if st.button("➕ Crear"):
            if tit and pre >= 0 and stk >= 0:
                insertar_videojuego(tit, pre, stk, m[plat_sel])
                st.success("🎮 Videojuego creado")
                st.rerun()
            else:
                st.error("Completa todos los campos válidos")

        if st.button("✏️ Actualizar"):
            if vid > 0 and tit:
                actualizar_videojuego(vid, tit, pre, stk, m[plat_sel])
                st.success("✏️ Videojuego actualizado")
                st.rerun()
            else:
                st.error("Selecciona ID y completa título")

        if st.button("🗑️ Eliminar"):
            if vid > 0:
                eliminar_videojuego(vid)
                st.success("🗑️ Videojuego eliminado")
                st.rerun()
            else:
                st.error("Selecciona ID válido")

# —————————————— Plataformas ——————————————
elif menu == "Plataformas":
    st.header("CRUD Plataformas")
    plats = obtener_plataformas()
    data_p = [tuple(p) for p in plats]
    dfp = pd.DataFrame(data_p, columns=["ID", "Nombre"])
    st.dataframe(dfp, use_container_width=True)

    pid = st.number_input("ID Plataforma", min_value=0, step=1)
    pname = st.text_input("Nombre Plataforma")

    if st.button("➕ Crear Plataforma"):
        if pname:
            insertar_plataforma(pname)
            st.success("✅ Plataforma creada")
            st.rerun()
        else:
            st.error("Ingresa nombre")

    if st.button("✏️ Actualizar Plataforma"):
        if pid > 0 and pname:
            actualizar_plataforma(pid, pname)
            st.success("✅ Plataforma actualizada")
            st.rerun()
        else:
            st.error("ID y nombre válidos")

    if st.button("🗑️ Eliminar Plataforma"):
        if pid > 0:
            eliminar_plataforma(pid)
            st.success("✅ Plataforma eliminada")
            st.rerun()
        else:
            st.error("ID válido")

# —————————————— Estadísticas ——————————————
elif menu == "Estadísticas":
    st.header("📊 Estadísticas de Videojuegos")
    rows = obtener_videojuegos()
    data = [tuple(r) for r in rows]
    df = pd.DataFrame(data, columns=["ID", "Título", "Precio", "Stock", "ID_Plataforma", "Plataforma"])

    if st.button("Cantidad de juegos por plataforma"):
        conteo = df["Plataforma"].value_counts()
        fig, ax = plt.subplots()
        ax.bar(conteo.index, conteo.values)
        ax.set_ylabel("Cantidad")
        plt.xticks(rotation=45)
        st.pyplot(fig)

    st.markdown("---")

    if st.button("Precio promedio por plataforma"):
        prom = df.groupby("Plataforma")["Precio"].mean().sort_values(ascending=False)
        st.bar_chart(prom)

# —————————————— SteamBD Explorer ——————————————
elif menu == "SteamBD Explorer":
    st.header("🔍 SteamBD Explorer")
    st.markdown("Visualiza las dos tablas de tu base SteamBD:")

    # SteamPurchases
    st.subheader("SteamPurchases")
    filtro_p = st.text_input("Filtrar compras por juego", key="filt_pur")
    df_pur = steam_streamlit.obtener_compras_sql()
    if filtro_p:
        df_pur = df_pur[df_pur["Juego"].str.contains(filtro_p, case=False)]
    st.dataframe(df_pur, use_container_width=True)

    st.markdown("---")

    # SteamPlayStats
    st.subheader("SteamPlayStats")
    filtro_j = st.text_input("Filtrar jugados por juego", key="filt_play")
    topn2 = st.slider("Máx filas", 5, 100, 20, key="filt_play_n")
    df_play = steam_streamlit.obtener_playstats_sql(topn2)
    if filtro_j:
        df_play = df_play[df_play["Juego"].str.contains(filtro_j, case=False)]
    st.dataframe(df_play, use_container_width=True)

# —————————————— Steam Analytics con Pestañas ——————————————
else:
    st.header("📊 Steam Analytics")
    tabs = st.tabs([
        "🔹 API Compras", "🔹 API Jugados",
        "🔹 SQL Compras", "🔹 SQL Jugados",
        "🔹 Dashboard", "💾 Volcar SQL"
    ])

    with tabs[0]:
        st.markdown("### 🎟️ Juegos más comprados (API SteamSpy)")
        if st.button("📥 Cargar Compras API"):
            df_api = steam_streamlit.obtener_juegos_comprados()
            st.dataframe(df_api, use_container_width=True)

    with tabs[1]:
        st.markdown("### 🔥 Juegos más jugados (SteamCharts)")
        topn = st.slider("Top N API", 5, 50, 20, key="tab1_topn")
        if st.button("📥 Cargar Jugados API"):
            df_chart = steam_streamlit.obtener_juegos_mas_jugados(topn)
            st.dataframe(df_chart, use_container_width=True)

    with tabs[2]:
        st.markdown("### 💾 Compras desde SQL Server")
        if st.button("📥 Cargar Compras SQL"):
            df_sql_comp = steam_streamlit.obtener_compras_sql()
            st.dataframe(df_sql_comp, use_container_width=True)

    with tabs[3]:
        st.markdown("### 💾 Jugados desde SQL Server")
        topn2 = st.slider("Top N SQL", 5, 50, 20, key="tab3_topn")
        if st.button("📥 Cargar Jugados SQL"):
            df_sql_jug = steam_streamlit.obtener_playstats_sql(topn2)
            st.dataframe(df_sql_jug, use_container_width=True)

    with tabs[4]:
        st.markdown("### 📈 Dashboard de Estadísticas")
        choice = st.selectbox(
            "Selecciona estadística",
            ["Mas Jugados (SQL)", "Mas Plataformas", "Precio: caro→barato"]
        )
        if choice == "Mas Jugados (SQL)":
            df_sql_jug = steam_streamlit.obtener_playstats_sql(20)
            st.bar_chart(df_sql_jug.set_index("Juego")["Jugadores Actuales"])
        elif choice == "Mas Plataformas":
            rows = obtener_videojuegos()
            data = [tuple(r) for r in rows]
            df_crud = pd.DataFrame(data, columns=["ID", "Título", "Precio", "Stock", "ID_Plataforma", "Plataforma"])
            st.bar_chart(df_crud["Plataforma"].value_counts())
        else:
            rows = obtener_videojuegos()
            data = [tuple(r) for r in rows]
            df_crud = pd.DataFrame(data, columns=["ID", "Título", "Precio", "Stock", "ID_Plataforma", "Plataforma"])
            top_price = df_crud.sort_values("Precio", ascending=False).set_index("Título")["Precio"]
            st.bar_chart(top_price)

    with tabs[5]:
        st.markdown("### 💾 Volcado a SteamBD")
        limit = st.slider("Top N jugados a insertar", 5, 50, 20, key="volcar_lim")
        if st.button("💾 Insertar en SteamBD"):
            try:
                steambd.volcar_steambd(limit_jug=limit)
                st.success("✅ Datos volcados en SteamBD")
            except Exception as e:
                st.error(f"Error al volcar datos: {e}")
