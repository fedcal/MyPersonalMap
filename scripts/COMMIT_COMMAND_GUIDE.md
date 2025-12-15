# Smart Commit Command - Guida Completa

## Overview

Il comando `commit` dell'agent automatizza completamente il processo di commit quando risolvi una criticità:
- 🎯 **Auto-staging**: Stage automatico dei file coinvolti
- 📝 **Smart commit message**: Genera messaggio conventional commit
- ✅ **Auto-resolve**: Marca criticità come risolta
- 📊 **Status update**: Mostra summary aggiornato

## Usage

```bash
python scripts/criticality_agent.py commit <criticality_id> [note_aggiuntive]
```

### Esempi

```bash
# Commit base
python scripts/criticality_agent.py commit C001

# Commit con note aggiuntive
python scripts/criticality_agent.py commit C001 "Implementata generazione SECRET_KEY automatica"

# Con alias (se configurato)
crit commit C001 "Fix completata"
```

## Workflow Completo

### 1️⃣ Prima di Iniziare

```bash
# Ottieni task da fare
python scripts/criticality_agent.py next

# Output:
# 🎯 Next Recommended Task:
# ID:       C001
# Priority: 🔴 CRITICA
# Title:    Credenziali di Sicurezza Non Sicure
# Files to modify:
#   📁 pymypersonalmap/.env
#   📁 pymypersonalmap/config/settings.py
```

### 2️⃣ Implementa la Fix

Lavora sui file indicati, implementando la soluzione descritta in `CRITICITA.md`.

### 3️⃣ Testa le Modifiche

```bash
# Esegui test
pytest tests/

# Verifica che l'app funzioni
python pymypersonalmap/gui/app.py
```

### 4️⃣ Commit con l'Agent

```bash
python scripts/criticality_agent.py commit C001 "Implementata auto-generation SECRET_KEY"
```

## Output Dettagliato

### Step 1: Informazioni Criticità

```
======================================================================
📝 COMMITTING FIX FOR CRITICALITY
======================================================================

ID:       C001
Priority: 🔴 CRITICA
Title:    Credenziali di Sicurezza Non Sicure
Category: Security

Files involved:
  📁 pymypersonalmap/.env
  📁 pymypersonalmap/config/settings.py
```

### Step 2: Git Status

```
📋 Git Status:
 M pymypersonalmap/.env
 M pymypersonalmap/config/settings.py
 M pymypersonalmap/gui/setup_wizard.py
```

### Step 3: Commit Message Preview

```
💬 Generated Commit Message:
──────────────────────────────────────────────────────────────────────
security: 🔴 Fix C001 - Credenziali di Sicurezza Non Sicure

Resolves criticality C001 (CRITICA)
Category: Security

Implementata generazione automatica SECRET_KEY sicura nel setup wizard.
Validazione password database con requisiti minimi (8 caratteri).
Aggiornato settings.py con controlli di sicurezza.

Notes: Implementata auto-generation SECRET_KEY

Files modified:
- pymypersonalmap/.env
- pymypersonalmap/config/settings.py

🤖 Generated with Criticality Management Agent
──────────────────────────────────────────────────────────────────────
```

### Step 4: Conferma

```
❓ Actions to perform:
   1. Stage files: pymypersonalmap/.env, pymypersonalmap/config/settings.py
   2. Commit with generated message
   3. Mark C001 as resolved in agent state

🚀 Proceed with commit? (y/n):
```

### Step 5: Esecuzione

```
📦 Staging files...
   ✅ Staged: pymypersonalmap/.env
   ✅ Staged: pymypersonalmap/config/settings.py
   ✅ Staged: CRITICITA.md

💾 Creating commit...
✅ Commit created successfully!
[master abc1234] security: 🔴 Fix C001 - Credenziali di Sicurezza Non Sicure
 3 files changed, 45 insertions(+), 12 deletions(-)

✅ Criticality C001 marked as resolved!
   📝 Remember to update CRITICITA.md manually
```

### Step 6: Status Aggiornato

