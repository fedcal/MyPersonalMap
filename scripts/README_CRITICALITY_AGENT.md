# Criticality Management Agent

## Overview

The **Criticality Management Agent** is an automated tool for managing, prioritizing, and tracking project criticalities. It analyzes the `CRITICITA.md` file, generates actionable reports, and helps developers focus on the most urgent issues.

## Features

✅ **Automated Parsing**: Reads and parses `CRITICITA.md` automatically
✅ **Priority-Based Sorting**: Orders criticalities by urgency (Critical → High → Low)
✅ **Smart Recommendations**: Suggests next task based on priority and effort
✅ **Progress Tracking**: Tracks resolution history and current focus
✅ **Multiple Reports**: Summary, roadmap, mapping table, full report
✅ **Blocked Detection**: Identifies and flags blocked criticalities

## Installation

No installation required! The agent is a standalone Python script.

```bash
# Make executable (if not already)
chmod +x scripts/criticality_agent.py
```

## Usage

### Quick Start

```bash
# Get a quick summary
python scripts/criticality_agent.py summary

# Get next task to work on
python scripts/criticality_agent.py next

# Generate full report
python scripts/criticality_agent.py report
```

### Commands

#### 1. **Summary** - Quick Overview
```bash
python scripts/criticality_agent.py summary
```

**Output:**
- Current status (Critical/High/Low/Resolved counts)
- Blocked criticalities count
- Total estimated effort
- Progress percentage
- Next recommended task

**Use case:** Daily standup, quick check before starting work

---

#### 2. **Roadmap** - Resolution Plan
```bash
python scripts/criticality_agent.py roadmap
```

**Output:**
- Phase-by-phase resolution plan
- Criticalities ordered by priority
- Effort estimation per criticality
- Blocked items highlighted

**Use case:** Sprint planning, task assignment, weekly reviews

---

#### 3. **Mapping Table** - File-to-Criticality Map
```bash
python scripts/criticality_agent.py mapping
```

**Output:**
- Table with: ID | Priority | Title | Files | Status
- Easy to see which files need attention
- Quick reference for code reviews

**Use case:** Understanding which files are involved, code review preparation

---

#### 4. **Next Task** - What to Work on Now
```bash
python scripts/criticality_agent.py next
```

**Output:**
- Most urgent, non-blocked task
- Full details: priority, effort, files, description
- Ready to start implementation

**Algorithm:**
1. Filter out blocked criticalities
2. Sort by priority (Critical → High → Low)
3. For same priority, choose lowest effort first
4. Return top result

**Use case:** Starting a new work session, task selection

---

#### 5. **Full Report** - Complete Analysis
```bash
python scripts/criticality_agent.py report
```

**Output:**
- Summary + Mapping Table + Roadmap
- Complete picture of all criticalities
- Export-friendly format

**Use case:** Weekly reports, stakeholder updates, documentation

---

#### 6. **Mark Resolved** - Update Progress
```bash
python scripts/criticality_agent.py resolve <criticality_id> [notes]
```

**Example:**
```bash
python scripts/criticality_agent.py resolve C001 "Implemented ErrorHandler class"
```

**Effect:**
- Updates `.criticality_state.json` tracking file
- Adds to resolution history
- **Note:** You still need to manually update `CRITICITA.md`

**Use case:** After completing a criticality fix (without git commit)

---

### 7. **Smart Commit** - Auto-Commit Fix ⭐ NEW
```bash
python scripts/criticality_agent.py commit <criticality_id> [notes]
```

**Example:**
```bash
python scripts/criticality_agent.py commit C001 "Implemented auto SECRET_KEY generation"
```

**What it does:**
1. Shows criticality info and git status
2. Generates conventional commit message
3. Stages files involved in the criticality
4. Commits with smart message
5. Marks criticality as resolved
6. Shows updated summary

**Output Example:**
```
security: 🔴 Fix C001 - Credenziali di Sicurezza Non Sicure

Resolves criticality C001 (CRITICA)
Category: Security

Implemented automatic SECRET_KEY generation in setup wizard.
Added password validation with minimum security requirements.

Files modified:
- pymypersonalmap/.env
- pymypersonalmap/config/settings.py

🤖 Generated with Criticality Management Agent
```

**Features:**
- ✅ **Conventional Commits** format
- ✅ Auto-staging of involved files
- ✅ Smart message generation
- ✅ Interactive confirmation
- ✅ Auto-resolve in agent state
- ✅ Post-commit summary

**Use case:** Complete workflow - implement fix, test, and commit in one command

**Documentation:** See `COMMIT_COMMAND_GUIDE.md` for full guide

---

## Workflow Integration

### Daily Development Workflow

#### Option A: With Smart Commit (Recommended) ⭐

```bash
# 1. Morning - Check what to work on
python scripts/criticality_agent.py next

# 2. Work on the suggested task
# ... implement fixes ...
# ... run tests ...

# 3. Smart commit (does everything)
python scripts/criticality_agent.py commit C006 "ErrorHandler implemented with MySQL-specific mappings"

# 4. Push changes
git push origin main

# 5. Update CRITICITA.md manually and commit
# Move criticality to "Risolte" section
git add CRITICITA.md
git commit -m "docs: Update CRITICITA.md - C006 resolved"
git push

# 6. End of day - Generate summary
python scripts/criticality_agent.py summary
```

#### Option B: Manual Workflow

