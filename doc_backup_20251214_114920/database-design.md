# Database Design - My Personal Map

## Panoramica

Il database MySQL è progettato per gestire dati geografici, relazionali e metadata flessibili. Utilizza tipi di dati spaziali nativi di MySQL per ottimizzare query geografiche.

## Schema E-R (Entity-Relationship)

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│    users    │         │   markers    │         │   labels    │
├─────────────┤         ├──────────────┤         ├─────────────┤
│ id (PK)     │────┐    │ id (PK)      │    ┌────│ id (PK)     │
│ username    │    │    │ user_id (FK) │────┘    │ name        │
│ email       │    └───→│ name         │         │ color       │
│ password    │         │ coordinates  │         │ icon        │
│ created_at  │         │ description  │         │ user_id(FK) │
└─────────────┘         │ created_at   │         │ created_at  │
                        │ updated_at   │         └─────────────┘
                        └──────────────┘               │
                               │                       │
                               │                       │
                        ┌──────┴──────────┐           │
                        │                 │           │
                        ▼                 ▼           │
                 ┌──────────────┐  ┌──────────────────┴────┐
                 │  gps_tracks  │  │  marker_labels (JOIN) │
                 ├──────────────┤  ├───────────────────────┤
                 │ id (PK)      │  │ marker_id (FK)        │
                 │ marker_id(FK)│  │ label_id (FK)         │
                 │ name         │  │ created_at            │
                 │ track_data   │  └───────────────────────┘
                 │ distance     │
                 │ duration     │
                 │ created_at   │
                 └──────────────┘
                        │
                        │
                 ┌──────┴──────────┐
                 │     routes      │
                 ├─────────────────┤
                 │ id (PK)         │
                 │ user_id (FK)    │
                 │ name            │
                 │ start_point     │
                 │ waypoints (JSON)│
                 │ total_distance  │
                 │ created_at      │
                 └─────────────────┘
```

## Tabelle del Database

### 1. users
Tabella per la gestione degli utenti dell'applicazione.

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    is_active BOOLEAN DEFAULT TRUE,
    INDEX idx_username (username),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Campi**:
- `id`: Chiave primaria auto-incrementale
- `username`: Nome utente univoco
- `email`: Email univoca
- `password_hash`: Hash della password (bcrypt/argon2)
- `full_name`: Nome completo (opzionale)
- `created_at`: Data creazione account
- `updated_at`: Data ultimo aggiornamento
- `last_login`: Data ultimo accesso
- `is_active`: Flag account attivo

### 2. markers
Tabella principale per i segnaposti geografici.

```sql
CREATE TABLE markers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(200) NOT NULL,
    coordinates POINT NOT NULL SRID 4326,
    description TEXT,
    address VARCHAR(500),
    metadata JSON,
    visit_count INT DEFAULT 0,
    is_favorite BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    SPATIAL INDEX idx_coordinates (coordinates),
    INDEX idx_user_id (user_id),
    INDEX idx_name (name),
    INDEX idx_is_favorite (is_favorite),
    FULLTEXT INDEX idx_fulltext_search (name, description)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Campi**:
- `id`: Chiave primaria
- `user_id`: Riferimento all'utente proprietario
- `name`: Nome del luogo
- `coordinates`: Punto geografico (latitudine, longitudine) con SRID 4326 (WGS84)
- `description`: Descrizione dettagliata
- `address`: Indirizzo testuale (da geocoding)
- `metadata`: Dati aggiuntivi in formato JSON (es: orari, telefono, sito web)
- `visit_count`: Numero di visite
- `is_favorite`: Flag per luoghi preferiti
- `created_at`: Data creazione
- `updated_at`: Data ultimo aggiornamento

**Indici Spaziali**:
- `idx_coordinates`: Indice spaziale per query geografiche veloci

**Esempio Inserimento**:
```sql
INSERT INTO markers (user_id, name, coordinates, description)
VALUES (
    1,
    'Colosseo',
    ST_GeomFromText('POINT(12.4924 41.8902)', 4326),
    'Anfiteatro Flavio, simbolo di Roma'
);
```

**Query Geografiche**:
```sql
-- Trova markers entro 5km da un punto
SELECT id, name,
       ST_Distance_Sphere(
           coordinates,
           ST_GeomFromText('POINT(12.4924 41.8902)', 4326)
       ) / 1000 AS distance_km
FROM markers
WHERE ST_Distance_Sphere(
    coordinates,
    ST_GeomFromText('POINT(12.4924 41.8902)', 4326)
) <= 5000
ORDER BY distance_km;
```

