#!/usr/bin/env python3
'''
Axionax DevTools - Main Entry Point
'''

import sys
from pathlib import Path

# Add scripts to path
scripts_path = Path(__file__).parent / 'scripts'
sys.path.insert(0, str(scripts_path / 'testing'))
sys.path.insert(0, str(scripts_path / 'refactoring'))
sys.path.insert(0, str(scripts_path / 'fixing'))
sys.path.insert(0, str(scripts_path / 'analysis'))

def main():
    print("Axionax DevTools")
    print("================")
    print()
    print("Available commands:")
    print("  test     - Run integration tests")
    print("  refactor - Run refactoring")
    print("  fix      - Quick fixes")
    print("  analyze  - Analyze code quality")
    print()
    print("Usage: python -m axionax-devtools <command>")

if __name__ == '__main__':
    main()
