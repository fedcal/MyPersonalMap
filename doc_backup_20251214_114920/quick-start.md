# Quick Start Guide - My Personal Map

Guida rapida per avviare My Personal Map in meno di 10 minuti.

## Prerequisiti

- Python 3.9+ (raccomandato 3.11+)
- MySQL 8.0+
- Git

## Installazione Rapida

### 1. Clona il Repository

```bash
git clone https://github.com/tuousername/myPersonalMap.git
cd myPersonalMap
```

### 2. Setup Database MySQL

```bash
# Accedi a MySQL
mysql -u root -p

# Esegui questi comandi SQL
CREATE DATABASE mypersonalmap CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'mypersonalmap_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON mypersonalmap.* TO 'mypersonalmap_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3. Configura Ambiente Python

```bash
# Crea virtual environment
python3 -m venv venv

# Attiva virtual environment
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Installa dipendenze
cd pymypersonalmap
pip install -r requirements.txt
```

### 4. Configura File .env

```bash
# Copia il template
cp .env.example .env

# Genera secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Modifica .env con i tuoi dati
```

Configurazione minima `.env`:

```env
# Database
DATABASE_URL=mysql+pymysql://mypersonalmap_user:your_password@localhost:3306/mypersonalmap

# Security (usa la key generata sopra)
SECRET_KEY=tua-secret-key-generata-di-almeno-32-caratteri

# Application
DEBUG=true
ENVIRONMENT=development
```

### 5. Inizializza Database (Quando Disponibile)

```bash
# NOTA: Al momento il database va creato manualmente
# Le migration Alembic saranno disponibili nelle prossime fasi

# Quando disponibili, usa:
# alembic upgrade head
```

### 6. Avvia l'Applicazione

```bash
# Assicurati di essere nella directory pymypersonalmap
cd pymypersonalmap

# Avvia il server FastAPI
python main.py

# Oppure con uvicorn direttamente
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Output atteso:
```
==================================================
My Personal Map API Starting...
Version: 1.0.0
Environment: development
Debug Mode: true
==================================================
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## Verifica Installazione

### Test API

Apri il browser e visita:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

Dovresti vedere la documentazione interattiva dell'API.

### Test con curl

```bash
# Health check
curl http://localhost:8000/health

# Risposta attesa:
# {
#   "status": "healthy",
#   "version": "1.0.0",
#   "message": "My Personal Map API is running"
# }
```

## Stato Attuale del Progetto

L'applicazione è attualmente in fase MVP iniziale:

- ✅ **Completato**: Struttura FastAPI base, endpoints placeholder
- ⏳ **In Sviluppo**: Database models, SQLAlchemy integration
- 📋 **Pianificato**: Service layer, GUI, Import/Export

Vedi [development-roadmap.md](development-roadmap.md) per il piano completo di sviluppo.

## Prossimi Passi

1. Segui il [Development Roadmap](development-roadmap.md) per implementare le funzionalità
2. Consulta [setup-guide.md](setup-guide.md) per dettagli avanzati
3. Leggi [architecture.md](architecture.md) per comprendere l'architettura

## Troubleshooting Rapido

### Errore: Port 8000 already in use

```bash
# Linux/macOS
lsof -i :8000
kill -9 <PID>

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Oppure usa porta diversa
uvicorn main:app --reload --port 8001
```

### Errore: MySQL Connection Failed

```bash
# Verifica MySQL attivo
sudo systemctl status mysql  # Linux
brew services list           # macOS

# Test connessione
mysql -u mypersonalmap_user -p -h localhost

# Verifica .env DATABASE_URL
cat .env | grep DATABASE_URL
```

### Errore: ModuleNotFoundError

```bash
# Verifica virtual environment attivo
which python  # Dovrebbe puntare a venv/bin/python

# Reinstalla requirements
pip install -r requirements.txt --upgrade
```

### Errore: Import GDAL/Fiona

**Linux**:
```bash
sudo apt install gdal-bin libgdal-dev
pip install GDAL==$(gdal-config --version)
```

**macOS**:
```bash
brew install gdal
pip install --upgrade --force-reinstall fiona
```

**Windows**:
```bash
pip install pipwin
pipwin install gdal
pipwin install fiona
```

## Supporto

Per problemi più complessi, consulta:
- [setup-guide.md](setup-guide.md) - Guida completa con troubleshooting esteso
- [GitHub Issues](https://github.com/tuousername/myPersonalMap/issues)
- Documentazione completa in `doc/`

## Sviluppo

### Eseguire i Test

```bash
# Quando disponibili
pytest
pytest --cov=pymypersonalmap
```

### Formattazione Codice

```bash
# Formatta con black
black pymypersonalmap/

# Lint con flake8
flake8 pymypersonalmap/
```

### Modalità Debug

L'applicazione è già in modalità debug per default. Per maggiori log:

```bash
LOG_LEVEL=DEBUG python main.py
```

## Note Importanti

1. **Secret Key**: Genera sempre una nuova secret key per produzione
2. **Database**: Cambia la password di default in produzione
3. **CORS**: Aggiorna `CORS_ORIGINS` in .env per ambienti specifici
4. **Geocoding**: Nominatim richiede 1 sec tra richieste (rispetta rate limit)

## Comandi Rapidi di Riferimento

```bash
# Attiva virtual environment
source venv/bin/activate

# Avvia server sviluppo
cd pymypersonalmap && python main.py

# Avvia con hot reload
uvicorn main:app --reload

# Run tests
pytest

# Format code
black pymypersonalmap/

# Genera migration (quando disponibile)
alembic revision --autogenerate -m "description"

# Applica migration
alembic upgrade head
```
