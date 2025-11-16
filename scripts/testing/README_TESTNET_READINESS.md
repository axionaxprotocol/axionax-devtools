# Testnet Readiness Checker

Comprehensive automated validation tool for AxionAx Protocol testnet deployment readiness.

## Overview

The Testnet Readiness Checker performs **28 validation checks** across **7 critical categories** to ensure your system is ready for public testnet launch. It provides a scored assessment (0-100) with clear pass/fail indicators and actionable recommendations.

## Quick Start

### Windows
```powershell
.\check-testnet-readiness.ps1
```

### Linux/macOS
```bash
./check-testnet-readiness.sh
```

### Direct Python
```bash
python axionax-devtools/scripts/testing/testnet_readiness_checker.py
```

## What It Checks

### 📦 Infrastructure (15% weight)
- ✅ Repository structure (all 6 repos present)
- ✅ Git configuration (clean state)
- ✅ Dependencies installed (Rust, Node.js, Python, Docker)
- ✅ Build tools functional

### 💻 Codebase (20% weight)
- ✅ Code quality score ≥ 60/100
- ✅ All tests passing
- ✅ All builds successful
- ✅ Linting configurations present

### 🔒 Security (25% weight) - **CRITICAL**
- ❌ **No hardcoded secrets** (BLOCKING)
- ✅ No critical vulnerabilities
- ❌ **Security audit completed** (BLOCKING)
- ✅ Access controls configured

### ⚡ Performance (15% weight)
- ✅ Benchmark suite present
- ✅ Build optimization enabled
- ⚠️ Load testing completed

### 📚 Documentation (10% weight)
- ✅ Core documentation complete
- ✅ API documentation present
- ✅ Deployment guides available
- ✅ Code examples provided

### 🚀 Deployment (10% weight)
- ✅ Docker configurations ready
- ✅ Environment configs present
- ✅ Deployment scripts functional

### 📊 Monitoring (5% weight)
- ✅ Logging configured
- ⚠️ Metrics collection setup
- ⚠️ Health endpoints implemented

## Scoring System

| Score Range | Status | Action |
|-------------|--------|--------|
| **≥ 70** | ✅ **READY** | Approved for testnet launch |
| **50-69** | ⚠️ **CAUTION** | Fix high priority items first |
| **< 50** | ❌ **NOT READY** | Significant work required |

### Category Weights
- Security: **25%** (highest priority)
- Codebase: **20%**
- Infrastructure: **15%**
- Performance: **15%**
- Documentation: **10%**
- Deployment: **10%**
- Monitoring: **5%**

## Critical Blockers

These checks are marked as **CRITICAL** and will block testnet launch even if overall score ≥ 70:

1. ❌ **No Hardcoded Secrets**
   - Scans for: `password`, `api_key`, `secret`, `token`, `private_key`
   - **Must be 100% clean before launch**

2. ❌ **Security Audit Status**
   - Requires: `SECURITY_AUDIT.md` or `AUDIT_REPORT.md`
   - **Must be completed by professional firm**

## Output

### Console Output
Color-coded results with real-time progress:
- ✅ Green = Passed
- ⚠️ Yellow = Warning (not blocking)
- ❌ Red = Failed (critical if marked)

### JSON Report
Generated file: `TESTNET_READINESS_REPORT.json`

```json
{
  "timestamp": "2025-11-15T23:16:29",
  "overall_passed": false,
  "overall_score": 50.0,
  "results": [
    {
      "name": "Repository Structure",
      "category": "infrastructure",
      "passed": true,
      "score": 100,
      "message": "All 6 repos present",
      "critical": false
    }
  ]
}
```

## CI/CD Integration

### GitHub Actions

Workflow file: `.github/workflows/testnet-readiness.yml`

**Triggers:**
- Push to `main`, `develop`, `testnet-*` branches
- Pull requests to `main`, `develop`
- Weekly on Mondays at 9 AM UTC
- Manual workflow dispatch

**Features:**
- Automated readiness checks on every push
- PR comment with results
- Artifact upload (90-day retention)
- Auto-create issue if weekly check fails
- Fail main branch pushes if score < 70

## Common Issues & Fixes

### Issue: Hardcoded Secrets Found
```bash
# Find them
git grep -i "password\|api_key\|secret" | grep -v node_modules

# Fix: Move to .env
echo "API_KEY=your_key" >> .env
echo ".env" >> .gitignore
```

### Issue: Security Audit Missing
```bash
# Create audit report template
cat > SECURITY_AUDIT.md << 'EOF'
# Security Audit Report

**Audit Firm:** [Name]
**Date:** [Date]
**Version:** [Version]

## Executive Summary
[Summary of findings]

## Vulnerabilities Found
[List of issues and remediations]

## Certification
[Sign-off from audit firm]
EOF
```

### Issue: Build Failures
```bash
# Rust
cd axionax-core
cargo clean && cargo build --release

# TypeScript
cd axionax-sdk-ts
rm -rf node_modules && npm install && npm run build
```

### Issue: Low Code Quality Score
```bash
# Run quality analyzer
python axionax-devtools/scripts/analysis/repo_quality_analyzer.py

# Address top issues first
# - Add missing documentation
# - Create code examples
# - Add installation scripts
```

## Best Practices

1. **Run Daily** during pre-launch phase
2. **Track Progress** with dated reports
3. **Fix Critical First** before optimizing scores
4. **Document All Changes** in CHANGELOG.md
5. **Re-run After** every significant change

## Example Workflow

```bash
# 1. Initial check
./check-testnet-readiness.sh
# Score: 50/100 ❌

# 2. Fix critical issues
# - Remove hardcoded secrets
# - Complete security audit

# 3. Check again
./check-testnet-readiness.sh
# Score: 65/100 ⚠️

# 4. Address high-priority items
# - Improve code quality
# - Add load testing
# - Set up monitoring

# 5. Final check
./check-testnet-readiness.sh
# Score: 75/100 ✅ READY!
```

## Minimum Launch Requirements

✅ **Overall score ≥ 70/100**
✅ **All critical checks passed**
✅ **Security audit completed**
✅ **No hardcoded secrets**
✅ **All tests passing**
✅ **Documentation complete**
✅ **Deployment scripts tested**

## Advanced Usage

### Verbose Mode
```bash
python testnet_readiness_checker.py -v
```

### Run Specific Categories
```python
from testnet_readiness_checker import TestnetReadinessChecker

checker = TestnetReadinessChecker(workspace_root)
checker._check_security()  # Run only security checks
```

### Custom Thresholds
Edit the script to adjust:
- Category weights
- Minimum score requirements
- Critical check definitions

## Support

- 📖 **Full Guide:** [TESTNET_READINESS_GUIDE.md](../../TESTNET_READINESS_GUIDE.md)
- 📋 **Quick Reference:** [TESTNET_READINESS_QUICK_REF.md](../../TESTNET_READINESS_QUICK_REF.md)
- 🐛 **Issues:** [GitHub Issues](https://github.com/axionaxprotocol/axionax-devtools/issues)

## Version History

### v1.9.0 (2025-11-15)
- Initial release
- 28 validation checks across 7 categories
- Weighted scoring system
- Critical blocker detection
- JSON report generation
- CI/CD integration

---

**Ready to launch?** Run `./check-testnet-readiness.sh` and aim for 70+ 🚀
