USE PuertoGames2025;
GO

-- Eliminar tablas si existen
IF OBJECT_ID('dbo.Videojuegos', 'U') IS NOT NULL
    DROP TABLE dbo.Videojuegos;
GO
IF OBJECT_ID('dbo.Plataformas', 'U') IS NOT NULL
    DROP TABLE dbo.Plataformas;
GO

-- Crear tabla Plataformas
CREATE TABLE dbo.Plataformas (
    id_plataforma INT IDENTITY(1,1) PRIMARY KEY,
    nombre         NVARCHAR(100) NOT NULL
);
GO

-- Crear tabla Videojuegos
CREATE TABLE dbo.Videojuegos (
    id_videojuego INT IDENTITY(1,1) PRIMARY KEY,
    titulo        NVARCHAR(200) NOT NULL,
    precio        DECIMAL(10,2) NOT NULL CHECK (precio >= 0),
    stock         INT NOT NULL CHECK (stock >= 0),
    id_plataforma INT NOT NULL
        CONSTRAINT FK_Videojuegos_Plataformas
        REFERENCES dbo.Plataformas(id_plataforma)
);
GO

-- Reiniciar identidad solo para Videojuegos (opcional, ya que está recién creada)
DBCC CHECKIDENT ('dbo.Videojuegos', RESEED, 0);
GO

-- Insertar plataformas
INSERT INTO dbo.Plataformas (nombre) VALUES
('PlayStation 5'),
('Xbox Series X/S'),
('Nintendo Switch'),
('PC (Windows/Linux/macOS)'),
('Steam Deck');
GO


-- Insertar videojuegos (10 por plataforma)

-- PlayStation 5 (id_plataforma = 1)
INSERT INTO dbo.Videojuegos (titulo, precio, stock, id_plataforma) VALUES
('Astro''s Playroom', 0.00, 100, 1),
('Ratchet & Clank: Rift Apart', 49.99, 50, 1),
('Returnal', 59.99, 40, 1),
('Demon''s Souls', 69.99, 35, 1),
('Spider-Man: Miles Morales', 39.99, 60, 1),
('Gran Turismo 7', 59.99, 45, 1),
('Horizon Forbidden West', 69.99, 70, 1),
('Final Fantasy XVI', 69.99, 20, 1),
('God of War: Ragnarok', 69.99, 30, 1),
('Sackboy: A Big Adventure', 49.99, 55, 1);

-- Xbox Series X/S (id_plataforma = 2)
INSERT INTO dbo.Videojuegos (titulo, precio, stock, id_plataforma) VALUES
('Halo Infinite', 59.99, 60, 2),
('Forza Horizon 5', 59.99, 50, 2),
('Gears 5', 39.99, 70, 2),
('Microsoft Flight Simulator', 69.99, 25, 2),
('Psychonauts 2', 29.99, 40, 2),
('State of Decay 2', 19.99, 30, 2),
('Ori and the Will of the Wisps', 29.99, 45, 2),
('Grounded', 24.99, 60, 2),
('Redfall', 49.99, 20, 2),
('Starfield', 69.99, 15, 2);

-- Nintendo Switch (id_plataforma = 3)
INSERT INTO dbo.Videojuegos (titulo, precio, stock, id_plataforma) VALUES
('The Legend of Zelda: Breath of the Wild', 59.99, 80, 3),
('Super Mario Odyssey', 59.99, 75, 3),
('Animal Crossing: New Horizons', 59.99, 90, 3),
('Mario Kart 8 Deluxe', 59.99, 85, 3),
('Metroid Dread', 49.99, 40, 3),
('Splatoon 3', 59.99, 60, 3),
('Kirby and the Forgotten Land', 59.99, 45, 3),
('Fire Emblem: Engage', 59.99, 50, 3),
('Bayonetta 3', 59.99, 35, 3),
('Pikmin 4', 49.99, 25, 3);

-- PC (id_plataforma = 4)
INSERT INTO dbo.Videojuegos (titulo, precio, stock, id_plataforma) VALUES
('Counter-Strike 2', 0.00, 1000, 4),
('Valorant', 0.00, 1000, 4),
('Cyberpunk 2077', 59.99, 100, 4),
('Baldur''s Gate 3', 69.99, 80, 4),
('The Witcher 3: Wild Hunt', 39.99, 90, 4),
('Elden Ring', 59.99, 75, 4),
('Stardew Valley', 14.99, 120, 4),
('Minecraft (Java Edition)', 26.95, 110, 4),
('Hades', 24.99, 60, 4),
('Terraria', 9.99, 140, 4);

-- Steam Deck (id_plataforma = 5)
INSERT INTO dbo.Videojuegos (titulo, precio, stock, id_plataforma) VALUES
('Portal 2', 9.99, 100, 5),
('Half-Life 2', 8.99, 120, 5),
('Hollow Knight', 14.99, 90, 5),
('Celeste', 19.99, 80, 5),
('Dead Cells', 24.99, 70, 5),
('Slay the Spire', 21.99, 65, 5),
('Disco Elysium', 39.99, 50, 5),
('Doom Eternal', 59.99, 45, 5),
('The Binding of Isaac: Rebirth', 14.99, 60, 5),
('Vampire Survivors', 4.99, 150, 5);
GO
