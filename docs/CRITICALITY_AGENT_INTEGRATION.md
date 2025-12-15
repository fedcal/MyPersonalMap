# Integrazione Criticality Agent nel Workflow

## Overview

Il **Criticality Management Agent** è un tool automatico che analizza `CRITICITA.md`, prioritizza i task e suggerisce quali criticità risolvere per primi.

## Quick Start

```bash
# Installa (nessuna dipendenza extra richiesta)
chmod +x scripts/criticality_agent.py

# Vedi summary
python scripts/criticality_agent.py summary

# Ottieni prossimo task
python scripts/criticality_agent.py next
```

## Workflow Raccomandato

### 🌅 Inizio Giornata

```bash
# 1. Check status criticità
python scripts/criticality_agent.py summary

# 2. Genera roadmap settimanale (Lunedì)
python scripts/criticality_agent.py roadmap > weekly_plan.txt

# 3. Ottieni task da fare oggi
python scripts/criticality_agent.py next
```

**Output esempio:**
```
🎯 Next Recommended Task:

ID:       C001
Priority: 🔴 CRITICA
Title:    Credenziali di Sicurezza Non Sicure
Category: Security
Effort:   2.0 hours
Files to modify:
  📁 pymypersonalmap/.env
  📁 pymypersonalmap/config/settings.py
```

### 💻 Durante Sviluppo

1. **Lavora sul task suggerito** (sempre il più urgente e non bloccato)
2. **Implementa la soluzione** seguendo le indicazioni in `CRITICITA.md`
3. **Testa la fix**

### ✅ Dopo Completamento

```bash
# 1. Marca come risolto nell'agent
python scripts/criticality_agent.py resolve C001 "SECRET_KEY auto-generation implementata"

# 2. Aggiorna CRITICITA.md manualmente
# - Sposta criticità da sezione attiva a "✅ Criticità Risolte"
# - Aggiungi entry in changelog
# - Aggiorna statistiche

# 3. Commit
git add CRITICITA.md pymypersonalmap/.env pymypersonalmap/config/settings.py
git commit -m "Fix C001: Implement secure credential generation"

# 4. Ottieni prossimo task
python scripts/criticality_agent.py next
```

## Integrazioni Avanzate

### Pre-commit Hook

Mostra summary criticità prima di ogni commit:

```bash
# .git/hooks/pre-commit
#!/bin/bash

echo "📊 Current Criticality Status:"
python scripts/criticality_agent.py summary

echo ""
read -p "Continue with commit? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
fi
```

### Daily Standup Report

```bash
# scripts/daily_standup.sh
#!/bin/bash

echo "=== DAILY STANDUP REPORT ==="
echo ""

echo "📊 Criticality Status:"
python scripts/criticality_agent.py summary

echo ""
echo "🎯 Today's Focus:"
python scripts/criticality_agent.py next

echo ""
echo "📅 Roadmap:"
python scripts/criticality_agent.py roadmap | head -30
```

### Bash Alias

Aggiungi al tuo `~/.bashrc` o `~/.zshrc`:

```bash
alias crit="python scripts/criticality_agent.py"
alias crit-next="python scripts/criticality_agent.py next"
alias crit-sum="python scripts/criticality_agent.py summary"
alias crit-map="python scripts/criticality_agent.py roadmap"
```

**Uso:**
```bash
crit-sum   # Quick summary
crit-next  # Next task
crit-map   # Roadmap
```

### VS Code Task

Aggiungi a `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Criticality Summary",
      "type": "shell",
      "command": "python",
      "args": ["scripts/criticality_agent.py", "summary"],
      "group": "none",
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    },
    {
      "label": "Next Criticality",
      "type": "shell",
      "command": "python",
      "args": ["scripts/criticality_agent.py", "next"],
      "group": "none"
    }
  ]
}
```

## Comandi Disponibili

| Comando | Scopo | Quando Usarlo |
|---------|-------|---------------|
| `summary` | Overview rapido con statistiche | Daily standup, check veloce |
| `next` | Task più urgente da fare | Inizio sessione lavoro |
| `roadmap` | Piano di risoluzione completo | Planning settimanale, sprint |
| `mapping` | Tabella criticità → file | Code review, refactoring |
| `report` | Report completo (tutti i report) | Report settimanali, stakeholder |
| `resolve <id>` | Marca criticità risolta | Dopo fix completata |

