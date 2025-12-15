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

### Opzione 1: MySQL (Raccomandato)

L'applicazione supporta pienamente MySQL con tutte le funzionalità spatial.

**Windows**:
```bash
# Scarica MySQL Installer da: https://dev.mysql.com/downloads/installer/
# Segui il wizard di installazione
```

**macOS**:
```bash
brew install mysql
brew services start mysql
mysql_secure_installation
```

**Linux (Ubuntu/Debian)**:
```bash
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
```

Il wizard dell'applicazione ti guiderà nella creazione del database al primo avvio.

### Opzione 2: SQLite (Fallback)

Puoi usare SQLite se non hai MySQL installato, ma con funzionalità limitate:
- ⚠️ Supporto limitato per query spaziali avanzate
- ⚠️ Performance ridotte su grandi dataset

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
- SQLAlchemy 2.0.25 + GeoAlchemy2
- MySQL 8.0+ / SQLite

**GUI**:
- CustomTkinter 5.2.1 (cross-platform framework)
- tkinterweb 3.24.8 (HTML rendering)
- Folium 0.15.1 (interactive maps)

**Geospatial**:
- GeoPandas, Shapely, Fiona
- GeoPy (geocoding)

**Build**:
- PyInstaller 6.3.0

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
pip install -e .

# Setup database
cp .env.example .env
# Edit .env with your MySQL credentials

# Run application
python pymypersonalmap/gui/app.py
```

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
├── pymypersonalmap/
│   ├── gui/                 # GUI Desktop (CustomTkinter)
│   │   ├── components/      # Componenti UI
│   │   ├── layouts/         # Layout principali
│   │   ├── themes/          # Temi e stili
│   │   ├── app.py          # Entry point
│   │   ├── backend_manager.py
│   │   ├── setup_wizard.py
│   │   └── config_manager.py
│   ├── models/             # SQLAlchemy models
│   ├── services/           # Business logic
│   ├── database/           # Database session
│   ├── config/             # Configuration
│   └── main.py            # FastAPI app
├── scripts/               # Build scripts
├── build_config.spec      # PyInstaller config
├── pyproject.toml         # Package config
└── README.md
```

---

## 🗺️ Roadmap

### ✅ Fase 1 - MVP Desktop (Completato)
- [x] GUI desktop con CustomTkinter
- [x] Mappa interattiva con Folium
- [x] Sistema di markers e labels
- [x] Setup wizard database
- [x] Build system cross-platform

### 🚧 Fase 2 - Funzionalità Core (In Corso)
- [ ] Implementazione completa CRUD markers via GUI
- [ ] Integrazione geocoding (ricerca indirizzi)
- [ ] Sistema di ricerca e filtri
- [ ] Statistiche e dashboard

### 📅 Fase 3 - Advanced Features
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
