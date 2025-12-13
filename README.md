# My Personal Map

Una mappa interattiva personale per gestire e organizzare i luoghi significativi della tua vita.

## Descrizione

Questo progetto nasce con l'intenzione di gestire una mappa personale in cui è possibile inserire le coordinate dei posti a cui l'utente tiene per diversi motivi. L'applicazione permette di catalogare, organizzare e pianificare visite ai propri luoghi preferiti.

## Funzionalità

### Gestione Segnaposti
- **Aggiunta segnaposti**: Inserisci luoghi con coordinate geografiche
- **Etichettatura multipla**: Ogni posto può avere diverse etichette (labels)
- **Descrizioni personalizzate**: Aggiungi note e descrizioni dettagliate per ogni luogo

### Categorie Predefinite
Il sistema supporta diverse categorie di luoghi, tra cui:
- Urbex
- Ristoranti
- Pizzerie
- Fotografia
- Drone
- Personalizzabili (gestione custom delle labels)

### Pianificazione Itinerari
- Organizza itinerari personalizzati
- Scegli il punto di partenza:
  - Posizione attuale (GPS)
  - Posizione inserita manualmente
  - Un altro segnaposto salvato

### Importazione ed Esportazione
- **Import**: Aggiungi segnaposti tramite:
  - Web scraping
  - Importazione file (vari formati supportati)
- **Tracciati GPS**: Salva e gestisci tracciati GPS completi

## Architettura Tecnica

### Backend
- **Linguaggio**: Python
- **Database**: MySQL
- **Features**:
  - API per gestione CRUD dei segnaposti
  - Sistema di etichettatura flessibile
  - Algoritmi di pianificazione itinerari

### Storage
- Database MySQL per persistenza dati
- Supporto per tracciati GPS
- Sistema di importazione/esportazione file

## Installazione

```bash
# Clona il repository
git clone https://github.com/tuousername/myPersonalMap.git

# Entra nella directory del progetto
cd myPersonalMap

# Installa le dipendenze
pip install -r pymypersonalmap/requirements.txt
```

## Configurazione Database

```sql
# Crea il database MySQL
CREATE DATABASE mypersonalmap;
```

Configura le credenziali del database nel file di configurazione (da creare).

## Utilizzo

```bash
# Avvia l'applicazione
python pymypersonalmap/main.py
```

## Roadmap

- [ ] Implementazione backend base
- [ ] Sistema di autenticazione utenti
- [ ] API REST per gestione segnaposti
- [ ] Interfaccia web interattiva
- [ ] Sistema di importazione file (GPX, KML, CSV)
- [ ] Algoritmo di ottimizzazione itinerari
- [ ] Web scraping per luoghi di interesse
- [ ] App mobile companion

## Contribuire

Le contribuzioni sono benvenute! Sentiti libero di aprire issue o pull request.

## Licenza

Da definire

## Contatti

Per domande o suggerimenti, apri una issue su GitHub.