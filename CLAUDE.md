# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

My Personal Map è un'applicazione Python per gestire mappe personali con segnaposti geografici. Utilizza FastAPI per il backend REST, MySQL per la persistenza con supporto spatial data types, e una GUI desktop con CustomTkinter.

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
```bash
# Create MySQL database
mysql -u root -p
CREATE DATABASE mypersonalmap;
CREATE USER 'mypersonalmap_user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON mypersonalmap.* TO 'mypersonalmap_user'@'localhost';
FLUSH PRIVILEGES;

# Configure .env file
cp .env.example .env
# Edit .env with your database credentials and SECRET_KEY
```

### Running the Application
```bash
# Development server (auto-reload enabled)
cd pymypersonalmap
python main.py

# Or with uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
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
   - Map viewer con Folium/Leaflet embedded

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

## Tech Stack (MVP)

**Backend**:
- FastAPI 0.109.0 (REST API)
- SQLAlchemy 2.0.25 (ORM)
- Alembic 1.13.1 (migrations)

**Geospatial**:
- GeoPandas 0.14.2 (data manipulation)
- Shapely 2.0.2 (geometrie)
- Fiona 1.9.5 (I/O file geospaziali)
- GeoPy 2.4.1 (geocoding)
- Folium 0.15.1 (mappe interattive)
- GPXPy 1.6.1 (tracciati GPS)

**GUI**: CustomTkinter 5.2.1

**Security**: PyJWT 2.8.0, passlib[bcrypt] 1.7.4

**Testing**: pytest 7.4.4, httpx 0.26.0

## Important Implementation Notes

### Coordinate Validation
Sempre validare:
- Latitude: -90 to +90
- Longitude: -180 to +180
- SRID 4326 (WGS84) per compatibilità GPS

### Geocoding Rate Limits
- Nominatim: 1 request/second (rispettare per evitare ban)
- Implementare caching in `GeocodingService`
- Fallback su provider multipli

### Spatial Index Usage
Le query geografiche devono usare `ST_Distance_Sphere()` per sfruttare indici spaziali. Query con `LIKE` su coordinate sono inefficienti.

### Import/Export Formats
- **GPX**: Standard GPS, usa `gpxpy` library
- **KML**: Google Earth, usa `fiona`
- **GeoJSON**: Standard web, nativo in GeoPandas
- **CSV**: Richiede mapping colonne lat/lon

### GUI Integration
Folium genera HTML embedded in GUI via WebView. Comunicazione bidirezionale tramite JavaScript callbacks.

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

**MVP (Current Phase)**:
- [ ] Implement SQLAlchemy models (markers, labels, users)
- [ ] Create database migrations with Alembic
- [ ] Implement service layer (MarkerService, GeocodingService)
- [ ] Complete API endpoints with database integration
- [ ] Add authentication (JWT)

**Phase 2**:
- [ ] Desktop GUI implementation
- [ ] Import/Export functionality (GPX, KML)
- [ ] Route planning algorithms

**Phase 3**:
- [ ] Statistics dashboard
- [ ] Web scraping integration
- [ ] Sharing functionality