```bash
# 1. Morning - Check what to work on
python scripts/criticality_agent.py next

# 2. Work on the suggested task
# ... implement fixes ...

# 3. After completion - Mark as resolved
python scripts/criticality_agent.py resolve C006 "Error handler implemented"

# 4. Commit manually
git add pymypersonalmap/gui/error_handler.py
git commit -m "feat: Add ErrorHandler class"

# 5. Update CRITICITA.md manually
# Move criticality to "Risolte" section

# 6. End of day - Generate summary
python scripts/criticality_agent.py summary
```

### Weekly Planning Workflow

```bash
# 1. Monday - Generate roadmap for the week
python scripts/criticality_agent.py roadmap > weekly_plan.txt

# 2. Assign tasks from roadmap to team members

# 3. Friday - Generate full report
python scripts/criticality_agent.py report > weekly_report.txt

# 4. Review progress in standup
python scripts/criticality_agent.py summary
```

### Sprint Planning

```bash
# 1. Generate roadmap
python scripts/criticality_agent.py roadmap

# 2. Check total effort
python scripts/criticality_agent.py summary  # See "Total Effort"

# 3. Select criticalities for sprint based on:
#    - Team velocity (e.g., 40 hours/sprint)
#    - Priority (focus on Critical first)
#    - Dependencies (blocked items last)

# 4. Create sprint backlog from selected items
```

## State Tracking

The agent maintains state in `.criticality_state.json`:

```json
{
  "last_update": "2025-12-15T14:30:00",
  "resolved_today": [
    {
      "id": "C006",
      "title": "Nessun Error Handling in GUI",
      "timestamp": "2025-12-15T14:00:00",
      "notes": "ErrorHandler class implemented"
    }
  ],
  "current_focus": "C001",
  "history": [
    {
      "action": "resolve",
      "criticality_id": "C006",
      "timestamp": "2025-12-15T14:00:00"
    }
  ]
}
```

## Example Outputs

### Example: Summary

```
╔════════════════════════════════════════════════════════════╗
║         CRITICALITY MANAGEMENT AGENT - SUMMARY            ║
╚════════════════════════════════════════════════════════════╝

📊 Current Status:
   🔴 Critical:   2
   🟡 High:       3
   🟢 Low:        4
   ✅ Resolved:  10
   ════════════════
   📋 Total Active: 9

⚠️  Blocked: 1
⏱️  Total Effort: 23.0 hours

📈 Progress:
   Resolution Rate: 52.6%
   Active vs Target: 9/3 (target)

🎯 Next Recommended Task:
   [C001] 🔴 Credenziali di Sicurezza Non Sicure
   ⏱️  Effort: 2.0h | 📂 Security
```

### Example: Roadmap

```
╔════════════════════════════════════════════════════════════╗
║         CRITICALITY RESOLUTION ROADMAP                     ║
╚════════════════════════════════════════════════════════════╝

📍 PHASE 1: Critical Issues (URGENT)
────────────────────────────────────────────────────────────
   [C001] Credenziali di Sicurezza Non Sicure
    ⏱️  2.0h | 📂 Security | ⚠️ IN SOSPESO
    📁 Files: pymypersonalmap/.env, pymypersonalmap/config/settings.py

🚧 [C003] GUI Non Testata con Display Real
    ⏱️  7.0h | 📂 Quality Assurance | 🚧 BLOCCATO
    🚧 BLOCKED: richiede display + MySQL
    📁 Files: Tutti i componenti GUI

📍 PHASE 2: High Priority
────────────────────────────────────────────────────────────
   [C002] Build Size Ancora Sopra Target
    ⏱️  2.0h | 📂 Deployment | 🟡 IN PROGRESS
    📁 Files: build_config.spec, dist/MyPersonalMap/

💡 Total Estimated Effort: 11.0 hours
```

## Advanced Usage

### Filtering Criticalities

The agent automatically handles:
- **Blocked criticalities**: Excluded from "next task" recommendations
- **Priority sorting**: Critical → High → Low
- **Effort-based sorting**: Within same priority, lowest effort first

### Customization

You can modify the agent behavior by editing `criticality_agent.py`:

```python
# Change prioritization algorithm (line 170)
def get_next_task(self):
    # Modify sorting logic here
    available.sort(key=lambda c: (c.priority.rank, c.effort_hours))
```

### Integration with CI/CD

```yaml
# .github/workflows/criticality-check.yml
name: Criticality Check

on: [push, pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Criticality Agent
        run: |
          python scripts/criticality_agent.py summary
          python scripts/criticality_agent.py roadmap
```

## Troubleshooting

### Problem: "CRITICITA.md not found"
**Solution:** Run from project root or specify path:
```bash
cd /path/to/myPersonalMap
python scripts/criticality_agent.py summary
```

### Problem: No criticalities parsed
**Solution:** Check CRITICITA.md format matches expected structure:
- Sections: `## 🔴 Criticità Critiche`, `## 🟡 Criticità Medie`, etc.
- Items: `### N. Title`
- Required fields: `**Severità**:`, `**Categoria**:`, `**File Coinvolti**:`

### Problem: Incorrect effort estimation
**Solution:** Ensure `#### Effort:` field in CRITICITA.md contains hours:
```markdown
#### Effort: 2 ore
```

## Roadmap (Agent Improvements)

Future enhancements:
- [ ] Auto-update CRITICITA.md when marking resolved
- [ ] GitHub issue integration
- [ ] Time tracking per criticality
- [ ] Team assignment recommendations
- [ ] Burndown chart generation
- [ ] Email/Slack notifications
- [ ] Web dashboard UI

## Support

For issues or feature requests, see project documentation or open an issue.

---

**Created**: 15 Dicembre 2025
**Version**: 1.0.0
**Maintainer**: Development Team