```
======================================================================
📊 UPDATED STATUS
======================================================================

╔════════════════════════════════════════════════════════════╗
║         CRITICALITY MANAGEMENT AGENT - SUMMARY            ║
╚════════════════════════════════════════════════════════════╝

📊 Current Status:
   🔴 Critical:   1
   🟡 High:       3
   🟢 Low:        4
   ✅ Resolved:  11
   ════════════════
   📋 Total Active: 8

⚠️  Blocked: 1
⏱️  Total Effort: 21.0 hours

📈 Progress:
   Resolution Rate: 57.9%
   Active vs Target: 8/3 (target)

🎯 Next Recommended Task:
   [C002] 🟡 Build Size Ancora Sopra Target
   ⏱️  Effort: 2.0h | 📂 Deployment
```

### Step 7: Reminder

```
✅ SUCCESS! Don't forget to:
   1. Push changes: git push
   2. Update CRITICITA.md (move C001 to Risolte section)
   3. Get next task: python scripts/criticality_agent.py next
```

## Formato Commit Message

### Conventional Commits

Il comando genera messaggi in formato **Conventional Commits**:

```
<type>: <emoji> Fix <id> - <title>

<body>
```

### Mapping Category → Type

| Category | Commit Type | Descrizione |
|----------|-------------|-------------|
| Security | `security` | Fix di sicurezza |
| Deployment | `build` | Build/deploy changes |
| Quality Assurance | `test` | Test e QA |
| Functionality | `feat` | Nuove features |
| Database Management | `feat` | Database features |
| User Experience | `feat` | UX improvements |
| Code Quality | `refactor` | Refactoring |
| Observability | `chore` | Logging, monitoring |
| Configuration | `chore` | Config changes |
| Distribution | `build` | Release/packaging |

### Emoji Priority Markers

- 🔴 = CRITICA
- 🟡 = MEDIA
- 🟢 = MINORE

### Esempio Completo

```
security: 🔴 Fix C001 - Credenziali di Sicurezza Non Sicure

Resolves criticality C001 (CRITICA)
Category: Security

Implementata generazione automatica SECRET_KEY nel DatabaseSetupWizard.
Aggiunta validazione password con requisiti minimi di sicurezza.
Settings.py ora controlla SECRET_KEY all'avvio e solleva errore se invalida.

Notes: Generazione automatica + validazione runtime

Files modified:
- pymypersonalmap/.env
- pymypersonalmap/config/settings.py
- pymypersonalmap/gui/setup_wizard.py

🤖 Generated with Criticality Management Agent
```

## Cosa fa il Comando

### 1. Validazione

✅ Verifica che criticità esista
✅ Controlla git working tree
✅ Valida che ci siano modifiche da committare

### 2. File Staging

Il comando stage automaticamente:
- Tutti i file elencati in `**File Coinvolti**` della criticità
- `CRITICITA.md` (se modificato)

**Nota**: Altri file modificati NON vengono staged automaticamente.

### 3. Commit Creation

- Genera messaggio conventional commit
- Esegue `git commit -m "..."`
- Include emoji, categoria, priorità

### 4. State Update

- Marca criticità come risolta in `.criticality_state.json`
- Aggiorna history e timestamp
- Traccia notes aggiuntive

### 5. Post-Commit

- Mostra summary aggiornato
- Suggerisce prossimo task
- Ricorda di pushare e aggiornare `CRITICITA.md`

## Opzioni e Flags

### Note Aggiuntive

```bash
# Aggiungi dettagli alla fix
python scripts/criticality_agent.py commit C001 "Dettagli implementazione qui"
```

Le note vengono:
- Incluse nel commit message
- Salvate nello state dell'agent
- Mostrate nei report futuri

### Interactive Mode

Il comando è **sempre interattivo**:
- Mostra preview del commit message
- Chiede conferma prima di committare
- Permette di cancellare (`n`) se qualcosa non va

## Best Practices

### ✅ DO

1. **Testa prima di committare**
   ```bash
   pytest tests/
   python scripts/criticality_agent.py commit C001
   ```

2. **Usa note aggiuntive per dettagli**
   ```bash
   crit commit C001 "Aggiunto fallback per MySQL connection error"
   ```

3. **Aggiorna CRITICITA.md dopo commit**
   - Sposta criticità in sezione "Risolte"
   - Aggiorna statistiche e changelog
   - Commit separato per CRITICITA.md se necessario

4. **Verifica file staged**
   ```bash
   git status  # Prima di confermare
   ```

5. **Push subito dopo**
   ```bash
   git push origin main
   ```

