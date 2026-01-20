# Migration Checklist

This checklist helps you migrate from the old structure to the new organized structure.

## ✅ Pre-Migration Checklist

- [ ] Backup your current project
- [ ] Commit any uncommitted changes
- [ ] Note location of any important files

## 📦 Reorganization Steps

### 1. Pull Latest Changes
```bash
git pull origin main
```

### 2. Verify New Directories Exist
```bash
ls -la
# Should see:
# - docs/
# - output/
# - logs/
# - scripts/
```

### 3. Create Missing Directories (if needed)
```bash
mkdir -p output/{scans,backtests,charts}
mkdir -p logs
```

### 4. Move Old Files (if applicable)

#### Move old scans
```bash
mv scan_*.txt output/scans/ 2>/dev/null || echo "No old scans to move"
```

#### Move old backtests
```bash
mv backtest_*.txt output/backtests/ 2>/dev/null || echo "No old backtests to move"
```

#### Move old charts
```bash
mv *.png output/charts/ 2>/dev/null || echo "No old charts to move"
```

### 5. Verify Git Ignore
```bash
git status
# Output should be clean, no output/ or logs/ files shown
```

### 6. Make Scripts Executable
```bash
chmod +x scripts/*.sh
```

## ✅ Post-Migration Checklist

### Verify Structure
- [ ] `src/` directory exists with Python code
- [ ] `docs/` directory contains documentation
- [ ] `watchlists/` directory contains stock lists
- [ ] `output/` directory exists with scans/, backtests/, charts/
- [ ] `logs/` directory exists
- [ ] `scripts/` directory contains utility scripts

### Test Functionality
- [ ] Run test scan: `python -m src.main BBCA BBRI TLKM`
- [ ] Save scan: `python -m src.main BBCA > output/scans/test.txt`
- [ ] Check cleanup script: `./scripts/cleanup.sh`
- [ ] Verify git status is clean: `git status`

### Review Documentation
- [ ] Read `README.md`
- [ ] Review `docs/QUICK_START.md`
- [ ] Check `docs/ORGANIZATION_GUIDE.md`
- [ ] Understand `docs/DIRECTORY_STRUCTURE.md`

## 📚 New File Locations

| Old Location | New Location |
|--------------|--------------|
| `BACKTESTING_SUMMARY.md` | `docs/BACKTESTING_SUMMARY.md` |
| `GEMINI.md` | `docs/GEMINI.md` |
| `QUICK_START.md` | `docs/QUICK_START.md` |
| `RATE_LIMIT_FIXES.md` | `docs/RATE_LIMIT_FIXES.md` |
| `run_scanner.sh` | `scripts/run_scanner.sh` |
| `todo.txt` | `scripts/todo.txt` |
| `scan_*.txt` (wherever) | `output/scans/scan_*.txt` |
| `backtest_*.txt` (wherever) | `output/backtests/backtest_*.txt` |
| `*.png` (wherever) | `output/charts/*.png` |

## 🔧 Update Your Scripts/Aliases

If you have custom scripts or aliases pointing to old paths, update them:

### Old
```bash
python -m src.main > results.txt
```

### New
```bash
python -m src.main > output/scans/scan_$(date +%Y%m%d).txt
```

## 🎯 New Workflows

### Daily Scan
```bash
TODAY=$(date +%Y%m%d)
python -m src.main --list lq45 > output/scans/lq45_scan_${TODAY}.txt
```

### Weekly Cleanup
```bash
./scripts/cleanup.sh
```

### Monthly Archive
```bash
MONTH=$(date +%Y%m)
mkdir -p output/archive/${MONTH}
cp output/backtests/*summary* output/archive/${MONTH}/
```

## ❓ Troubleshooting

### "Directory not found" error
```bash
mkdir -p output/{scans,backtests,charts} logs scripts
```

### Git tracking output files
```bash
git rm --cached output/scans/*.txt
git status  # Should not show output files
```

### Scripts not executable
```bash
chmod +x scripts/*.sh
ls -la scripts/  # Should show -rwxr-xr-x permissions
```

### Documentation moved
All `.md` files (except README and LICENSE) are now in `docs/`:
```bash
ls docs/
# BACKTESTING_SUMMARY.md
# DIRECTORY_STRUCTURE.md
# GEMINI.md
# ORGANIZATION_GUIDE.md
# QUICK_START.md
# RATE_LIMIT_FIXES.md
```

## ✅ Migration Complete!

Once all checklist items are done:

1. Your project is organized
2. Git is tracking only code and watchlists
3. Output files are separated
4. Documentation is centralized
5. Cleanup is automated

**Next Steps:**
- Read `docs/QUICK_START.md` for usage
- Run your first organized scan
- Set up weekly cleanup automation
- Enjoy a cleaner, more maintainable project!

---

**Happy Trading! 📈**
