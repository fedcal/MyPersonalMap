# Use Cases - My Personal Map

## Panoramica

Questo documento descrive i principali casi d'uso dell'applicazione My Personal Map, identificando attori, precondizioni, flussi principali e alternativi, e postcondizioni.

## Attori

### 1. Utente Registrato
Utente che ha creato un account e ha effettuato il login nell'applicazione.

### 2. Sistema
Il sistema My Personal Map che gestisce i dati e le operazioni.

### 3. Servizi Esterni
- Servizi di geocoding (Nominatim, Google Maps)
- Fornitori di mappe (OpenStreetMap, Google Maps)
- Servizi di routing (OSRM, GraphHopper)

---

## UC-01: Registrazione Utente

**Attore Primario**: Nuovo Utente

**Precondizioni**:
- L'utente non ha un account esistente
- L'applicazione è in esecuzione

**Flusso Principale**:
1. L'utente avvia l'applicazione
2. L'utente seleziona "Registrati"
3. Il sistema mostra il form di registrazione
4. L'utente inserisce username, email e password
5. Il sistema valida i dati:
   - Username univoco
   - Email valida e univoca
   - Password rispetta requisiti di sicurezza (min 8 caratteri)
6. Il sistema crea l'account e invia email di conferma
7. L'utente conferma l'email
8. Il sistema attiva l'account

**Flussi Alternativi**:
- **5a**: Username già esistente
  - Il sistema mostra messaggio di errore
  - Ritorna al passo 4
- **5b**: Email già registrata
  - Il sistema suggerisce recupero password
  - Offre opzione login
- **5c**: Password non sicura
  - Il sistema mostra requisiti password
  - Ritorna al passo 4

**Postcondizioni**:
- Nuovo account utente creato nel database
- Email di conferma inviata
- Utente può effettuare il login

---

## UC-02: Aggiungere Segnaposto Manualmente

**Attore Primario**: Utente Registrato

**Precondizioni**:
- L'utente ha effettuato il login
- L'utente sta visualizzando la mappa

**Flusso Principale**:
1. L'utente clicca su "Aggiungi Segnaposto"
2. Il sistema mostra il form di inserimento
3. L'utente inserisce:
   - Nome del luogo
   - Coordinate (latitudine/longitudine) o indirizzo
   - Descrizione (opzionale)
   - Seleziona una o più etichette
4. L'utente può cliccare sulla mappa per selezionare le coordinate
5. Se inserito indirizzo, il sistema effettua geocoding per ottenere coordinate
6. L'utente conferma l'inserimento
7. Il sistema valida i dati
8. Il sistema salva il segnaposto nel database
9. Il sistema aggiorna la visualizzazione della mappa con il nuovo marker

**Flussi Alternativi**:
- **3a**: L'utente inserisce solo l'indirizzo
  - Il sistema richiede geocoding al servizio esterno
  - Mostra coordinate trovate per conferma
- **5a**: Geocoding fallisce
  - Il sistema chiede di inserire coordinate manualmente
- **7a**: Coordinate non valide
  - Il sistema mostra messaggio errore
  - Ritorna al passo 3
- **8a**: Errore di salvataggio
  - Il sistema mostra messaggio errore
  - I dati inseriti vengono preservati per retry

**Postcondizioni**:
- Nuovo segnaposto salvato nel database
- Marker visibile sulla mappa
- Contatore markers utente incrementato

---

## UC-03: Cercare Segnaposti

**Attore Primario**: Utente Registrato

**Precondizioni**:
- L'utente ha effettuato il login
- Esistono segnaposti salvati

**Flusso Principale**:
1. L'utente inserisce criteri di ricerca:
   - Testo libero (nome/descrizione)
   - Filtro per etichette
   - Filtro per area geografica
   - Filtro per preferiti
2. Il sistema esegue la ricerca nel database
3. Il sistema mostra risultati in lista
4. Il sistema evidenzia i markers corrispondenti sulla mappa
5. L'utente può selezionare un risultato per vedere dettagli

**Flussi Alternativi**:
- **2a**: Nessun risultato trovato
  - Il sistema mostra messaggio "Nessun risultato"
  - Suggerisce di modificare i criteri
