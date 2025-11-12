# 🚀 Quick Start Guide - axionax-devtools

## Overview

**axionax-devtools** เป็น development tools และ testing utilities สำหรับ axionax protocol ประกอบด้วย scripts สำหรับ testing, refactoring, fixing, และ analysis

**Repository:** https://github.com/axionaxprotocol/axionax-devtools

---

## 📋 Prerequisites

```bash
# Required
- Python 3.10+
- Git
- Node.js 18+ (for TypeScript projects)
- Rust 1.70+ (for Rust projects)

# Recommended
- VS Code with Python extensions
- PowerShell/Bash
```

---

## 🔧 Installation

### 1. Clone Repository

```bash
git clone https://github.com/axionaxprotocol/axionax-devtools.git
cd axionax-devtools
```

### 2. Setup Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows
venv\Scripts\activate
# On Linux/Mac
source venv/bin/activate

# Install dependencies (if requirements.txt exists)
pip install -r requirements.txt
```

### 3. Verify Setup

```bash
# Test a simple script
python scripts/testing/check_repo_health.py

# Should show repository health scores
```

---

## 🏗️ Repository Structure

```
axionax-devtools/
├── scripts/                    # All development scripts
│   ├── testing/                # Testing scripts
│   │   ├── test_repo_integration.py    # 49 integration tests
│   │   ├── test_repo_links.py          # Link validation
│   │   └── check_repo_health.py        # Health checks
│   │
│   ├── refactoring/            # Code quality scripts
│   │   ├── refactor_and_clean.py       # Main refactoring
│   │   ├── analyze_code_quality.py     # Code analysis
│   │   └── master_refactor.py          # Orchestrator
│   │
│   ├── fixing/                 # Fix scripts
│   │   ├── quick_fix.py                # Interactive fixes
│   │   ├── fix_critical_issues.py      # Critical fixes
│   │   ├── fix_warnings.py             # Warning fixes
│   │   ├── fix_npm_workspaces.py       # NPM workspace setup
│   │   ├── fix_protocol_names.py       # Name corrections
│   │   ├── fix_axionax_name.py         # Brand corrections
│   │   └── fix_domain.py               # Domain changes
│   │
│   ├── analysis/               # Analysis scripts
│   │   └── check_repo_connections.py   # Repository analysis
│   │
│   └── *.{ps1,sh,bat}          # Shell scripts
│       ├── auto_fix.ps1
│       ├── auto_fix.sh
│       ├── commit_all.bat
│       ├── fix_names.ps1
│       └── fix_protocol_name.ps1
│
├── docs/                       # Documentation
│   ├── REFACTORING_GUIDE.md    # Refactoring guide
│   ├── REFACTORING_SUMMARY.md  # Use cases
│   ├── REFACTORING_COMPLETE.md # Completion report
│   └── INTEGRATION_SUMMARY.md  # Test summaries
│
├── __init__.py                 # Module entry point
├── README.md                   # Main documentation
└── QUICK_START.md              # This file
```

---

## 🔨 Common Development Tasks

### 1. Run Integration Tests

```bash
# Run all 49 integration tests across 7 repos
python scripts/testing/test_repo_integration.py

# Expected output:
# - Total tests: 49
# - Passed: ~28 (57.1%)
# - Warnings: ~5 (10.2%)
# - Failed: 0 (0.0%)
```

### 2. Check Repository Health

```bash
# Check health of all repos
python scripts/testing/check_repo_health.py

# Output shows scores:
# - axionax-web: 85.7/100 🟢
# - axionax-core: 78.6/100 🟡
# - axionax-marketplace: 71.4/100 🟡
# - etc.
```

### 3. Test Repository Links

```bash
# Validate all file: links between repos
python scripts/testing/test_repo_links.py

# Ensures no workspace: links (only file: links)
```

### 4. Analyze Code Quality

```bash
# Deep analysis of code quality issues
python scripts/refactoring/analyze_code_quality.py

# Finds:
# - Long functions
# - Magic numbers
# - Nested if statements
# - TODO comments
# - .unwrap() usage (Rust)
# - Missing documentation
```

### 5. Refactor and Clean Code

```bash
# Clean all repositories
python scripts/refactoring/refactor_and_clean.py

# Clean specific repo
python scripts/refactoring/refactor_and_clean.py --repo axionax-web

# Skip formatting (only lint)
python scripts/refactoring/refactor_and_clean.py --skip-formatting

# Skip linting (only format)
python scripts/refactoring/refactor_and_clean.py --skip-linting
```

### 6. Quick Interactive Fixes

```bash
# Interactive menu for common fixes
python scripts/fixing/quick_fix.py

