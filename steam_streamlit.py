# steam_streamlit.py

import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import pyodbc

# Cadena de conexión a SteamBD
_CONN_STEAM = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost;'
    'DATABASE=SteamBD;'
    'Trusted_Connection=yes;'
)

def _connect_steambd():
    return pyodbc.connect(_CONN_STEAM)

@st.cache_data(ttl=600)
def obtener_juegos_comprados():
    """
    Usa la API pública de SteamSpy para traer el top 100 de juegos 
    por propietarios y promedio de jugadores en últimas 2 semanas.
    """
    url = "http://steamspy.com/api.php?request=top100in2weeks"
    res = requests.get(url)
    data = res.json()

    df = pd.DataFrame.from_dict(data, orient="index")
    df = df.rename(columns={
        "name": "Juego",
        "owners": "OwnersRaw",
        "average_2weeks": "Promedio 2 Semanas"
    })

    def parse_owners(s: str) -> int:
        low = s.split("..")[0]
        digits = re.sub(r"[^\d]", "", low)
        return int(digits) if digits else 0

    df["Propietarios"] = df["OwnersRaw"].apply(parse_owners)
    df["Propietarios"] = df["Propietarios"].apply(lambda x: f"{x:,}")

    return (
        df[["Juego", "Propietarios", "Promedio 2 Semanas"]]
        .sort_values(
            by="Propietarios",
            key=lambda col: col.str.replace(",", "").astype(int),
            ascending=False
        )
        .reset_index(drop=True)
    )

@st.cache_data(ttl=300)
def obtener_juegos_mas_jugados(limit: int = 20):
    """
    Scrapea steamcharts.com para obtener los top N juegos por jugadores actuales.
    """
    url = "https://steamcharts.com/top"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")
    table = soup.find("table", {"class": "common-table"})
    rows = []
    for tr in table.tbody.find_all("tr")[:limit]:
        cols = tr.find_all("td")
        rank_raw = cols[0].get_text(strip=True)
        rank     = int(re.sub(r"[^\d]", "", rank_raw))
        juego    = cols[1].get_text(strip=True)
        players  = int(cols[2].get_text(strip=True).replace(",", ""))
        change   = cols[3].get_text(strip=True)
        rows.append((rank, juego, players, change))
    return pd.DataFrame(rows, columns=[
        "Rank", "Juego", "Jugadores Actuales", "Cambio 24h"
    ])

@st.cache_data(ttl=600)
def obtener_compras_sql():
    """
    Extrae de SteamBD la tabla SteamPurchases.
    Devuelve un DataFrame con columnas exactly: Juego, Propietarios, Promedio2Sem.
    """
    conn = _connect_steambd()
    cur  = conn.cursor()
    cur.execute("""
        SELECT Juego, Propietarios, Promedio2Sem
        FROM dbo.SteamPurchases
        ORDER BY Propietarios DESC
    """)
    rows = cur.fetchall()
    conn.close()
    df = pd.DataFrame.from_records(
        rows,
        columns=["Juego", "Propietarios", "Promedio2Sem"]
    )
    # Formatear Propietarios como string con comas
    df["Propietarios"] = df["Propietarios"].apply(lambda x: f"{x:,}")
    return df

@st.cache_data(ttl=600)
def obtener_playstats_sql(limit: int = 20):
    """
    Extrae de SteamBD la tabla SteamPlayStats.
    Devuelve un DataFrame con columnas: RankSteam, Juego, JugadoresActuales, Cambio24h.
    """
    conn = _connect_steambd()
    cur  = conn.cursor()
    cur.execute(f"""
        SELECT TOP (?) RankSteam, Juego, JugadoresActuales, Cambio24h
        FROM dbo.SteamPlayStats
        ORDER BY JugadoresActuales DESC
    """, limit)
    rows = cur.fetchall()
    conn.close()
    return pd.DataFrame.from_records(
        rows,
        columns=["Rank", "Juego", "Jugadores Actuales", "Cambio 24h"]
    )

def main():
    st.header("📊 Steam Analytics")

    # -- SteamSpy API --
    st.subheader("🎟️ SteamSpy: Juegos más ‘comprados’")
    if st.button("📥 Cargar desde API"):
        df_api = obtener_juegos_comprados()
        st.dataframe(df_api, use_container_width=True)

    # -- SteamCharts scrape --
    st.subheader("🔥 SteamCharts: Juegos más jugados ahora")
    top_n = st.slider("Filas Top N", 5, 50, 20, key="api_topn")
    if st.button("📥 Cargar de SteamCharts"):
        df_chart = obtener_juegos_mas_jugados(top_n)
        st.dataframe(df_chart, use_container_width=True)

    st.markdown("---")

    # -- Datos desde SteamBD --
    st.subheader("💾 SteamBD: Datos cargados en SQL Server")
    if st.button("📥 Cargar compras desde SQL"):
        df_sql_comp = obtener_compras_sql()
        st.dataframe(df_sql_comp, use_container_width=True)
    if st.button("📥 Cargar jugados desde SQL"):
        df_sql_jug = obtener_playstats_sql(top_n)
        st.dataframe(df_sql_jug, use_container_width=True)
