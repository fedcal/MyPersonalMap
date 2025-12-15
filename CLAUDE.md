# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

My Personal Map è un'applicazione desktop cross-platform per gestire mappe personali con segnaposti geografici. Utilizza FastAPI per il backend REST (embedded), MySQL per la persistenza con supporto spatial data types, e una GUI desktop con CustomTkinter. L'applicazione è distribuibile come eseguibile standalone per Windows, macOS e Linux.

## Development Setup

### Environment Setup
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r pymypersonalmap/requirements.txt
```

### Database Setup

**Default: SQLite (Embedded)** - Recommended for Production
```bash
# Configure .env file for SQLite (default)
cp .env.example .env
# Set DATABASE_TYPE=spatialite in .env (already configured)

# Database will be automatically created at:
# - Development: pymypersonalmap/mypersonalmap.db
# - Production: ~/.mypersonalmap/mypersonalmap.db
```

**Optional: MySQL for Development**
```bash
# Start MySQL container (optional)
docker run -d --name mysql-db-root \
  -e MYSQL_ROOT_PASSWORD=password \
  -p 3306:3306 mysql:8.0

# Create database and user
docker exec mysql-db-root mysql -u root -ppassword -e \
  "CREATE DATABASE mypersonalmap; \
   CREATE USER 'mypersonalmap_user'@'%' IDENTIFIED BY 'mypersonalmap_pass'; \
   GRANT ALL PRIVILEGES ON mypersonalmap.* TO 'mypersonalmap_user'@'%'; \
   FLUSH PRIVILEGES;"

# Configure .env for MySQL
# Set DATABASE_TYPE=mysql in .env
```

**Database Auto-Initialization**: The application automatically creates tables and initializes 10 system labels on first startup. No manual migration needed.

**Key Changes**:
- Now uses SQLite with lat/lon columns instead of spatial types
- Zero external dependencies - works out of the box
- Perfect for desktop distribution with PyInstaller

### Running the Application

**IMPORTANT**: When running from project root, always set PYTHONPATH:
```bash
export PYTHONPATH=/path/to/myPersonalMap  # Linux/macOS
# or
set PYTHONPATH=C:\path\to\myPersonalMap   # Windows
```

**Full Application (GUI + Backend)** - Recommended:
```bash
# From project root (requires PYTHONPATH)
PYTHONPATH=$(pwd) python3 pymypersonalmap/main.py

# The application will:
# 1. Show splash screen during initialization
# 2. Start FastAPI backend in background thread (port 8000)
# 3. Auto-initialize database if needed
# 4. Display GUI with interactive map
```

**Backend Only** (for API development):
```bash
# Option 1: From project root with flag
PYTHONPATH=$(pwd) python3 pymypersonalmap/main.py --backend-only

# Option 2: From pymypersonalmap directory (no PYTHONPATH needed)
cd pymypersonalmap && python3 main.py

# Option 3: With uvicorn directly
cd pymypersonalmap && uvicorn main:app --reload
```

**GUI Only** (alternative):
```bash
# Direct GUI launch (also starts backend automatically)
PYTHONPATH=$(pwd) python3 pymypersonalmap/gui/app.py
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pymypersonalmap

# Run specific test file
pytest tests/test_marker_service.py

# Run with verbose output
pytest -v
```

### Code Quality
```bash
# Format code with black
black pymypersonalmap/

# Lint with flake8
flake8 pymypersonalmap/

# Type checking with mypy
mypy pymypersonalmap/
```

## Architecture

### Layered Architecture (5 Layers)

Il progetto segue un'architettura a livelli con separazione chiara delle responsabilità:

1. **Presentation Layer** (`gui/`)
   - Desktop GUI con CustomTkinter
   - Map viewer con Folium embedded in WebView (tkinterweb)
   - Backend FastAPI runs in background thread

2. **API Layer** (`main.py`, `api/routes/`)
   - FastAPI REST endpoints
   - CORS middleware, authentication, validation
   - Swagger auto-documentation at `/docs`

3. **Business Logic Layer** (`services/`)
   - MarkerService: CRUD markers, validazione geografica
   - GeocodingService: Conversione indirizzo ↔ coordinate (GeoPy)
   - RouteService: Algoritmi ottimizzazione itinerari (TSP)
   - ImportExportService: GPX, KML, GeoJSON, CSV

4. **Data Access Layer** (Repository pattern - da implementare in `models/`)
   - MarkerRepository, LabelRepository, RouteRepository
   - Astrazione query database via SQLAlchemy

5. **Database Layer**
   - MySQL 8.0+ con spatial data types (POINT, LINESTRING)
   - Indici spaziali per query geografiche efficienti

### Key Design Patterns

- **Repository Pattern**: Astrazione accesso dati per testabilità
- **Service Layer**: Business logic separata da controllers
- **Dependency Injection**: FastAPI's `Depends()` per database sessions
- **DTO Pattern**: Pydantic models per validazione e serializzazione

### Request Flow Example

```
POST /api/v1/markers
  ↓