### ❌ DON'T

1. **Non committare senza testare**
   - Esegui sempre test prima

2. **Non dimenticare CRITICITA.md**
   - L'agent NON aggiorna CRITICITA.md automaticamente
   - Devi farlo manualmente

3. **Non usare per commit generici**
   - Il comando è specifico per criticità
   - Per commit normali usa `git commit` standard

4. **Non committare file non correlati**
   - L'agent stage solo file della criticità
   - Altri file vanno committati separatamente

## Troubleshooting

### Problema: "No changes detected"

**Causa**: Nessun file modificato o già committato

**Soluzione**:
```bash
git status  # Verifica cosa c'è da committare
# Assicurati di aver salvato i file
```

### Problema: "Criticality already resolved"

**Causa**: Criticità già marcata come risolta

**Soluzione**:
- Rispondi `y` per continuare comunque
- Oppure `n` per cancellare e verificare

### Problema: "Could not stage file"

**Causa**: File non esiste o path errato

**Soluzione**:
- Verifica che il file esista
- Controlla il path in `CRITICITA.md`
- Stage manualmente: `git add <file>`

### Problema: "Commit failed"

**Causa**: Errore git (es. pre-commit hook failed)

**Soluzione**:
```bash
git status  # Vedi cosa è staged
git commit  # Prova commit manuale per vedere errore
# Fix l'errore e riprova
```

## Integrazione CI/CD

### Pre-commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash

# Verifica che criticità commitata sia aggiornata in CRITICITA.md
if git diff --cached --name-only | grep -q "CRITICITA.md"; then
    echo "✅ CRITICITA.md updated"
else
    if git log -1 --pretty=%B | grep -q "Fix C"; then
        echo "⚠️  Warning: Committing criticality fix but CRITICITA.md not updated"
        echo "   Consider updating CRITICITA.md"
    fi
fi
```

### Commit Message Linting

```bash
# .commitlintrc.js
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      [
        'feat', 'fix', 'docs', 'style', 'refactor',
        'test', 'chore', 'security', 'build'
      ]
    ]
  }
}
```

## Esempi Completi

### Esempio 1: Fix Security Critical

```bash
# 1. Get task
python scripts/criticality_agent.py next
# → C001 Security

# 2. Implement fix
# ... edit files ...

# 3. Test
pytest tests/test_security.py

# 4. Commit
python scripts/criticality_agent.py commit C001 "Implementata auto-generation SECRET_KEY nel wizard"

# 5. Push
git push origin main

# 6. Update CRITICITA.md
# ... move C001 to Risolte ...
git add CRITICITA.md
git commit -m "docs: Update CRITICITA.md - C001 resolved"
git push
```

### Esempio 2: Fix con Più File

```bash
# Fix che tocca più file
python scripts/criticality_agent.py commit C006 "Creato ErrorHandler centralizzato per tutti i componenti GUI"

# Output stage:
# ✅ Staged: pymypersonalmap/gui/error_handler.py (new)
# ✅ Staged: pymypersonalmap/gui/app.py
# ✅ Staged: pymypersonalmap/gui/components/map_viewer.py
# ✅ Staged: CRITICITA.md
```

### Esempio 3: Fix Bloccata Poi Sbloccata

```bash
# Prima: C003 è bloccata
python scripts/criticality_agent.py next
# → Skips C003 (blocked)

# Setup display e MySQL...

# Dopo: C003 sbloccata
python scripts/criticality_agent.py commit C003 "Completati test GUI con display real e MySQL configurato"
```

## FAQ

### Q: Posso modificare il commit message?
**A:** Sì, cancella con `n` e usa `git commit` manualmente.

### Q: Cosa succede se il commit fallisce?
**A:** L'agent NON marca la criticità come risolta. Puoi correggere e riprovare.

### Q: Posso usare il comando per commit parziali?
**A:** No, stage solo file della criticità. Per commit parziali usa git direttamente.

### Q: L'agent pusha automaticamente?
**A:** No, devi fare `git push` manualmente.

### Q: Posso ammendare il commit?
**A:** Sì, usa `git commit --amend` dopo.

---

**Versione**: 1.0.0
**Ultima Modifica**: 15 Dicembre 2025
**Compatibilità**: Git 2.x+, Python 3.11+
