# User Guide - My Personal Map

## Benvenuto in My Personal Map

My Personal Map è la tua mappa personale per organizzare, catalogare e pianificare visite ai luoghi che ami. Questa guida ti mostrerà come utilizzare tutte le funzionalità dell'applicazione.

---

## Indice

1. [Primo Avvio](#primo-avvio)
2. [Interfaccia Principale](#interfaccia-principale)
3. [Gestione Segnaposti](#gestione-segnaposti)
4. [Organizzazione con Etichette](#organizzazione-con-etichette)
5. [Ricerca e Filtri](#ricerca-e-filtri)
6. [Pianificazione Itinerari](#pianificazione-itinerari)
7. [Importazione Dati](#importazione-dati)
8. [Esportazione Dati](#esportazione-dati)
9. [Tracciati GPS](#tracciati-gps)
10. [Statistiche e Analisi](#statistiche-e-analisi)
11. [Impostazioni](#impostazioni)
12. [Tips & Tricks](#tips--tricks)

---

## Primo Avvio

### Registrazione Account

1. Avvia l'applicazione My Personal Map
2. Clicca su **"Registrati"**
3. Compila il form:
   - **Username**: Scegli un nome utente univoco (3-50 caratteri)
   - **Email**: Inserisci un indirizzo email valido
   - **Password**: Minimo 8 caratteri, meglio se con numeri e simboli
   - **Nome completo** (opzionale): Il tuo nome e cognome
4. Clicca **"Conferma Registrazione"**
5. Controlla la tua email per il link di conferma (se attivo)
6. Clicca sul link per attivare l'account

### Login

1. Dalla schermata principale, inserisci:
   - **Username** o **Email**
   - **Password**
2. (Opzionale) Spunta **"Ricordami"** per rimanere connesso
3. Clicca **"Accedi"**

---

## Interfaccia Principale

### Layout Applicazione

```
┌────────────────────────────────────────────────────────────┐
│  My Personal Map                    [○] [□] [×]            │
├──────────┬─────────────────────────────────────────────────┤
│          │                                                  │
│  MENU    │           MAPPA INTERATTIVA                     │
│          │                                                  │
│  Home    │    ┌─────────────────────────────┐             │
│  Markers │    │  🗺️  OpenStreetMap         │             │
│  Labels  │    │                             │             │
│  Routes  │    │    📍 Markers visualizzati  │             │
│  Import  │    │                             │             │
│  Export  │    │                             │             │
│  Stats   │    └─────────────────────────────┘             │
│          │                                                  │
│  ⚙️ Settings                                               │
│  👤 Profile                                                │
├──────────┴─────────────────────────────────────────────────┤
│  Status: 150 markers | Ultima sync: 13/12/2025 15:30      │
└────────────────────────────────────────────────────────────┘
```

### Componenti Principali

**1. Menu Laterale (Sidebar)**:
- Navigazione tra sezioni
- Accesso rapido funzionalità
- Info account

**2. Mappa Centrale**:
- Visualizzazione interattiva markers
- Zoom e pan con mouse/touch
- Popup info cliccando markers

**3. Barra Superiore**:
- Ricerca rapida
- Notifiche
- Profilo utente

**4. Status Bar**:
- Statistiche veloci
- Stato sincronizzazione
- Messaggi sistema

---

## Gestione Segnaposti

### Aggiungere un Nuovo Segnaposto

#### Metodo 1: Click sulla Mappa

1. Clicca sul pulsante **"+"** nella toolbar mappa
2. Clicca sulla mappa nel punto desiderato
3. Si apre il form di creazione:
   ```
   ┌─────────────────────────────────┐
   │  Nuovo Segnaposto              │
   ├─────────────────────────────────┤
   │  Nome: [________________]       │
   │  Coordinate:                    │
   │    Lat: 41.8902  Lon: 12.4922  │
   │  Indirizzo: [________________]  │
   │  Descrizione:                   │
   │  [________________________]     │
   │  [________________________]     │
   │  Etichette:                     │
   │  ☑ Fotografia ☐ Ristorante     │
   │  ☐ Urbex      ☐ Drone          │
   │  ⭐ Aggiungi ai Preferiti       │
   │                                 │
   │  [Annulla]  [Salva]            │
   └─────────────────────────────────┘
   ```
4. Compila i campi:
   - **Nome** (obbligatorio): Nome del luogo
   - **Coordinate**: Auto-compilate dal click (modificabili)
   - **Indirizzo**: Inserisci per geocoding automatico
   - **Descrizione**: Note, informazioni utili
   - **Etichette**: Seleziona categorie pertinenti
   - **Preferiti**: Spunta se luogo importante
5. Clicca **"Salva"**

#### Metodo 2: Inserimento da Indirizzo

1. Menu → **"Markers"** → **"Nuovo da Indirizzo"**
2. Inserisci indirizzo completo:
   ```
   Esempio: "Piazza del Colosseo, 1, Roma, Italia"
   ```
3. Clicca **"Trova Posizione"**
4. L'app mostra coordinate trovate su mappa
5. Conferma o aggiusta posizione
6. Completa form e salva

#### Metodo 3: Inserimento Manuale Coordinate

1. Menu → **"Markers"** → **"Nuovo da Coordinate"**
2. Inserisci coordinate:
   - **Latitudine**: -90 a +90 (es: 41.8902)
   - **Longitudine**: -180 a +180 (es: 12.4922)
3. Formato supportati:
   - Decimale: `41.8902, 12.4922`
   - DMS: `41°53'24.72"N 12°29'31.92"E`
4. Completa altri campi e salva

### Modificare un Segnaposto

1. **Sulla Mappa**: Click destro sul marker → **"Modifica"**
2. **Da Lista**: Menu Markers → Seleziona marker → **"✏️ Modifica"**
3. Modifica campi desiderati
4. Clicca **"Salva Modifiche"**

**Campi Modificabili**:
- Nome, descrizione
- Coordinate (con drag&drop marker sulla mappa)
- Etichette
- Stato preferito
- Metadata personalizzati

### Eliminare un Segnaposto

1. Seleziona marker da modificare
2. Clicca **"🗑️ Elimina"**
3. Conferma eliminazione nel popup:
   ```
   ⚠️  Sei sicuro di voler eliminare questo marker?

   Nome: Colosseo
   Questa azione non può essere annullata.

   Verranno anche rimossi da:
   - 2 itinerari salvati

   [ Annulla ]  [ Elimina Definitivamente ]
   ```
4. Clicca **"Elimina Definitivamente"**

### Visualizzare Dettagli

**Click su Marker**: Mostra popup con info base
```
┌──────────────────────┐
│  📍 Colosseo         │
├──────────────────────┤
│  Piazza del Colosseo │
│  Roma, Italia        │
│                      │
│  🏷️ Fotografia      │
│  🏷️ Museo           │
│                      │
│  ⭐ Preferito        │
│  👁️ Visitato 5 volte│
│                      │
│  [Dettagli] [Route] │
└──────────────────────┘
```

**Click "Dettagli"**: Apre pannello completo
- Info complete
- Metadata aggiuntivi
- Storico modifiche
- Opzioni avanzate

---

## Organizzazione con Etichette

### Etichette Predefinite

L'app include etichette di sistema:
- 🏚️ **Urbex**: Luoghi abbandonati da esplorare
- 🍽️ **Ristorante**: Ristoranti e locali
- 🍕 **Pizzeria**: Pizzerie
- 📷 **Fotografia**: Luoghi fotografici
- 🚁 **Drone**: Spot per riprese drone
- 🌳 **Natura**: Parchi e natura
- 🏛️ **Museo**: Musei e gallerie

### Creare Etichetta Personalizzata

1. Menu → **"Labels"** → **"+ Nuova Label"**
2. Compila form:
   ```
   ┌──────────────────────────────┐
   │  Nuova Etichetta            │
   ├──────────────────────────────┤
   │  Nome: [____________]        │
   │  Colore: [🎨] #FF5733       │
   │  Icona: [📝] Scegli...      │
   │  Descrizione:                │
   │  [____________________]      │
   │                              │
   │  Anteprima:                  │
   │  [  🎨 Nome Label  ]        │
   │                              │
   │  [Annulla]  [Crea]          │
   └──────────────────────────────┘
   ```
3. **Nome**: Univoco, massimo 50 caratteri
4. **Colore**: Click su picker colore
5. **Icona**: Scegli da libreria FontAwesome
6. **Descrizione**: Opzionale, per riferimento
7. Clicca **"Crea"**

### Gestire Etichette

**Modificare**:
1. Menu → **"Labels"**
2. Click su label da modificare
3. Modifica colore/icona/descrizione
4. Salva

**Nota**: Non puoi modificare nome se label è già in uso

**Eliminare**:
1. Seleziona label
2. Click **"Elimina"**
3. Se in uso, scegli azione:
   - **Rimuovi da tutti markers**: Elimina associazioni
   - **Reassegna a**: Sposta markers ad altra label
4. Conferma

### Filtrare per Etichette

**Sulla Mappa**:
1. Pannello **"Filtri"** (icona imbuto)
2. Seleziona etichette da visualizzare
3. Mappa aggiorna in tempo reale

**Lista Markers**:
1. Menu → **"Markers"**
2. Filtro laterale → Seleziona labels
3. Lista filtra risultati

---

## Ricerca e Filtri

### Ricerca Rapida

**Barra Ricerca Superiore**:
```
┌────────────────────────────────────────┐
│  🔍 Cerca markers...                   │
└────────────────────────────────────────┘
```

1. Digita testo (cerca in nome + descrizione + indirizzo)
2. Risultati aggiornano in tempo reale
3. Click su risultato per centrare mappa

**Esempi Ricerca**:
- `"colosseo"` → Trova markers con "colosseo" nel nome
- `"pizza roma"` → Cerca in nome/descrizione/indirizzo
- `"41.89, 12.49"` → Cerca vicino a coordinate

### Ricerca Avanzata

Menu → **"Markers"** → **"🔍 Ricerca Avanzata"**

**Filtri Disponibili**:

1. **Testo**:
   - Nome contiene
   - Descrizione contiene
   - Indirizzo contiene

2. **Etichette**:
   - Seleziona una o più labels
   - Modalità: AND (tutte) / OR (almeno una)

3. **Area Geografica**:
   - **Cerchio**: Centro + raggio km
   - **Rettangolo**: Disegna su mappa
   - **Poligono**: Area personalizzata

4. **Attributi**:
   - Solo preferiti
   - Visitati / Non visitati
   - Data creazione (da/a)
   - Data ultimo aggiornamento

5. **Ordinamento**:
   - Nome (A-Z / Z-A)
   - Data creazione (recenti / vecchi)
   - Distanza (da punto)
   - Numero visite

**Esempio Ricerca**:
```
Trova: Tutti i ristoranti
Dove:  Entro 5km da posizione attuale
Con:   Rating > 4 stelle (metadata)
Ordina: Per distanza crescente
```

### Ricerca Geografica

**Markers Vicini**:
1. Click destro su mappa → **"Trova Vicini"**
2. Imposta raggio (1km, 5km, 10km, custom)
3. Visualizza risultati in lista e mappa

**Da Posizione Attuale**:
1. Click **"📍 La Mia Posizione"**
2. Autorizza GPS
3. Mappa centra su posizione
4. Usa filtro distanza per trovare vicini

---

## Pianificazione Itinerari

### Creare un Itinerario

1. Menu → **"Routes"** → **"+ Nuovo Itinerario"**
2. **Step 1: Info Base**
   ```
   Nome: [Tour Roma Classica    ]
   Descrizione: [Monumenti principali...]
   ```

3. **Step 2: Punto di Partenza**
   Scegli uno:
   - ⦿ Posizione Attuale (GPS)
   - ⦿ Indirizzo Specifico: [____________]
   - ⦿ Marker Salvato: [Dropdown ▼]

4. **Step 3: Aggiungi Destinazioni**
   ```
   Markers nell'Itinerario:
   ┌────────────────────────────────┐
   │  1. 📍 Colosseo               │
   │  2. 📍 Foro Romano            │
   │  3. 📍 Fontana di Trevi       │
   │  [+ Aggiungi Marker]          │
   └────────────────────────────────┘
   ```
   - Click **"Aggiungi Marker"**
   - Seleziona da lista o mappa
   - Riordina con drag & drop

5. **Step 4: Opzioni Ottimizzazione**
   ```
   Tipo Percorso:
   ⦿ Più breve (distanza minima)
   ⦿ Più veloce (tempo minimo)
   ⦿ Panoramico

   ☑ Ottimizza ordine tappe
   ☐ Evita autostrade
   ☐ Preferisci strade principali
   ```

6. **Step 5: Anteprima e Salva**
   ```
   ┌────────────────────────────────┐
   │  Riepilogo Itinerario         │
   ├────────────────────────────────┤
   │  Distanza Totale: 15.3 km     │
   │  Tempo Stimato: 4h 15m        │
   │  Numero Tappe: 5              │
   │                                │
   │  [Anteprima Mappa]            │
   │  ━━━━━━━━━━━━━━━━━━━━━━━━━   │
   │  1→2→3→4→5                    │
   │                                │
   │  [Indietro] [Salva Itinerario]│
   └────────────────────────────────┘
   ```

### Visualizzare Itinerario

1. Menu → **"Routes"** → Seleziona itinerario
2. Visualizzazione:
   - **Mappa**: Percorso completo con tappe numerate
   - **Lista Tappe**: Dettagli ogni tappa
   - **Profilo**: Elevazione se disponibile

**Info Visualizzate**:
- Distanza tra tappe
- Tempo stimato tappa-tappa
- Note per ogni tappa
- Totali cumulativi

### Modificare Itinerario

**Riordinare Tappe**:
- Drag & drop markers in lista
- Click **"Ricalcola Percorso"**

**Aggiungere/Rimuovere Tappe**:
- **+** per aggiungere
- **×** su tappa per rimuovere
- Auto-ricalcolo percorso

**Ottimizzare Automaticamente**:
1. Click **"⚡ Ottimizza Ordine"**
2. Algoritmo calcola ordine ottimale
3. Conferma o annulla

### Seguire Itinerario

1. Apri itinerario salvato
2. Click **"▶️ Avvia Navigazione"**
3. Modalità Navigazione:
   ```
   ┌────────────────────────────────┐
   │  🧭 Prossima Tappa            │
   ├────────────────────────────────┤
   │  📍 Colosseo                  │
   │  📏 800 metri                 │
   │  ⏱️ 10 minuti                 │
   │                                │
   │  [Mostra Mappa] [Completato] │
   │                                │
   │  Tappa 1 di 5                 │
   │  ████░░░░░░░░░░░░ 20%        │
   └────────────────────────────────┘
   ```
4. Segna tappe **"Completato"** man mano
5. Statistiche salvate automaticamente

### Condividere Itinerario

1. Apri itinerario
2. Click **"⤴️ Condividi"**
3. Opzioni:
   - **Link Pubblico**: Genera URL view-only
   - **Export GPX**: Scarica file per GPS
   - **Export PDF**: Stampa itinerario
   - **Condividi Social**: Facebook, Twitter

---

## Importazione Dati

### Import da File GPX

**GPX** (GPS Exchange Format): Standard per tracciati GPS

1. Menu → **"Import"** → **"📁 Import GPX"**
2. Click **"Seleziona File"** o drag & drop
3. Anteprima import:
   ```
   ┌────────────────────────────────┐
   │  File: track_2025.gpx         │
   ├────────────────────────────────┤
   │  Waypoints: 23                │
   │  Tracciati: 1                 │
   │                                │
   │  Anteprima Mappa:             │
   │  [Mappa con punti]            │
   │                                │
   │  Opzioni Import:              │
   │  ☑ Importa waypoints          │
   │  ☑ Importa tracciati          │
   │  ☐ Ignora duplicati           │
   │                                │
   │  Assegna Etichette:           │
   │  ☑ Fotografia ☐ Natura       │
   │                                │
   │  [Annulla] [Importa]          │
   └────────────────────────────────┘
   ```
4. Configura opzioni
5. Click **"Importa"**
6. Riepilogo:
   ```
   ✅ Import Completato

   Importati: 21 markers
   Duplicati: 2 (ignorati)
   Errori: 0
   Tracciati: 1
   ```

### Import da KML

**KML** (Keyhole Markup Language): Formato Google Earth

1. Menu → **"Import"** → **"Import KML"**
2. Processo simile a GPX
3. Supporta:
   - Placemarks (markers)
   - Folders (convertiti in labels)
   - Percorsi (LineStrings)

### Import da GeoJSON

**GeoJSON**: Formato standard per dati geografici

1. Menu → **"Import"** → **"Import GeoJSON"**
2. Supporta:
   - Features: Point (markers)
   - Properties: Metadata automatici
   - FeatureCollection: Import multipli

### Import da CSV

**CSV**: File tabellare con coordinate

1. Menu → **"Import"** → **"Import CSV"**
2. Requisiti file:
   ```
   name,latitude,longitude,description,labels
   "Colosseo",41.8902,12.4922,"Anfiteatro","Fotografia,Museo"
   "Trevi",41.9009,12.4833,"Fontana","Fotografia"
   ```
3. Mapping colonne:
   - Seleziona colonna Nome
   - Seleziona colonna Lat/Lon
   - Opzionali: descrizione, labels, etc.

### Web Scraping (Avanzato)

**Importa da Siti Web**:

1. Menu → **"Import"** → **"Web Scraping"**
2. Inserisci URL:
   ```
   URL: https://example.com/restaurants

   Tipo Contenuto:
   ⦿ Lista luoghi (automatico)
   ⦿ Configurazione personalizzata

   Area Geografica:
   [Roma, Italia          ] 📍
   ```
3. Preview dati estratti
4. Conferma import

**Nota**: Rispetta sempre robots.txt e termini di servizio siti

---

## Esportazione Dati

### Export Markers

1. Menu → **"Export"**
2. Seleziona formato:
   - **GPX**: Per GPS devices
   - **KML**: Per Google Earth/Maps
   - **GeoJSON**: Standard geospaziale
   - **CSV**: Tabella dati
   - **JSON**: Backup completo

3. Filtri export (opzionali):
   ```
   ☑ Tutti markers
   ⦿ Solo markers selezionati
   ⦿ Filtra per:
     ☑ Etichette: [Fotografia, Natura]
     ☐ Area geografica
     ☐ Solo preferiti
   ```

4. Opzioni formato:
   ```
   Formato GPX:
   ☑ Includi waypoints
   ☑ Includi tracciati
   ☐ Includi metadata estesi
   ```

5. Click **"Esporta"** → File scaricato

### Backup Completo

**Backup Tutti Dati**:

1. Menu → **"Export"** → **"💾 Backup Completo"**
2. Include:
   - Tutti markers
   - Labels personalizzate
   - Itinerari
   - Tracciati GPS
   - Impostazioni
3. Formato: ZIP con JSON + GPX
4. Usa per migrate o restore

---

## Tracciati GPS

### Importare Tracciato

1. Menu → **"Tracks"** → **"📁 Import Track"**
2. Seleziona file GPX con track
3. Associa a marker (opzionale):
   ```
   Tracciato: trail_monte_bianco.gpx

   Associa a Marker:
   [Monte Bianco ▼]  [Crea Nuovo]

   Statistiche Rilevate:
   📏 Distanza: 12.5 km
   ⏱️ Durata: 4h 15m
   📈 Dislivello: +850m / -200m
   ⛰️ Quota Max: 2450m
   ```

### Visualizzare Tracciato

**Su Mappa**:
- Linea colorata mostra percorso
- Markers start/end
- Waypoints intermedi

**Grafico Elevazione**:
```
Altitudine (m)
2500 │     ╱╲
2000 │    ╱  ╲___
1500 │   ╱       ╲
1000 │  ╱         ╲
 500 │_╱           ╲___
     └────────────────────→ Distanza (km)
     0  2  4  6  8  10  12
```

**Statistiche**:
- Distanza totale
- Tempo percorrenza
- Velocità media/max
- Elevazione gain/loss
- Calorie (stima)

### Registrare Tracciato (GPS)

**In Tempo Reale**:

1. Menu → **"Tracks"** → **"🔴 Registra"**
2. Autorizza GPS
3. Recording attivo:
   ```
   ┌────────────────────────────────┐
   │  🔴 Registrazione in corso    │
   ├────────────────────────────────┤
   │  ⏱️ 01:23:45                  │
   │  📏 8.3 km                    │
   │  🚶 5.2 km/h                  │
   │                                │
   │  [⏸️ Pausa] [⏹️ Stop]        │
   └────────────────────────────────┘
   ```
4. Pausa per soste
5. Stop al termine
6. Salva con nome

---

## Statistiche e Analisi

### Dashboard Statistiche

Menu → **"📊 Statistics"**

**Overview**:
```
┌────────────────────────────────────────┐
│  Le Tue Statistiche                   │
├────────────────────────────────────────┤
│  📍 Markers Totali: 150               │
│  ⭐ Preferiti: 23                     │
│  🏷️ Etichette: 12 (5 custom)         │
│  🗺️ Itinerari: 5                     │
│  📏 Distanza Totale: 245.8 km        │
└────────────────────────────────────────┘
```

**Markers per Etichetta** (Grafico a Torta):
```
    Fotografia (40%)
    Ristorante (20%)
    Urbex (25%)
    Natura (15%)
```

**Activity Timeline**:
```
Markers Creati per Mese
 50│    ╱╲
 40│   ╱  ╲  ╱╲
 30│  ╱    ╲╱  ╲
 20│ ╱          ╲___
 10│╱
   └────────────────────→
   Gen Feb Mar Apr Mag
```

**Heatmap Geografica**:
- Mappa densità markers
- Aree più visitate
- Zone da esplorare

**Top 10**:
- Markers più visitati
- Etichette più usate
- Itinerari più lunghi

---

## Impostazioni

Menu → **"⚙️ Settings"**

### Account

```
┌────────────────────────────────┐
│  Informazioni Account         │
├────────────────────────────────┤
│  Username: mario_rossi        │
│  Email: mario@example.com     │
│  Membro da: 15/01/2025        │
│                                │
│  [Modifica Email]             │
│  [Cambia Password]            │
│  [Elimina Account]            │
└────────────────────────────────┘
```

### Mappa

```
Provider Mappa:
⦿ OpenStreetMap (default)
○ Google Maps (richiede API key)
○ Mapbox

Stile Mappa:
⦿ Standard
○ Satellite
○ Terreno
○ Dark Mode

Marker Clustering:
☑ Raggruppa markers vicini
Soglia: [10 markers ▼]
```

### Geocoding

```
Provider Geocoding:
⦿ Nominatim (gratuito)
○ Google Maps
○ Bing Maps

Rate Limiting:
1 richiesta/secondo ☑ Rispetta limiti

Cache:
☑ Salva risultati geocoding
Dimensione cache: 100 MB
[Pulisci Cache]
```

### Privacy

```
☑ Condividi statistiche anonime
☐ Backup automatico cloud
☐ Sincronizza su dispositivi

Dati Posizione:
☑ Salva posizione attuale
☐ Tracking automatico movimenti
```

### Notifiche

```
☑ Notifiche desktop
☑ Email per import completati
☐ Promemoria itinerari
☐ Suggerimenti settimanali
```

### Avanzate

```
Unità di Misura:
⦿ Metriche (km, m)
○ Imperiali (mi, ft)

Formato Coordinate:
⦿ Decimale (41.8902)
○ DMS (41°53'24.72"N)

Lingua:
[Italiano ▼]

Database:
[Backup Database]
[Restore Database]
[Ottimizza Database]
```

---

## Tips & Tricks

### Shortcuts Tastiera

**Generali**:
- `Ctrl+N`: Nuovo marker
- `Ctrl+F`: Ricerca
- `Ctrl+S`: Salva
- `Ctrl+Z`: Annulla
- `Ctrl+Q`: Esci

**Mappa**:
- `+` / `-`: Zoom in/out
- `Arrows`: Pan mappa
- `F`: Centra su marker selezionato
- `M`: Toggle modalità mappa (standard/satellite)

**Navigazione**:
- `Alt+1`: Vai a Home
- `Alt+2`: Vai a Markers
- `Alt+3`: Vai a Routes
- `Alt+4`: Vai a Statistics

### Best Practices

**Organizzazione**:
1. Usa etichette multiple per markers versatili
2. Crea labels custom per categorie specifiche
3. Aggiungi descrizioni dettagliate per reference futura
4. Marca preferiti per accesso rapido

**Backup**:
1. Export backup mensile
2. Salva in cloud (Google Drive, Dropbox)
3. Test restore periodicamente

**Performance**:
1. Usa marker clustering con molti markers
2. Filtra markers non necessari su mappa
3. Pulisci cache geocoding periodicamente

**Itinerari**:
1. Salva waypoints intermedi interessanti
2. Aggiungi note tappe (orari apertura, etc.)
3. Verifica percorso prima di partire
4. Usa ottimizzazione automatica ordine

### FAQ

**Q: Come importo markers da Google Maps?**
A: Export da Google Maps in KML, poi Import KML in app.

**Q: Posso usare offline?**
A: Mappe richiedono connessione. Markers salvati accessibili offline.

**Q: Limite numero markers?**
A: No limite hard. Performance ottimale fino 10,000 markers.

**Q: Come condivido mappa con amici?**
A: Export in formato standard (GPX/KML) o genera link pubblico itinerario.

**Q: Posso sincronizzare tra dispositivi?**
A: Prossima versione includerà sync cloud. Ora usa export/import.

---

## Supporto

**Problemi o Domande?**

1. Consulta questa guida
2. Vedi [Setup Guide](setup-guide.md) per problemi tecnici
3. Apri issue su [GitHub](https://github.com/tuousername/myPersonalMap/issues)
4. Email: support@mypersonalmap.com

**Contribuisci**:
- Report bugs
- Suggerisci features
- Contribuisci codice
- Migliora documentazione

---

**Versione Guida**: 1.0
**Ultimo Aggiornamento**: Dicembre 2025

Buon viaggio con My Personal Map! 🗺️✨
