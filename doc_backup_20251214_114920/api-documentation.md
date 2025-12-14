# API REST Documentation - My Personal Map

## Panoramica

L'API REST di My Personal Map è costruita con FastAPI e fornisce endpoint per gestire markers, labels, routes, tracciati GPS e operazioni di import/export.

**Base URL**: `http://localhost:8000/api/v1`

**Formato Risposta**: JSON

**Autenticazione**: JWT Bearer Token

---

## Autenticazione

### POST /auth/register
Registra un nuovo utente.

**Request Body**:
```json
{
  "username": "string (3-50 chars, required)",
  "email": "string (valid email, required)",
  "password": "string (min 8 chars, required)",
  "full_name": "string (optional)"
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "username": "mario_rossi",
  "email": "mario@example.com",
  "full_name": "Mario Rossi",
  "created_at": "2025-12-13T10:30:00Z"
}
```

**Error Responses**:
- `400 Bad Request`: Dati non validi
- `409 Conflict`: Username o email già esistente

---

### POST /auth/login
Effettua login e ottiene JWT token.

**Request Body**:
```json
{
  "username": "mario_rossi",
  "password": "securepassword123"
}
```

**Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

**Error Responses**:
- `401 Unauthorized`: Credenziali errate
- `403 Forbidden`: Account disabilitato

---

### POST /auth/refresh
Rinnova access token usando refresh token.

**Request Body**:
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

---

### POST /auth/logout
Invalida il token corrente.

**Headers**:
```
Authorization: Bearer {access_token}
```

**Response** (200 OK):
```json
{
  "message": "Logout successful"
}
```

---

## Markers

### GET /markers
Recupera lista markers dell'utente con filtri opzionali.

**Headers**:
```
Authorization: Bearer {access_token}
```

**Query Parameters**:
- `label_ids` (array[int], optional): Filtra per label IDs
- `search` (string, optional): Ricerca full-text in nome/descrizione
- `lat` (float, optional): Latitudine centro ricerca
- `lon` (float, optional): Longitudine centro ricerca
- `radius_km` (float, optional): Raggio ricerca in km (richiede lat/lon)
- `is_favorite` (boolean, optional): Solo preferiti
- `limit` (int, default=100): Numero massimo risultati
- `offset` (int, default=0): Offset per paginazione

**Example Request**:
```
GET /api/v1/markers?label_ids=1,3&radius_km=10&lat=41.9&lon=12.5&limit=50
```

**Response** (200 OK):
```json
{
  "total": 150,
  "limit": 50,
  "offset": 0,
  "markers": [
    {
      "id": 1,
      "name": "Colosseo",
      "coordinates": {
        "latitude": 41.8902,
        "longitude": 12.4922
      },
      "description": "Anfiteatro Flavio",
      "address": "Piazza del Colosseo, Roma",
      "labels": [
        {
          "id": 1,
          "name": "Fotografia",
          "color": "#4444ff",
          "icon": "camera"
        }
      ],
      "is_favorite": true,
      "visit_count": 5,
      "metadata": {
        "opening_hours": "09:00-19:00",
        "website": "https://colosseo.it"
      },
      "created_at": "2025-01-15T14:30:00Z",
      "updated_at": "2025-02-20T10:15:00Z"
    }
  ]
}
```

---

### GET /markers/{marker_id}
Recupera dettagli singolo marker.

**Headers**:
```
Authorization: Bearer {access_token}
```

**Response** (200 OK):
```json
{
  "id": 1,
  "name": "Colosseo",
  "coordinates": {
    "latitude": 41.8902,
    "longitude": 12.4922
  },
  "description": "Anfiteatro Flavio, simbolo di Roma antica",
  "address": "Piazza del Colosseo, 1, 00184 Roma RM",
  "labels": [
    {"id": 1, "name": "Fotografia", "color": "#4444ff", "icon": "camera"},
    {"id": 7, "name": "Museo", "color": "#9932cc", "icon": "landmark"}
  ],
  "is_favorite": true,
  "visit_count": 5,
  "metadata": {
    "opening_hours": "09:00-19:00",
    "ticket_price": "16 EUR",
    "website": "https://colosseo.it",
    "phone": "+39 06 3996 7700"
  },
  "created_at": "2025-01-15T14:30:00Z",
  "updated_at": "2025-02-20T10:15:00Z"
}
```

