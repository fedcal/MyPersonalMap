# Development Roadmap - My Personal Map

Piano di sviluppo progressivo dalle funzionalità base a quelle avanzate.

## Indice

1. [Panoramica](#panoramica)
2. [Fase 0: Setup Iniziale](#fase-0-setup-iniziale)
3. [Fase 1: Database e Modelli Base](#fase-1-database-e-modelli-base)
4. [Fase 2: CRUD Markers Completo](#fase-2-crud-markers-completo)
5. [Fase 3: Sistema Labels](#fase-3-sistema-labels)
6. [Fase 4: Autenticazione](#fase-4-autenticazione)
7. [Fase 5: Servizi Geospaziali](#fase-5-servizi-geospaziali)
8. [Fase 6: Import/Export Base](#fase-6-importexport-base)
9. [Fase 7: GUI Desktop](#fase-7-gui-desktop)
10. [Fase 8: Route Planning](#fase-8-route-planning)
11. [Fase 9: Funzionalità Avanzate](#fase-9-funzionalità-avanzate)
12. [Fase 10: Production Ready](#fase-10-production-ready)

---

## Panoramica

Questo roadmap segue un approccio **incrementale**, dove ogni fase produce un'applicazione funzionante e testabile. Ogni fase costruisce sulle precedenti, permettendo di avere sempre una versione deployabile.

### Principi Guida

- **Incrementalità**: Ogni fase aggiunge valore utilizzabile
- **Testabilità**: Ogni funzionalità è accompagnata da test
- **Documentazione**: API docs aggiornate ad ogni fase
- **Deploy continuo**: Possibilità di deploy dopo ogni fase

### Durata Stimata per Fase

- Fase 0: 30 minuti (setup)
- Fase 1-3: 2-3 giorni ciascuna (fondamenta)
- Fase 4-6: 1-2 giorni ciascuna (funzionalità core)
- Fase 7-8: 3-5 giorni ciascuna (features complesse)
- Fase 9-10: ongoing (miglioramenti continui)

---

## Fase 0: Setup Iniziale

**Obiettivo**: Ambiente di sviluppo funzionante con API skeleton.

### Stato Attuale
- ✅ Struttura progetto creata
- ✅ FastAPI skeleton con endpoints placeholder
- ✅ File .env.example pronto
- ✅ Documentazione base

### Task da Completare

#### 0.1 Verifica Setup Ambiente
```bash
# Verifica Python
python3 --version  # Deve essere 3.9+

# Verifica MySQL
mysql --version    # Deve essere 8.0+

# Verifica virtual environment
source venv/bin/activate
pip list | grep fastapi  # Deve mostrare FastAPI
```

#### 0.2 Test Server Base
```bash
cd pymypersonalmap
python main.py
```

Verifica che funzioni:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/health (Health check)

#### 0.3 Setup Git Hooks (Opzionale)
```bash
# Pre-commit hook per formattazione
pip install pre-commit
pre-commit install
```

### Deliverables Fase 0
- [x] Server FastAPI avviabile
- [x] Swagger docs accessibile
- [x] Virtual environment configurato
- [ ] Database MySQL creato e accessibile

### Test di Accettazione
```bash
curl http://localhost:8000/health
# Deve ritornare: {"status": "healthy", "version": "1.0.0", ...}
```

---

## Fase 1: Database e Modelli Base

**Obiettivo**: Database funzionante con tabelle principali e ORM SQLAlchemy.

### Prerequisiti
- Fase 0 completata
- MySQL server running
- Database `mypersonalmap` creato

### 1.1 Setup SQLAlchemy Base

**File**: `pymypersonalmap/database/base.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.settings import settings

# Database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,
    pool_pre_ping=True,
    pool_recycle=3600
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class per models
Base = declarative_base()

# Dependency per FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 1.2 Crea Model Marker

**File**: `pymypersonalmap/models/marker.py`

```python
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
from database.base import Base

class Marker(Base):
    __tablename__ = "markers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    address = Column(String(500), nullable=True)

    # Spatial data
    coordinates = Column(Geometry('POINT', srid=4326), nullable=False)

    # Metadata
    is_favorite = Column(Boolean, default=False, index=True)
    visit_count = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships (da aggiungere in Fase 3)
    # labels = relationship("Label", secondary="marker_labels", back_populates="markers")
```

### 1.3 Setup Alembic Migrations

```bash
# Inizializza Alembic
alembic init alembic

# Configura alembic/env.py per importare Base e models
# Modifica alembic.ini con DATABASE_URL
```

**File**: `alembic/env.py` (modifica)

```python
# Importa Base e models
from database.base import Base
from models import marker  # Import esplicito per autogenerate

target_metadata = Base.metadata
```

### 1.4 Crea e Applica Prima Migration

```bash
# Genera migration
alembic revision --autogenerate -m "Create markers table"

# Verifica migration generata in alembic/versions/

# Applica migration
alembic upgrade head

# Verifica in MySQL
mysql -u mypersonalmap_user -p
> USE mypersonalmap;
> SHOW TABLES;  # Deve mostrare 'markers' e 'alembic_version'
> DESCRIBE markers;
```

### 1.5 Test Database Connection

**File**: `pymypersonalmap/tests/test_database.py`

```python
import pytest
from sqlalchemy import create_engine, text
from database.base import SessionLocal, get_db

def test_database_connection():
    """Test connessione database"""
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT 1"))
        assert result.scalar() == 1
    finally:
        db.close()

def test_markers_table_exists():
    """Verifica esistenza tabella markers"""
    db = SessionLocal()
    try:
        result = db.execute(text("SHOW TABLES LIKE 'markers'"))
        assert result.scalar() is not None
    finally:
        db.close()
```

Run test:
```bash
pytest tests/test_database.py -v
```

### Deliverables Fase 1
- [ ] SQLAlchemy Base configurato
- [ ] Model Marker creato
- [ ] Alembic migrations funzionanti
- [ ] Tabella markers in database
- [ ] Test database passano

### Test di Accettazione
```sql
-- MySQL: Verifica spatial index
SHOW INDEX FROM markers WHERE Column_name = 'coordinates';

-- Test insert manuale
INSERT INTO markers (name, coordinates)
VALUES ('Test Marker', ST_GeomFromText('POINT(12.4922 41.8902)', 4326));

SELECT id, name, ST_AsText(coordinates) FROM markers;
```

---

## Fase 2: CRUD Markers Completo

**Obiettivo**: API funzionanti per creare, leggere, aggiornare, eliminare markers.

### Prerequisiti
- Fase 1 completata
- Tabella markers in database

### 2.1 Crea Pydantic Schemas

**File**: `pymypersonalmap/api/schemas/marker.py`

```python
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class CoordinatesSchema(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

class MarkerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    address: Optional[str] = None
    coordinates: CoordinatesSchema
    is_favorite: bool = False

class MarkerCreate(MarkerBase):
    pass

class MarkerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    address: Optional[str] = None
    coordinates: Optional[CoordinatesSchema] = None
    is_favorite: Optional[bool] = None

class MarkerResponse(MarkerBase):
    id: int
    visit_count: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
```

### 2.2 Crea Repository Pattern

**File**: `pymypersonalmap/repositories/marker_repository.py`

```python
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from geoalchemy2.functions import ST_GeomFromText, ST_AsText
from models.marker import Marker

class MarkerRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str, lat: float, lon: float,
               description: str = None, address: str = None,
               is_favorite: bool = False) -> Marker:
        """Crea nuovo marker"""
        point_wkt = f'POINT({lon} {lat})'
        marker = Marker(
            name=name,
            description=description,
            address=address,
            coordinates=ST_GeomFromText(point_wkt, 4326),
            is_favorite=is_favorite
        )
        self.db.add(marker)
        self.db.commit()
        self.db.refresh(marker)
        return marker

    def get_by_id(self, marker_id: int) -> Optional[Marker]:
        """Recupera marker per ID"""
        return self.db.query(Marker).filter(Marker.id == marker_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Marker]:
        """Recupera tutti i markers con paginazione"""
        return self.db.query(Marker).offset(skip).limit(limit).all()

    def update(self, marker_id: int, **kwargs) -> Optional[Marker]:
        """Aggiorna marker"""
        marker = self.get_by_id(marker_id)
        if not marker:
            return None

        # Aggiorna coordinate se fornite
        if 'latitude' in kwargs and 'longitude' in kwargs:
            point_wkt = f"POINT({kwargs['longitude']} {kwargs['latitude']})"
            marker.coordinates = ST_GeomFromText(point_wkt, 4326)
            kwargs.pop('latitude')
            kwargs.pop('longitude')

        # Aggiorna altri campi
        for key, value in kwargs.items():
            if hasattr(marker, key) and value is not None:
                setattr(marker, key, value)

        self.db.commit()
        self.db.refresh(marker)
        return marker

    def delete(self, marker_id: int) -> bool:
        """Elimina marker"""
        marker = self.get_by_id(marker_id)
        if not marker:
            return False
        self.db.delete(marker)
        self.db.commit()
        return True

    def search(self, query: str) -> List[Marker]:
        """Cerca markers per nome o descrizione"""
        search_term = f"%{query}%"
        return self.db.query(Marker).filter(
            (Marker.name.like(search_term)) |
            (Marker.description.like(search_term))
        ).all()
```

### 2.3 Aggiorna Endpoints FastAPI

**File**: `pymypersonalmap/api/routes/markers.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database.base import get_db
from api.schemas.marker import MarkerCreate, MarkerUpdate, MarkerResponse
from repositories.marker_repository import MarkerRepository

router = APIRouter(prefix="/api/v1/markers", tags=["Markers"])

@router.post("/", response_model=MarkerResponse, status_code=status.HTTP_201_CREATED)
def create_marker(marker: MarkerCreate, db: Session = Depends(get_db)):
    """Crea nuovo marker"""
    repo = MarkerRepository(db)
    new_marker = repo.create(
        name=marker.name,
        lat=marker.coordinates.latitude,
        lon=marker.coordinates.longitude,
        description=marker.description,
        address=marker.address,
        is_favorite=marker.is_favorite
    )
    return new_marker

@router.get("/", response_model=List[MarkerResponse])
def get_markers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Recupera lista markers"""
    repo = MarkerRepository(db)
    markers = repo.get_all(skip=skip, limit=limit)
    return markers

@router.get("/{marker_id}", response_model=MarkerResponse)
def get_marker(marker_id: int, db: Session = Depends(get_db)):
    """Recupera singolo marker"""
    repo = MarkerRepository(db)
    marker = repo.get_by_id(marker_id)
    if not marker:
        raise HTTPException(status_code=404, detail="Marker not found")
    return marker

@router.put("/{marker_id}", response_model=MarkerResponse)
def update_marker(marker_id: int, marker: MarkerUpdate, db: Session = Depends(get_db)):
    """Aggiorna marker"""
    repo = MarkerRepository(db)
    update_data = marker.dict(exclude_unset=True)

    # Estrai coordinate se presenti
    if 'coordinates' in update_data:
        update_data['latitude'] = update_data['coordinates']['latitude']
        update_data['longitude'] = update_data['coordinates']['longitude']
        del update_data['coordinates']

    updated_marker = repo.update(marker_id, **update_data)
    if not updated_marker:
        raise HTTPException(status_code=404, detail="Marker not found")
    return updated_marker

@router.delete("/{marker_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_marker(marker_id: int, db: Session = Depends(get_db)):
    """Elimina marker"""
    repo = MarkerRepository(db)
    if not repo.delete(marker_id):
        raise HTTPException(status_code=404, detail="Marker not found")
    return None
```

### 2.4 Registra Router in main.py

**File**: `pymypersonalmap/main.py` (modifica)

```python
from api.routes import markers

# Registra router
app.include_router(markers.router)
```

### 2.5 Test Integration

**File**: `pymypersonalmap/tests/test_markers_api.py`

```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_marker():
    """Test creazione marker"""
    response = client.post("/api/v1/markers/", json={
        "name": "Colosseo",
        "coordinates": {"latitude": 41.8902, "longitude": 12.4922},
        "description": "Anfiteatro Flavio",
        "is_favorite": True
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Colosseo"
    assert data["id"] is not None

def test_get_markers():
    """Test recupero markers"""
    response = client.get("/api/v1/markers/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_marker_by_id():
    """Test recupero marker singolo"""
    # Crea marker
    create_response = client.post("/api/v1/markers/", json={
        "name": "Test Marker",
        "coordinates": {"latitude": 45.0, "longitude": 9.0}
    })
    marker_id = create_response.json()["id"]

    # Recupera marker
    response = client.get(f"/api/v1/markers/{marker_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Marker"

def test_update_marker():
    """Test aggiornamento marker"""
    # Crea marker
    create_response = client.post("/api/v1/markers/", json={
        "name": "Original Name",
        "coordinates": {"latitude": 45.0, "longitude": 9.0}
    })
    marker_id = create_response.json()["id"]

    # Aggiorna marker
    response = client.put(f"/api/v1/markers/{marker_id}", json={
        "name": "Updated Name"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"

def test_delete_marker():
    """Test eliminazione marker"""
    # Crea marker
    create_response = client.post("/api/v1/markers/", json={
        "name": "To Delete",
        "coordinates": {"latitude": 45.0, "longitude": 9.0}
    })
    marker_id = create_response.json()["id"]

    # Elimina marker
    response = client.delete(f"/api/v1/markers/{marker_id}")
    assert response.status_code == 204

    # Verifica eliminazione
    response = client.get(f"/api/v1/markers/{marker_id}")
    assert response.status_code == 404
```

Run tests:
```bash
pytest tests/test_markers_api.py -v
```

### Deliverables Fase 2
- [ ] Pydantic schemas per validazione
- [ ] Repository pattern implementato
- [ ] CRUD endpoints funzionanti
- [ ] Test integration completi
- [ ] Swagger docs aggiornata

### Test di Accettazione
```bash
# Test manuale completo
# 1. Crea marker
curl -X POST "http://localhost:8000/api/v1/markers/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Fontana di Trevi",
    "coordinates": {"latitude": 41.9009, "longitude": 12.4833},
    "description": "Famosa fontana barocca"
  }'

# 2. Lista markers
curl http://localhost:8000/api/v1/markers/

# 3. Aggiorna marker (usa ID dalla creazione)
curl -X PUT "http://localhost:8000/api/v1/markers/1" \
  -H "Content-Type: application/json" \
  -d '{"is_favorite": true}'

# 4. Elimina marker
curl -X DELETE "http://localhost:8000/api/v1/markers/1"
```

---

## Fase 3: Sistema Labels

**Obiettivo**: Gestione etichette (system + custom) e associazione marker-labels.

### 3.1 Crea Model Label

**File**: `pymypersonalmap/models/label.py`

```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.base import Base

# Tabella associativa many-to-many
marker_labels = Table(
    'marker_labels',
    Base.metadata,
    Column('marker_id', Integer, ForeignKey('markers.id', ondelete='CASCADE'), primary_key=True),
    Column('label_id', Integer, ForeignKey('labels.id', ondelete='CASCADE'), primary_key=True),
    Column('assigned_at', DateTime(timezone=True), server_default=func.now())
)

class Label(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    color = Column(String(7), nullable=False)  # Hex color #RRGGBB
    icon = Column(String(50), nullable=False)
    is_system = Column(Boolean, default=False, index=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    markers = relationship("Marker", secondary=marker_labels, back_populates="labels")
```

**Aggiorna** `pymypersonalmap/models/marker.py`:

```python
# Aggiungi relationship a Marker model
from sqlalchemy.orm import relationship

class Marker(Base):
    # ... campi esistenti ...

    # Relationship
    labels = relationship("Label", secondary="marker_labels", back_populates="markers")
```

### 3.2 Migration Labels

```bash
alembic revision --autogenerate -m "Add labels and marker_labels tables"
alembic upgrade head
```

### 3.3 Seed System Labels

**File**: `pymypersonalmap/scripts/seed_system_labels.py`

```python
from database.base import SessionLocal
from models.label import Label

def seed_system_labels():
    """Popola database con labels di sistema"""
    db = SessionLocal()

    system_labels = [
        {"name": "Urbex", "color": "#8b4513", "icon": "building", "is_system": True},
        {"name": "Ristorante", "color": "#ff4444", "icon": "utensils", "is_system": True},
        {"name": "Pizzeria", "color": "#ff8c00", "icon": "pizza-slice", "is_system": True},
        {"name": "Fotografia", "color": "#4444ff", "icon": "camera", "is_system": True},
        {"name": "Drone", "color": "#00ccff", "icon": "helicopter", "is_system": True},
        {"name": "Natura", "color": "#44ff44", "icon": "tree", "is_system": True},
        {"name": "Museo", "color": "#9932cc", "icon": "landmark", "is_system": True},
        {"name": "Panorama", "color": "#ff69b4", "icon": "mountain", "is_system": True},
    ]

    for label_data in system_labels:
        # Verifica se esiste già
        existing = db.query(Label).filter(Label.name == label_data["name"]).first()
        if not existing:
            label = Label(**label_data)
            db.add(label)

    db.commit()
    print(f"Seeded {len(system_labels)} system labels")
    db.close()

if __name__ == "__main__":
    seed_system_labels()
```

Run seed:
```bash
python scripts/seed_system_labels.py
```

### 3.4 Crea API Labels

**File**: `pymypersonalmap/api/routes/labels.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.base import get_db
from models.label import Label
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/labels", tags=["Labels"])

class LabelCreate(BaseModel):
    name: str
    color: str
    icon: str

class LabelResponse(BaseModel):
    id: int
    name: str
    color: str
    icon: str
    is_system: bool

    class Config:
        from_attributes = True

@router.get("/", response_model=List[LabelResponse])
def get_labels(db: Session = Depends(get_db)):
    """Recupera tutte le labels"""
    return db.query(Label).all()

@router.post("/", response_model=LabelResponse, status_code=201)
def create_label(label: LabelCreate, db: Session = Depends(get_db)):
    """Crea label custom"""
    # Verifica unicità nome
    existing = db.query(Label).filter(Label.name == label.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Label name already exists")

    new_label = Label(**label.dict(), is_system=False)
    db.add(new_label)
    db.commit()
    db.refresh(new_label)
    return new_label
```

Registra in main.py:
```python
from api.routes import labels
app.include_router(labels.router)
```

### 3.5 Aggiorna Marker Endpoints per Labels

Modifica `MarkerCreate` e `MarkerResponse` schemas per includere labels:

```python
# In api/schemas/marker.py
class MarkerCreate(MarkerBase):
    label_ids: List[int] = []

class MarkerResponse(MarkerBase):
    id: int
    labels: List[str]  # Lista nomi labels
    # ... altri campi ...
```

Aggiorna repository per gestire labels.

### Deliverables Fase 3
- [ ] Model Label creato
- [ ] Tabella associativa marker_labels
- [ ] System labels seeded
- [ ] API labels CRUD
- [ ] Markers possono avere labels
- [ ] Test completi

---

## Fase 4: Autenticazione

**Obiettivo**: Sistema JWT per autenticazione API.

### 4.1 Crea Model User

**File**: `pymypersonalmap/models/user.py`

```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from database.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
```

Migration:
```bash
alembic revision --autogenerate -m "Add users table"
alembic upgrade head
```

### 4.2 Implementa Password Hashing

**File**: `pymypersonalmap/utils/security.py`

```python
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from config.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash password"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica password"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Crea JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
```

### 4.3 Crea Auth Endpoints

**File**: `pymypersonalmap/api/routes/auth.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database.base import get_db
from models.user import User
from utils.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/register", status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Registrazione nuovo utente"""
    # Verifica username esistente
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")

    # Verifica email esistente
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Crea utente
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}

@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login e generazione JWT token"""
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
```

### 4.4 Proteggi Endpoints

Crea dependency per verificare token:

**File**: `pymypersonalmap/api/dependencies.py`

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from config.settings import settings
from database.base import get_db
from models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Recupera utente corrente da JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user
```

Usa in endpoints:
```python
@router.post("/api/v1/markers/")
def create_marker(marker: MarkerCreate,
                  current_user: User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    # ... implementazione ...
```

### Deliverables Fase 4
- [ ] User model e tabella
- [ ] Password hashing con bcrypt
- [ ] JWT token generation
- [ ] Registration endpoint
- [ ] Login endpoint
- [ ] Protected endpoints
- [ ] Test autenticazione

---

## Fase 5: Servizi Geospaziali

**Obiettivo**: Geocoding, reverse geocoding, ricerca per prossimità.

### 5.1 Implementa Geocoding Service

**File**: `pymypersonalmap/services/geocoding_service.py`

```python
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from typing import Optional, Tuple
import time

class GeocodingService:
    def __init__(self, user_agent: str = "MyPersonalMap/1.0"):
        self.geocoder = Nominatim(user_agent=user_agent)
        self.last_request_time = 0
        self.rate_limit_seconds = 1  # Nominatim richiede 1 sec tra richieste

    def _respect_rate_limit(self):
        """Rispetta rate limit di Nominatim"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit_seconds:
            time.sleep(self.rate_limit_seconds - elapsed)
        self.last_request_time = time.time()

    def geocode(self, address: str) -> Optional[Tuple[float, float]]:
        """Converte indirizzo in coordinate (lat, lon)"""
        try:
            self._respect_rate_limit()
            location = self.geocoder.geocode(address)
            if location:
                return (location.latitude, location.longitude)
            return None
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            print(f"Geocoding error: {e}")
            return None

    def reverse_geocode(self, latitude: float, longitude: float) -> Optional[str]:
        """Converte coordinate in indirizzo"""
        try:
            self._respect_rate_limit()
            location = self.geocoder.reverse(f"{latitude}, {longitude}")
            if location:
                return location.address
            return None
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            print(f"Reverse geocoding error: {e}")
            return None

    def validate_coordinates(self, latitude: float, longitude: float) -> bool:
        """Valida coordinate geografiche"""
        return -90 <= latitude <= 90 and -180 <= longitude <= 180
```

### 5.2 Aggiungi Endpoint Geocoding

**File**: `pymypersonalmap/api/routes/geocoding.py`

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.geocoding_service import GeocodingService

router = APIRouter(prefix="/api/v1/geocoding", tags=["Geocoding"])
geocoding_service = GeocodingService()

class GeocodeRequest(BaseModel):
    address: str

class GeocodeResponse(BaseModel):
    latitude: float
    longitude: float
    address: str

@router.post("/geocode", response_model=GeocodeResponse)
def geocode_address(request: GeocodeRequest):
    """Converti indirizzo in coordinate"""
    coords = geocoding_service.geocode(request.address)
    if not coords:
        raise HTTPException(status_code=404, detail="Address not found")
    return {
        "latitude": coords[0],
        "longitude": coords[1],
        "address": request.address
    }

@router.get("/reverse")
def reverse_geocode(latitude: float, longitude: float):
    """Converti coordinate in indirizzo"""
    if not geocoding_service.validate_coordinates(latitude, longitude):
        raise HTTPException(status_code=400, detail="Invalid coordinates")

    address = geocoding_service.reverse_geocode(latitude, longitude)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    return {"address": address, "latitude": latitude, "longitude": longitude}
```

### 5.3 Ricerca per Prossimità

Aggiungi metodo al MarkerRepository:

```python
def find_nearby(self, latitude: float, longitude: float, radius_km: float = 5.0):
    """Trova markers entro radius_km da coordinate"""
    from geoalchemy2.functions import ST_Distance_Sphere, ST_GeomFromText

    point_wkt = f'POINT({longitude} {latitude})'
    point = ST_GeomFromText(point_wkt, 4326)

    return self.db.query(Marker).filter(
        ST_Distance_Sphere(Marker.coordinates, point) <= radius_km * 1000
    ).all()
```

Aggiungi endpoint:
```python
@router.get("/api/v1/markers/nearby")
def get_nearby_markers(
    latitude: float,
    longitude: float,
    radius_km: float = 5.0,
    db: Session = Depends(get_db)
):
    """Trova markers vicini a coordinate"""
    repo = MarkerRepository(db)
    markers = repo.find_nearby(latitude, longitude, radius_km)
    return markers
```

### Deliverables Fase 5
- [ ] GeocodingService implementato
- [ ] Geocode endpoint
- [ ] Reverse geocode endpoint
- [ ] Ricerca per prossimità
- [ ] Rate limiting Nominatim
- [ ] Validazione coordinate

---

## Fase 6: Import/Export Base

**Obiettivo**: Importare ed esportare markers da/verso file GPX, KML, GeoJSON, CSV.

### 6.1 Implementa Import Service

**File**: `pymypersonalmap/services/import_export_service.py`

```python
import gpxpy
import json
import csv
from typing import List, Dict
from io import StringIO
import geopandas as gpd
from shapely.geometry import Point

class ImportExportService:

    def import_from_gpx(self, gpx_content: str) -> List[Dict]:
        """Importa waypoints da file GPX"""
        gpx = gpxpy.parse(gpx_content)
        markers = []

        for waypoint in gpx.waypoints:
            markers.append({
                "name": waypoint.name or "Unnamed",
                "latitude": waypoint.latitude,
                "longitude": waypoint.longitude,
                "description": waypoint.description or waypoint.comment,
            })

        return markers

    def import_from_geojson(self, geojson_content: str) -> List[Dict]:
        """Importa da GeoJSON"""
        data = json.loads(geojson_content)
        markers = []

        for feature in data.get("features", []):
            geom = feature["geometry"]
            props = feature.get("properties", {})

            if geom["type"] == "Point":
                lon, lat = geom["coordinates"]
                markers.append({
                    "name": props.get("name", "Unnamed"),
                    "latitude": lat,
                    "longitude": lon,
                    "description": props.get("description"),
                })

        return markers

    def import_from_csv(self, csv_content: str) -> List[Dict]:
        """Importa da CSV (formato: name,latitude,longitude,description)"""
        reader = csv.DictReader(StringIO(csv_content))
        markers = []

        for row in reader:
            markers.append({
                "name": row.get("name", "Unnamed"),
                "latitude": float(row["latitude"]),
                "longitude": float(row["longitude"]),
                "description": row.get("description"),
            })

        return markers

    def export_to_gpx(self, markers: List[Dict]) -> str:
        """Esporta markers in formato GPX"""
        gpx = gpxpy.gpx.GPX()

        for marker in markers:
            waypoint = gpxpy.gpx.GPXWaypoint(
                latitude=marker["latitude"],
                longitude=marker["longitude"],
                name=marker["name"],
                description=marker.get("description")
            )
            gpx.waypoints.append(waypoint)

        return gpx.to_xml()

    def export_to_geojson(self, markers: List[Dict]) -> str:
        """Esporta markers in GeoJSON"""
        features = []

        for marker in markers:
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [marker["longitude"], marker["latitude"]]
                },
                "properties": {
                    "name": marker["name"],
                    "description": marker.get("description"),
                }
            }
            features.append(feature)

        geojson = {
            "type": "FeatureCollection",
            "features": features
        }

        return json.dumps(geojson, indent=2)

    def export_to_csv(self, markers: List[Dict]) -> str:
        """Esporta markers in CSV"""
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=["name", "latitude", "longitude", "description"])
        writer.writeheader()
        writer.writerows(markers)
        return output.getvalue()
```

### 6.2 Crea Import/Export Endpoints

**File**: `pymypersonalmap/api/routes/import_export.py`

```python
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
from database.base import get_db
from services.import_export_service import ImportExportService
from repositories.marker_repository import MarkerRepository

router = APIRouter(prefix="/api/v1", tags=["Import/Export"])
import_export_service = ImportExportService()

@router.post("/import/gpx")
async def import_gpx(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Importa markers da file GPX"""
    if not file.filename.endswith('.gpx'):
        raise HTTPException(status_code=400, detail="File must be .gpx")

    content = await file.read()
    markers_data = import_export_service.import_from_gpx(content.decode('utf-8'))

    # Salva in database
    repo = MarkerRepository(db)
    created = []
    for marker in markers_data:
        new_marker = repo.create(**marker)
        created.append(new_marker.id)

    return {"imported": len(created), "marker_ids": created}

@router.post("/import/geojson")
async def import_geojson(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Importa markers da GeoJSON"""
    if not file.filename.endswith('.geojson') and not file.filename.endswith('.json'):
        raise HTTPException(status_code=400, detail="File must be .geojson or .json")

    content = await file.read()
    markers_data = import_export_service.import_from_geojson(content.decode('utf-8'))

    repo = MarkerRepository(db)
    created = []
    for marker in markers_data:
        new_marker = repo.create(**marker)
        created.append(new_marker.id)

    return {"imported": len(created), "marker_ids": created}

@router.get("/export/gpx")
def export_gpx(db: Session = Depends(get_db)):
    """Esporta tutti i markers in GPX"""
    repo = MarkerRepository(db)
    markers = repo.get_all(limit=10000)

    markers_data = [
        {
            "name": m.name,
            "latitude": m.coordinates.latitude,
            "longitude": m.coordinates.longitude,
            "description": m.description
        }
        for m in markers
    ]

    gpx_content = import_export_service.export_to_gpx(markers_data)

    return Response(
        content=gpx_content,
        media_type="application/gpx+xml",
        headers={"Content-Disposition": "attachment; filename=markers.gpx"}
    )
```

### Deliverables Fase 6
- [ ] ImportExportService implementato
- [ ] Import da GPX, GeoJSON, CSV
- [ ] Export verso GPX, GeoJSON, CSV
- [ ] File upload endpoints
- [ ] Download endpoints
- [ ] Validazione formati

---

## Fase 7: GUI Desktop

**Obiettivo**: Interfaccia desktop con CustomTkinter e visualizzazione mappa.

### 7.1 Struttura GUI Base

**File**: `pymypersonalmap/gui/main_window.py`

```python
import customtkinter as ctk
import requests
from typing import List, Dict

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("My Personal Map")
        self.geometry("1200x800")

        # API base URL
        self.api_url = "http://localhost:8000/api/v1"

        # Setup UI
        self.setup_ui()
        self.load_markers()

    def setup_ui(self):
        """Configura interfaccia utente"""
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=300)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)

        # Title
        title = ctk.CTkLabel(self.sidebar, text="My Personal Map",
                             font=("Arial", 24, "bold"))
        title.pack(pady=20)

        # Buttons
        self.btn_add = ctk.CTkButton(self.sidebar, text="Aggiungi Marker",
                                     command=self.add_marker_dialog)
        self.btn_add.pack(pady=10, padx=20, fill="x")

        self.btn_refresh = ctk.CTkButton(self.sidebar, text="Aggiorna",
                                         command=self.load_markers)
        self.btn_refresh.pack(pady=10, padx=20, fill="x")

        # Markers list
        list_label = ctk.CTkLabel(self.sidebar, text="Markers:",
                                  font=("Arial", 16, "bold"))
        list_label.pack(pady=(20, 10))

        self.markers_listbox = ctk.CTkTextbox(self.sidebar, width=260, height=500)
        self.markers_listbox.pack(padx=20, pady=10)

        # Main content (mappa placeholder)
        self.content = ctk.CTkFrame(self)
        self.content.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        map_label = ctk.CTkLabel(self.content, text="Mappa (da implementare con Folium)",
                                 font=("Arial", 20))
        map_label.pack(expand=True)

    def load_markers(self):
        """Carica markers dall'API"""
        try:
            response = requests.get(f"{self.api_url}/markers")
            if response.status_code == 200:
                markers = response.json()
                self.display_markers(markers)
            else:
                self.show_error("Errore caricamento markers")
        except Exception as e:
            self.show_error(f"Errore: {str(e)}")

    def display_markers(self, markers: List[Dict]):
        """Visualizza markers nella lista"""
        self.markers_listbox.delete("1.0", "end")
        for marker in markers:
            text = f"{marker['name']} - {marker['coordinates']['latitude']:.4f}, {marker['coordinates']['longitude']:.4f}\n"
            self.markers_listbox.insert("end", text)

    def add_marker_dialog(self):
        """Dialog per aggiungere nuovo marker"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Aggiungi Marker")
        dialog.geometry("400x300")

        # Form fields
        ctk.CTkLabel(dialog, text="Nome:").pack(pady=5)
        name_entry = ctk.CTkEntry(dialog, width=300)
        name_entry.pack(pady=5)

        ctk.CTkLabel(dialog, text="Latitudine:").pack(pady=5)
        lat_entry = ctk.CTkEntry(dialog, width=300)
        lat_entry.pack(pady=5)

        ctk.CTkLabel(dialog, text="Longitudine:").pack(pady=5)
        lon_entry = ctk.CTkEntry(dialog, width=300)
        lon_entry.pack(pady=5)

        def save():
            try:
                data = {
                    "name": name_entry.get(),
                    "coordinates": {
                        "latitude": float(lat_entry.get()),
                        "longitude": float(lon_entry.get())
                    }
                }
                response = requests.post(f"{self.api_url}/markers", json=data)
                if response.status_code == 201:
                    dialog.destroy()
                    self.load_markers()
                else:
                    self.show_error("Errore creazione marker")
            except Exception as e:
                self.show_error(str(e))

        btn_save = ctk.CTkButton(dialog, text="Salva", command=save)
        btn_save.pack(pady=20)

    def show_error(self, message: str):
        """Mostra errore"""
        error_dialog = ctk.CTkToplevel(self)
        error_dialog.title("Errore")
        error_dialog.geometry("300x100")
        ctk.CTkLabel(error_dialog, text=message).pack(pady=20)
        ctk.CTkButton(error_dialog, text="OK",
                     command=error_dialog.destroy).pack()

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = MainWindow()
    app.mainloop()
```

### 7.2 Integrazione Mappa Folium

**File**: `pymypersonalmap/gui/map_viewer.py`

```python
import folium
from folium.plugins import MarkerCluster
import webbrowser
import os

class MapViewer:
    def __init__(self):
        self.map = None

    def create_map(self, markers: list, center=None):
        """Crea mappa con markers"""
        if not center and markers:
            # Centro sulla media delle coordinate
            avg_lat = sum(m['coordinates']['latitude'] for m in markers) / len(markers)
            avg_lon = sum(m['coordinates']['longitude'] for m in markers) / len(markers)
            center = [avg_lat, avg_lon]
        elif not center:
            center = [41.9028, 12.4964]  # Roma default

        self.map = folium.Map(location=center, zoom_start=10)

        # Aggiungi marker cluster
        marker_cluster = MarkerCluster().add_to(self.map)

        for marker in markers:
            folium.Marker(
                location=[marker['coordinates']['latitude'],
                         marker['coordinates']['longitude']],
                popup=marker['name'],
                tooltip=marker['name']
            ).add_to(marker_cluster)

        return self.map

    def save_and_open(self, filename="map.html"):
        """Salva mappa e apri in browser"""
        if self.map:
            self.map.save(filename)
            webbrowser.open('file://' + os.path.realpath(filename))
```

### Deliverables Fase 7
- [ ] MainWindow CustomTkinter
- [ ] Lista markers funzionante
- [ ] Dialog aggiungi marker
- [ ] Integrazione API
- [ ] Map viewer con Folium
- [ ] Visualizzazione markers su mappa

---

## Fase 8: Route Planning

**Obiettivo**: Calcolo itinerari ottimali tra markers.

### 8.1 Implementa Route Service

**File**: `pymypersonalmap/services/route_service.py`

```python
from typing import List, Dict
import math

class RouteService:

    def calculate_distance(self, lat1: float, lon1: float,
                          lat2: float, lon2: float) -> float:
        """Calcola distanza Haversine tra due punti in km"""
        R = 6371  # Raggio Terra in km

        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))

        return R * c

    def nearest_neighbor_route(self, markers: List[Dict],
                               start_index: int = 0) -> List[Dict]:
        """Algoritmo Nearest Neighbor per TSP approssimato"""
        if not markers:
            return []

        unvisited = markers.copy()
        route = [unvisited.pop(start_index)]

        while unvisited:
            current = route[-1]
            nearest = min(
                unvisited,
                key=lambda m: self.calculate_distance(
                    current['coordinates']['latitude'],
                    current['coordinates']['longitude'],
                    m['coordinates']['latitude'],
                    m['coordinates']['longitude']
                )
            )
            route.append(nearest)
            unvisited.remove(nearest)

        return route

    def calculate_route_stats(self, route: List[Dict]) -> Dict:
        """Calcola statistiche percorso"""
        total_distance = 0

        for i in range(len(route) - 1):
            dist = self.calculate_distance(
                route[i]['coordinates']['latitude'],
                route[i]['coordinates']['longitude'],
                route[i+1]['coordinates']['latitude'],
                route[i+1]['coordinates']['longitude']
            )
            total_distance += dist

        return {
            "total_distance_km": round(total_distance, 2),
            "waypoints_count": len(route),
            "avg_distance_km": round(total_distance / (len(route) - 1), 2) if len(route) > 1 else 0
        }
```

### 8.2 Crea Route Endpoints

**File**: `pymypersonalmap/api/routes/routes.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from database.base import get_db
from services.route_service import RouteService
from repositories.marker_repository import MarkerRepository

router = APIRouter(prefix="/api/v1/routes", tags=["Routes"])
route_service = RouteService()

class RouteRequest(BaseModel):
    marker_ids: List[int]

class RouteResponse(BaseModel):
    waypoints: List[dict]
    stats: dict

@router.post("/optimize", response_model=RouteResponse)
def optimize_route(request: RouteRequest, db: Session = Depends(get_db)):
    """Ottimizza percorso tra markers"""
    repo = MarkerRepository(db)

    # Recupera markers
    markers = []
    for marker_id in request.marker_ids:
        marker = repo.get_by_id(marker_id)
        if not marker:
            raise HTTPException(status_code=404, detail=f"Marker {marker_id} not found")
        markers.append({
            "id": marker.id,
            "name": marker.name,
            "coordinates": {
                "latitude": marker.coordinates.latitude,
                "longitude": marker.coordinates.longitude
            }
        })

    # Ottimizza route
    optimized = route_service.nearest_neighbor_route(markers)
    stats = route_service.calculate_route_stats(optimized)

    return {
        "waypoints": optimized,
        "stats": stats
    }
```

### Deliverables Fase 8
- [ ] RouteService con algoritmo TSP
- [ ] Calcolo distanze Haversine
- [ ] Endpoint ottimizzazione route
- [ ] Statistiche percorso
- [ ] Visualizzazione route su mappa

---

## Fase 9: Funzionalità Avanzate

**Obiettivo**: Features aggiuntive per produzione.

### 9.1 Statistics Dashboard

- Endpoint statistiche: markers count, labels distribution, favorite count
- Heatmap markers per area geografica
- Timeline creazione markers

### 9.2 Web Scraping (Opzionale)

- Scraping POI da fonti pubbliche
- Import automatico luoghi di interesse
- Validazione e deduplicazione

### 9.3 Sharing & Collaboration

- Condivisione markers tramite link
- Export markers selezionati
- Gruppi di markers (collections)

### 9.4 Search & Filters Avanzati

- Full-text search su name/description
- Filtri multipli combinati
- Salvataggio ricerche preferite

---

## Fase 10: Production Ready

**Obiettivo**: Preparare applicazione per deployment produzione.

### 10.1 Performance Optimization

- Database indexes ottimizzati
- Query optimization
- Caching con Redis (opzionale)
- Connection pooling tuning

### 10.2 Security Hardening

- Rate limiting per endpoint
- Input sanitization
- SQL injection prevention audit
- HTTPS enforcement
- Security headers

### 10.3 Monitoring & Logging

- Structured logging
- Error tracking (Sentry)
- Performance monitoring
- Health checks avanzati

### 10.4 Documentation

- API documentation completa
- User guide dettagliata
- Deployment guide
- Troubleshooting guide

### 10.5 Testing Coverage

- Unit tests > 80%
- Integration tests completi
- E2E tests GUI
- Performance tests

### 10.6 CI/CD Pipeline

- GitHub Actions workflow
- Automated testing
- Docker build
- Automated deployment

---

## Checklist Completa per Deploy

### Pre-Production Checklist

- [ ] Tutti i test passano
- [ ] Code coverage > 80%
- [ ] Security audit completato
- [ ] Performance testing eseguito
- [ ] Documentation aggiornata
- [ ] Backup strategy definita
- [ ] Monitoring setup
- [ ] Error tracking configurato

### Production Deployment

- [ ] Environment variables configurate
- [ ] Database migrations applicate
- [ ] SSL certificates installati
- [ ] Reverse proxy configurato (Nginx)
- [ ] Systemd service o Docker container
- [ ] Log rotation configurato
- [ ] Backup automatici schedulati
- [ ] Health checks funzionanti

---

## Risorse e Tool Raccomandati

### Development Tools
- **IDE**: VS Code con Python extension
- **API Testing**: Postman o Insomnia
- **Database**: MySQL Workbench, DBeaver
- **Git**: GitKraken o CLI

### Testing Tools
- **Unit Tests**: pytest
- **API Tests**: httpx, TestClient
- **Coverage**: pytest-cov
- **Load Testing**: Locust

### Production Tools
- **Containerization**: Docker, Docker Compose
- **Process Manager**: Systemd, Supervisor
- **Reverse Proxy**: Nginx, Caddy
- **Monitoring**: Prometheus, Grafana
- **Logging**: ELK Stack, Loki

---

## Conclusioni

Questo roadmap fornisce un percorso chiaro e incrementale per sviluppare My Personal Map dalle fondamenta fino a un'applicazione production-ready.

**Principi chiave**:
1. Ogni fase è deployabile e utilizzabile
2. Testing continuo ad ogni fase
3. Documentazione aggiornata progressivamente
4. Refactoring quando necessario

**Prossimi Passi**:
1. Inizia con Fase 0 e Fase 1
2. Completa ogni fase prima di passare alla successiva
3. Testa approfonditamente ogni funzionalità
4. Documenta eventuali deviazioni dal piano

Per supporto e domande, consulta la documentazione completa in `doc/`.