FastAPI validates JWT + request schema (Pydantic)
  ↓
MarkerService.create_marker()
  ├─ GeocodingService: valida coordinate
  ├─ LabelService: verifica labels
  └─ MarkerRepository.save()
      ↓
  SQLAlchemy ORM → MySQL INSERT
      ↓
  Response: MarkerResponse model
```

## Configuration

### Environment Variables (.env)

**Critical variables**:
- `DATABASE_URL`: MySQL connection string con formato `mysql+pymysql://user:pass@host/db`
- `SECRET_KEY`: Min 32 chars for JWT signing (generate with `python -c "import secrets; print(secrets.token_urlsafe(32))"`)
- `GEOCODING_PROVIDER`: `nominatim` (free) o `google` (richiede API key)

**Development vs Production**:
- `DEBUG=true` enables auto-reload and detailed errors
- `WORKERS=4` for production (uvicorn workers)
- `CORS_ORIGINS`: Comma-separated allowed origins

Settings are managed centrally in `config/settings.py` using Pydantic's `BaseSettings`.

## Database Schema

### Core Tables

**markers**:
- `coordinates POINT SRID 4326`: Lat/lon con sistema WGS84
- `metadata JSON`: Dati flessibili (orari, telefono, etc.)
- Spatial index on `coordinates` for fast geo queries

**labels**:
- System labels (`is_system=TRUE`): Urbex, Ristorante, Fotografia, Drone, etc.
- User custom labels

**marker_labels**: Many-to-many join table

**routes**:
- `waypoints JSON`: Array di marker_id in ordine
- `route_geometry LINESTRING`: Percorso calcolato

**gps_tracks**:
- `track_data LINESTRING`: Coordinate complete tracciato
- `elevation_data JSON`: Array altezze

### Spatial Queries Example
```sql
-- Markers entro 5km da un punto
SELECT * FROM markers
WHERE ST_Distance_Sphere(
    coordinates,
    ST_GeomFromText('POINT(12.4922 41.8902)', 4326)
) <= 5000;
```

## Tech Stack

**Backend**:
- FastAPI 0.109.0 (REST API)
- SQLAlchemy 2.0.25 (ORM)
- SQLite 3 (embedded database, zero-config)

**Geographic Calculations**:
- Pure Python Haversine formulas (no external dependencies)
- GeoPy 2.4.1 (geocoding - optional)
- Folium 0.15.1 (interactive maps)

**Optional Geospatial** (for import/export only):
- GeoPandas 0.14.2 (GPX/KML processing)
- Shapely 2.0.2 (geometry handling)
- GPXPy 1.6.1 (GPS tracks)

**GUI**:
- CustomTkinter 5.2.1 (desktop framework)
- tkinterweb 3.24.8 (HTML rendering for maps)
- Pillow 10.2.0 (image handling)

**Security**: PyJWT 2.8.0, passlib[bcrypt] 1.7.4

**Build**: PyInstaller 6.3.0 (executable packaging)

**Testing**: pytest 7.4.4, pytest-cov 7.0.0

## Important Implementation Notes

### Coordinate Storage
**Important**: Coordinates are stored as separate `latitude` and `longitude` columns (REAL/Float type):
- Latitude: -90 to +90 (always validate)
- Longitude: -180 to +180 (always validate)
- WGS84 (EPSG:4326) standard

**Why separate columns?**:
- Works with pure SQLite (no spatial extensions needed)
- Perfect for desktop distribution
- Simpler schema, easier to query
- Indexes on (lat, lon) for bounding box queries

### Geographic Calculations
Use `pymypersonalmap.services.geo_utils` for:
- **Distance**: Haversine formula (accuracy <0.5%)
- **Bounding Box**: For area queries
- **Bearing**: Direction between points
- **Midpoint**: Center between coordinates

Example:
```python
from pymypersonalmap.services.geo_utils import haversine_distance

# Distance in km
dist = haversine_distance(45.4642, 9.1900, 41.9028, 12.4964)
# Returns: 477.58 km (Milan to Rome)
```

### Query Optimization
For geographic queries use bounding box first, then distance:
```python
# 1. Get bounding box for 10km radius
bbox = get_bounding_box(center_lat, center_lon, 10)
min_lat, min_lon, max_lat, max_lon = bbox

# 2. Query markers in bounding box (fast, uses index)
markers = db.query(Marker).filter(
    Marker.latitude.between(min_lat, max_lat),
    Marker.longitude.between(min_lon, max_lon)
).all()

# 3. Calculate exact distance for each (accurate)
for marker in markers:
    dist = haversine_distance(
        center_lat, center_lon,
        marker.latitude, marker.longitude
    )
    if dist <= 10:  # Within radius
        results.append(marker)
```