# Menu options:
# 1. Fix .gitignore files
# 2. Fix package-lock.json
# 3. Clean git artifacts
# 4. Fix dependencies
# 5. Fix line endings
```

### 7. Run Master Refactor

```bash
# Orchestrates all refactoring tasks
python scripts/refactoring/master_refactor.py

# Runs in sequence:
# 1. Integration tests
# 2. Health checks
# 3. Code analysis
# 4. Refactoring
# 5. Final tests
```

---

## 📊 Testing Scripts

### test_repo_integration.py

**Purpose:** Comprehensive integration testing across all 7 repos

**Tests Performed:**
- Repository existence
- Git status
- Package.json validity
- Dependencies check
- Import statement validation
- Build system verification
- File structure checks

**Usage:**
```bash
python scripts/testing/test_repo_integration.py

# With verbose output
python scripts/testing/test_repo_integration.py -v
```

### check_repo_health.py

**Purpose:** Health score calculation for each repo

**Checks:**
- .gitignore presence
- Uncommitted changes
- package-lock.json
- Missing dependencies
- README.md
- Test coverage

**Usage:**
```bash
python scripts/testing/check_repo_health.py

# Generate report
python scripts/testing/check_repo_health.py --report health_report.txt
```

### test_repo_links.py

**Purpose:** Validate inter-repository links

**Validates:**
- file: protocol usage (✅ correct)
- No workspace: protocol (❌ forbidden)
- Relative path correctness
- Target file existence

**Usage:**
```bash
python scripts/testing/test_repo_links.py

# Show only errors
python scripts/testing/test_repo_links.py --errors-only
```

---

## 🔧 Refactoring Scripts

### refactor_and_clean.py

**Purpose:** Main refactoring tool with multiple options

**Actions:**
- Remove console.log (TypeScript)
- Remove debugger statements
- Remove trailing whitespace
- Fix empty lines
- Run Prettier (TypeScript)
- Run ESLint (TypeScript)
- Run rustfmt (Rust)
- Run clippy (Rust)

**Usage:**
```bash
# Clean all repos
python scripts/refactoring/refactor_and_clean.py

# Specific repo
python scripts/refactoring/refactor_and_clean.py --repo axionax-core

# Skip formatting
python scripts/refactoring/refactor_and_clean.py --skip-formatting

# Skip linting
python scripts/refactoring/refactor_and_clean.py --skip-linting

# Dry run (no changes)
python scripts/refactoring/refactor_and_clean.py --dry-run
```

### analyze_code_quality.py

**Purpose:** Deep code quality analysis

**TypeScript Analysis:**
- Functions > 50 lines
- Magic numbers
- Nested if > 3 levels
- TODO/FIXME comments
- `any` type usage
- Empty catch blocks

**Rust Analysis:**
- .unwrap() usage
- .expect() usage
- .clone() overuse
- unsafe blocks
- Missing documentation

**Usage:**
```bash
# Analyze all repos
python scripts/refactoring/analyze_code_quality.py

# Specific repo
python scripts/refactoring/analyze_code_quality.py --repo axionax-web

# Generate report
python scripts/refactoring/analyze_code_quality.py --output quality_report.txt
```

### master_refactor.py

**Purpose:** Orchestrate complete refactoring workflow

**Workflow:**
1. Run integration tests (baseline)
2. Check repository health
3. Analyze code quality
4. Run refactoring
5. Re-run tests (validation)
6. Generate summary report

**Usage:**
```bash
# Full workflow
python scripts/refactoring/master_refactor.py

# Skip tests
python scripts/refactoring/master_refactor.py --skip-tests

# Specific repos only
python scripts/refactoring/master_refactor.py --repos axionax-core,axionax-web
```

---

## 🔍 Analysis Scripts

### check_repo_connections.py

**Purpose:** Analyze dependencies between repositories

**Output:**
- Connection graph (Mermaid diagram)
- 34 connections found
- Import analysis
- Dependency tree

**Usage:**
```bash
# Analyze connections
python scripts/analysis/check_repo_connections.py

# Generate Mermaid diagram
python scripts/analysis/check_repo_connections.py --mermaid > connections.md

# Generate JSON
python scripts/analysis/check_repo_connections.py --json > connections.json
```

---

## 🛠️ Fixing Scripts

### quick_fix.py

**Purpose:** Interactive menu for common fixes

**Features:**
- Fix .gitignore files
- Fix package-lock.json
- Clean git artifacts
- Fix dependencies
- Fix line endings (CRLF/LF)

**Usage:**
```bash
# Interactive mode
python scripts/fixing/quick_fix.py