- **3a**: Troppi risultati (>100)
  - Il sistema mostra primi 100 risultati
  - Suggerisce di raffinare la ricerca
- **4a**: Ricerca per area geografica
  - L'utente disegna area sulla mappa
  - Il sistema cerca markers nell'area delimitata

**Postcondizioni**:
- Risultati visualizzati
- Mappa centrata sui risultati

---

## UC-04: Pianificare Itinerario

**Attore Primario**: Utente Registrato

**Precondizioni**:
- L'utente ha almeno 2 segnaposti salvati
- L'utente ha effettuato il login

**Flusso Principale**:
1. L'utente seleziona "Crea Itinerario"
2. Il sistema mostra interfaccia di pianificazione
3. L'utente seleziona punto di partenza:
   - Posizione attuale (GPS)
   - Indirizzo personalizzato
   - Un segnaposto esistente
4. L'utente aggiunge destinazioni (segnaposti) all'itinerario
5. L'utente può riordinare le tappe
6. L'utente seleziona tipo di ottimizzazione:
   - Percorso più breve
   - Percorso più veloce
   - Percorso panoramico
7. Il sistema calcola l'itinerario ottimale
8. Il sistema mostra:
   - Percorso sulla mappa
   - Distanza totale
   - Tempo stimato
   - Ordine tappe ottimizzato
9. L'utente salva l'itinerario con un nome

**Flussi Alternativi**:
- **3a**: L'utente sceglie posizione attuale
  - Il sistema richiede permesso GPS
  - Ottiene coordinate attuali
- **7a**: Calcolo itinerario fallisce
  - Il sistema usa calcolo base (linea retta)
  - Mostra warning
- **7b**: Ottimizzazione richiesta
  - Il sistema applica algoritmo TSP
  - Riordina tappe per minimizzare distanza
- **8a**: Itinerario troppo lungo
  - Il sistema avvisa l'utente
  - Suggerisce di dividere in più giorni

**Postcondizioni**:
- Itinerario salvato nel database
- Percorso visualizzato sulla mappa
- Statistiche itinerario calcolate

---

## UC-05: Importare Dati da File GPX

**Attore Primario**: Utente Registrato

**Precondizioni**:
- L'utente ha un file GPX valido
- L'utente ha effettuato il login

**Flusso Principale**:
1. L'utente seleziona "Importa" → "File GPX"
2. Il sistema mostra dialog selezione file
3. L'utente seleziona file GPX dal file system
4. Il sistema valida il file:
   - Formato XML corretto
   - Tag GPX validi
   - Coordinate valide
5. Il sistema mostra anteprima:
   - Numero waypoints trovati
   - Numero tracciati trovati
   - Anteprima su mappa
6. L'utente configura importazione:
   - Seleziona quali waypoints importare
   - Sceglie etichette da applicare
   - Decide se importare anche tracciati
7. L'utente conferma importazione
8. Il sistema importa i dati:
   - Crea markers per waypoints
   - Salva tracciati GPS se richiesto
   - Controlla duplicati
9. Il sistema mostra riepilogo importazione:
   - Elementi importati
   - Duplicati ignorati
   - Eventuali errori

**Flussi Alternativi**:
- **4a**: File non valido
  - Il sistema mostra errori specifici
  - Permette selezione nuovo file
- **4b**: Coordinate fuori range
  - Il sistema mostra warning
  - Chiede conferma per ignorare punti invalidi
- **8a**: Duplicati trovati
  - Il sistema evidenzia duplicati
  - Chiede se aggiornare o ignorare
- **8b**: Errore durante importazione
  - Il sistema effettua rollback
  - Mostra log errori dettagliato

**Postcondizioni**:
- Nuovi markers creati dal GPX
- Tracciati GPS salvati (se richiesto)
- Record importazione salvato in import_history
- Mappa aggiornata con nuovi dati

---

## UC-06: Gestire Etichette Personalizzate

**Attore Primario**: Utente Registrato

**Precondizioni**:
- L'utente ha effettuato il login

