# conexion_sqlserver.py

import pyodbc

def conectar_bd():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost;'
        'DATABASE=PuertoGames2025;'
        'Trusted_Connection=yes;'
    )

# — VIDEOJUEGOS —
def obtener_videojuegos(filtro=None):
    sql = """
        SELECT v.id_videojuego, v.titulo, v.precio, v.stock,
               p.id_plataforma, p.nombre
        FROM Videojuegos v
        JOIN Plataformas p ON v.id_plataforma = p.id_plataforma
    """
    params = []
    if filtro:
        sql += " WHERE v.titulo LIKE ? OR p.nombre LIKE ?"
        params = [f'%{filtro}%', f'%{filtro}%']
    conn = conectar_bd()
    cur = conn.cursor()
    cur.execute(sql, params)
    rows = cur.fetchall()
    conn.close()
    return rows

def obtener_videojuegos_ordenado(ascendente=True):
    orden = "ASC" if ascendente else "DESC"
    sql = f"""
        SELECT v.id_videojuego, v.titulo, v.precio, v.stock,
               p.id_plataforma, p.nombre
        FROM Videojuegos v
        JOIN Plataformas p ON v.id_plataforma = p.id_plataforma
        ORDER BY v.precio {orden}
    """
    conn = conectar_bd()
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    return rows

def insertar_videojuego(titulo, precio, stock, id_plataforma):
    sql = """
        INSERT INTO Videojuegos (titulo, precio, stock, id_plataforma)
        VALUES (?,?,?,?)
    """
    conn = conectar_bd()
    cur = conn.cursor()
    cur.execute(sql, titulo, precio, stock, id_plataforma)
    conn.commit()
    conn.close()

def actualizar_videojuego(id_vid, titulo, precio, stock, id_plataforma):
    sql = """
        UPDATE Videojuegos
        SET titulo=?, precio=?, stock=?, id_plataforma=?
        WHERE id_videojuego=?
    """
    conn = conectar_bd()
    cur = conn.cursor()
    cur.execute(sql, titulo, precio, stock, id_plataforma, id_vid)
    conn.commit()
    conn.close()

def eliminar_videojuego(id_vid):
    sql = "DELETE FROM Videojuegos WHERE id_videojuego=?"
    conn = conectar_bd()
    cur = conn.cursor()
    cur.execute(sql, id_vid)
    conn.commit()
    conn.close()

# — PLATAFORMAS —
def obtener_plataformas():
    conn = conectar_bd()
    cur = conn.cursor()
    cur.execute("SELECT id_plataforma, nombre FROM Plataformas")
    rows = cur.fetchall()
    conn.close()
    return rows

def insertar_plataforma(nombre):
    conn = conectar_bd()
    cur = conn.cursor()
    cur.execute("INSERT INTO Plataformas (nombre) VALUES (?)", nombre)
    conn.commit()
    conn.close()

def actualizar_plataforma(id_plat, nombre):
    conn = conectar_bd()
    cur = conn.cursor()
    cur.execute("UPDATE Plataformas SET nombre=? WHERE id_plataforma=?", nombre, id_plat)
    conn.commit()
    conn.close()

def eliminar_plataforma(id_plat):
    conn = conectar_bd()
    cur = conn.cursor()
    cur.execute("DELETE FROM Plataformas WHERE id_plataforma=?", id_plat)
    conn.commit()
    conn.close()