# Non-interactive (all fixes)
python scripts/fixing/quick_fix.py --all
```

### fix_critical_issues.py

**Purpose:** Fix critical blocking issues

**Fixes:**
- UTF-8 BOM removal
- Workspace config issues
- Circular dependencies
- Missing files

**Usage:**
```bash
python scripts/fixing/fix_critical_issues.py
```

### fix_npm_workspaces.py

**Purpose:** Setup npm workspace structure

**Actions:**
- Create workspace root package.json
- Configure workspaces
- Update dependencies to file: links
- Run npm install

**Usage:**
```bash
python scripts/fixing/fix_npm_workspaces.py
```

---

## 🔌 Integration with Other Repos

### Testing axionax-core

```bash
cd ../axionax-core

# Run devtools tests on core
python ../axionax-devtools/scripts/testing/test_repo_integration.py

# Analyze core code quality
python ../axionax-devtools/scripts/refactoring/analyze_code_quality.py --repo axionax-core
```

### Refactoring axionax-web

```bash
cd ../axionax-web

# Clean and refactor
python ../axionax-devtools/scripts/refactoring/refactor_and_clean.py --repo axionax-web

# Check results
python ../axionax-devtools/scripts/testing/check_repo_health.py
```

### Full Workspace Testing

```bash
# From workspace root
cd axionax-devtools

# Test all repos
python scripts/testing/test_repo_integration.py

# Analyze all connections
python scripts/analysis/check_repo_connections.py

# Refactor all repos
python scripts/refactoring/master_refactor.py
```

---

## 📖 Documentation

### Available Guides

1. **REFACTORING_GUIDE.md** - Complete refactoring guide
   ```bash
   # Read guide
   cat docs/REFACTORING_GUIDE.md
   ```

2. **REFACTORING_SUMMARY.md** - Use cases and workflows
   ```bash
   # Read summary
   cat docs/REFACTORING_SUMMARY.md
   ```

3. **REFACTORING_COMPLETE.md** - Completion report with KPIs
   ```bash
   # View completion status
   cat docs/REFACTORING_COMPLETE.md
   ```

4. **INTEGRATION_SUMMARY.md** - Test result summaries
   ```bash
   # View test results
   cat docs/INTEGRATION_SUMMARY.md
   ```

---

## 🚀 Automation Scripts

### Shell Scripts

```bash
# PowerShell (Windows)
.\scripts\auto_fix.ps1
.\scripts\fix_names.ps1
.\scripts\fix_protocol_name.ps1

# Bash (Linux/Mac)
./scripts/auto_fix.sh

# Batch (Windows CMD)
scripts\commit_all.bat
```

### Automated Workflows

```bash
# Full automated workflow
# 1. Test → 2. Fix → 3. Refactor → 4. Test again

# Windows PowerShell
.\scripts\auto_fix.ps1

# Linux/Mac
./scripts/auto_fix.sh
```

---

## 🐛 Debugging Scripts

### Enable Debug Output

```python
# Add to script
import logging
logging.basicConfig(level=logging.DEBUG)

# Run script
python scripts/testing/test_repo_integration.py
```

### Verbose Mode

```bash
# Most scripts support -v or --verbose
python scripts/testing/test_repo_integration.py -v
python scripts/refactoring/analyze_code_quality.py --verbose
```

---

## 🚨 Troubleshooting

### Script Not Found

```bash
# Make sure you're in axionax-devtools directory
cd axionax-devtools

# Check file exists
ls scripts/testing/test_repo_integration.py

# Use correct path
python scripts/testing/test_repo_integration.py  # ✅ Correct
python test_repo_integration.py                   # ❌ Wrong
```

### Python Module Errors

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install missing modules
pip install -r requirements.txt

# Check Python version
python --version  # Should be 3.10+
```

### Permission Errors

```bash
# Linux/Mac: Add execute permission
chmod +x scripts/testing/*.py
chmod +x scripts/*.sh

# Windows: Run as Administrator if needed
```

---

## 📝 Configuration

### Environment Variables

```bash
# Set workspace root (if needed)
export AXIONAX_WORKSPACE=D:\Desktop\axionaxius01

# Set Python path
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Enable debug mode
export DEBUG=1
```

---

## 📚 Additional Resources

- **Main README:** [README.md](README.md)
- **Refactoring Guide:** [docs/REFACTORING_GUIDE.md](docs/REFACTORING_GUIDE.md)
- **Integration Summary:** [docs/INTEGRATION_SUMMARY.md](docs/INTEGRATION_SUMMARY.md)
- **axionax Docs:** [axionax-docs](https://github.com/axionaxprotocol/axionax-docs)

---

## 🤝 Getting Help

- **Issues:** Report bugs on [GitHub Issues](https://github.com/axionaxprotocol/axionax-devtools/issues)
- **Documentation:** Check [axionax-docs](https://github.com/axionaxprotocol/axionax-docs)
- **Contributing:** See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 License

MIT - See [LICENSE](LICENSE) file for details

---

<p align="center">
  <sub>Built with ❤️ by the axionax protocol Team</sub>
</p>
