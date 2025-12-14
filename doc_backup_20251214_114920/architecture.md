# Architettura del Sistema - My Personal Map

## Panoramica

My Personal Map è progettato seguendo un'architettura a livelli (layered architecture) che separa le responsabilità e facilita la manutenzione e l'estensibilità del sistema.

## Architettura ad Alto Livello

```
┌───────────────────────────────────────────────────────────┐
│                   Presentation Layer                      │
│   ┌─────────────────────┐      ┌─────────────────────┐    │
│   │   Desktop GUI       │      │   Map Viewer        │    │
│   │   (CustomTkinter)   │      │   (Folium/Leaflet)  │    │
│   └─────────────────────┘      └─────────────────────┘    │
└───────────────────────────────────────────────────────────┘
                          │
                          ▼
┌───────────────────────────────────────────────────────────┐
│                     API Layer (REST)                      │
│   ┌────────────────────────────────────────────────────┐  │
│   │                FastAPI Application                 │  │
│   │  ┌──────────┐ ┌──────────┐ ┌─────────────────┐     │  │
│   │  │ Markers  │ │  Labels  │ │  Routes/Import  │     │  │
│   │  │ Endpoint │ │ Endpoint │ │    Endpoints    │     │  │
│   │  └──────────┘ └──────────┘ └─────────────────┘     │  │
│   └────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────┘
                          │
                          ▼
┌───────────────────────────────────────────────────────────┐
│                   Business Logic Layer                    │
│   ┌────────────────────────────────────────────────────┐  │
│   │               Service Components                   │  │
│   │  ┌──────────────┐  ┌──────────────────────────┐    │  │
│   │  │   Marker     │  │   Route Planning         │    │  │
│   │  │   Service    │  │   Service                │    │  │
│   │  └──────────────┘  └──────────────────────────┘    │  │
│   │  ┌──────────────┐  ┌──────────────────────────┐    │  │
│   │  │   Import/    │  │   Geocoding              │    │  │
│   │  │   Export     │  │   Service                │    │  │
│   │  │   Service    │  │   (GeoPy)                │    │  │
│   │  └──────────────┘  └──────────────────────────┘    │  │
│   └────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────┘
                          │
                          ▼
┌───────────────────────────────────────────────────────────┐
│                  Data Access Layer                        │
│   ┌────────────────────────────────────────────────────┐  │
│   │          Repository Pattern (SQLAlchemy)           │  │
│   │  ┌──────────────┐  ┌──────────────────────────┐    │  │
│   │  │   Marker     │  │   Label                  │    │  │
│   │  │   Repository │  │   Repository             │    │  │
│   │  └──────────────┘  └──────────────────────────┘    │  │
│   │  ┌──────────────┐  ┌──────────────────────────┐    │  │
│   │  │   Route      │  │   GPS Track              │    │  │
│   │  │   Repository │  │   Repository             │    │  │
│   │  └──────────────┘  └──────────────────────────┘    │  │
│   └────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────┘
                          │
                          ▼
┌───────────────────────────────────────────────────────────┐
│                     Database Layer                        │
│   ┌────────────────────────────────────────────────────┐  │
│   │              MySQL Database                        │  │
│   │  ┌──────────┐ ┌────────┐ ┌──────────┐ ┌────────┐   │  │
│   │  │ markers  │ │ labels │ │  routes  │ │ tracks │   │  │
│   │  └──────────┘ └────────┘ └──────────┘ └────────┘   │  │
│   └────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────┘
```

## Componenti Principali

### 1. Presentation Layer (Livello di Presentazione)

#### Desktop GUI (CustomTkinter)
**Responsabilità**:
- Interfaccia utente principale
- Gestione input utente
- Visualizzazione dati in formato tabellare/lista
- Dialoghi e form per inserimento dati

**Componenti**:
- `MainWindow`: Finestra principale dell'applicazione
- `MarkerListView`: Vista lista segnaposti
- `MarkerFormDialog`: Form per creazione/modifica segnaposto
- `LabelManager`: Gestione etichette
- `RoutePlanner`: Interfaccia pianificazione itinerari
- `SettingsPanel`: Pannello impostazioni

#### Map Viewer (Folium/Leaflet)
**Responsabilità**:
- Visualizzazione mappa interattiva
- Rendering markers sulla mappa
- Visualizzazione tracciati GPS
- Interazione con elementi della mappa

**Integrazione**:
- Embedded in GUI tramite WebView
- Genera HTML dinamico con Folium
- Comunicazione bidirezionale con GUI

