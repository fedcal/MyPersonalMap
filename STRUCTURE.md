# Project Structure

This document describes the organization of the My Personal Map project.

## Overview

My Personal Map follows a clean, layered architecture with clear separation of concerns. The project is organized into logical modules following Python best practices.

```
myPersonalMap/
├── .claude/                      # Claude Code configuration
│   ├── agents/                  # Custom Claude Code agents
│   │   ├── backend-dev.md       # Backend development agent
│   │   ├── database-expert.md   # Database specialist agent
│   │   ├── documentation-writer.md # Documentation agent
│   │   └── test-engineer.md     # Testing specialist agent
│   ├── commands/                # Custom slash commands
│   │   ├── add-endpoint.md      # Command to add API endpoint
│   │   ├── add-model.md         # Command to add database model
│   │   ├── add-test.md          # Command to add tests
│   │   ├── debug-spatial.md     # Spatial debugging command
│   │   ├── document-api.md      # API documentation command
│   │   └── setup-project.md     # Project setup command
│   ├── AGENT_QUICKSTART.md      # Quick guide for using agents
│   ├── COMMANDS_REFERENCE.md    # Command reference guide
│   ├── COMMIT_COMMAND_GUIDE.md  # Guide for commit commands
│   ├── README.md                # Claude Code configuration docs
│   ├── settings.json            # Claude Code settings
│   └── settings.local.json      # Local settings override
├── .github/                      # GitHub configuration (CI/CD, templates)
├── docs/                         # Project documentation
│   ├── development/              # Developer documentation
│   ├── guides/                   # User guides and tutorials
│   ├── planning/                 # Project planning documents
│   ├── BUILD_NOTES.md           # Build process notes
│   ├── CRITICALITY_AGENT_INTEGRATION.md
│   ├── CRITICITA.md             # Criticality analysis
│   ├── DESIGN_SYSTEM.md         # Design system documentation
│   └── INSTALL.md               # Installation guide
├── scripts/                      # Build and development scripts
│   ├── build/                   # Platform-specific build scripts
│   │   ├── build_linux.sh       # Linux build script
│   │   ├── build_macos.sh       # macOS build script
│   │   └── build_windows.bat    # Windows build script
│   ├── criticality_agent.py     # Code criticality analysis tool
│   ├── README_CRITICALITY_AGENT.md # Criticality agent docs
│   └── README.md                # Scripts documentation
├── pymypersonalmap/             # Main application package
│   ├── api/                     # REST API layer
│   │   ├── __init__.py
│   │   └── routes/              # API route definitions
│   │       └── __init__.py
│   ├── config/                  # Application configuration
│   │   ├── __init__.py
│   │   └── settings.py          # Settings loaded from .env
│   ├── database/                # Database session management
│   │   ├── __init__.py
│   │   └── session.py           # SQLAlchemy engine and session
│   ├── gui/                     # Desktop GUI (CustomTkinter)
│   │   ├── app.py               # Main GUI application
│   │   ├── backend_manager.py   # FastAPI backend thread manager
│   │   ├── config_manager.py    # GUI configuration manager
│   │   ├── error_handler.py     # Error handling and logging
│   │   ├── setup_wizard.py      # First-run setup wizard
│   │   ├── splash.py            # Splash screen
│   │   ├── theme.py             # Theme management
│   │   ├── assets/              # Icons, images, fonts
│   │   ├── components/          # Reusable UI components
│   │   │   ├── custom_button.py
│   │   │   ├── custom_sidebar.py
│   │   │   ├── map_viewer.py    # Folium map integration
│   │   │   └── __init__.py
│   │   ├── layouts/             # Layout components
│   │   │   ├── main_layout.py
│   │   │   └── __init__.py
│   │   ├── themes/              # Theme configuration files
│   │   │   └── mypersonalmap_theme.json
│   │   └── __init__.py
│   ├── models/                  # SQLAlchemy models (database entities)
│   │   ├── __init__.py
│   │   ├── user.py              # User model
│   │   ├── marker.py            # Marker model (lat/lon storage)
│   │   ├── labels.py            # Label model
│   │   └── marker_label.py      # Many-to-many association
│   ├── repository/              # Data access layer (repository pattern)
│   │   ├── __init__.py
│   │   ├── user_repository.py   # User data access
│   │   ├── marker_repository.py # Marker CRUD operations
│   │   └── labels_repository.py # Label operations
│   ├── services/                # Business logic layer
│   │   ├── __init__.py
│   │   ├── geo_utils.py         # Geographic utilities (Haversine, etc.)
│   │   ├── user_service.py      # User business logic
│   │   ├── marker_service.py    # Marker business logic
│   │   └── label_service.py     # Label business logic
│   ├── tests/                   # Test suite
│   │   ├── __init__.py
│   │   ├── conftest.py          # Pytest fixtures and configuration
│   │   ├── unit/                # Unit tests (isolated components)
│   │   │   ├── __init__.py
│   │   │   ├── test_geo_utils.py    # Geographic utilities tests
│   │   │   └── test_models.py       # Database model tests
│   │   └── integration/         # Integration tests (multiple components)
│   │       ├── __init__.py
│   │       └── test_gui_components.py # GUI integration tests
│   ├── utils/                   # Utility functions and helpers
│   │   └── __init__.py
│   ├── main.py                  # Application entry point
│   ├── requirements.txt         # Python dependencies
│   └── mypersonalmap.db        # SQLite database file (gitignored)
├── build/                       # Build artifacts (gitignored)
├── dist/                        # Distribution packages (gitignored)
├── .env                         # Environment variables (gitignored)
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
├── build_config.spec            # PyInstaller build configuration
├── pyproject.toml               # Python project metadata and config
├── README.md                    # Main project readme
├── CLAUDE.md                    # Claude Code development instructions
├── STRUCTURE.md                 # This file - project structure documentation
└── LICENSE                      # Project license (MIT)
```

