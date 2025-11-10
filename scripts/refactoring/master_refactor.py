#!/usr/bin/env python3
"""
Master Refactor Script
รันการ refactor ทั้งหมดในคำสั่งเดียว
"""

import subprocess
import sys
from pathlib import Path

BOLD = '\033[1m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
RESET = '\033[0m'

def run_command(description: str, command: list):
    """รันคำสั่งและแสดงผล"""
    print(f"\n{BOLD}{BLUE}{'='*80}{RESET}")
    print(f"{BOLD}{BLUE}{description}{RESET}")
    print(f"{BOLD}{BLUE}{'='*80}{RESET}\n")
    
    result = subprocess.run(command, shell=True)
    
    if result.returncode != 0:
        print(f"{YELLOW}⚠ Warning: {description} returned non-zero exit code{RESET}")
    
    return result.returncode

def main():
    print(f"\n{BOLD}{MAGENTA}{'='*80}{RESET}")
    print(f"{BOLD}{MAGENTA}🚀 AXIONAX PROTOCOL - MASTER REFACTOR & CLEAN{RESET}")
    print(f"{BOLD}{MAGENTA}{'='*80}{RESET}\n")
    
    scripts = [
        ("📋 Step 1: Health Check", "python check_repo_health.py"),
        ("🔗 Step 2: Link Testing", "python test_repo_links.py"),
        ("🔍 Step 3: Code Quality Analysis", "python analyze_code_quality.py"),
        ("🧹 Step 4: Refactor & Clean", "python refactor_and_clean.py"),
        ("✅ Step 5: Final Integration Test", "python test_repo_integration.py"),
    ]
    
    results = {}
    
    for description, command in scripts:
        exit_code = run_command(description, command)
        results[description] = exit_code
    
    # Summary
    print(f"\n{BOLD}{MAGENTA}{'='*80}{RESET}")
    print(f"{BOLD}{MAGENTA}📊 EXECUTION SUMMARY{RESET}")
    print(f"{BOLD}{MAGENTA}{'='*80}{RESET}\n")
    
    all_success = True
    for description, exit_code in results.items():
        status = f"{GREEN}✓ SUCCESS{RESET}" if exit_code == 0 else f"{YELLOW}⚠ WARNING{RESET}"
        print(f"{status} - {description}")
        if exit_code != 0:
            all_success = False
    
    print(f"\n{BOLD}{MAGENTA}{'='*80}{RESET}")
    
    if all_success:
        print(f"{BOLD}{GREEN}✅ All steps completed successfully!{RESET}")
    else:
        print(f"{BOLD}{YELLOW}⚠ Some steps completed with warnings. Review output above.{RESET}")
    
    print(f"\n{BOLD}💡 Next Steps:{RESET}")
    print(f"  1. Review changes: git diff")
    print(f"  2. Test builds: npm run build / cargo build")
    print(f"  3. Run tests: npm test / cargo test")
    print(f"  4. Commit: git add -A && git commit -m 'refactor: improve code quality'")
    print(f"  5. Push: git push")
    print(f"{BOLD}{MAGENTA}{'='*80}{RESET}\n")

if __name__ == '__main__':
    main()
