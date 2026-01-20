# Project Tree - Swing Trading Filter (IDX)

Visual representation of the complete project structure after reorganization.

## 📁 Complete Project Structure

```
swing-trading-filter-idx/
│
├── 📄 README.md                          # Main project documentation
├── 📄 LICENSE                            # MIT License
├── 📄 requirements.txt                   # Python dependencies
├── 📄 .gitignore                         # Git ignore rules (430 lines)
├── 📄 MIGRATION_CHECKLIST.md            # Migration guide
├── 📄 REORGANIZATION_SUMMARY.md         # Summary of changes
│
├── 📂 src/                               # 💻 SOURCE CODE
│   ├── __init__.py
│   ├── main.py                          # CLI entry point
│   ├── config.py                        # Configuration settings
│   ├── data.py                          # Data fetching (Yahoo Finance)
│   ├── strategy.py                      # Trading strategy logic
│   ├── rate_limiter.py                  # API rate limiting
│   │
│   └── 📂 backtest/                     # Backtesting engine
│       ├── __init__.py
│       ├── engine.py                    # Main backtest engine
│       ├── portfolio.py                 # Portfolio management
│       ├── metrics.py                   # Performance metrics
│       └── reports.py                   # Report generation
│
├── 📂 docs/                              # 📚 DOCUMENTATION
│   ├── DIRECTORY_STRUCTURE.md           # Complete directory reference (364 lines)
│   ├── ORGANIZATION_GUIDE.md            # Workflow & maintenance guide (587 lines)
│   ├── QUICK_START.md                   # Quick start guide (304 lines)
│   ├── RATE_LIMIT_FIXES.md              # Rate limit documentation (317 lines)
│   ├── BACKTESTING_SUMMARY.md           # Backtesting guide
│   └── GEMINI.md                        # Project objectives
│
├── 📂 watchlists/                        # 📊 STOCK WATCHLISTS
│   ├── default.txt                      # Personal picks (2 stocks)
│   ├── lq45.txt                         # LQ45 blue chips (47 stocks)
│   └── idx_liquid.txt                   # Liquid stocks (130 stocks)
│
├── 📂 output/                            # 📁 GENERATED FILES (not in git)
│   ├── README.md                        # Output directory guide
│   │
│   ├── 📂 scans/                        # Daily scan results
│   │   └── .gitkeep                     # README + placeholder
│   │
│   ├── 📂 backtests/                    # Backtest reports
│   │   └── .gitkeep                     # README + placeholder
│   │
│   └── 📂 charts/                       # Generated charts
│       └── .gitkeep                     # README + placeholder
│
├── 📂 logs/                              # 📝 APPLICATION LOGS (not in git)
│   └── .gitkeep                         # README + placeholder
│
├── 📂 scripts/                           # 🔧 UTILITY SCRIPTS
│   ├── cleanup.sh                       # Maintenance utility (259 lines)
│   ├── run_scanner.sh                   # Daily scan automation
│   └── todo.txt                         # Development TODO
│
├── 📂 cache/                             # 💾 YFINANCE CACHE (not in git)
│   ├── tkr-tz.db                        # Timezone database
│   ├── tkr-tz.db-shm                    # Shared memory
│   ├── tkr-tz.db-wal                    # Write-ahead log
│   └── cookies.db                       # Session cookies
│
└── 📂 venv/                              # 🐍 VIRTUAL ENVIRONMENT (not in git)
    └── (Python packages)
```

## 📊 File Statistics

### By Category

| Category | Files | Lines | Notes |
|----------|-------|-------|-------|
| **Source Code** | 10 | ~3,000 | Python modules |
| **Documentation** | 9 | ~2,400 | Markdown guides |
| **Scripts** | 2 | ~300 | Bash utilities |
| **Watchlists** | 3 | 179 | Stock symbols |
| **Configuration** | 3 | ~450 | Setup files |
| **Total** | **27** | **~6,329** | Tracked by git |

### Generated Files (Not in Git)

| Category | Location | Pattern |
|----------|----------|---------|
| Scan Results | `output/scans/` | `*_scan_*.txt` |
| Backtest Reports | `output/backtests/` | `backtest_*.txt` |
| Charts | `output/charts/` | `*.png` |
| Logs | `logs/` | `*.log` |
| Cache | `cache/` | `*.db*` |

## 🎯 Key Directories

### 📦 `src/` - Source Code
**Purpose:** All Python application code  
**Tracked:** ✅ Yes (version controlled)  
**Files:** 10 Python modules  
**Key Files:**
- `main.py` - Entry point and CLI
- `config.py` - All configuration parameters
- `data.py` - Yahoo Finance API integration
- `strategy.py` - EMA crossover strategy
- `backtest/` - Complete backtesting framework

### 📚 `docs/` - Documentation
**Purpose:** Comprehensive project documentation  
**Tracked:** ✅ Yes (version controlled)  
**Files:** 6 markdown documents  
**Total Lines:** ~2,400 lines  
**Key Guides:**
- `QUICK_START.md` - Getting started
- `ORGANIZATION_GUIDE.md` - Workflows and best practices
- `DIRECTORY_STRUCTURE.md` - Complete reference
- `RATE_LIMIT_FIXES.md` - API rate limiting details

### 📊 `watchlists/` - Stock Lists
**Purpose:** Pre-configured stock watchlists  
**Tracked:** ✅ Yes (version controlled)  
**Files:** 3 text files (179 total stocks)  
**Format:** One ticker per line (e.g., `BBCA.JK`)  
**Usage:** `python -m src.main --list lq45`