**Flusso Principale**:
1. L'utente seleziona "Gestisci Etichette"
2. Il sistema mostra lista etichette esistenti:
   - Etichette di sistema (non modificabili)
   - Etichette personalizzate utente
3. L'utente seleziona azione:
   - Crea nuova etichetta
   - Modifica etichetta esistente
   - Elimina etichetta
4. **Se crea nuova**:
   - Inserisce nome
   - Sceglie colore
   - Seleziona icona
   - Aggiunge descrizione
5. **Se modifica**:
   - Cambia colore/icona/descrizione
   - Non può cambiare nome se usata
6. **Se elimina**:
   - Il sistema verifica se in uso
   - Chiede conferma
7. Il sistema salva le modifiche
8. Il sistema aggiorna visualizzazione mappa

**Flussi Alternativi**:
- **4a**: Nome etichetta già esistente
  - Il sistema mostra errore
  - Chiede nome diverso
- **6a**: Etichetta in uso su markers
  - Il sistema mostra numero markers affetti
  - Chiede conferma eliminazione
  - Rimuove associazioni o offre reassegnazione
- **6b**: Tentativo eliminazione etichetta sistema
  - Il sistema nega operazione
  - Mostra messaggio informativo

**Postcondizioni**:
- Etichetta creata/modificata/eliminata
- Markers aggiornati con nuove etichette
- Legenda mappa aggiornata

---

## UC-07: Esportare Dati

**Attore Primario**: Utente Registrato

**Precondizioni**:
- L'utente ha segnaposti salvati
- L'utente ha effettuato il login

**Flusso Principale**:
1. L'utente seleziona "Esporta"
2. Il sistema mostra opzioni esportazione:
   - Formato file (GPX, KML, GeoJSON, CSV, JSON)
   - Filtri dati da esportare
   - Opzioni formato specifico
3. L'utente seleziona formato desiderato
4. L'utente applica eventuali filtri:
   - Per etichette
   - Per area geografica
   - Per data creazione
   - Solo preferiti
5. L'utente configura opzioni formato
6. L'utente conferma esportazione
7. Il sistema genera file:
   - Recupera dati filtrati
   - Converte nel formato scelto
   - Valida output
8. Il sistema salva file e mostra dialog download

**Flussi Alternativi**:
- **3a**: Formato GPX selezionato
  - Opzioni: includi tracciati, includi waypoints
- **3b**: Formato CSV selezionato
  - Opzioni: separatore, encoding, campi da includere
- **7a**: Troppi dati da esportare
  - Il sistema suggerisce applicare filtri
  - Offre esportazione suddivisa
- **7b**: Errore generazione file
  - Il sistema mostra messaggio errore
  - Offre retry o formato alternativo

**Postcondizioni**:
- File esportato generato
- Download disponibile per utente
- Record export salvato (per tracking)

---

## UC-08: Visualizzare Statistiche

**Attore Primario**: Utente Registrato

**Precondizioni**:
- L'utente ha effettuato il login
- L'utente ha dati salvati

**Flusso Principale**:
1. L'utente seleziona "Statistiche"
2. Il sistema calcola e mostra:
   - Numero totale segnaposti
   - Numero markers per etichetta
   - Distribuzione geografica
   - Luoghi più visitati
   - Distanza totale itinerari
   - Timeline creazioni
3. Il sistema mostra grafici:
   - Grafico a torta per etichette
   - Mappa di calore per densità
   - Grafico timeline attività
4. L'utente può filtrare statistiche per periodo

**Flussi Alternativi**:
- **2a**: Dati insufficienti
  - Il sistema mostra messaggio informativo
  - Suggerisce di aggiungere più dati

**Postcondizioni**:
- Statistiche visualizzate
- Grafici renderizzati

---

## UC-09: Condividere Itinerario

**Attore Primario**: Utente Registrato

**Precondizioni**:
- L'utente ha un itinerario salvato
- L'utente ha effettuato il login

**Flusso Principale**:
1. L'utente seleziona un itinerario
2. L'utente clicca "Condividi"
3. Il sistema mostra opzioni condivisione:
   - Link pubblico (read-only)
   - Export file
   - Condivisione social
