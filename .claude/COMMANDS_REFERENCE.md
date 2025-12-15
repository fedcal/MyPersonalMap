# Criticality Agent - Commands Reference

Quick reference for all available commands.

## All Commands

```bash
# Help
python scripts/criticality_agent.py

# Summary
python scripts/criticality_agent.py summary

# Next task
python scripts/criticality_agent.py next

# Smart commit ⭐
python scripts/criticality_agent.py commit <id> [notes]

# Roadmap
python scripts/criticality_agent.py roadmap

# Mapping table
python scripts/criticality_agent.py mapping

# Full report
python scripts/criticality_agent.py report

# Mark resolved
python scripts/criticality_agent.py resolve <id> [notes]
```

## Command Details

### `summary`
**Purpose**: Quick overview with stats
**Output**: Current status, next task suggestion, progress %
**Use when**: Daily standup, quick check

```bash
python scripts/criticality_agent.py summary
```

---

### `next`
**Purpose**: Get most urgent task to work on
**Output**: Full task details with files and description
**Use when**: Starting work session, task selection

```bash
python scripts/criticality_agent.py next
```

---

### `commit <id> [notes]` ⭐ RECOMMENDED
**Purpose**: Complete commit workflow
**Output**: Interactive commit process with confirmation
**Use when**: After implementing and testing fix

**What it does:**
1. Shows criticality info and git status
2. Generates conventional commit message
3. Stages involved files + CRITICITA.md
4. Creates commit
5. Marks as resolved
6. Shows updated summary

```bash
# Basic
python scripts/criticality_agent.py commit C001

# With notes
python scripts/criticality_agent.py commit C001 "Implemented auto SECRET_KEY generation"
```

**Commit message format:**
```
<type>: <emoji> Fix <id> - <title>

Resolves criticality <id> (<priority>)
Category: <category>

<description>

Notes: <your notes>

Files modified:
- file1
- file2

🤖 Generated with Criticality Management Agent
```

**See**: `COMMIT_COMMAND_GUIDE.md` for complete guide

---

### `roadmap`
**Purpose**: Phase-by-phase resolution plan
**Output**: All criticalities organized by priority
**Use when**: Sprint planning, weekly planning

```bash
python scripts/criticality_agent.py roadmap
```

---

### `mapping`
**Purpose**: File-to-criticality mapping table
**Output**: Table with ID | Priority | Title | Files | Status
**Use when**: Code review prep, understanding impact

```bash
python scripts/criticality_agent.py mapping
```

---

### `report`
**Purpose**: Complete analysis
**Output**: Summary + Mapping + Roadmap combined
**Use when**: Weekly reports, stakeholder updates

```bash
python scripts/criticality_agent.py report
```

---

### `resolve <id> [notes]`
**Purpose**: Mark criticality as resolved (manual workflow)
**Output**: Confirmation message
**Use when**: Manual git workflow (not using `commit` command)

```bash
# Basic
python scripts/criticality_agent.py resolve C001

# With notes
python scripts/criticality_agent.py resolve C001 "ErrorHandler implemented"
```

**Note**: This does NOT create git commit. Use `commit` command for complete workflow.

---

## Workflow Comparison

### Recommended: Smart Commit Workflow

```bash
# 1. Get task
python scripts/criticality_agent.py next

# 2. Implement fix
# ... code ...

# 3. Test
pytest tests/

# 4. Commit (does everything)
python scripts/criticality_agent.py commit C001 "Fix implemented"

# 5. Push
git push

# 6. Update CRITICITA.md manually
```

**Pros:**
- ✅ One command does everything
- ✅ Conventional commit format
- ✅ Auto-resolves in agent state
- ✅ Consistent commit messages

**Cons:**
- ⚠️ Less control over commit message
- ⚠️ Still need manual CRITICITA.md update

---

### Alternative: Manual Workflow

```bash
# 1. Get task
python scripts/criticality_agent.py next

# 2. Implement fix
# ... code ...

# 3. Test
pytest tests/

# 4. Commit manually
git add <files>
git commit -m "fix: ..."
git push

# 5. Mark resolved
python scripts/criticality_agent.py resolve C001

# 6. Update CRITICITA.md manually
```

**Pros:**
- ✅ Full control over commit
- ✅ Can use custom commit message

**Cons:**
- ⚠️ More manual steps
- ⚠️ Need to remember all steps
- ⚠️ Inconsistent commit messages

---

## Quick Reference Table

| Command | Args | Interactive | Git Action | Updates State |
|---------|------|-------------|------------|---------------|
| `summary` | None | No | No | No |
| `next` | None | No | No | No |
| `commit` | `<id> [notes]` | Yes | Stages + Commits | Yes |
| `roadmap` | None | No | No | No |
| `mapping` | None | No | No | No |
| `report` | None | No | No | No |
| `resolve` | `<id> [notes]` | No | No | Yes |

## Aliases Setup

Add to `~/.bashrc` or `~/.zshrc`:

```bash
# Basic alias
alias crit="python scripts/criticality_agent.py"

# Common commands
alias crit-sum="crit summary"
alias crit-next="crit next"
alias crit-commit="crit commit"
alias crit-map="crit roadmap"

# Usage
crit-next              # Get next task
crit-commit C001       # Commit fix
crit-sum               # Check status
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (invalid command, criticality not found, git error) |

## Examples

### Daily Workflow
```bash
# Morning
crit-next  # C001 Security

# After implementing
crit-commit C001 "Auto SECRET_KEY generation"

# Push
git push

# End of day
crit-sum
```

### Sprint Planning
```bash
# Generate roadmap for sprint
crit roadmap > sprint_plan.txt

# Check total effort
crit summary | grep "Total Effort"

# Select tasks based on team velocity
```

### Code Review
```bash
# See which files have criticalities
crit mapping

# Check specific criticality
crit next  # Shows full details
```

## Tips

1. **Always use `next`** - Ensures working on highest priority
2. **Use `commit` for consistency** - Better commit messages
3. **Check `summary` daily** - Track progress
4. **Run `roadmap` weekly** - Plan ahead
5. **Use aliases** - Faster workflow

## Documentation

- **Quick Start**: `AGENT_QUICKSTART.md`
- **Full Guide**: `README_CRITICALITY_AGENT.md`
- **Commit Guide**: `COMMIT_COMMAND_GUIDE.md`
- **Integration**: `../CRITICALITY_AGENT_INTEGRATION.md`

---

**Version**: 1.0.0
**Last Updated**: 15 Dicembre 2025