## Architecture Layers

The application follows a **5-layer architecture**:

### 1. Presentation Layer (`gui/`)
- **Purpose**: User interface and interaction
- **Technology**: CustomTkinter (desktop framework)
- **Components**:
  - Main window and layouts
  - Reusable UI components (buttons, sidebar, map viewer)
  - Theme management
  - Error handling and user feedback
- **Integration**: Communicates with backend via HTTP (localhost:8000)

### 2. API Layer (`api/`, `main.py`)
- **Purpose**: REST API endpoints
- **Technology**: FastAPI (embedded in background thread for desktop app)
- **Responsibilities**:
  - HTTP request/response handling
  - Input validation (Pydantic models)
  - CORS middleware
  - Authentication and authorization
  - Swagger documentation at `/docs`

### 3. Business Logic Layer (`services/`)
- **Purpose**: Core business logic and domain operations
- **Pattern**: Service layer pattern
- **Responsibilities**:
  - Marker operations (create, update, search)
  - Geographic calculations (distance, bounding box)
  - Label management
  - User authentication and authorization
  - Data validation and transformation

### 4. Data Access Layer (`repository/`)
- **Purpose**: Database operations abstraction
- **Pattern**: Repository pattern
- **Responsibilities**:
  - CRUD operations for each entity
  - Complex queries (spatial queries, filtering)
  - Database transaction management
  - Query optimization

### 5. Database Layer (`database/`, `models/`)
- **Purpose**: Data persistence
- **Technology**: SQLite (embedded, zero-config)
- **Components**:
  - SQLAlchemy ORM models
  - Database session management
  - Schema migrations (Alembic)

## Key Design Patterns

### Repository Pattern
Data access is abstracted through repository classes, making the codebase more testable and maintainable.

```python
# Example: Marker repository usage
from pymypersonalmap.repository.marker_repository import get_marker_by_id

def get_marker_details(db, marker_id):
    return get_marker_by_id(db, marker_id)
```

