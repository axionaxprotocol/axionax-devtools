# Axionax DevTools - Copilot Instructions
# Target Model: GPT-5.1 (Instant)

**Context:** CLI Tools, Benchmarking Scripts, Migration Utilities.

## 💻 CLI UX STANDARDS
1.  **Argument Parsing:**
    - Use `argparse` (Python) or `clap` (Rust).
    - Always provide `--help` documentation.

2.  **Error Reporting:**
    - Output human-readable errors. Dump stack traces only with `--debug`.
    - Use ANSI colors: Info (Green), Warning (Yellow), Error (Red).

3.  **Performance Scripts:**
    - Ensure statistical significance in benchmarks.
    - Clean up temporary files (Trap signals in Bash).

4.  **Code Style:**
    - Python: PEP-8 compliant.
    - Bash: `set -euo pipefail`.