4. L'utente seleziona opzione
5. **Se link pubblico**:
   - Il sistema genera URL univoco
   - Copia link in clipboard
   - Mostra QR code
6. **Se export file**:
   - Genera GPX/KML dell'itinerario
7. Il sistema registra condivisione

**Flussi Alternativi**:
- **5a**: Link già esistente
  - Il sistema mostra link esistente
  - Offre opzione rigenera
- **5b**: Opzione revoca link
  - L'utente può invalidare link precedenti

**Postcondizioni**:
- Itinerario condiviso
- Link/file generato
- Log condivisione salvato

---

## UC-10: Web Scraping Luoghi

**Attore Primario**: Utente Registrato

**Precondizioni**:
- L'utente ha effettuato il login
- URL sorgente valido disponibile

**Flusso Principale**:
1. L'utente seleziona "Importa da Web"
2. Il sistema mostra form:
   - Campo URL sorgente
   - Tipo contenuto (ristoranti, musei, etc.)
   - Area geografica target
3. L'utente inserisce URL e parametri
4. L'utente avvia scraping
5. Il sistema:
   - Accede alla pagina web
   - Estrae dati strutturati
   - Identifica coordinate o indirizzi
   - Effettua geocoding se necessario
6. Il sistema mostra anteprima dati estratti
7. L'utente seleziona luoghi da importare
8. L'utente assegna etichette
9. L'utente conferma importazione
10. Il sistema salva markers

**Flussi Alternativi**:
- **5a**: Pagina richiede JavaScript
  - Il sistema usa browser headless (Selenium)
- **5b**: Dati non strutturati
  - Il sistema chiede pattern personalizzato
  - Offre wizard configurazione
- **5c**: Geocoding fallisce per alcuni indirizzi
  - Il sistema segna voci problematiche
  - Permette correzione manuale
- **10a**: Molti duplicati trovati
  - Il sistema mostra elenco duplicati
  - Chiede conferma per procedere

**Postcondizioni**:
- Nuovi markers importati da web
- Record import_history creato
- Mappa aggiornata

---

## UC-11: Modificare Segnaposto Esistente

**Attore Primario**: Utente Registrato

**Precondizioni**:
- L'utente ha effettuato il login
- Esiste almeno un segnaposto

**Flusso Principale**:
1. L'utente seleziona un marker sulla mappa o dalla lista
2. L'utente clicca "Modifica"
3. Il sistema mostra form pre-compilato con dati attuali
4. L'utente modifica campi desiderati:
   - Nome
   - Coordinate
   - Descrizione
   - Etichette
   - Metadata
5. L'utente conferma modifiche
6. Il sistema valida dati
7. Il sistema salva aggiornamento
8. Il sistema aggiorna visualizzazione

**Flussi Alternativi**:
- **4a**: L'utente sposta marker sulla mappa
  - Il sistema aggiorna coordinate automaticamente
- **6a**: Dati non validi
  - Il sistema mostra errori specifici
  - Preserva modifiche per correzione

**Postcondizioni**:
- Segnaposto aggiornato nel database
- Timestamp updated_at aggiornato
- Visualizzazione aggiornata

---

## UC-12: Eliminare Segnaposto

**Attore Primario**: Utente Registrato

**Precondizioni**:
- L'utente ha effettuato il login
- Esiste almeno un segnaposto

**Flusso Principale**:
1. L'utente seleziona marker da eliminare
2. L'utente clicca "Elimina"
3. Il sistema verifica se marker è usato in:
   - Itinerari salvati
   - Tracciati GPS associati
4. Il sistema mostra dialog conferma con dettagli impatto
5. L'utente conferma eliminazione
6. Il sistema elimina marker e dipendenze
7. Il sistema aggiorna visualizzazione

**Flussi Alternativi**:
- **3a**: Marker usato in itinerari
  - Il sistema mostra lista itinerari affetti
  - Offre opzioni:
    - Elimina marker e rimuovi da itinerari
    - Annulla operazione
- **5a**: L'utente annulla
  - Nessuna modifica effettuata