### 2. API Layer (Livello API REST)

#### FastAPI Application
**Responsabilità**:
- Esposizione endpoint REST
- Autenticazione e autorizzazione
- Validazione richieste
- Serializzazione/deserializzazione dati
- Gestione errori

**Middleware**:
- CORS Middleware: Gestione cross-origin requests
- Authentication Middleware: Verifica JWT tokens
- Rate Limiting: Protezione da abuse
- Logging Middleware: Tracciamento richieste

**Router Principali**:
```python
/api/v1/
├── /markers/          # CRUD segnaposti
├── /labels/           # Gestione etichette
├── /routes/           # Pianificazione itinerari
├── /import/           # Importazione dati
├── /export/           # Esportazione dati
├── /tracks/           # Tracciati GPS
└── /auth/             # Autenticazione
```

### 3. Business Logic Layer (Livello Logica di Business)

#### Marker Service
**Responsabilità**:
- Creazione/modifica/eliminazione markers
- Validazione dati geografici
- Gestione associazioni marker-label
- Ricerca e filtraggio markers

**Funzionalità**:
```python
- create_marker(name, coordinates, description, labels)
- update_marker(id, data)
- delete_marker(id)
- search_markers(filters)
- get_markers_by_label(label_id)
- get_nearby_markers(coordinates, radius)
```

#### Route Planning Service
**Responsabilità**:
- Calcolo itinerari ottimali
- Algoritmi di routing (TSP - Traveling Salesman Problem)
- Calcolo distanze e tempi
- Generazione waypoints

**Algoritmi**:
- Nearest Neighbor per itinerari semplici
- Genetic Algorithm per ottimizzazione multi-punto
- Integrazione con servizi esterni (OSRM, GraphHopper)

#### Import/Export Service
**Responsabilità**:
- Importazione da file (GPX, KML, CSV, JSON)
- Esportazione in vari formati
- Validazione dati importati
- Web scraping luoghi di interesse

**Formati Supportati**:
- **GPX**: Tracciati GPS standard
- **KML**: Google Earth format
- **GeoJSON**: Formato geografico standard
- **CSV**: Dati tabellari con coordinate
- **JSON**: Export completo database

#### Geocoding Service
**Responsabilità**:
- Conversione indirizzi → coordinate (geocoding)
- Conversione coordinate → indirizzi (reverse geocoding)
- Validazione coordinate
- Cache risultati geocoding

**Provider**:
- Nominatim (OpenStreetMap) - Default
- Google Maps API - Opzionale
- Fallback multipli per affidabilità

### 4. Data Access Layer (Livello Accesso Dati)

#### Repository Pattern
**Responsabilità**:
- Astrazione accesso database
- Query building
- Gestione transazioni
- Caching query frequenti

**Repositories**:

**MarkerRepository**:
```python
- find_all()
- find_by_id(id)
- find_by_coordinates(lat, lon, radius)
- find_by_labels(label_ids)
- save(marker)
- delete(id)
- search(query, filters)
```

**LabelRepository**:
```python
- find_all()
- find_by_id(id)
- find_by_name(name)
- save(label)
- delete(id)
- get_markers_count(label_id)
```

**RouteRepository**:
```python
- find_all()
- find_by_id(id)
- save(route)
- delete(id)
- find_by_user(user_id)
```

**GPSTrackRepository**:
```python
- find_all()
- find_by_id(id)
- save(track)
- delete(id)
- get_statistics(track_id)
```

### 5. Database Layer (Livello Database)

#### MySQL Database
**Responsabilità**:
- Persistenza dati
- Integrità referenziale
- Query spaziali
- Backup e recovery

**Ottimizzazioni**:
- Indici spaziali su colonne POINT/LINESTRING
- Indici su campi di ricerca frequente
- Partitioning per performance (se necessario)
- Connection pooling

## Pattern Architetturali Utilizzati

### 1. Layered Architecture
Separazione netta tra livelli con dipendenze unidirezionali (top-down).

### 2. Repository Pattern
Astrazione dell'accesso ai dati per facilitare testing e manutenzione.

### 3. Service Layer Pattern
Logica di business centralizzata in servizi dedicati.

### 4. Dependency Injection
Gestione dipendenze tramite container DI per maggiore testabilità.

### 5. DTO (Data Transfer Objects)
Uso di Pydantic models per trasferimento dati tra livelli.

## Flusso di una Richiesta Tipica

### Esempio: Creazione Nuovo Marker

