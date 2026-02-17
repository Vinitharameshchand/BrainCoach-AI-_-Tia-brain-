# 📁 BrainCoach AI - Project Structure

## Complete Directory Organization

```
braincoach-ai/
│
├── 📄 app.py                           # Flask application entry point
├── 📄 config.py                        # Application configuration
├── 📄 models.py                        # SQLAlchemy database models
├── 📄 requirements.txt                 # Python package dependencies
├── 📄 .gitignore                       # Git ignore patterns
├── 📄 README.md                        # Project overview
├── 📄 PROJECT_STRUCTURE.md             # This file
│
├── 📂 routes/                          # Flask blueprints (URL routes)
│   ├── 📄 __init__.py                 # Package initializer
│   ├── 📄 auth.py                     # Authentication routes (login, register, logout)
│   ├── 📄 dashboard.py                # Parent dashboard routes
│   ├── 📄 session.py                  # Training session management
│   ├── 📄 student.py                  # Student portal routes
│   └── 📄 analytics.py                # Analytics API endpoints
│
├── 📂 utils/                           # Utility modules
│   ├── 📄 __init__.py                 # Package initializer
│   ├── 📄 advanced_scoring.py         # ML-based scoring algorithms
│   └── 📄 pdf_generator.py            # PDF report generation
│
├── 📂 templates/                       # Jinja2 HTML templates
│   ├── 📄 base.html                   # Base template with navbar
│   ├── 📄 login.html                  # Parent login page
│   ├── 📄 register.html               # Parent registration
│   ├── 📄 dashboard.html              # Parent dashboard (main page)
│   ├── 📄 dashboard_enhanced.html     # Enhanced dashboard variant
│   ├── 📄 dashboard_backup.html       # Backup version
│   ├── 📄 session.html                # Training session interface
│   ├── 📄 exercise_selection.html     # Exercise selection page
│   ├── 📄 student_login.html          # Student login (6-digit code)
│   ├── 📄 student_dashboard.html      # Student main dashboard
│   ├── 📄 student_training.html       # Student training interface
│   ├── 📄 student_sessions.html       # Student session history
│   └── 📄 child_sessions.html         # Parent view of child sessions
│
├── 📂 static/                          # Static assets
│   ├── 📂 css/
│   │   └── 📄 style.css               # Main stylesheet (modern premium theme)
│   ├── 📂 js/
│   │   └── 📄 hands.js                # MediaPipe hand tracking logic
│   ├── 📂 images/                     # Image assets
│   └── 📂 videos/                     # Exercise demo videos
│
├── 📂 migrations/                      # Database migrations (Alembic/Flask-Migrate)
│   └── 📄 (migration files)
│
├── 📂 scripts/                         # Utility & maintenance scripts
│   ├── 📄 add_child_access_code.py    # Add access codes to existing children
│   ├── 📄 add_columns_migration.py    # Column migration helper
│   ├── 📄 migrate_access_codes.py     # Improved access code migration
│   ├── 📄 migrate_database.py         # Database migration runner
│   └── 📄 seed.py                     # Seed initial/demo data
│
├── 📂 tests/                           # Test suite
│   ├── 📄 __init__.py                 # Package initializer
│   ├── 📄 test_advanced_scoring.py    # Tests for scoring algorithms
│   └── 📄 test_dashboard.py           # Tests for dashboard
│
├── 📂 docs/                            # Documentation
│   ├── 📄 QUICK_START.md              # Quick start guide
│   ├── 📄 STUDENT_SYSTEM.md           # Student system documentation
│   ├── 📄 PARENT_STUDENT_INTEGRATION.md  # Integration guide
│   ├── 📄 SYSTEM_ARCHITECTURE.md      # Architecture overview
│   ├── 📄 UI_IMPROVEMENTS.md          # UI theme documentation
│   ├── 📄 LINTING_NOTES.md            # Linting & template notes
│   ├── 📄 TEST_RESULTS.md             # Test results & reports
│   ├── 📄 ADVANCED_SCORING_DOCUMENTATION.md  # ML algorithms explained
│   ├── 📄 INTEGRATION_COMPLETE.md     # Integration completion report
│   ├── 📄 INTEGRATION_GUIDE.md        # Integration guide
│   ├── 📄 SESSION_JOIN_FLOW.md        # Session join flow docs
│   ├── 📄 MATHEMATICAL_FORMULAS_SUMMARY.md  # Math formulas used
│   ├── 📄 FRONTEND_ENHANCEMENTS.md    # Frontend improvements
│   ├── 📄 IMPROVEMENTS_SUMMARY.md     # Summary of improvements
│   ├── 📄 BUGFIXES_APPLIED.md         # Bug fixes log
│   ├── 📄 CHART_FIX.md                # Chart-specific fixes
│   ├── 📄 CHART_INFINITE_LOOP_FIX.md  # Infinite loop fix
│   ├── 📄 IMPROVEMENT_PLAN.md         # Future improvement plans
│   ├── 📄 VERIFICATION_REPORT.md      # Verification report
│   └── 📄 QUICK_START.txt             # Plain text quick start
│
├── 📂 instance/                        # Instance-specific files (not in git)
│   └── 📄 braincoach.db               # SQLite database file
│
├── 📂 reports/                         # Generated PDF reports
│   ├── 📂 child_1/                    # Reports for child ID 1
│   ├── 📂 child_4/                    # Reports for child ID 4
│   └── 📂 child_*/                    # Per-child folders
│
├── 📂 .vscode/                         # VS Code configuration
│   └── 📄 settings.json               # Editor settings (Jinja2 support)
│
├── 📂 .claude/                         # Claude AI persistent memory
│   └── 📂 projects/
│       └── 📂 memory/                 # Memory files
│
└── 📂 venv/                            # Virtual environment (not in git)
    └── 📂 (Python packages)
```

