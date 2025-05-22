import pyodbc

def conectar_bd():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost;'
        'DATABASE=PuertoGames2025;'
        'Trusted_Connection=yes;'
    )

def obtener_videojuegos(nombre_busqueda=None):
    conn = conectar_bd()
    cursor = conn.cursor()
    if nombre_busqueda:
        sql = """
        SELECT v.IDVideojuego, v.Nombre, v.Genero, v.Precio, v.Stock, p.Nombre
        FROM Videojuego v
        JOIN Plataforma p ON v.IDPlataforma = p.IDPlataforma
        WHERE v.Nombre LIKE ?
        """
        cursor.execute(sql, '%' + nombre_busqueda + '%')
    else:
        sql = """
        SELECT v.IDVideojuego, v.Nombre, v.Genero, v.Precio, v.Stock, p.Nombre
        FROM Videojuego v
        JOIN Plataforma p ON v.IDPlataforma = p.IDPlataforma
        """
        cursor.execute(sql)
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def obtener_videojuegos_ordenado(ascendente=True):
    conn = conectar_bd()
    cursor = conn.cursor()
    orden = "ASC" if ascendente else "DESC"
    sql = f"""
    SELECT v.IDVideojuego, v.Nombre, v.Genero, v.Precio, v.Stock, p.Nombre
    FROM Videojuego v
    JOIN Plataforma p ON v.IDPlataforma = p.IDPlataforma
    ORDER BY v.Precio {orden}
    """
    cursor.execute(sql)
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def insertar_videojuego(nombre, genero, precio, stock, id_plataforma):
    conn = conectar_bd()
    cursor = conn.cursor()
    sql = """
    INSERT INTO Videojuego (Nombre, Genero, Precio, Stock, IDPlataforma)
    VALUES (?, ?, ?, ?, ?)
    """
    cursor.execute(sql, nombre, genero, precio, stock, id_plataforma)
    conn.commit()
    conn.close()

def actualizar_videojuego(id_videojuego, nombre, genero, precio, stock, id_plataforma):
    conn = conectar_bd()
    cursor = conn.cursor()
    sql = """
    UPDATE Videojuego
    SET Nombre = ?, Genero = ?, Precio = ?, Stock = ?, IDPlataforma = ?
    WHERE IDVideojuego = ?
    """
    cursor.execute(sql, nombre, genero, precio, stock, id_plataforma, id_videojuego)
    conn.commit()
    conn.close()

def eliminar_videojuego(id_videojuego):
    conn = conectar_bd()
    cursor = conn.cursor()
    sql = "DELETE FROM Videojuego WHERE IDVideojuego = ?"
    cursor.execute(sql, id_videojuego)
    conn.commit()
    conn.close()