```
1. User Input (GUI)
   └─> Utente compila form nuovo marker

2. GUI Layer
   └─> Valida input localmente
   └─> Prepara richiesta API

3. API Request
   └─> POST /api/v1/markers
   └─> Body: {name, lat, lon, description, labels}

4. API Layer (FastAPI)
   └─> Valida JWT token
   └─> Valida schema richiesta (Pydantic)
   └─> Chiama MarkerService.create_marker()

5. Business Logic Layer
   └─> MarkerService:
       ├─> Valida coordinate (Geocoding Service)
       ├─> Verifica labels esistenti (Label Service)
       ├─> Crea oggetto Marker
       └─> Chiama MarkerRepository.save()

6. Data Access Layer
   └─> MarkerRepository:
       ├─> Converte DTO → Model SQLAlchemy
       ├─> Esegue INSERT query
       └─> Gestisce transazione

7. Database Layer
   └─> MySQL:
       ├─> Esegue INSERT
       ├─> Aggiorna indici spaziali
       └─> Ritorna ID generato

8. Response Path (bottom-up)
   └─> Repository → Service → API → GUI
   └─> GUI aggiorna lista markers
   └─> Mappa aggiorna con nuovo marker
```

## Gestione Errori

### Strategia Multi-Livello

**Presentation Layer**:
- Mostra messaggi user-friendly
- Logging errori non critici

**API Layer**:
- HTTP status codes appropriati
- Error responses strutturati
- Logging completo errori

**Business Logic Layer**:
- Custom exceptions per casi specifici
- Validazioni business rules
- Rollback transazioni in caso errore

**Data Access Layer**:
- Gestione errori database
- Retry logic per errori transitori
- Connection pooling error handling

### Esempio Error Flow

```python
try:
    # Business Logic
    marker = marker_service.create_marker(data)
except ValidationError as e:
    # 400 Bad Request
    return {"error": "Invalid data", "details": e.errors()}
except GeocodingError as e:
    # 422 Unprocessable Entity
    return {"error": "Invalid coordinates", "message": str(e)}
except DatabaseError as e:
    # 500 Internal Server Error
    logger.error(f"Database error: {e}")
    return {"error": "Internal server error"}
```

## Sicurezza

### Authentication & Authorization
- JWT tokens per autenticazione API
- Refresh tokens per sessioni lunghe
- Role-based access control (RBAC)

### Data Protection
- Password hashing (bcrypt/argon2)
- SQL injection prevention (ORM parametrizzato)
- XSS prevention (sanitizzazione input)
- HTTPS obbligatorio in produzione

### Rate Limiting
- Limite richieste per IP
- Limite per utente autenticato
- Protezione endpoint sensibili

## Scalabilità

### Scalabilità Verticale
- Connection pooling database
- Caching query frequenti
- Ottimizzazione query spaziali

### Scalabilità Orizzontale (Futura)
- Load balancer per multiple istanze API
- Database replication (master-slave)
- Redis per session/cache distribuito
- Separazione read/write database

## Testing

### Architettura Testabile

**Unit Tests**:
- Service layer (mock repositories)
- Repository layer (in-memory database)
- Utility functions

**Integration Tests**:
- API endpoints completi
- Database interactions
- Servizi esterni (mock/stub)

**End-to-End Tests**:
- Flussi utente completi
- GUI automation (pytest-qt)
- API workflows

## Deployment Architecture

```
┌──────────────────────────────────────────┐
│           Production Server              │
│  ┌────────────────────────────────────┐ │
│  │      Nginx (Reverse Proxy)         │ │
│  │         Port 80/443                │ │
│  └────────────────────────────────────┘ │
│                  │                       │
│                  ▼                       │
│  ┌────────────────────────────────────┐ │
│  │    Uvicorn (FastAPI)               │ │
│  │         Port 8000                  │ │
│  └────────────────────────────────────┘ │
│                  │                       │
│                  ▼                       │
│  ┌────────────────────────────────────┐ │
│  │      MySQL Server                  │ │
│  │         Port 3306                  │ │
│  └────────────────────────────────────┘ │
└──────────────────────────────────────────┘
```

## Considerazioni Future

### Microservices (Opzionale)
- Separazione servizio import/export pesante
- Servizio geocoding dedicato
- Message queue (RabbitMQ/Kafka) per comunicazione

### Caching Layer
- Redis per cache distribuito
- Cache query geografiche
- Session storage

### CDN
- Static assets (mappa tiles)
- File export generati