**Error Responses**:
- `404 Not Found`: Marker non esistente o non accessibile

---

### POST /markers
Crea nuovo marker.

**Headers**:
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body**:
```json
{
  "name": "Fontana di Trevi",
  "coordinates": {
    "latitude": 41.9009,
    "longitude": 12.4833
  },
  "description": "Fontana monumentale barocca",
  "address": "Piazza di Trevi, Roma (optional se coordinates fornite)",
  "label_ids": [1, 3],
  "is_favorite": false,
  "metadata": {
    "custom_field": "custom_value"
  }
}
```

**Alternative Request** (geocoding da indirizzo):
```json
{
  "name": "Fontana di Trevi",
  "address": "Piazza di Trevi, Roma",
  "label_ids": [1, 3]
}
```

**Response** (201 Created):
```json
{
  "id": 42,
  "name": "Fontana di Trevi",
  "coordinates": {
    "latitude": 41.9009,
    "longitude": 12.4833
  },
  "address": "Piazza di Trevi, 00187 Roma RM",
  "labels": [
    {"id": 1, "name": "Fotografia"},
    {"id": 3, "name": "Urbex"}
  ],
  "is_favorite": false,
  "created_at": "2025-12-13T15:45:00Z"
}
```

**Error Responses**:
- `400 Bad Request`: Dati non validi
- `422 Unprocessable Entity`: Geocoding fallito

---

### PUT /markers/{marker_id}
Aggiorna marker esistente.

**Headers**:
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body** (tutti campi opzionali):
```json
{
  "name": "Colosseo - Anfiteatro Flavio",
  "description": "Descrizione aggiornata",
  "coordinates": {
    "latitude": 41.8903,
    "longitude": 12.4923
  },
  "label_ids": [1, 7],
  "is_favorite": true,
  "metadata": {
    "visited_date": "2025-03-15"
  }
}
```

**Response** (200 OK):
```json
{
  "id": 1,
  "name": "Colosseo - Anfiteatro Flavio",
  "updated_at": "2025-12-13T16:00:00Z",
  ...
}
```

**Error Responses**:
- `404 Not Found`: Marker non trovato
- `403 Forbidden`: Non autorizzato a modificare

---

### DELETE /markers/{marker_id}
Elimina marker.

**Headers**:
```
Authorization: Bearer {access_token}
```

**Response** (204 No Content)

**Error Responses**:
- `404 Not Found`: Marker non trovato
- `403 Forbidden`: Non autorizzato a eliminare

---

### POST /markers/batch
Crea multipli markers in batch.

**Request Body**:
```json
{
  "markers": [
    {
      "name": "Marker 1",
      "coordinates": {"latitude": 41.9, "longitude": 12.5},
      "label_ids": [1]
    },
    {
      "name": "Marker 2",
      "coordinates": {"latitude": 41.91, "longitude": 12.51},
      "label_ids": [2]
    }
  ]
}
```

**Response** (201 Created):
```json
{
  "created": 2,
  "failed": 0,
  "markers": [
    {"id": 43, "name": "Marker 1"},
    {"id": 44, "name": "Marker 2"}
  ]
}
```

---

## Labels

### GET /labels
Recupera tutte le labels (sistema + custom utente).

**Headers**:
```
Authorization: Bearer {access_token}
```

**Response** (200 OK):
```json
{
  "labels": [
    {
      "id": 1,
      "name": "Urbex",
      "color": "#8b4513",
      "icon": "building",
      "description": "Luoghi abbandonati da esplorare",
      "is_system": true,
      "marker_count": 15,
      "created_at": "2025-01-01T00:00:00Z"
    },
    {
      "id": 10,
      "name": "My Custom Label",
      "color": "#ff00ff",
      "icon": "star",
      "description": "Mia categoria personalizzata",
      "is_system": false,
      "marker_count": 3,
      "created_at": "2025-03-10T12:00:00Z"
    }
  ]
}
```

---

### GET /labels/{label_id}
Dettagli singola label.

