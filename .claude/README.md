# Claude Code Configuration

Questa cartella contiene la configurazione personalizzata per Claude Code nel progetto My Personal Map.

## Struttura

```
.claude/
├── README.md                    # Questo file
├── settings.json                # Configurazione principale Claude Code
├── settings.local.json          # Configurazione locale (non committare)
├── agents/                      # Agent specializzati
│   ├── backend-dev.md          # Sviluppo backend FastAPI
│   ├── database-expert.md      # Database MySQL e SQLAlchemy
│   ├── documentation-writer.md # Scrittura documentazione
│   └── test-engineer.md        # Testing con pytest
├── commands/                    # Slash commands personalizzati
│   ├── add-endpoint.md         # /add-endpoint - Crea nuovo endpoint API
│   ├── add-model.md            # /add-model - Crea nuovo modello SQLAlchemy
│   ├── add-test.md             # /add-test - Scrive test
│   ├── document-api.md         # /document-api - Documenta endpoint
│   ├── debug-spatial.md        # /debug-spatial - Debug problemi geospaziali
│   └── setup-project.md        # /setup-project - Setup iniziale progetto
└── prompts/                     # Prompt riutilizzabili (opzionale)
```

## Agents Disponibili

### backend-dev.md
Esperto FastAPI e sviluppo backend. Usa quando devi:
- Creare nuovi endpoint REST
- Implementare servizi di business logic
- Lavorare con GeoPy, Shapely, GeoPandas
- Gestire autenticazione JWT

### database-expert.md
Specialista database MySQL con spatial types. Usa quando devi:
- Creare modelli SQLAlchemy con colonne spatial
- Scrivere query spaziali (ST_Distance_Sphere, etc.)
- Creare migrazioni Alembic
- Ottimizzare performance database

### documentation-writer.md
Scrittore tecnico per documentazione. Usa quando devi:
- Documentare endpoint API
- Scrivere docstring Python (Google style)
- Creare guide utente
- Aggiornare documentazione tecnica

### test-engineer.md
Ingegnere test con pytest. Usa quando devi:
- Scrivere unit test per servizi
- Creare integration test per API
- Testare operazioni geospaziali
- Aumentare code coverage

## Slash Commands

Usa questi comandi preceduti da `/` nella chat:

- `/add-endpoint` - Guidato per aggiungere nuovo endpoint FastAPI
- `/add-model` - Guidato per creare nuovo modello SQLAlchemy + migration
- `/add-test` - Assistenza scrittura test completi
- `/document-api` - Documenta endpoint con esempi e schemi
- `/debug-spatial` - Debug problemi coordinate/distanze/geocoding
- `/setup-project` - Setup completo progetto da zero

## Settings

Il file `settings.json` configura:
- **Permissions**: Cosa Claude può fare automaticamente
- **Project**: Info sul progetto (nome, root, moduli)
- **Agents**: Lista agent disponibili
- **Context**: File prioritari e pattern da includere
- **Commit**: Formato commit messages

## Uso

### Attivare un Agent
```
Please use the backend-dev agent to help me implement a new geocoding service.
```

### Usare un Command
```
/add-endpoint

(Claude ti guiderà attraverso i passaggi)
```

### Override Locale
Crea `settings.local.json` per override personali che non verranno committati:
```json
{
  "environment": {
    "DATABASE_URL": "mysql://localhost/mypersonalmap_local"
  }
}
```

## Best Practices

1. **Usa gli agent** quando lavori in aree specifiche del progetto
2. **Slash commands** per task ripetitivi e guidati
3. **Documenta modifiche** agli agent in questo README
4. **Non committare** settings.local.json (è in .gitignore)
5. **Aggiorna settings.json** quando aggiungi nuovi pattern di progetto

## Aggiungere Nuovi Agent

1. Crea file in `.claude/agents/nome-agent.md`
2. Segui il template degli agent esistenti
3. Documenta:
   - Role e expertise
   - Task che può svolgere
   - Code patterns comuni
   - Guidelines e best practices
4. Aggiungi a `settings.json` in `agents.available`
5. Aggiorna questo README

## Aggiungere Nuovi Commands

1. Crea file in `.claude/commands/nome-comando.md`
2. Scrivi prompt che guida Claude step-by-step
3. Includi esempi e output attesi
4. Testa il comando
5. Documenta qui

## Note

- Agents e commands sono specifici per questo progetto
- Basati su architettura layered e tech stack definiti
- Aggiornare quando cambiano pattern o tecnologie
- Consultare `CLAUDE.md` per overview architetturale
