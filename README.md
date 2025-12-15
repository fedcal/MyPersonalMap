# My Personal Map 🗺️

**Applicazione desktop cross-platform per gestire e organizzare i tuoi luoghi preferiti**

My Personal Map è un'applicazione desktop standalone che ti permette di catalogare, organizzare e visualizzare i luoghi significativi della tua vita su una mappa interattiva.

---

## 🌟 Caratteristiche Principali

### 📍 Gestione Markers
- Aggiungi luoghi con coordinate geografiche precise
- Etichettatura multipla per organizzare i tuoi luoghi
- Descrizioni personalizzate e note dettagliate
- Sistema di preferiti per accesso rapido

### 🗺️ Mappa Interattiva
- Visualizzazione su mappa Leaflet/OpenStreetMap
- Zoom, pan, e navigazione fluida
- Markers colorati per categorie diverse
- Popup informativi al click

### 🏷️ Categorie e Label
Categorie predefinite:
- 🏚️ Urbex
- 🍝 Ristoranti
- 🍕 Pizzerie
- 📸 Fotografia
- 🚁 Drone
- ➕ Label personalizzate

### 🛣️ Pianificazione Itinerari (Coming Soon)
- Organizza percorsi tra i tuoi luoghi
- Ottimizzazione tragitti
- Export in formato GPX

### 📥📤 Import/Export (Coming Soon)
- Importa da GPX, KML, GeoJSON, CSV
- Esporta i tuoi dati
- Backup completo del database

---

## 💻 Download e Installazione

### Requisiti di Sistema

**Tutti i Sistemi**:
- MySQL 8.0+ (raccomandato) o SQLite (funzionalità limitate)

**Windows**:
- Windows 10 o superiore
- 4GB RAM minimo

**macOS**:
- macOS 11 (Big Sur) o superiore
- 4GB RAM minimo

**Linux**:
- Ubuntu 20.04+ / Fedora 35+ / Debian 11+ o equivalenti
- 4GB RAM minimo

### Installazione

#### Windows
1. Scarica `MyPersonalMap-Windows-x64.zip` dalla pagina Releases
2. Estrai lo ZIP in una cartella a tua scelta
3. Esegui `MyPersonalMap.exe`
4. Segui il wizard di setup del database al primo avvio

#### macOS
1. Scarica `MyPersonalMap-macOS.dmg` dalla pagina Releases
2. Apri il DMG e trascina l'app nella cartella Applications
3. Al primo avvio: `System Settings → Privacy & Security → Open Anyway`
4. Segui il wizard di setup del database

#### Linux
1. Scarica `MyPersonalMap-Linux-x86_64.AppImage`
2. Rendi eseguibile: `chmod +x MyPersonalMap-*.AppImage`
3. Esegui: `./MyPersonalMap-*.AppImage`
4. Segui il wizard di setup del database

---

## 🗄️ Setup Database

### SQLite Embedded (Predefinito) ✅

L'applicazione usa **SQLite** come database embedded - **nessuna installazione richiesta!**

✅ **Zero configurazione**: Funziona subito
✅ **File unico**: Tutto in `~/.mypersonalmap/mypersonalmap.db`
✅ **Portabile**: Perfetto per desktop
✅ **Calcoli geografici**: Formula Haversine pura Python

Il database viene creato automaticamente al primo avvio.

### MySQL (Opzionale - Solo per Sviluppo)

Se preferisci MySQL durante lo sviluppo:

**Docker**:
```bash
docker run -d \
  --name mysql-db-root \
  -e MYSQL_ROOT_PASSWORD=password \
  -p 3306:3306 \
  mysql:8.0

# Configura .env con DATABASE_TYPE=mysql
```

**Nota**: La versione distribuita userà sempre SQLite embedded.

---

## 🚀 Uso dell'Applicazione

### Primo Avvio
1. Avvia l'applicazione
2. Il wizard di setup ti guiderà nella configurazione del database
3. Inserisci le credenziali MySQL o scegli SQLite
4. L'applicazione creerà automaticamente le tabelle necessarie

### Aggiungere un Marker
1. Clicca su "Nuovo Marker" nella sidebar
2. Inserisci nome e coordinate (o cerca un indirizzo)
3. Aggiungi descrizione e labels
4. Salva - il marker apparirà sulla mappa

### Navigazione
- **Sidebar**: Menu di navigazione e azioni rapide
- **Top Bar**: Ricerca e filtri
- **Mappa**: Visualizzazione principale dei tuoi luoghi

---

## 🛠️ Sviluppo

### Tech Stack

**Backend**:
- FastAPI 0.109.0 (embedded in background thread)
- SQLAlchemy 2.0.25
- SQLite 3 (embedded, zero-config)

**GUI**:
- CustomTkinter 5.2.1 (cross-platform framework)
- tkinterweb 3.24.8 (HTML rendering)
- Folium 0.15.1 (interactive maps)

**Geographic**:
- Pure Python Haversine (distanze)
- GeoPy (geocoding - optional)

**Build**:
- PyInstaller 6.3.0

**Testing**:
- pytest 7.4.4 + pytest-cov
- 47 test suite con 100% model coverage

### Setup Ambiente di Sviluppo