**Postcondizioni**:
- Marker eliminato da database
- Associazioni rimosse (cascade delete)
- Mappa aggiornata

---

## Matrice Tracciabilità Requisiti

| Use Case | Requisiti Funzionali | Requisiti Non-Funzionali |
|----------|---------------------|--------------------------|
| UC-01 | RF-01: Gestione utenti | RNF-01: Sicurezza autenticazione |
| UC-02 | RF-02: CRUD markers | RNF-02: Validazione dati |
| UC-03 | RF-03: Ricerca avanzata | RNF-03: Performance query |
| UC-04 | RF-04: Pianificazione itinerari | RNF-04: Algoritmi ottimizzazione |
| UC-05 | RF-05: Import GPX | RNF-05: Gestione file grandi |
| UC-06 | RF-06: Gestione labels | RNF-06: Usabilità interfaccia |
| UC-07 | RF-07: Export dati | RNF-07: Formati standard |
| UC-08 | RF-08: Statistiche | RNF-08: Performance calcoli |
| UC-09 | RF-09: Condivisione | RNF-09: Sicurezza link pubblici |
| UC-10 | RF-10: Web scraping | RNF-10: Robustezza parsing |
| UC-11 | RF-02: CRUD markers | RNF-02: Validazione dati |
| UC-12 | RF-02: CRUD markers | RNF-11: Integrità referenziale |

---

## Diagrammi Use Case

### Diagramma Principale

```
                         My Personal Map System
    ┌────────────────────────────────────────────────────────┐
    │                                                        │
    │  ┌─────────────┐      ┌──────────────────────┐       │
    │  │  Registrati │      │  Gestisci Markers    │       │
    │  └─────────────┘      │  ┌─────────────────┐ │       │
    │                       │  │ Aggiungi        │ │       │
    │  ┌─────────────┐      │  │ Modifica        │ │       │
    │  │   Login     │      │  │ Elimina         │ │       │
    │  └─────────────┘      │  │ Cerca           │ │       │
    │                       │  └─────────────────┘ │       │
    │                       └──────────────────────┘       │
Utente                                                      │
    │  ┌──────────────────────────────────────────┐       │
    │  │  Gestisci Itinerari                      │       │
    │  │  ┌────────────────────────────────────┐  │       │
    │  │  │ Pianifica Itinerario               │  │       │
    │  │  │ Salva Itinerario                   │  │       │
    │  │  │ Condividi Itinerario               │  │       │
    │  │  └────────────────────────────────────┘  │       │
    │  └──────────────────────────────────────────┘       │
    │                                                        │
    │  ┌──────────────────────────────────────────┐       │
    │  │  Import/Export                           │       │
    │  │  ┌────────────────────────────────────┐  │       │
    │  │  │ Importa GPX/KML                    │  │       │
    │  │  │ Web Scraping                       │  │       │
    │  │  │ Esporta Dati                       │  │       │
    │  │  └────────────────────────────────────┘  │       │
    │  └──────────────────────────────────────────┘       │
    │                                                        │
    │  ┌─────────────────┐  ┌──────────────────┐          │
    │  │ Gestisci Labels │  │  Visualizza      │          │
    │  └─────────────────┘  │  Statistiche     │          │
    │                       └──────────────────┘          │
    └────────────────────────────────────────────────────────┘
                              │
                              │ <<uses>>
                              ▼
                    ┌──────────────────┐
                    │ Servizi Esterni  │
                    │ - Geocoding      │
                    │ - Mappe          │
                    │ - Routing        │
                    └──────────────────┘
```

## Priorità Implementation

### Alta Priorità (MVP)
- UC-01: Registrazione Utente
- UC-02: Aggiungere Segnaposto
- UC-03: Cercare Segnaposti
- UC-06: Gestire Etichette
- UC-11: Modificare Segnaposto
- UC-12: Eliminare Segnaposto

### Media Priorità
- UC-04: Pianificare Itinerario
- UC-05: Importare GPX
- UC-07: Esportare Dati
- UC-08: Visualizzare Statistiche

### Bassa Priorità (Nice-to-have)
- UC-09: Condividere Itinerario
- UC-10: Web Scraping Luoghi