### Service Layer Pattern
Business logic is isolated in service classes, separating concerns from API controllers and repositories.

```python
# Example: Service layer usage
from pymypersonalmap.services.marker_service import create_marker

marker = create_marker(db, title="Milan", lat=45.46, lon=9.19, user_id=1)
```

### Dependency Injection
FastAPI's dependency injection is used for database sessions and service initialization.

```python
@app.post("/api/v1/markers")
def create_marker_endpoint(
    marker_data: MarkerCreate,
    db: Session = Depends(get_db)
):
    return create_marker(db, **marker_data.dict())
```

## Directory Purposes

### `/.claude` - Claude Code Configuration
Claude Code AI assistant configuration and customizations:
- **agents/**: Custom specialized agents for specific tasks
  - `backend-dev.md`: Backend development specialist
  - `database-expert.md`: Database design and optimization
  - `documentation-writer.md`: Technical documentation
  - `test-engineer.md`: Test creation and debugging
- **commands/**: Custom slash commands for common workflows
  - `/add-endpoint`: Scaffold new API endpoints
  - `/add-model`: Create new database models
  - `/add-test`: Generate test files
  - `/debug-spatial`: Debug geographic/spatial issues
  - `/document-api`: Generate API documentation
  - `/setup-project`: Initialize project setup
- **Documentation**: Quick references and guides
  - `AGENT_QUICKSTART.md`: How to use custom agents
  - `COMMANDS_REFERENCE.md`: Available commands
  - `COMMIT_COMMAND_GUIDE.md`: Git commit workflow

### `/docs` - Documentation
Comprehensive project documentation organized by audience:
- **development/**: Architecture, database schema, API docs (for developers)
- **guides/**: Installation, quick start, user guide (for users and new developers)
- **planning/**: Roadmap, use cases (for project management)

### `/scripts` - Build & Development Scripts
Build automation and development tools:
- **build/**: Platform-specific build scripts (Linux, macOS, Windows)
- **criticality_agent.py**: Code complexity and criticality analysis tool
- **Documentation**: README files for scripts usage

### `/pymypersonalmap` - Main Package
The core application code following Python package structure:
- Clear separation between layers (API, services, repository, models)
- GUI isolated in its own module
- Tests co-located with source code
- Configuration centralized in `config/`

## Database Structure

### SQLite Embedded Database
- **Location**: `pymypersonalmap/mypersonalmap.db`
- **Format**: SQLite 3 (single-file, zero-config)
- **Coordinates**: Stored as separate `latitude` and `longitude` REAL columns
- **Indexes**: Spatial indexes on lat/lon for performance

### Models
- **User**: Authentication and user data
- **Marker**: Geographic markers with lat/lon, metadata, labels
- **Label**: Categorization tags (system and user-defined)
- **MarkerLabel**: Many-to-many association table

## Testing Structure

### Unit Tests (`tests/unit/`)
Test individual components in isolation:
- `test_models.py`: Database model operations
- `test_geo_utils.py`: Geographic calculation functions
- Mock external dependencies
- Fast execution

### Integration Tests (`tests/integration/`)
Test multiple components working together:
- `test_gui_components.py`: GUI and backend integration
- `test_api_endpoints.py`: API endpoints with database (future)
- Use test database
- Slower but more comprehensive

### Test Configuration
- **Fixtures**: Defined in `conftest.py`
- **Database**: In-memory SQLite for test isolation
- **Coverage**: Target 80%+ coverage for critical paths
- **Runner**: pytest with coverage reporting

## Build and Distribution

### PyInstaller Configuration
- **Spec File**: `build_config.spec`
- **Output**: Standalone executables for Windows, macOS, Linux
- **Bundle**: Single-file or directory bundle
- **Assets**: GUI themes, icons bundled automatically

### Build Scripts
Platform-specific scripts in `scripts/build/`:
- Handle dependencies, compilation, packaging
- Create installers (DMG, MSI, AppImage)
- Sign executables (macOS, Windows)

## Configuration Management

### Environment Variables
- **Development**: `pymypersonalmap/.env`
- **Production**: `~/.mypersonalmap/.env`
- **Template**: `.env.example` (version controlled)

### Settings Priority
1. Environment variables
2. `.env` file
3. Default values in `config/settings.py`

## Development Workflow

### Setup
```bash
# Clone and setup
git clone <repo>
cd myPersonalMap
python3 -m venv venv
source venv/bin/activate
pip install -r pymypersonalmap/requirements.txt

# Create .env
cp .env.example pymypersonalmap/.env
```

### Running
```bash
# Desktop GUI + Backend
python3 pymypersonalmap/main.py

# Backend only (development)
python3 pymypersonalmap/main.py --backend-only
```

### Testing
```bash
# All tests
pytest

# Specific category
pytest pymypersonalmap/tests/unit/
pytest pymypersonalmap/tests/integration/

# With coverage
pytest --cov=pymypersonalmap
```

### Building
```bash
# Linux
./scripts/build/build_linux.sh

# macOS
./scripts/build/build_macos.sh

# Windows
scripts\build\build_windows.bat
```

## Adding New Features

### Adding a New Model
1. Create model in `models/` (inherit from `Base`)
2. Create repository in `repository/`
3. Create service in `services/`
4. Add API routes in `api/routes/`
5. Create migration: `alembic revision --autogenerate`
6. Write tests in `tests/unit/` and `tests/integration/`

### Adding a New API Endpoint
1. Define Pydantic request/response models
2. Create route function in `api/routes/`
3. Use service layer for business logic
4. Inject database session with `Depends(get_db)`
5. Register router in `main.py`
6. Add integration tests

### Adding a New GUI Component
1. Create component class in `gui/components/`
2. Follow CustomTkinter patterns
3. Integrate with backend via HTTP requests
4. Add to appropriate layout in `gui/layouts/`
5. Update theme in `gui/themes/` if needed

## Code Organization Principles

### Single Responsibility
Each module, class, and function has one clear purpose.

### Separation of Concerns
- GUI doesn't access database directly (goes through API)
- Services don't handle HTTP requests (that's API's job)
- Repositories don't contain business logic (that's services' job)

### Dependency Direction
Dependencies flow downward through layers:
```
GUI → API → Services → Repository → Models → Database
```

### Testability
- Dependency injection for easy mocking
- Repository pattern allows swapping database implementations
- Service layer can be tested without API or GUI

## Documentation Standards

### Code Documentation
- Docstrings for all public functions and classes
- Type hints for function parameters and returns
- Inline comments for complex logic only

### Documentation Files
- `README.md`: Quick overview, getting started
- `CLAUDE.md`: Development instructions for AI assistants
- `STRUCTURE.md`: This file - project organization
- `docs/`: Detailed documentation by topic

### API Documentation
- Auto-generated from FastAPI decorators
- Available at `http://localhost:8000/docs` (Swagger UI)
- Pydantic models provide schema validation

## Maintenance and Evolution

### Adding Dependencies
Update `pymypersonalmap/requirements.txt` and rebuild virtual environment.

### Database Migrations
Use Alembic for schema changes:
```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

### Version Management
- Update version in `pyproject.toml`
- Tag releases in git: `git tag v1.0.0`
- Update `CHANGELOG.md` (future)

## Security Considerations

### Sensitive Data
- Database file: gitignored, stored in user directory
- `.env` file: gitignored, contains secrets
- API keys: environment variables only
- User passwords: hashed with bcrypt

### API Security
- JWT authentication for API endpoints (future)
- CORS configuration in `main.py`
- Input validation via Pydantic models
- SQL injection prevention via SQLAlchemy ORM

---

**Last Updated**: December 2024
**Version**: 1.0.0
**Maintained By**: Development Team