## 📦 Key Folders Explained

### `/routes` - Application Routes
Contains Flask blueprints that define URL endpoints and their handlers.

**Purpose**: Organize routes by feature/module
- `auth.py` - Login, register, logout
- `dashboard.py` - Parent dashboard, child management
- `session.py` - Training session lifecycle
- `student.py` - Student portal (login, exercises, history)
- `analytics.py` - Analytics API for charts/data

### `/utils` - Utility Modules
Reusable helper functions and algorithms.

**Purpose**: Keep business logic separate from routes
- `advanced_scoring.py` - ML algorithms (EMA, RMSE, Z-score, regression)
- `pdf_generator.py` - Generate session report PDFs

### `/templates` - HTML Templates
Jinja2 templates for rendering web pages.

**Purpose**: Frontend presentation layer
- Parent views: dashboard, session management
- Student views: login, exercises, progress
- Shared: base.html with navigation

### `/static` - Static Assets
CSS, JavaScript, images, videos.

**Purpose**: Client-side resources
- `css/style.css` - Modern premium theme (glass morphism, gradients)
- `js/hands.js` - MediaPipe hand tracking
- `videos/` - Exercise demonstration videos

### `/scripts` - Utility Scripts
One-time or maintenance scripts.

**Purpose**: Database migrations, seeding, utilities
- Not part of the main app
- Run manually when needed
- Examples: migrations, seeding data

### `/tests` - Test Suite
Automated tests for the application.

**Purpose**: Quality assurance
- Unit tests
- Integration tests
- Test data fixtures

### `/docs` - Documentation
Project documentation and guides.

**Purpose**: Knowledge base
- Setup guides
- Architecture docs
- Feature documentation
- API references

### `/instance` - Instance Files
Instance-specific files (database, configs).

**Purpose**: Per-deployment data
- Contains SQLite database
- Not committed to git
- Created automatically

### `/reports` - Generated Reports
PDF reports generated by the system.

**Purpose**: Store session reports
- Organized by child ID
- Generated on session completion
- Optionally emailed to parents

## 🔧 Configuration Files

### `app.py`
- Flask application factory
- Blueprint registration
- Database initialization
- Main entry point

### `config.py`
- Application settings
- Database URI
- Secret keys
- Debug flags

### `models.py`
- SQLAlchemy models
- Database schema
- Relationships
- Model methods