**Response** (200 OK):
```json
{
  "id": 1,
  "name": "Urbex",
  "color": "#8b4513",
  "icon": "building",
  "description": "Luoghi abbandonati da esplorare",
  "is_system": true,
  "marker_count": 15,
  "created_at": "2025-01-01T00:00:00Z"
}
```

---

### POST /labels
Crea nuova label personalizzata.

**Request Body**:
```json
{
  "name": "Gelaterias",
  "color": "#ff69b4",
  "icon": "ice-cream",
  "description": "Le migliori gelaterie"
}
```

**Response** (201 Created):
```json
{
  "id": 15,
  "name": "Gelaterias",
  "color": "#ff69b4",
  "icon": "ice-cream",
  "description": "Le migliori gelaterie",
  "is_system": false,
  "marker_count": 0,
  "created_at": "2025-12-13T17:00:00Z"
}
```

**Error Responses**:
- `400 Bad Request`: Nome già esistente
- `422 Unprocessable Entity`: Colore non valido

---

### PUT /labels/{label_id}
Aggiorna label personalizzata.

**Request Body**:
```json
{
  "color": "#ff1493",
  "icon": "ice-cream-cone",
  "description": "Descrizione aggiornata"
}
```

**Response** (200 OK)

**Error Responses**:
- `403 Forbidden`: Non puoi modificare labels di sistema

---

### DELETE /labels/{label_id}
Elimina label personalizzata.

**Query Parameters**:
- `reassign_to` (int, optional): ID label a cui reassegnare i markers

**Response** (204 No Content)

**Error Responses**:
- `403 Forbidden`: Non puoi eliminare labels di sistema
- `409 Conflict`: Label in uso (fornire reassign_to)

---

## Routes (Itinerari)

### GET /routes
Lista itinerari utente.

**Response** (200 OK):
```json
{
  "routes": [
    {
      "id": 1,
      "name": "Tour Roma Classica",
      "start_point": {
        "latitude": 41.9028,
        "longitude": 12.4964
      },
      "waypoints": [1, 5, 12, 23],
      "total_distance": 15.3,
      "estimated_duration": 240,
      "optimization_type": "shortest",
      "is_completed": false,
      "created_at": "2025-12-01T09:00:00Z"
    }
  ]
}
```

---

### POST /routes
Crea nuovo itinerario.

**Request Body**:
```json
{
  "name": "Weekend a Roma",
  "start_point": {
    "latitude": 41.9028,
    "longitude": 12.4964
  },
  "marker_ids": [1, 5, 12, 23, 8],
  "optimization_type": "shortest",
  "options": {
    "avoid_highways": false,
    "optimize_order": true
  }
}
```

**Response** (201 Created):
```json
{
  "id": 5,
  "name": "Weekend a Roma",
  "waypoints": [1, 12, 5, 23, 8],
  "optimized_order": true,
  "total_distance": 18.7,
  "estimated_duration": 280,
  "route_geometry": {
    "type": "LineString",
    "coordinates": [[12.4964, 41.9028], [12.4922, 41.8902], ...]
  }
}
```

---

### GET /routes/{route_id}
Dettagli itinerario con geometria completa.

**Response** (200 OK):
```json
{
  "id": 1,
  "name": "Tour Roma Classica",
  "description": "Itinerario principali monumenti",
  "start_point": {
    "latitude": 41.9028,
    "longitude": 12.4964
  },
  "waypoints": [
    {
      "order": 1,
      "marker": {
        "id": 1,
        "name": "Colosseo",
        "coordinates": {"latitude": 41.8902, "longitude": 12.4922}
      },
      "distance_from_previous": 0,
      "estimated_time": 0
    },
    {
      "order": 2,
      "marker": {
        "id": 5,
        "name": "Fontana di Trevi",
        "coordinates": {"latitude": 41.9009, "longitude": 12.4833}
      },
      "distance_from_previous": 2.3,
      "estimated_time": 30
    }
  ],
  "total_distance": 15.3,
  "estimated_duration": 240,
  "route_geometry": {
    "type": "LineString",
    "coordinates": [[12.4964, 41.9028], [12.4922, 41.8902], ...]
  }
}
```

---

### PUT /routes/{route_id}
Aggiorna itinerario.

