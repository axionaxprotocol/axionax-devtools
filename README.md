# axionax protocol - Developer Tools 🔧

Scripts and utilities for axionax protocol development and testing.

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Protocol](https://img.shields.io/badge/Protocol-axionax-purple)](https://axionax.org)
[![Status](https://img.shields.io/badge/Status-Pre--Testnet-orange)](https://github.com/axionaxprotocol/axionax-core)

---

## 📢 Latest Update (November 2025)

🎯 **Testing & Quality Assurance for Public Testnet!**

Active development focus:

✅ **Testing Infrastructure:**
- Unit Tests - Target >80% coverage across all repos
- Integration Tests - End-to-end workflow validation
- E2E Tests - User journey testing
- Performance Benchmarks - VRF, block validation, TX throughput

🔥 **Current Phase:**
- Running comprehensive test suites
- Performance optimization ongoing
- Benchmark comparisons (Rust vs Go)
- Quality metrics tracking

📦 **Tools Ready:** All testing utilities validated and production-ready

---

## 📖 About

Developer tools and automation scripts for building, testing, and maintaining
the **axionax protocol** ecosystem.

### Part of axionax Ecosystem

These tools support the entire axionax protocol development workflow:

- **Protocol Core**: [`../axionax-core`](../axionax-core) - Main development target
- **Web Interface**: [`../axionax-web`](../axionax-web) - Frontend development & testing
- **SDK**: [`../axionax-sdk-ts`](../axionax-sdk-ts) - SDK testing & validation
- **Marketplace**: [`../axionax-marketplace`](../axionax-marketplace) - dApp testing
- **Documentation**: [`../axionax-docs`](../axionax-docs) - Doc link validation
- **Deployment**: [`../axionax-deploy`](../axionax-deploy) - Infrastructure testing
- **Issue Manager**: [`../issue-manager`](../issue-manager) - Task automation

**Main Repository**:
[axionaxprotocol/axionaxiues](https://github.com/axionaxprotocol/axionaxiues)

**Pre-Testnet Status:** All testing tools operational, active test execution phase

---

## 📦 Contents

### Dependency Installation Scripts

Automated installers for all major platforms:

- **`install_dependencies_linux.sh`** - Ubuntu/Debian/CentOS/RHEL/Arch/Alpine
- **`install_dependencies_macos.sh`** - macOS 10.15+
- **`install_dependencies_windows.ps1`** - Windows 10/11 (PowerShell)

**Installs**:

- Rust 1.75+ & Cargo
- Python 3.10+
- Node.js 20 LTS
- Docker & Docker Compose
- PostgreSQL, Nginx, Redis
- Build tools and dependencies

### Testing & Benchmarking

Located in `tools/`:

- **`benchmark.py`** - Performance benchmarks for axionax protocol
  - VRF operations (22,817 ops/sec target)
  - Block validation (3,500 blocks/sec target)
  - Transaction verification (45,000 tx/sec target)
  - Memory usage analysis (45MB idle target)
  - **Rust vs Go comparison** (3x improvement target)
- **`run_tests.sh`** - Unified test runner (all tests)
- **`test-quick.ps1`** / **`quick-test.ps1`** - Quick sanity checks
- **`test.ps1`** - Full test suite (unit + integration + E2E)

### Development Utilities

- **`create_genesis.py`** - Genesis block generator for axionax protocol
- **`migrate_go_to_rust.py`** - Migration utilities (legacy)
- **`check-links.sh`** - Documentation link validator

---

## 🚀 Usage

### Quick Dependency Setup

#### Linux

```bash
cd devtools
chmod +x install_dependencies_linux.sh
./install_dependencies_linux.sh
```

#### macOS

```bash
cd devtools
chmod +x install_dependencies_macos.sh
./install_dependencies_macos.sh
```

#### Windows (PowerShell as Administrator)

```powershell
cd devtools
.\install_dependencies_windows.ps1
```

### Run Protocol Benchmarks

```bash
cd devtools
python tools/benchmark.py
```

**Expected Outputs (Rust v1.6):**

- **VRF operations**: ~22,817 ops/sec (2.68x faster than Go)
- **Block validation**: ~3,500 blocks/sec (2.92x faster)
- **Transaction throughput**: ~45,000 tx/sec (3.0x faster)
- **Memory usage**: ~45 MB idle (2.67x less than Go)
- **Comparison**: Detailed Rust vs Go v1.5 metrics

### Run Test Suite

```bash
# Quick sanity check (< 1 min)
cd devtools
./test-quick.ps1

# Full test suite (unit + integration)
./test.ps1

# All tests including benchmarks
./run_tests.sh
```

### Generate Genesis Block

```bash
cd devtools
python tools/create_genesis.py --chain-id 86137 --output ../axionax-core/genesis.json
```

---

## 🎯 Pre-Testnet Testing Checklist

Use these tools to verify readiness:

- [ ] ✅ **Unit Tests** - Run `test.ps1` - Target >80% coverage
- [ ] 🔗 **Integration Tests** - Run `run_tests.sh` - All workflows pass
- [ ] 🧪 **E2E Tests** - Validate user journeys
- [ ] 📊 **Benchmarks** - Run `benchmark.py` - Meet performance targets
- [ ] 🔍 **Link Validation** - Run `check-links.sh` - No broken links
- [ ] 🏗️ **Genesis Block** - Generate with `create_genesis.py`

Track progress: [`../issue-manager`](../issue-manager)

---

## 🔗 axionax protocol Ecosystem

| Component           | Description             | Location                                         | Status     |
| ------------------- | ----------------------- | ------------------------------------------------ | ---------- |
| **DevTools** (this) | Development utilities   | `axionax-devtools/`                              | ✅ Ready   |
| **Core**            | Protocol implementation | [`../axionax-core`](../axionax-core)             | ✅ Ready   |
| **Web**             | Web interface           | [`../axionax-web`](../axionax-web)               | ✅ Ready   |
| **SDK**             | TypeScript SDK          | [`../axionax-sdk-ts`](../axionax-sdk-ts)         | ✅ Ready   |
| **Marketplace**     | Compute marketplace     | [`../axionax-marketplace`](../axionax-marketplace) | 🚧 Beta  |
| **Docs**            | Documentation           | [`../axionax-docs`](../axionax-docs)             | 📝 Active  |
| **Deploy**          | Infrastructure          | [`../axionax-deploy`](../axionax-deploy)         | 🔥 Testing |
| **Issue Manager**   | Task tracking           | [`../issue-manager`](../issue-manager)           | 🎉 New!    |

---

## 📝 Contributing

1. Fork the main repository:
   [axionaxprotocol/axionax-core](https://github.com/axionaxprotocol/axionax-core)
2. Create your feature branch
3. Add/update scripts in `devtools/` directory
4. Document usage in script headers
5. Test on target platforms
6. Submit Pull Request

**Guidelines**:

- Keep scripts idempotent (safe to re-run)
- Add usage examples in comments
- Support cross-platform when possible

---

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🔗 Links

- **Main Repository**: https://github.com/axionaxprotocol/axionax-core
- **Protocol Core**: [`../axionax-core`](../axionax-core)
- **Documentation**: [`../axionax-docs`](../axionax-docs) or https://docs.axionax.org
- **Issues**: https://github.com/axionaxprotocol/axionax-core/issues

---

## 📊 Performance Targets

### Rust v1.6 Performance Goals

| Metric              | Target           | vs Go v1.5  |
| ------------------- | ---------------- | ----------- |
| VRF Operations      | 22,817 ops/sec   | 2.68x       |
| Block Validation    | 3,500 blocks/sec | 2.92x       |
| TX Verification     | 45,000 tx/sec    | 3.0x        |
| Memory Usage (Idle) | 45 MB            | 2.67x less  |
| Test Coverage       | >80%             | Improved    |

Run `benchmark.py` to verify your build meets these targets!

---

**Part of the axionax protocol Ecosystem**

**Last Updated**: November 7, 2025
