# Scripts Directory

This directory contains utility scripts and agents for project management and automation.

## Available Tools

### 📊 Criticality Management Agent

**Purpose**: Automated management and prioritization of project criticalities

**Quick Start:**
```bash
python scripts/criticality_agent.py summary
```

**Documentation:**
- **Quick Start**: `AGENT_QUICKSTART.md` - Get started in 5 minutes
- **Full Guide**: `README_CRITICALITY_AGENT.md` - Complete documentation

**Common Commands:**
```bash
# Get summary of all criticalities
python scripts/criticality_agent.py summary

# Get next task to work on
python scripts/criticality_agent.py next

# ⭐ Smart commit (recommended workflow)
python scripts/criticality_agent.py commit C001 "Fix notes"

# Generate resolution roadmap
python scripts/criticality_agent.py roadmap

# See file-to-criticality mapping
python scripts/criticality_agent.py mapping

# Mark criticality as resolved (manual workflow)
python scripts/criticality_agent.py resolve C001 "Notes here"

# Full report (summary + roadmap + mapping)
python scripts/criticality_agent.py report
```

**Features:**
- ✅ Automatic parsing of `CRITICITA.md`
- ✅ Priority-based task recommendations
- ✅ Progress tracking with state management
- ✅ Multiple report formats (summary, roadmap, mapping, full)
- ✅ Smart blocked criticality detection
- ✅ Resolution history tracking

**Workflow Integration:**
The agent integrates seamlessly into your daily development workflow:

1. **Morning**: `python scripts/criticality_agent.py next` - see what to work on
2. **Work**: Implement the suggested fix
3. **Complete**: `python scripts/criticality_agent.py resolve C001` - mark done
4. **Repeat**: Get next task

**Use Cases:**
- Daily standup preparation
- Sprint planning
- Task prioritization
- Progress tracking
- Code review preparation
- Team coordination
- Stakeholder reporting

## Future Tools

Additional scripts planned for this directory:
- Build automation scripts
- Database migration helpers
- Code quality checkers
- Performance profilers
- Deployment utilities

## Contributing

When adding new scripts to this directory:
1. Create the script with descriptive name
2. Add shebang line (`#!/usr/bin/env python3`)
3. Include docstring with usage examples
4. Make executable (`chmod +x script.py`)
5. Update this README with:
   - Script name and purpose
   - Quick usage example
   - Link to detailed documentation (if applicable)

## Directory Structure

```
scripts/
├── README.md                          # This file
├── AGENT_QUICKSTART.md                # 5-minute guide to criticality agent
├── README_CRITICALITY_AGENT.md        # Full criticality agent documentation
├── criticality_agent.py               # Criticality management agent
└── .criticality_state.json            # Agent state (auto-generated)
```

## Getting Help

For issues or questions:
1. Check the relevant README file in this directory
2. Run script with `-h` or `--help` flag (if supported)
3. See main project documentation in `doc/` directory
4. Open an issue on the project repository

---

**Last Updated**: 15 Dicembre 2025
**Maintainer**: Development Team
