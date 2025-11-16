# AxionAx DevTools - Scripts Organization

## 📁 Directory Structure

```
axionax-devtools/
├── scripts/
│   ├── testing/
│   │   ├── testnet_readiness_checker.py  # Main readiness validation
│   │   ├── test_repo_links.py            # Repository link validation
│   │   ├── test_repo_integration.py      # Integration testing
│   │   └── check_repo_health.py          # Repository health checks
│   ├── analysis/
│   │   ├── repo_quality_analyzer.py      # Code quality analysis
│   │   ├── check_repo_connections.py     # Dependency analysis
│   │   └── generate_summary.py           # Summary generation
│   ├── fixing/
│   │   ├── fix_protocol_names.py         # Protocol name corrections
│   │   ├── fix_critical_issues.py        # Critical bug fixes
│   │   ├── fix_warnings.py               # Warning resolution
│   │   └── quick_fix.py                  # Quick fix utility
│   ├── refactoring/
│   │   ├── master_refactor.py            # Master refactoring script
│   │   ├── refactor_and_clean.py         # Clean & refactor
│   │   └── analyze_code_quality.py       # Quality analysis
│   ├── check-testnet-readiness.ps1       # PowerShell wrapper
│   ├── check-testnet-readiness.sh        # Bash wrapper
│   ├── auto_fix.ps1                      # Auto-fix PowerShell
│   └── auto_fix.sh                       # Auto-fix Bash
├── tools/
│   ├── benchmark.py                      # Performance benchmarking
│   ├── create_genesis.py                 # Genesis block creation
│   ├── migrate_go_to_rust.py             # Go to Rust migration
│   ├── test-links.ps1                    # Link testing utility
│   └── check-links.sh                    # Link checker (Bash)
└── docs/
    ├── PRE_TESTNET_REPORT.md             # Pre-testnet status
    ├── TESTNET_READINESS_GUIDE.md        # Readiness guide
    ├── TESTNET_READINESS_QUICK_REF.md    # Quick reference
    ├── TESTNET_DEPLOYMENT_PLAN.md        # Deployment plan
    ├── COMPLETED_TASKS_CHECKLIST.md      # Task tracking
    ├── QUALITY_IMPROVEMENT_REPORT.md     # Quality report
    ├── REPOSITORY_FLOW.md                # Repository structure
    └── REPOSITORY_ANALYSIS.txt           # Analysis results
```

## 🚀 Quick Start

### Testnet Readiness Check

**Windows (PowerShell):**
```powershell
.\scripts\check-testnet-readiness.ps1
```

**Linux/macOS (Bash):**
```bash
./scripts/check-testnet-readiness.sh
```

**Python (Direct):**
```bash
python scripts/testing/testnet_readiness_checker.py
```

### Code Quality Analysis

```bash
python scripts/analysis/repo_quality_analyzer.py
```

### Auto-Fix Issues

**PowerShell:**
```powershell
.\scripts\auto_fix.ps1
```

**Bash:**
```bash
./scripts/auto_fix.sh
```

## 📋 Script Categories

### Testing Scripts
- **testnet_readiness_checker.py**: Comprehensive testnet validation (28 checks, 7 categories)
- **test_repo_links.py**: Validates repository links and references
- **test_repo_integration.py**: Integration testing across repositories
- **check_repo_health.py**: Repository health monitoring

### Analysis Scripts
- **repo_quality_analyzer.py**: Deep code quality analysis
- **check_repo_connections.py**: Dependency and import analysis
- **generate_summary.py**: Generate project summaries

### Fixing Scripts
- **fix_protocol_names.py**: Standardize protocol naming
- **fix_critical_issues.py**: Address critical security/stability issues
- **fix_warnings.py**: Resolve compiler/linter warnings
- **quick_fix.py**: Quick automated fixes

### Refactoring Scripts
- **master_refactor.py**: Comprehensive codebase refactoring
- **refactor_and_clean.py**: Code cleanup and organization
- **analyze_code_quality.py**: Pre-refactoring analysis

### Tools
- **benchmark.py**: Performance benchmarking suite
- **create_genesis.py**: Genesis block generation
- **migrate_go_to_rust.py**: Go to Rust migration utility
- **test-links.ps1**: Link validation (PowerShell)
- **check-links.sh**: Link validation (Bash)

## 📊 Report Files

All generated reports are stored in the root directory:
- `TESTNET_READINESS_REPORT.json`: Latest readiness check results
- `QUALITY_ANALYSIS.json`: Code quality metrics

## 🔧 Usage Examples

### Run Full Testnet Readiness Check
```bash
python scripts/testing/testnet_readiness_checker.py
```

**Output:**
- Console: Color-coded check results
- File: `TESTNET_READINESS_REPORT.json`
- Score: 0-100 (≥70 = READY)

### Analyze Code Quality
```bash
python scripts/analysis/repo_quality_analyzer.py
```

**Generates:**
- `QUALITY_ANALYSIS.json`: Detailed quality metrics
- Console: Score breakdown by category

### Fix Protocol Names
```bash
python scripts/fixing/fix_protocol_names.py
```

**Actions:**
- Scans for inconsistent protocol names
- Applies standardized naming (AxionAx)
- Updates imports and references

### Create Genesis Block
```bash
python tools/create_genesis.py --chain-id 86137 --output genesis.json
```

## 🎯 Best Practices

1. **Before Commits**: Run `testnet_readiness_checker.py`
2. **After Major Changes**: Run `repo_quality_analyzer.py`
3. **Before Deployment**: Run full readiness check with `check-testnet-readiness.ps1`
4. **Weekly**: Review `QUALITY_ANALYSIS.json` for trends

## 📖 Documentation

For detailed guides, see:
- [Testnet Readiness Guide](docs/TESTNET_READINESS_GUIDE.md)
- [Quick Reference](docs/TESTNET_READINESS_QUICK_REF.md)
- [Deployment Plan](docs/TESTNET_DEPLOYMENT_PLAN.md)

## 🔗 Related Repositories

- **axionax-core**: Core protocol implementation
- **axionax-deploy**: Deployment scripts and configs
- **axionax-sdk-ts**: TypeScript SDK
- **axionax-docs**: Documentation and guides

## 🆘 Support

For issues or questions:
1. Check [TESTNET_READINESS_GUIDE.md](docs/TESTNET_READINESS_GUIDE.md)
2. Review [REPOSITORY_FLOW.md](docs/REPOSITORY_FLOW.md)
3. Open issue in axionax-devtools repository