### 📁 `output/` - Generated Files
**Purpose:** All scanner and backtest outputs  
**Tracked:** ❌ No (ignored by git)  
**Structure:**
- `scans/` - Daily scan results
- `backtests/` - Backtest reports
- `charts/` - Performance charts

### 📝 `logs/` - Application Logs
**Purpose:** Debug and error logs  
**Tracked:** ❌ No (ignored by git)  
**Files:** Auto-generated `.log` files  
**Rotation:** Keep last 30 days

### 🔧 `scripts/` - Utility Scripts
**Purpose:** Automation and maintenance  
**Tracked:** ✅ Yes (version controlled)  
**Files:** 2 bash scripts  
**Key Script:** `cleanup.sh` - Interactive maintenance utility

## 🔒 What's Ignored by Git

### AI Tools & Agents (20+ tools)
```
.agents/          # Amp agent files
.cursor/          # Cursor IDE
.copilot/         # GitHub Copilot
.codeium/         # Codeium
.tabnine/         # Tabnine
.opencode/        # OpenCode
.windsurf/        # Windsurf
.continue/        # Continue.dev
.aider/           # Aider
.git/opencode/    # OpenCode git integration
# ... and 10+ more
```

### Generated Files
```
output/           # All output files
logs/             # All log files
cache/            # YFinance cache
*.png             # Charts
*.csv             # Data exports
*.log             # Log files
```

### Development
```
venv/             # Virtual environment
__pycache__/      # Python bytecode
*.pyc             # Compiled Python
.DS_Store         # macOS files
Thumbs.db         # Windows files
.vscode/          # VS Code settings
.idea/            # PyCharm settings
```

### Security
```
.env              # Environment variables
secrets.json      # API keys
*.pem             # Certificates
*.key             # Private keys
```

## 📈 Growth Statistics

### Before Reorganization
- **Structure:** Flat, unorganized
- **Documentation:** 5 files in root
- **Scripts:** 2 files in root
- **Git Ignore:** 65 lines
- **Output Management:** None
- **AI Tool Support:** None

### After Reorganization
- **Structure:** Organized, hierarchical
- **Documentation:** 9 files in `docs/`
- **Scripts:** 3 files in `scripts/`
- **Git Ignore:** 430 lines (+561%)
- **Output Management:** Structured directories
- **AI Tool Support:** 20+ tools excluded

## 🎨 Color Legend

| Icon | Meaning |
|------|---------|
| 📂 | Directory |
| 📄 | File (general) |
| 💻 | Source code |
| 📚 | Documentation |
| 📊 | Data/Lists |
| 📁 | Output (generated) |
| 📝 | Logs |
| 🔧 | Scripts/Tools |
| 💾 | Cache |
| 🐍 | Python/Environment |

## 🚀 Quick Navigation

### Development
```bash
cd src/              # Source code
cd src/backtest/     # Backtesting engine
```

### Documentation
```bash
cd docs/             # All documentation
cat docs/QUICK_START.md
```

### Running
```bash
python -m src.main --list lq45                    # Run scan
python -m src.main --backtest                     # Run backtest
```

### Output
```bash
cd output/scans/     # Scan results
cd output/backtests/ # Backtest reports
cd output/charts/    # Charts
```

### Maintenance
```bash
./scripts/cleanup.sh # Interactive cleanup
cd logs/             # View logs
```

## 📦 Installation Locations

### System-Wide
```
~/.gitconfig         # Git configuration
~/.bashrc            # Shell aliases
```

### Project-Specific
```
./venv/              # Virtual environment
./cache/             # Data cache
./output/            # Generated files
./logs/              # Application logs
```

## 🔍 Finding Files

### By Type
```bash
# Find all Python files
find src/ -name "*.py"

# Find all documentation
find docs/ -name "*.md"

# Find all watchlists
find watchlists/ -name "*.txt"

# Find recent scans
find output/scans/ -name "*.txt" -mtime -7
```

### By Content
```bash
# Find files containing "EMA"
grep -r "EMA" src/

# Find files with rate limit config
grep -r "REQUEST_DELAY" src/
```

## 📊 Disk Usage Estimates

| Directory | Typical Size | Notes |
|-----------|--------------|-------|
| `src/` | < 1 MB | Source code |
| `docs/` | < 1 MB | Documentation |
| `watchlists/` | < 100 KB | Stock lists |
| `output/` | 10-100 MB | Grows over time |
| `logs/` | 1-10 MB | Grows over time |
| `cache/` | 1-5 MB | YFinance cache |
| `venv/` | 100-500 MB | Python packages |

**Total (without venv):** ~20-120 MB  
**Total (with venv):** ~150-650 MB

## ✅ Structure Verification

Run this command to verify your structure:

```bash
# Check all directories exist
for dir in src docs watchlists output logs scripts; do
  [ -d "$dir" ] && echo "✅ $dir/" || echo "❌ $dir/ MISSING"
done

# Check key files exist
for file in README.md LICENSE requirements.txt; do
  [ -f "$file" ] && echo "✅ $file" || echo "❌ $file MISSING"
done
```

Expected output:
```
✅ src/
✅ docs/
✅ watchlists/
✅ output/
✅ logs/
✅ scripts/
✅ README.md
✅ LICENSE
✅ requirements.txt
```

## 📖 Related Documentation

- **Main Guide:** `README.md`
- **Quick Start:** `docs/QUICK_START.md`
- **Organization:** `docs/ORGANIZATION_GUIDE.md`
- **Structure Details:** `docs/DIRECTORY_STRUCTURE.md`
- **Migration:** `MIGRATION_CHECKLIST.md`
- **Changes:** `REORGANIZATION_SUMMARY.md`

---

**Last Updated:** January 2024  
**Version:** 2.0 (Reorganized)  
**Status:** ✅ Production Ready