### Import/Export Formats
- **GPX**: Standard GPS, usa `gpxpy` library
- **KML**: Google Earth, usa `fiona`
- **GeoJSON**: Standard web, nativo in GeoPandas
- **CSV**: Direct lat/lon mapping

### GUI Integration
- Folium genera HTML embedded in CustomTkinter GUI via tkinterweb.HtmlFrame
- Backend FastAPI gira in thread daemon separato gestito da `BackendManager`
- GUI comunica con backend via HTTP localhost:8000
- Mappa interattiva con markers, layers, e controlli Leaflet

### Common Bugs and Fixes

**Bug: Folium plugins AttributeError**
```python
# WRONG
import folium
folium.plugins.Fullscreen()  # AttributeError: module 'folium' has no attribute 'plugins'

# CORRECT
from folium import plugins as folium_plugins
folium_plugins.Fullscreen()
```

**Bug: Splash screen initialization order**
```python
# WRONG - _message used before initialization
def __init__(self):
    self._create_content()  # Uses self._message
    self._message = "Loading..."  # Initialized too late

# CORRECT - initialize before use
def __init__(self):
    self._message = "Loading..."  # Initialize first
    self._create_content()  # Now can use self._message
```

**Bug: ModuleNotFoundError when running from project root**
```bash
# WRONG
python3 pymypersonalmap/main.py  # Can't find 'pymypersonalmap' module

# CORRECT
PYTHONPATH=$(pwd) python3 pymypersonalmap/main.py
# or
cd pymypersonalmap && python3 main.py
```

## API Documentation

Once running, interactive API docs available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

## Common Development Tasks

### Adding a New Model
1. Create SQLAlchemy model in `models/` with Base class
2. Import in `database/session.py` for `init_db()`
3. Create Alembic migration: `alembic revision --autogenerate -m "description"`
4. Apply: `alembic upgrade head`

### Adding a New Endpoint
1. Create route function in `api/routes/`
2. Add Pydantic request/response models
3. Inject database session with `Depends(get_db)`
4. Call appropriate service layer function
5. Register router in `main.py`

### Adding a New Service
1. Create service class in `services/`
2. Inject repository dependencies
3. Implement business logic with proper error handling
4. Use custom exceptions for domain errors

## Testing Strategy

- **Unit tests**: Mock repositories, test services in isolation
- **Integration tests**: Real database (use test DB), test API endpoints
- **E2E tests**: Full flow including GUI (use pytest-qt)

Create test database: `CREATE DATABASE mypersonalmap_test;`

## Detailed Documentation

Full documentation in `doc/` (organized by category):

**Getting Started**:
- `doc/01. Getting Started/01. Quick Start.md`: Quick setup (<10 min)
- `doc/01. Getting Started/02. Setup Guide.md`: Complete setup instructions

**Planning & Specs**:
- `doc/02. Planning/01. Use Cases.md`: Functional requirements
- `doc/02. Planning/02. Development Roadmap.md`: Implementation phases

**Architecture**:
- `doc/03. Architecture/01. Architecture.md`: Complete architecture details
- `doc/03. Architecture/02. Tech Stack.md`: Technology stack and rationale
- `doc/03. Architecture/03. Mapping Services Comparison.md`: Library comparisons

**Implementation**:
- `doc/04. Implementation/01. Database Design.md`: Full schema with tables, indexes, procedures
- `doc/04. Implementation/02. API Documentation.md`: All endpoints with examples

**Reference**:
- `doc/05. Reference/01. Sources.md`: Bibliography and references
- `doc/05. Reference/02. User Guide.md`: End-user manual

**Index**: See `doc/00. Index.md` for navigation guide

## Roadmap Priority

**Phase 1 - Backend & Database** (✅ Completato):
- [x] Implement SQLAlchemy models (markers, labels, users)
- [x] Create database migrations with Alembic
- [x] Implement service layer (MarkerService, GeocodingService)
- [x] FastAPI endpoints structure
- [x] Auto-initialization database and system labels
- [x] Docker setup support

**Phase 2 - Desktop GUI** (✅ Completato):
- [x] Implement CustomTkinter GUI components
- [x] Backend manager (FastAPI in thread)
- [x] Database setup wizard
- [x] Map viewer with Folium
- [x] Splash screen with progress tracking
- [x] Error handling and logging
- [x] Integrated startup (main.py starts GUI + Backend)

**Phase 3 - Core Features** (🚧 In Corso):
- [ ] Complete CRUD markers via GUI
- [ ] Geocoding integration (address search)
- [ ] Search and filter system
- [ ] Statistics dashboard

**Phase 4 - Packaging**:
- [ ] PyInstaller configuration
- [ ] Build scripts (Windows, macOS, Linux)
- [ ] Cross-platform testing
- [ ] Installer creation

**Phase 5 - Advanced Features**:
- [ ] Import/Export functionality (GPX, KML)
- [ ] Route planning algorithms
- [ ] GPS tracks support
- [ ] Web scraping integration