### `requirements.txt`
- Python package dependencies
- Version specifications
- Install with: `pip install -r requirements.txt`

### `.gitignore`
- Files/folders to exclude from git
- Virtual environment
- Database files
- IDE settings
- Secrets

### `.vscode/settings.json`
- VS Code configuration
- Jinja2 template support
- Linting settings

## 🎯 File Naming Conventions

### Python Files
- **snake_case**: `advanced_scoring.py`, `pdf_generator.py`
- **Blueprint names**: Match folder (e.g., `student.py` blueprint)
- **Test files**: Prefix with `test_` (e.g., `test_dashboard.py`)

### HTML Templates
- **snake_case**: `student_login.html`, `child_sessions.html`
- **Descriptive names**: Clearly indicate purpose
- **Consistent prefixes**: `student_*` for student portal

### Documentation
- **UPPERCASE.md**: Important docs (README.md)
- **Title_Case.md**: Feature docs (UI_IMPROVEMENTS.md)
- **Descriptive**: Clear purpose from filename

## 🚀 Adding New Features

### New Route/Page
1. Create blueprint in `routes/new_feature.py`
2. Register in `app.py`
3. Add template in `templates/new_feature.html`
4. Add styles in `static/css/style.css` (if needed)
5. Add docs in `docs/NEW_FEATURE.md`

### New Database Model
1. Add model class in `models.py`
2. Create migration script in `scripts/`
3. Run migration
4. Update docs

### New Utility Function
1. Add to appropriate file in `utils/`
2. Or create new file for major feature
3. Document with docstrings
4. Add tests in `tests/`

## 📚 Import Patterns

### Absolute Imports (Preferred)
```python
from models import db, Parent, Child
from utils.advanced_scoring import calculate_score
from routes.auth import auth
```

### Relative Imports (Within package)
```python
from .advanced_scoring import calculate_score
from ..models import Child
```

## 🎨 Code Organization Best Practices

1. **Separation of Concerns**
   - Routes handle HTTP requests/responses
   - Utils contain business logic
   - Models define data structure

2. **Single Responsibility**
   - Each file has one clear purpose
   - Functions do one thing well
   - Classes represent one concept

3. **DRY (Don't Repeat Yourself)**
   - Reuse utility functions
   - Shared templates extend base.html
   - Common styles in style.css

4. **Clear Naming**
   - Descriptive variable names
   - Consistent conventions
   - Self-documenting code

5. **Documentation**
   - Docstrings for functions
   - Comments for complex logic
   - README for each major feature

## 🔍 Finding Things

### "Where do I...?"

**Add a new page?**
- Route: `routes/`
- Template: `templates/`
- Register: `app.py`

**Modify the database?**
- Models: `models.py`
- Migration: `scripts/`

**Change styling?**
- CSS: `static/css/style.css`
- Templates: `templates/`

**Add business logic?**
- Utility: `utils/`
- Or in route if simple

**Write tests?**
- Tests: `tests/`
- Name: `test_feature.py`

**Add documentation?**
- Docs: `docs/`
- Update: `README.md`

## 📊 Folder Size Guidelines

| Folder | Typical Size | Notes |
|--------|--------------|-------|
| `/routes` | 5-10 files | One per feature area |
| `/utils` | 3-8 files | Keep focused |
| `/templates` | 10-20 files | One per page/component |
| `/static/css` | 1-3 files | Consolidate styles |
| `/static/js` | 5-15 files | Modular JavaScript |
| `/tests` | Matches routes | One test per route file |
| `/docs` | 10-30 files | Comprehensive docs |
| `/scripts` | 5-10 files | Maintenance scripts |

## ✅ Structure Benefits

This organization provides:

✅ **Clear Separation**: Easy to find things
✅ **Scalability**: Easy to add features
✅ **Maintainability**: Easy to modify
✅ **Testability**: Easy to test
✅ **Collaboration**: Team-friendly
✅ **Documentation**: Self-explanatory
✅ **Professional**: Industry standard

---

**📁 A well-organized project is a joy to work with!**
