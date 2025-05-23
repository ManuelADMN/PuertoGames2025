# steambd.py

import pyodbc
import pandas as pd
import steam_streamlit

# Cadena de conexión a tu base SteamBD existente
CONN_STEAM = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost;'
    'DATABASE=SteamBD;'
    'Trusted_Connection=yes;'
)

def _get_connection():
    return pyodbc.connect(CONN_STEAM)

def limpiar_tablas():
    """
    Elimina todos los registros de SteamPurchases y SteamPlayStats
    para evitar duplicados al volver a volcar datos.
    """
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute("TRUNCATE TABLE dbo.SteamPurchases;")
    cur.execute("TRUNCATE TABLE dbo.SteamPlayStats;")
    conn.commit()
    conn.close()

def insertar_purchases(df: pd.DataFrame):
    """
    Inserta el DataFrame de compras en dbo.SteamPurchases.
    Espera columnas: Juego, Propietarios (formato '50,000,000'), Promedio 2 Semanas.
    """
    conn = _get_connection()
    cur = conn.cursor()
    sql = """
        INSERT INTO dbo.SteamPurchases
          (Juego, Propietarios, Promedio2Sem)
        VALUES (?,?,?)
    """
    for _, row in df.iterrows():
        # Convertir '50,000,000' → 50000000
        propietarios = int(row["Propietarios"].replace(",", ""))
        promedio2   = float(row["Promedio 2 Semanas"])
        cur.execute(sql, row["Juego"], propietarios, promedio2)
    conn.commit()
    conn.close()
    print(f"{len(df)} filas insertadas en SteamPurchases.")

def insertar_playstats(df: pd.DataFrame):
    """
    Inserta el DataFrame de jugados en dbo.SteamPlayStats.
    Espera columnas: Rank, Juego, Jugadores Actuales, Cambio 24h.
    """
    conn = _get_connection()
    cur = conn.cursor()
    sql = """
        INSERT INTO dbo.SteamPlayStats
          (RankSteam, Juego, JugadoresActuales, Cambio24h)
        VALUES (?,?,?,?)
    """
    for _, row in df.iterrows():
        rank   = int(row["Rank"])
        jugadores = int(row["Jugadores Actuales"])
        cambio = row["Cambio 24h"]
        cur.execute(sql, rank, row["Juego"], jugadores, cambio)
    conn.commit()
    conn.close()
    print(f"{len(df)} filas insertadas en SteamPlayStats.")

def volcar_steambd(limit_jug: int = 20):
    """
    Extrae datos de SteamSpy y SteamCharts y los vuelca
    a las tablas SteamPurchases y SteamPlayStats.
    Este proceso:
      1) Limpia las tablas (TRUNCATE)
      2) Inserta datos de compras (SteamSpy)
      3) Inserta datos de jugados (SteamCharts)
    """
    print("Iniciando volcado a SteamBD...")
    limpiar_tablas()

    # 1) Juegos más comprados
    df_comp = steam_streamlit.obtener_juegos_comprados()
    insertar_purchases(df_comp)

    # 2) Juegos más jugados
    df_jug = steam_streamlit.obtener_juegos_mas_jugados(limit_jug)
    insertar_playstats(df_jug)

    print("Volcado a SteamBD completado correctamente.")

if __name__ == "__main__":
    # Prueba de línea de comandos
    volcar_steambd(limit_jug=20)
