# AxionAX Protocol - Developer Tools 🔧

Scripts and utilities for AxionAX Protocol development and testing.

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Protocol](https://img.shields.io/badge/Protocol-AxionAX-purple)](https://axionax.org)

---

## 📖 About

Developer tools and automation scripts for building, testing, and maintaining
the **AxionAX Protocol** ecosystem.

### Part of AxionAX Ecosystem

These tools support the entire AxionAX Protocol development workflow:

- **Protocol Core**: [`../core`](../core) - Main development target
- **Web Interface**: [`../web`](../web) - Frontend development
- **SDK**: [`../sdk`](../sdk) - SDK testing
- **Documentation**: [`../docs`](../docs) - Protocol documentation
- **Deployment**: [`../deploy`](../deploy) - Infrastructure deployment

**Main Repository**:
[axionaxprotocol/axionaxiues](https://github.com/axionaxprotocol/axionaxiues)

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

- **`benchmark.py`** - Performance benchmarks for AxionAX Protocol
  - VRF operations
  - Block validation
  - Transaction verification
  - Memory usage analysis
- **`run_tests.sh`** - Unified test runner
- **`test-quick.ps1`** / **`quick-test.ps1`** - Quick sanity checks
- **`test.ps1`** - Full test suite

### Development Utilities

- **`create_genesis.py`** - Genesis block generator for AxionAX Protocol
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

Outputs:

- VRF operations/sec
- Block validation speed
- Transaction throughput
- Memory usage
- Comparison with baseline

### Generate Genesis Block

```bash
cd devtools
python tools/create_genesis.py --chain-id 86137 --output ../core/genesis.json
```

---

## 🔗 AxionAX Protocol Ecosystem

| Component           | Description             | Location                 |
| ------------------- | ----------------------- | ------------------------ |
| **DevTools** (this) | Development utilities   | `devtools/`              |
| **Core**            | Protocol implementation | [`../core`](../core)     |
| **Web**             | Web interface           | [`../web`](../web)       |
| **SDK**             | TypeScript SDK          | [`../sdk`](../sdk)       |
| **Docs**            | Documentation           | [`../docs`](../docs)     |
| **Deploy**          | Infrastructure          | [`../deploy`](../deploy) |

---

## 📝 Contributing

1. Fork the main repository:
   [axionaxprotocol/axionaxiues](https://github.com/axionaxprotocol/axionaxiues)
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

- **Main Repository**: https://github.com/axionaxprotocol/axionaxiues
- **Protocol Core**: [`../core`](../core)
- **Documentation**: [`../docs`](../docs) or https://docs.axionax.org
- **Issues**: https://github.com/axionaxprotocol/axionaxiues/issues

---

**Part of the AxionAX Protocol Ecosystem**

**Last Updated**: November 6, 2025
