# Testnet Readiness - Quick Reference

## ⚡ Quick Commands

```bash
# Run full check
python axionax-devtools/scripts/testing/testnet_readiness_checker.py

# Windows shortcut
.\check-testnet-readiness.ps1

# Linux/macOS shortcut
./check-testnet-readiness.sh
```

## 📊 Scoring Thresholds

| Score | Status | Action |
|-------|--------|--------|
| ≥ 70 | ✅ READY | Proceed with testnet |
| 50-69 | ⚠️ CAUTION | Fix high priority items |
| < 50 | ❌ NOT READY | Major work needed |

## 🔴 Critical Blockers

**These MUST be 100% before launch:**

1. ✅ **No Hardcoded Secrets**
   - Check: `git grep -i "password\|api_key\|secret\|token"`
   - Fix: Move to `.env` files

2. ✅ **Security Audit Completed**
   - Create: `SECURITY_AUDIT.md` or `AUDIT_REPORT.md`
   - Include: Audit firm name, date, findings, remediations

3. ✅ **No Critical Vulnerabilities**
   - Check: `npm audit` for Node projects
   - Fix: `npm audit fix` or update packages

## 📋 Check Categories

### 1. Infrastructure (15%)
- [ ] All 6 repos present
- [ ] Git state clean
- [ ] Rust, Node.js, Python, Docker installed
- [ ] Build tools functional

### 2. Codebase (20%)
- [ ] Quality score ≥ 60/100
- [ ] All tests passing
- [ ] All builds successful
- [ ] Linting configs present (5+)

### 3. Security (25%) ⚠️ CRITICAL
- [ ] No secrets in code
- [ ] No critical vulnerabilities
- [ ] Security audit complete
- [ ] Access controls configured

### 4. Performance (15%)
- [ ] Benchmarks present (2+)
- [ ] Build optimization enabled
- [ ] Load testing completed

### 5. Documentation (10%)
- [ ] Core docs: README, ARCHITECTURE, DEVELOPER_GUIDE, CONTRIBUTING
- [ ] API documentation (1+)
- [ ] Deployment guides (2+)
- [ ] Code examples (4+)

### 6. Deployment (10%)
- [ ] Docker configs (3+)
- [ ] Environment files (3+)
- [ ] Deployment scripts (3+)

### 7. Monitoring (5%)
- [ ] Logging configured
- [ ] Metrics collection setup
- [ ] Health endpoints implemented

## 🚨 Common Issues & Quick Fixes

### Issue: Hardcoded Secrets Found
```bash
# Find secrets
git grep -i "password\|api_key\|secret" | grep -v "node_modules"

# Fix: Move to .env
echo "API_KEY=your_key" >> .env
echo ".env" >> .gitignore
git add .gitignore
git commit -m "fix: secure API keys in .env"
```

### Issue: Build Failures
```bash
# Rust
cd axionax-core
cargo clean
cargo build --release

# TypeScript
cd axionax-sdk-ts
rm -rf node_modules
npm install
npm run build
```

### Issue: Missing Documentation
```bash
# Create required docs
touch CONTRIBUTING.md ARCHITECTURE.md docs/API_REFERENCE.md

# Copy templates from axionax-docs
cp axionax-docs/CONTRIBUTING.md ./
```

## 📈 Progress Tracking

```bash
# Save baseline
python testnet_readiness_checker.py
cp TESTNET_READINESS_REPORT.json baseline_report.json

# After fixes
python testnet_readiness_checker.py
diff baseline_report.json TESTNET_READINESS_REPORT.json

# View improvement
python -c "
import json
with open('baseline_report.json') as f: baseline = json.load(f)
with open('TESTNET_READINESS_REPORT.json') as f: current = json.load(f)
print(f'Score: {baseline[\"overall_score\"]} -> {current[\"overall_score\"]} (+{current[\"overall_score\"]-baseline[\"overall_score\"]:.1f})')
"
```

## 🎯 Launch Checklist (Final 24h)

### T-24 Hours
- [ ] Run final readiness check
- [ ] Overall score ≥ 70
- [ ] All critical checks passed
- [ ] Monitoring dashboards ready
- [ ] Rollback plan documented

### T-12 Hours
- [ ] Notify validators
- [ ] Community announcement
- [ ] Deploy to staging
- [ ] Verify all endpoints

### T-1 Hour
- [ ] Final build and deploy
- [ ] Health checks passing
- [ ] Validators online
- [ ] Block explorer ready

### Launch
- [ ] Genesis ceremony
- [ ] Monitor first 100 blocks
- [ ] Track validator participation
- [ ] Community support active

## 📞 Emergency Contacts

```bash
# View report details
cat TESTNET_READINESS_REPORT.json | jq '.'

# Check specific category
cat TESTNET_READINESS_REPORT.json | jq '.results[] | select(.category=="security")'

# List all failures
cat TESTNET_READINESS_REPORT.json | jq '.results[] | select(.passed==false)'

# Critical issues only
cat TESTNET_READINESS_REPORT.json | jq '.results[] | select(.critical==true and .passed==false)'
```

## 💡 Pro Tips

1. **Run daily** during pre-launch phase
2. **Track progress** with dated reports
3. **Fix critical first** before optimizing
4. **Document fixes** in CHANGELOG
5. **Re-run after** every major change

## 📊 Target Scores by Phase

| Phase | Min Score | Target Score | Status |
|-------|-----------|--------------|--------|
| Alpha | 40 | 50 | Development |
| Beta | 60 | 70 | Pre-Testnet |
| Testnet | 70 | 80 | **Launch Ready** ✅ |
| Mainnet | 85 | 95 | Production |

---

**Current Status**: Run `.\check-testnet-readiness.ps1` to check! 🚀
