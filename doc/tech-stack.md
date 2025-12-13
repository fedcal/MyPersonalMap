# Stack Tecnologico - My Personal Map

## Panoramica

Questo documento descrive le tecnologie utilizzate nel progetto My Personal Map e le motivazioni dietro ogni scelta.

## Backend

### Python 3.x
**Ruolo**: Linguaggio principale del backend

**Librerie Principali**:
- **FastAPI**: Framework moderno per la creazione di API REST
  - Performance elevate (basato su Starlette e Pydantic)
  - Documentazione automatica (Swagger/OpenAPI)
  - Type hints nativi
  - Validazione automatica dei dati

- **SQLAlchemy**: ORM per l'interazione con MySQL
  - Gestione delle migrazioni
  - Query builder type-safe
  - Connection pooling

- **Pydantic**: Validazione dati e serializzazione
  - Validazione automatica dei modelli
  - Conversione automatica dei tipi
  - Generazione schema JSON

**Motivazioni**:
- Ecosistema ricco di librerie per GIS e mapping
- Ottima integrazione con database
- Facilità di sviluppo e manutenzione
- Community attiva

## Database

### MySQL 8.0+
**Ruolo**: Database relazionale principale

**Funzionalità Utilizzate**:
- **Spatial Data Types**: Per memorizzare coordinate geografiche
  - POINT per singole coordinate
  - LINESTRING per tracciati GPS
  - Indici spaziali per query geografiche efficienti

- **JSON**: Per memorizzare metadata flessibili
- **Full-Text Search**: Per ricerca nei nomi e descrizioni
- **Foreign Keys**: Per garantire integrità referenziale

**Motivazioni**:
- Supporto nativo per dati geospaziali
- Affidabilità e maturità
- Performance eccellenti con indici spaziali
- Ampio supporto e documentazione

## Frontend / GUI

### Tkinter / CustomTkinter
**Ruolo**: Interfaccia grafica desktop

**Componenti**:
- **CustomTkinter**: Versione moderna di Tkinter con UI moderna
  - Temi dark/light
  - Widget personalizzabili
  - Look & feel moderno

**Alternative Considerate**:
- **PyQt5/PySide6**: Più potente ma più pesante
- **Kivy**: Orientato a mobile, meno adatto per desktop

**Motivazioni**:
- Incluso nella standard library Python
- Leggero e veloce
- Sufficiente per le esigenze del progetto
- Facile deployment senza dipendenze esterne pesanti

### Folium / Leaflet
**Ruolo**: Visualizzazione mappe interattive

**Caratteristiche**:
- Integrazione con OpenStreetMap
- Markers personalizzabili
- Layer multipli
- Supporto tracciati GPS

**Motivazioni**:
- Open source e gratuito
- Altamente personalizzabile
- Eccellente per applicazioni geografiche
- Embedding in applicazioni Python

## API REST

### FastAPI
**Ruolo**: Framework per servizi REST

**Endpoint Principali**:
- `/api/markers`: CRUD per segnaposti
- `/api/labels`: Gestione etichette
- `/api/routes`: Pianificazione itinerari
- `/api/import`: Importazione dati
- `/api/export`: Esportazione dati

**Features**:
- Autenticazione JWT
- Rate limiting
- CORS configurabile
- Documentazione auto-generata

**Motivazioni**:
- Performance superiori rispetto a Flask
- Validazione automatica tramite Pydantic
- Async/await nativo
- Documentazione integrata

## Librerie Aggiuntive

### Geolocalizzazione e Mapping

- **GeoPy**: Geocoding e calcolo distanze
  - Conversione indirizzi in coordinate
  - Calcolo distanze tra punti
  - Supporto vari provider (OpenStreetMap, Google, etc.)

- **Shapely**: Manipolazione geometrie
  - Operazioni su poligoni e linee
  - Calcoli geometrici
  - Validazione coordinate

- **GPXPy**: Parsing file GPX
  - Lettura tracciati GPS
  - Estrazione waypoints
  - Calcolo statistiche tracciati

### Web Scraping

- **Beautiful Soup 4**: Parsing HTML
  - Estrazione dati da pagine web
  - Navigazione DOM

- **Requests**: HTTP client
  - Chiamate HTTP per scraping
  - Session management

- **Selenium** (opzionale): Per siti con JavaScript
  - Scraping contenuti dinamici
  - Automazione browser

### Utilità

- **Python-dotenv**: Gestione variabili d'ambiente
  - Configurazione sensibile
  - Separazione config per ambiente

- **Pytest**: Testing framework
  - Unit tests
  - Integration tests
  - Test coverage

- **Black**: Code formatter
  - Formattazione consistente
  - Standard PEP 8

## Architettura Deployment

### Sviluppo
- **Virtual Environment**: Isolamento dipendenze
- **Git**: Version control
- **Docker** (opzionale): Containerizzazione per sviluppo

### Produzione
- **Uvicorn**: ASGI server per FastAPI
- **Nginx**: Reverse proxy (opzionale)
- **Systemd**: Process management
- **Docker Compose**: Orchestrazione multi-container

## Diagramma Stack

```
┌─────────────────────────────────────────┐
│           Client Layer                  │
│  ┌────────────┐      ┌──────────────┐  │
│  │   GUI      │      │  Web Browser │  │
│  │ (Tkinter)  │      │   (Folium)   │  │
│  └────────────┘      └──────────────┘  │
└─────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│        Application Layer                │
│  ┌──────────────────────────────────┐  │
│  │        FastAPI REST API           │  │
│  │  ┌──────────┐  ┌──────────────┐  │  │
│  │  │ Business │  │   Services   │  │  │
│  │  │  Logic   │  │  (GeoPy,etc) │  │  │
│  │  └──────────┘  └──────────────┘  │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│         Data Layer                      │
│  ┌──────────────────────────────────┐  │
│  │     SQLAlchemy ORM               │  │
│  └──────────────────────────────────┘  │
│                  │                      │
│                  ▼                      │
│  ┌──────────────────────────────────┐  │
│  │       MySQL Database             │  │
│  │  (Spatial + Relational Data)     │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

## Requisiti di Sistema

### Minimo
- Python 3.9+
- MySQL 8.0+
- 2GB RAM
- 500MB spazio disco

### Raccomandato
- Python 3.11+
- MySQL 8.0+
- 4GB RAM
- 1GB spazio disco
- Sistema operativo: Linux, macOS, o Windows 10+

## Considerazioni Future

### Possibili Migrazioni/Aggiunte
- **PostgreSQL + PostGIS**: Alternative a MySQL per funzionalità GIS avanzate
- **Redis**: Cache layer per performance
- **Celery**: Task queue per operazioni asincrone (import/export pesanti)
- **React/Vue**: Frontend web separato per esperienza web moderna
- **Mobile App**: React Native o Flutter per app mobile nativa