```bash
# Clone repository
git clone https://github.com/yourusername/mypersonalmap.git
cd mypersonalmap

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r pymypersonalmap/requirements.txt

# Setup database (Docker - opzionale ma consigliato)
docker run -d --name mysql-db-root \
  -e MYSQL_ROOT_PASSWORD=password \
  -p 3306:3306 mysql:8.0

# Crea database
docker exec mysql-db-root mysql -u root -ppassword -e \
  "CREATE DATABASE mypersonalmap; \
   CREATE USER 'mypersonalmap_user'@'%' IDENTIFIED BY 'mypersonalmap_pass'; \
   GRANT ALL PRIVILEGES ON mypersonalmap.* TO 'mypersonalmap_user'@'%'; \
   FLUSH PRIVILEGES;"

# Setup configuration
cp .env.example .env
# Edit .env se necessario (le credenziali di default funzionano con Docker)

# Run application (GUI + Backend)
PYTHONPATH=$(pwd) python3 pymypersonalmap/main.py

# Oppure solo backend (per sviluppo API)
PYTHONPATH=$(pwd) python3 pymypersonalmap/main.py --backend-only

# Oppure con uvicorn direttamente
cd pymypersonalmap && python main.py
```

**Note**:
- Il comando `PYTHONPATH=$(pwd)` è necessario quando si esegue da fuori la directory `pymypersonalmap`
- L'applicazione avvia automaticamente FastAPI in background thread quando si usa la GUI
- Il database e le tabelle vengono creati automaticamente al primo avvio
- Le system labels vengono inizializzate automaticamente

### Build da Sorgenti

**Windows**:
```bash
scripts\build_windows.bat
```

**macOS**:
```bash
./scripts/build_macos.sh
```

**Linux**:
```bash
./scripts/build_linux.sh
```

Gli eseguibili saranno disponibili nella directory `dist/`.

---

## 📂 Struttura Progetto

```
myPersonalMap/
├── docs/                    # 📚 Documentazione completa
│   ├── development/         # Docs per sviluppatori
│   ├── guides/              # Guide utente e tutorial
│   └── planning/            # Roadmap e pianificazione
├── scripts/                 # 🔧 Script di build e utility
│   ├── build/               # Script build (Linux, macOS, Windows)
│   └── utils/               # Tool di sviluppo
├── pymypersonalmap/         # 🎯 Pacchetto principale
│   ├── api/                 # REST API (FastAPI)
│   ├── config/              # Configurazione
│   ├── database/            # Gestione database
│   ├── gui/                 # GUI Desktop (CustomTkinter)
│   │   ├── components/      # Componenti UI riutilizzabili
│   │   ├── layouts/         # Layout principali
│   │   └── themes/          # Temi e stili
│   ├── models/              # SQLAlchemy ORM models
│   ├── repository/          # Data access layer
│   ├── services/            # Business logic
│   ├── tests/               # Test suite
│   │   ├── unit/            # Test unitari
│   │   └── integration/     # Test integrazione
│   ├── utils/               # Utility functions
│   └── main.py              # Entry point applicazione
├── build_config.spec        # Configurazione PyInstaller
├── pyproject.toml           # Configurazione progetto Python
├── STRUCTURE.md             # 📋 Documentazione struttura dettagliata
└── README.md                # Questo file
```

**Per la documentazione completa della struttura**, vedi [STRUCTURE.md](STRUCTURE.md)

---

## 🗺️ Roadmap

### ✅ Fase 1 - Backend & Database (Completato)
- [x] FastAPI REST API con SQLAlchemy
- [x] MySQL database con spatial types
- [x] Sistema di markers e labels
- [x] Database migrations con Alembic
- [x] Auto-inizializzazione database e system labels

### ✅ Fase 2 - Desktop GUI (Completato)
- [x] GUI desktop con CustomTkinter
- [x] Mappa interattiva con Folium
- [x] Backend manager (FastAPI in thread)
- [x] Setup wizard database
- [x] Splash screen durante startup
- [x] Error handling e logging
- [x] Integrated startup (GUI + Backend)

### 🚧 Fase 3 - Funzionalità Core (In Corso)
- [ ] Implementazione completa CRUD markers via GUI
- [ ] Integrazione geocoding (ricerca indirizzi)
- [ ] Sistema di ricerca e filtri
- [ ] Statistiche e dashboard

### 📅 Fase 4 - Advanced Features
- [ ] Import/Export (GPX, KML, GeoJSON, CSV)
- [ ] Pianificazione itinerari (TSP algorithm)
- [ ] Tracciati GPS
- [ ] Web scraping integration

### 🔮 Fase 4 - Polish
- [ ] Tema chiaro/scuro
- [ ] Backup automatico
- [ ] Auto-update system
- [ ] Sharing functionality

---

## 📄 Licenza

MIT License - Vedi file LICENSE per dettagli

---

## 🤝 Contribuire

Contributi sono benvenuti! Apri un issue o una pull request.

1. Fork del progetto
2. Crea il tuo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit delle modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

---

## 📞 Supporto

- **Issues**: [GitHub Issues](https://github.com/yourusername/mypersonalmap/issues)
- **Documentazione**: Vedi `/doc` directory

---

**Made with ❤️ using Python, CustomTkinter, and FastAPI**