**Request Body**:
```json
{
  "name": "Nuovo Nome",
  "marker_ids": [1, 5, 12],
  "is_completed": true,
  "completed_at": "2025-12-13T18:00:00Z"
}
```

---

### DELETE /routes/{route_id}
Elimina itinerario.

**Response** (204 No Content)

---

## GPS Tracks

### GET /tracks
Lista tracciati GPS.

**Response** (200 OK):
```json
{
  "tracks": [
    {
      "id": 1,
      "name": "Escursione Monte Bianco",
      "total_distance": 12.5,
      "total_duration": 14400,
      "avg_speed": 3.1,
      "max_elevation": 4808,
      "min_elevation": 1200,
      "created_at": "2025-08-15T08:00:00Z"
    }
  ]
}
```

---

### POST /tracks
Carica nuovo tracciato GPS.

**Request Body**:
```json
{
  "name": "Trail Running Appia Antica",
  "description": "Corsa sulla via Appia",
  "track_data": {
    "type": "LineString",
    "coordinates": [
      [12.5123, 41.8567, 45.5],
      [12.5125, 41.8570, 46.2],
      ...
    ]
  },
  "marker_id": 10
}
```

**Response** (201 Created):
```json
{
  "id": 5,
  "name": "Trail Running Appia Antica",
  "total_distance": 8.3,
  "total_duration": 3600,
  "avg_speed": 8.3,
  "max_elevation": 78.5,
  "min_elevation": 12.3
}
```

---

### GET /tracks/{track_id}
Dettagli tracciato completo con tutti i punti.

**Response** (200 OK):
```json
{
  "id": 1,
  "name": "Escursione Monte Bianco",
  "description": "Salita al rifugio",
  "track_data": {
    "type": "LineString",
    "coordinates": [[6.8650, 45.8326, 1200], ...]
  },
  "elevation_data": [1200, 1205, 1210, ...],
  "statistics": {
    "total_distance": 12.5,
    "total_duration": 14400,
    "avg_speed": 3.1,
    "max_elevation": 4808,
    "min_elevation": 1200,
    "elevation_gain": 3608,
    "elevation_loss": 0
  },
  "created_at": "2025-08-15T08:00:00Z"
}
```

---

### DELETE /tracks/{track_id}
Elimina tracciato GPS.

**Response** (204 No Content)

---

## Import/Export

### POST /import/gpx
Importa markers da file GPX.

**Request** (multipart/form-data):
```
Content-Type: multipart/form-data

file: [GPX file binary]
label_ids: [1, 3]
import_waypoints: true
import_tracks: true
```

**Response** (200 OK):
```json
{
  "import_id": 15,
  "status": "completed",
  "markers_imported": 23,
  "markers_duplicates": 2,
  "markers_errors": 0,
  "tracks_imported": 1,
  "summary": {
    "total_waypoints": 25,
    "imported_waypoints": 23,
    "duplicates": 2,
    "errors": []
  }
}
```

---

### POST /import/kml
Importa da file KML.

**Request** (multipart/form-data)

**Response** (200 OK): Simile a GPX import

---

### POST /import/geojson
Importa da GeoJSON.

**Request Body**:
```json
{
  "geojson": {
    "type": "FeatureCollection",
    "features": [
      {
        "type": "Feature",
        "geometry": {
          "type": "Point",
          "coordinates": [12.4964, 41.9028]
        },
        "properties": {
          "name": "Marker Name",
          "description": "Description"
        }
      }
    ]
  },
  "label_ids": [1, 3]
}
```

---

### POST /import/scrape
Web scraping luoghi (advanced).

**Request Body**:
```json
{
  "url": "https://example.com/places",
  "selector_config": {
    "name_selector": ".place-name",
    "address_selector": ".place-address"
  },
  "label_ids": [2],
  "max_results": 50
}
```

**Response** (202 Accepted):
```json
{
  "task_id": "abc123",
  "status": "processing",
  "message": "Scraping in background"
}
```

---

### GET /export/gpx
Esporta markers in formato GPX.

**Query Parameters**:
- `marker_ids` (array, optional): Specifici markers
- `label_ids` (array, optional): Filtra per labels
- `include_tracks` (bool, default=false)

