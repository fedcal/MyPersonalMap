# Criticality Agent - Quick Start Guide

## 5-Minute Setup

### 1. Check Installation

```bash
# Test the agent
python scripts/criticality_agent.py summary
```

You should see a summary of all criticalities.

### 2. Get Your Next Task

```bash
python scripts/criticality_agent.py next
```

This will show you the most urgent criticality to work on.

### 3. Start Working

The agent will suggest:
- **ID**: Unique criticality identifier (e.g., C001)
- **Priority**: 🔴 Critical / 🟡 Medium / 🟢 Low
- **Files**: Which files need to be modified
- **Effort**: Estimated time to complete

### 4. After Completion

When you've resolved a criticality:

#### Option A: Smart Commit (Recommended) ⭐

```bash
# One command does it all: stage + commit + mark resolved
python scripts/criticality_agent.py commit C001 "Implemented fix with auto SECRET_KEY"

# Then just push and update docs
git push
# Edit CRITICITA.md and commit separately
```

#### Option B: Manual

```bash
# Mark as resolved (updates tracking file)
python scripts/criticality_agent.py resolve C001 "Implemented fix"

# Manually commit
git add <files>
git commit -m "fix: ..."

# Update CRITICITA.md (move to "Risolte" section)
# ... edit CRITICITA.md ...

# Verify update
python scripts/criticality_agent.py summary
```

## Daily Workflow

```bash
# Morning: Check what to work on
python scripts/criticality_agent.py next

# Work on the task...

# Afternoon: Mark complete and get next
python scripts/criticality_agent.py resolve C001
python scripts/criticality_agent.py next
```

## Common Commands

| Command | Description | Use When |
|---------|-------------|----------|
| `summary` | Quick stats overview | Daily standup, quick check |
| `next` | Get next task | Starting work session |
| `commit <id>` ⭐ | Smart commit fix | After implementing fix |
| `roadmap` | Full resolution plan | Sprint planning |
| `mapping` | File-to-criticality map | Code review prep |
| `report` | Complete analysis | Weekly reports |
| `resolve <id>` | Mark as resolved | Manual workflow only |

## Integration Examples

### Pre-commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash
echo "📊 Criticality Status:"
python scripts/criticality_agent.py summary
```

### Make it Executable

```bash
chmod +x scripts/criticality_agent.py

# Now you can run without 'python'
./scripts/criticality_agent.py summary
```

### Alias in .bashrc

```bash
# Add to ~/.bashrc or ~/.zshrc
alias crit="python scripts/criticality_agent.py"

# Usage
crit summary
crit next
crit roadmap
```

## Tips

1. **Run `next` at start of each work session** - ensures you're working on highest priority
2. **Use `roadmap` for planning** - see big picture of what needs to be done
3. **Check `summary` daily** - track progress towards target (3 active criticalities)
4. **Use `mapping` for code reviews** - quickly see which files have open issues

## What's Next?

See **README_CRITICALITY_AGENT.md** for complete documentation.