### 3. labels
Tabella per le etichette/categorie dei markers.

```sql
CREATE TABLE labels (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    color VARCHAR(7) DEFAULT '#3388ff',
    icon VARCHAR(50) DEFAULT 'map-marker',
    description TEXT,
    is_system BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_label (user_id, name),
    INDEX idx_user_id (user_id),
    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Campi**:
- `id`: Chiave primaria
- `user_id`: Riferimento utente (per labels custom)
- `name`: Nome etichetta (es: "Ristorante", "Urbex")
- `color`: Colore hex per visualizzazione mappa
- `icon`: Nome icona FontAwesome o custom
- `description`: Descrizione categoria
- `is_system`: Flag per labels predefinite dal sistema
- `created_at`: Data creazione
- `updated_at`: Data ultimo aggiornamento

**Labels di Sistema Predefinite**:
```sql
INSERT INTO labels (user_id, name, color, icon, is_system) VALUES
(1, 'Urbex', '#8b4513', 'building', TRUE),
(1, 'Ristorante', '#ff4444', 'utensils', TRUE),
(1, 'Pizzeria', '#ff8c00', 'pizza-slice', TRUE),
(1, 'Fotografia', '#4444ff', 'camera', TRUE),
(1, 'Drone', '#00ccff', 'helicopter', TRUE),
(1, 'Natura', '#44ff44', 'tree', TRUE),
(1, 'Museo', '#9932cc', 'landmark', TRUE);
```

### 4. marker_labels
Tabella di join many-to-many tra markers e labels.

```sql
CREATE TABLE marker_labels (
    marker_id INT NOT NULL,
    label_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (marker_id, label_id),
    FOREIGN KEY (marker_id) REFERENCES markers(id) ON DELETE CASCADE,
    FOREIGN KEY (label_id) REFERENCES labels(id) ON DELETE CASCADE,
    INDEX idx_label_id (label_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Campi**:
- `marker_id`: Riferimento al marker
- `label_id`: Riferimento alla label
- `created_at`: Data associazione

**Query Utili**:
```sql
-- Trova tutti i markers con label "Ristorante"
SELECT m.*
FROM markers m
JOIN marker_labels ml ON m.id = ml.marker_id
JOIN labels l ON ml.label_id = l.id
WHERE l.name = 'Ristorante';

-- Conta markers per ogni label
SELECT l.name, COUNT(ml.marker_id) as count
FROM labels l
LEFT JOIN marker_labels ml ON l.id = ml.label_id
GROUP BY l.id, l.name;
```

### 5. gps_tracks
Tabella per tracciati GPS completi.

```sql
CREATE TABLE gps_tracks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    marker_id INT NULL,
    user_id INT NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    track_data LINESTRING NOT NULL SRID 4326,
    elevation_data JSON,
    total_distance DECIMAL(10, 2),
    total_duration INT,
    avg_speed DECIMAL(5, 2),
    max_elevation DECIMAL(7, 2),
    min_elevation DECIMAL(7, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (marker_id) REFERENCES markers(id) ON DELETE SET NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    SPATIAL INDEX idx_track_data (track_data),
    INDEX idx_user_id (user_id),
    INDEX idx_marker_id (marker_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Campi**:
- `id`: Chiave primaria
- `marker_id`: Marker associato (opzionale)
- `user_id`: Riferimento utente
- `name`: Nome tracciato
- `description`: Descrizione
- `track_data`: LINESTRING con coordinate tracciato
- `elevation_data`: Dati elevazione in JSON (array di altezze)
- `total_distance`: Distanza totale in km
- `total_duration`: Durata in secondi
- `avg_speed`: Velocità media km/h
- `max_elevation`: Altitudine massima metri
- `min_elevation`: Altitudine minima metri

**Esempio Inserimento**:
```sql
INSERT INTO gps_tracks (user_id, name, track_data, total_distance)
VALUES (
    1,
    'Escursione Monte Bianco',
    ST_GeomFromText('LINESTRING(
        6.8650 45.8326,
        6.8655 45.8330,
        6.8660 45.8335
    )', 4326),
    12.5
);
```

### 6. routes
Tabella per itinerari pianificati.

```sql
CREATE TABLE routes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    start_point POINT NOT NULL SRID 4326,
    waypoints JSON NOT NULL,
    route_geometry LINESTRING SRID 4326,
    total_distance DECIMAL(10, 2),
    estimated_duration INT,
    optimization_type ENUM('shortest', 'fastest', 'scenic') DEFAULT 'shortest',
    is_completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    SPATIAL INDEX idx_start_point (start_point),
    SPATIAL INDEX idx_route_geometry (route_geometry),
    INDEX idx_user_id (user_id),
    INDEX idx_is_completed (is_completed)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Campi**:
- `id`: Chiave primaria
- `user_id`: Riferimento utente
- `name`: Nome itinerario
- `description`: Descrizione
- `start_point`: Punto di partenza
- `waypoints`: Array JSON di marker_id da visitare in ordine
- `route_geometry`: Geometria percorso calcolato
- `total_distance`: Distanza totale km
- `estimated_duration`: Durata stimata minuti
- `optimization_type`: Tipo ottimizzazione percorso
- `is_completed`: Flag itinerario completato
- `completed_at`: Data completamento

**Esempio Waypoints JSON**:
```json
{
  "markers": [12, 45, 78, 23],
  "order_optimized": true,
  "avoid_highways": false,
  "notes": {
    "12": "Prima tappa - colazione",
    "45": "Sosta pranzo"
  }
}
```

### 7. import_history
Tabella per tracciare importazioni di dati.

```sql
CREATE TABLE import_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    import_type ENUM('gpx', 'kml', 'csv', 'json', 'scraping') NOT NULL,
    filename VARCHAR(255),
    source_url VARCHAR(500),
    markers_imported INT DEFAULT 0,
    markers_duplicates INT DEFAULT 0,
    markers_errors INT DEFAULT 0,
    status ENUM('pending', 'processing', 'completed', 'failed') DEFAULT 'pending',
    error_message TEXT,
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Campi**:
- `id`: Chiave primaria
- `user_id`: Riferimento utente
- `import_type`: Tipo file/sorgente
- `filename`: Nome file originale
- `source_url`: URL sorgente (per scraping)
- `markers_imported`: Numero markers importati con successo
- `markers_duplicates`: Duplicati ignorati
- `markers_errors`: Errori riscontrati
- `status`: Stato importazione
- `error_message`: Messaggio errore se fallito
- `metadata`: Dati aggiuntivi importazione

## Viste Database

### view_markers_with_labels
Vista denormalizzata per accesso rapido a markers con labels.

```sql
CREATE VIEW view_markers_with_labels AS
SELECT
    m.id,
    m.user_id,
    m.name,
    ST_X(m.coordinates) AS longitude,
    ST_Y(m.coordinates) AS latitude,
    m.description,
    m.address,
    m.is_favorite,
    m.created_at,
    GROUP_CONCAT(l.name ORDER BY l.name SEPARATOR ', ') AS labels,
    GROUP_CONCAT(l.color ORDER BY l.name SEPARATOR ',') AS label_colors
FROM markers m
LEFT JOIN marker_labels ml ON m.id = ml.marker_id
LEFT JOIN labels l ON ml.label_id = l.id
GROUP BY m.id;
```

### view_user_statistics
Vista con statistiche utente.

```sql
CREATE VIEW view_user_statistics AS
SELECT
    u.id AS user_id,
    u.username,
    COUNT(DISTINCT m.id) AS total_markers,
    COUNT(DISTINCT l.id) AS total_custom_labels,
    COUNT(DISTINCT r.id) AS total_routes,
    COUNT(DISTINCT gt.id) AS total_tracks,
    SUM(m.is_favorite) AS favorite_markers,
    MAX(m.created_at) AS last_marker_created
FROM users u
LEFT JOIN markers m ON u.id = m.user_id
LEFT JOIN labels l ON u.id = l.user_id AND l.is_system = FALSE
LEFT JOIN routes r ON u.id = r.user_id
LEFT JOIN gps_tracks gt ON u.id = gt.user_id
GROUP BY u.id;
```

## Stored Procedures

### sp_find_nearby_markers
Trova markers vicini a coordinate specifiche.

```sql
DELIMITER $$

CREATE PROCEDURE sp_find_nearby_markers(
    IN p_latitude DECIMAL(10, 8),
    IN p_longitude DECIMAL(11, 8),
    IN p_radius_km DECIMAL(10, 2),
    IN p_user_id INT
)
BEGIN
    SELECT
        m.id,
        m.name,
        ST_X(m.coordinates) AS longitude,
        ST_Y(m.coordinates) AS latitude,
        ST_Distance_Sphere(
            m.coordinates,
            ST_GeomFromText(CONCAT('POINT(', p_longitude, ' ', p_latitude, ')'), 4326)
        ) / 1000 AS distance_km,
        m.description,
        m.is_favorite
    FROM markers m
    WHERE m.user_id = p_user_id
    AND ST_Distance_Sphere(
        m.coordinates,
        ST_GeomFromText(CONCAT('POINT(', p_longitude, ' ', p_latitude, ')'), 4326)
    ) <= (p_radius_km * 1000)
    ORDER BY distance_km;
END$$

DELIMITER ;
```

### sp_calculate_route_distance
Calcola distanza totale itinerario.

```sql
DELIMITER $$

CREATE PROCEDURE sp_calculate_route_distance(
    IN p_waypoint_ids JSON,
    OUT p_total_distance DECIMAL(10, 2)
)
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE prev_coords POINT;
    DECLARE curr_coords POINT;
    DECLARE total DECIMAL(10, 2) DEFAULT 0;
    DECLARE i INT DEFAULT 0;
    DECLARE waypoint_count INT;

    SET waypoint_count = JSON_LENGTH(p_waypoint_ids);

    WHILE i < waypoint_count - 1 DO
        SELECT coordinates INTO prev_coords
        FROM markers
        WHERE id = JSON_EXTRACT(p_waypoint_ids, CONCAT('$[', i, ']'));

        SELECT coordinates INTO curr_coords
        FROM markers
        WHERE id = JSON_EXTRACT(p_waypoint_ids, CONCAT('$[', i + 1, ']'));

        SET total = total + (ST_Distance_Sphere(prev_coords, curr_coords) / 1000);
        SET i = i + 1;
    END WHILE;

    SET p_total_distance = total;
END$$

DELIMITER ;
```

## Triggers

### trg_marker_updated
Aggiorna timestamp quando marker viene modificato.

```sql
DELIMITER $$

CREATE TRIGGER trg_marker_updated
BEFORE UPDATE ON markers
FOR EACH ROW
BEGIN
    SET NEW.updated_at = CURRENT_TIMESTAMP;
END$$

DELIMITER ;
```

## Indici e Ottimizzazioni

### Indici Spaziali
- Tutti i campi POINT e LINESTRING hanno indici spaziali
- SRID 4326 (WGS84) per compatibilità GPS

### Indici Composti
```sql
-- Per query frequenti
CREATE INDEX idx_user_favorite ON markers(user_id, is_favorite);
CREATE INDEX idx_user_created ON markers(user_id, created_at DESC);
```

### Full-Text Search
```sql
-- Per ricerca testuale veloce
ALTER TABLE markers ADD FULLTEXT INDEX idx_search (name, description, address);

-- Esempio query
SELECT * FROM markers
WHERE MATCH(name, description, address) AGAINST('colosseo roma' IN NATURAL LANGUAGE MODE);
```

## Backup e Manutenzione

### Script Backup
```bash
# Backup completo
mysqldump -u root -p mypersonalmap > backup_$(date +%Y%m%d).sql

# Backup solo schema
mysqldump -u root -p --no-data mypersonalmap > schema.sql

# Backup solo dati
mysqldump -u root -p --no-create-info mypersonalmap > data.sql
```

### Manutenzione Indici Spaziali
```sql
-- Ottimizza tabelle con indici spaziali
OPTIMIZE TABLE markers;
OPTIMIZE TABLE gps_tracks;
OPTIMIZE TABLE routes;

-- Analizza performance query
EXPLAIN SELECT * FROM markers
WHERE ST_Distance_Sphere(coordinates, ST_GeomFromText('POINT(12 41)', 4326)) < 5000;
```

## Migrazione e Versioning

### Strumenti
- **Alembic**: Per migrazioni schema con SQLAlchemy
- **Flyway**: Alternative per migration management

### Esempio Migration
```python
# alembic/versions/001_create_markers_table.py
def upgrade():
    op.create_table(
        'markers',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(200), nullable=False),
        # ... altri campi
    )

def downgrade():
    op.drop_table('markers')
```

## Sicurezza Database

### User Privileges
```sql
-- User applicazione (read/write limitato)
CREATE USER 'mypersonalmap_app'@'localhost' IDENTIFIED BY 'secure_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON mypersonalmap.* TO 'mypersonalmap_app'@'localhost';

-- User read-only (per reporting)
CREATE USER 'mypersonalmap_ro'@'localhost' IDENTIFIED BY 'ro_password';
GRANT SELECT ON mypersonalmap.* TO 'mypersonalmap_ro'@'localhost';

FLUSH PRIVILEGES;
```

### SSL Connections
```sql
-- Richiedi SSL per connessioni
ALTER USER 'mypersonalmap_app'@'localhost' REQUIRE SSL;
```