**Response** (200 OK):
```xml
Content-Type: application/gpx+xml
Content-Disposition: attachment; filename="markers_export.gpx"

<?xml version="1.0"?>
<gpx version="1.1" creator="MyPersonalMap">
  <wpt lat="41.8902" lon="12.4922">
    <name>Colosseo</name>
    <desc>Anfiteatro Flavio</desc>
  </wpt>
  ...
</gpx>
```

---

### GET /export/geojson
Esporta in formato GeoJSON.

**Response** (200 OK):
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [12.4922, 41.8902]
      },
      "properties": {
        "id": 1,
        "name": "Colosseo",
        "description": "Anfiteatro Flavio",
        "labels": ["Fotografia", "Museo"]
      }
    }
  ]
}
```

---

### GET /export/csv
Esporta in CSV.

**Response** (200 OK):
```
Content-Type: text/csv
Content-Disposition: attachment; filename="markers_export.csv"

id,name,latitude,longitude,description,labels,created_at
1,Colosseo,41.8902,12.4922,Anfiteatro Flavio,"Fotografia,Museo",2025-01-15T14:30:00Z
```

---

## Statistics

### GET /statistics/user
Statistiche utente.

**Response** (200 OK):
```json
{
  "total_markers": 150,
  "favorite_markers": 23,
  "total_labels": 12,
  "total_routes": 5,
  "total_tracks": 8,
  "markers_by_label": {
    "Urbex": 45,
    "Ristorante": 30,
    "Fotografia": 60
  },
  "activity_timeline": [
    {"date": "2025-12", "markers_created": 15},
    {"date": "2025-11", "markers_created": 22}
  ],
  "total_distance_traveled": 245.8
}
```

---

## Error Handling

### Standard Error Response

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid coordinates provided",
    "details": {
      "field": "coordinates.latitude",
      "issue": "Value must be between -90 and 90"
    },
    "timestamp": "2025-12-13T18:30:00Z",
    "request_id": "req_abc123xyz"
  }
}
```

### Error Codes

| HTTP Status | Error Code | Descrizione |
|-------------|------------|-------------|
| 400 | VALIDATION_ERROR | Dati richiesta non validi |
| 401 | UNAUTHORIZED | Token mancante o invalido |
| 403 | FORBIDDEN | Accesso negato |
| 404 | NOT_FOUND | Risorsa non trovata |
| 409 | CONFLICT | Conflitto (es: duplicato) |
| 422 | UNPROCESSABLE_ENTITY | Dati processabili ma errati |
| 429 | RATE_LIMIT_EXCEEDED | Troppi richieste |
| 500 | INTERNAL_ERROR | Errore server |

---

## Rate Limiting

**Limiti**:
- Anonimi: 100 richieste/ora
- Autenticati: 1000 richieste/ora
- Import/Export: 10 operazioni/ora

**Headers Risposta**:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 950
X-RateLimit-Reset: 1702483200
```

---

## Versioning

L'API usa URL versioning: `/api/v1/...`

Quando una nuova versione viene rilasciata:
- Versione precedente supportata per 6 mesi
- Header `X-API-Version` indica versione usata
- Deprecation warnings tramite header `X-API-Deprecated`

---

## OpenAPI / Swagger

Documentazione interattiva disponibile a:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

---

## SDK / Client Libraries

### Python Client Example

```python
import requests

class MyPersonalMapClient:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token
        self.headers = {"Authorization": f"Bearer {token}"}

    def get_markers(self, **filters):
        response = requests.get(
            f"{self.base_url}/api/v1/markers",
            headers=self.headers,
            params=filters
        )
        return response.json()

    def create_marker(self, data):
        response = requests.post(
            f"{self.base_url}/api/v1/markers",
            headers=self.headers,
            json=data
        )
        return response.json()

# Usage
client = MyPersonalMapClient("http://localhost:8000", "your_token")
markers = client.get_markers(label_ids=[1, 3], limit=10)
```

---

## Webhooks (Future)

Pianificato supporto per webhooks su eventi:
- `marker.created`
- `marker.updated`
- `marker.deleted`
- `route.completed`
- `import.completed`

---

**Documento Versione**: 1.0
**Ultimo Aggiornamento**: Dicembre 2025
**Status**: In Development