## Algoritmo di Prioritizzazione

L'agent usa questo algoritmo per suggerire il prossimo task:

```python
1. Filtra criticità bloccate (🚧)
2. Ordina per priorità: 🔴 CRITICA > 🟡 MEDIA > 🟢 MINORE
3. A parità di priorità, ordina per effort (più basso = prima)
4. Restituisci il primo della lista
```

**Esempio:**
```
Criticità disponibili:
- C001 🔴 CRITICA  2h  ← Questo viene suggerito (critica + low effort)
- C002 🔴 CRITICA  7h
- C003 🔴 CRITICA  BLOCCATO (escluso)
- C004 🟡 MEDIA    2h
```

## State Tracking

L'agent traccia lo stato in `.criticality_state.json`:

```json
{
  "last_update": "2025-12-15T14:30:00",
  "resolved_today": [
    {
      "id": "C001",
      "title": "Credenziali Sicurezza",
      "timestamp": "2025-12-15T14:00:00",
      "notes": "SECRET_KEY auto-generation"
    }
  ],
  "current_focus": "C002",
  "history": [...]
}
```

**Nota:** Questo file è gitignored (locale).

## Metriche e KPI

L'agent traccia:

- **Resolution Rate**: % criticità risolte vs totale
- **Active Count**: Numero criticità attive (target: 3)
- **Total Effort**: Ore stimate rimanenti
- **Blocked Count**: Criticità bloccate
- **Priority Distribution**: 🔴/🟡/🟢 breakdown

## FAQ

### Q: Come marco una criticità come bloccata?
**A:** Aggiungi `🚧 BLOCCATO` nello status in `CRITICITA.md`. L'agent lo rileverà automaticamente e la escluderà dai suggerimenti.

### Q: L'agent può aggiornare CRITICITA.md automaticamente?
**A:** No, per ora l'update è manuale. Il comando `resolve` aggiorna solo il file di stato interno.

### Q: Posso cambiare l'algoritmo di prioritizzazione?
**A:** Sì, modifica la funzione `get_next_task()` in `criticality_agent.py`.

### Q: Come vedo tutte le criticità risolte?
**A:** Usa `grep "✅" CRITICITA.md` o leggi la sezione "Criticità Risolte" nel file.

### Q: L'agent funziona su Windows?
**A:** Sì, usa `python scripts/criticality_agent.py` invece di `./scripts/criticality_agent.py`.

## Troubleshooting

### Problema: "CRITICITA.md not found"
**Soluzione:** Esegui da project root:
```bash
cd /path/to/myPersonalMap
python scripts/criticality_agent.py summary
```

### Problema: "No criticalities found"
**Soluzione:** Verifica formato `CRITICITA.md`:
- Sezioni devono iniziare con `## 🔴 Criticità Critiche (Alta Priorità)`
- Criticità con `### N. Titolo`
- Campi `**Severità**:`, `**Categoria**:`, `**File Coinvolti**:`

### Problema: Effort sempre 0.0
**Soluzione:** Assicurati che `CRITICITA.md` contenga:
```markdown
#### Effort: 2 ore
```

## Best Practices

1. **Esegui `summary` ogni mattina** - mantieni consapevolezza dello status
2. **Usa `next` per task selection** - evita di scegliere arbitrariamente
3. **Aggiorna CRITICITA.md dopo ogni risoluzione** - mantieni sincronizzato
4. **Controlla roadmap settimanalmente** - pianifica sprint
5. **Target: 3 criticità attive** - mantieni focus, risolvi prima di aggiungere nuove

## Prossimi Sviluppi

Features in roadmap per l'agent:
- [ ] Auto-update `CRITICITA.md` dopo `resolve`
- [ ] GitHub issue integration
- [ ] Time tracking per criticality
- [ ] Team assignment recommendations
- [ ] Burndown chart generation
- [ ] Email/Slack notifications quando criticità critiche > 3
- [ ] Web dashboard UI

---

**Creato**: 15 Dicembre 2025
**Versione Agent**: 1.0.0
**Documentazione**: `scripts/README_CRITICALITY_AGENT.md`
