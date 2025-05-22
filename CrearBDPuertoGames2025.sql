USE PuertoGames2025;
GO

-- Eliminar tablas si existen
IF OBJECT_ID('dbo.Videojuego', 'U') IS NOT NULL
    DROP TABLE dbo.Videojuego;
IF OBJECT_ID('dbo.Plataforma', 'U') IS NOT NULL
    DROP TABLE dbo.Plataforma;
GO

-- Crear tablas
CREATE TABLE Plataforma ( 
    IDPlataforma INT PRIMARY KEY IDENTITY(1,1),
    Nombre       NVARCHAR(50) NOT NULL
);

CREATE TABLE Videojuego (
    IDVideojuego INT        PRIMARY KEY IDENTITY(1,1),
    Nombre        NVARCHAR(100) NOT NULL,
    Genero        NVARCHAR(100) NOT NULL,
    Precio        DECIMAL(10,2) NOT NULL,
    Stock         INT            NOT NULL CHECK (Stock >= 0),
    IDPlataforma  INT            NOT NULL
      FOREIGN KEY (IDPlataforma) REFERENCES Plataforma(IDPlataforma)
);
GO

-- Datos iniciales (ejemplos con stock)
INSERT INTO Plataforma (Nombre) VALUES
  ('Pc'), ('Xbox'), ('PS4'), ('Nintendo'), ('Atari');

INSERT INTO Videojuego (Nombre, Genero, Precio, Stock, IDPlataforma) VALUES
  ('GTA VI',           'OPEN WORLD',   80000,  50, 1),
  ('Balatro',          'Roguelike',     8500, 120, 1),
  ('nfs',              'Racing',       45000,  75, 1),
  ('Super Smash Bros','Fighting Game', 60000,  40, 1),
  ('Limbo',            'Metroidvania',  49990,  30, 1);
GO

-- Limpieza de temporal previa
IF OBJECT_ID('tempdb..#TempVideojuego') IS NOT NULL
    DROP TABLE #TempVideojuego;
GO

-- Tabla temporal para pruebas
SELECT IDVideojuego, Nombre, Genero, Precio, Stock, IDPlataforma
INTO #TempVideojuego
FROM Videojuego;

-- INSERT en temporal + validación
INSERT INTO #TempVideojuego (Nombre, Genero, Precio, Stock, IDPlataforma)
VALUES ('Test Game', 'Test Genre', 1234.56,  10, 2);

SELECT * FROM #TempVideojuego WHERE Nombre = 'Test Game';

-- UPDATE en temporal + validación
UPDATE #TempVideojuego
SET 
  Nombre = Nombre + ' - UPDATED',
  Precio = 2345.67,
  Stock  = Stock + 5
WHERE Nombre = 'Test Game';

SELECT * FROM #TempVideojuego WHERE Nombre LIKE '%UPDATED%';

-- DELETE en temporal + validación
DELETE FROM #TempVideojuego WHERE Nombre LIKE '%UPDATED%';

SELECT * FROM #TempVideojuego WHERE Nombre LIKE '%UPDATED%';  -- debe devolver 0 filas

-- Eliminar tabla temporal
DROP TABLE #TempVideojuego;
GO
