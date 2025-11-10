#!/usr/bin/env python3
"""
Quick Fix Script
แก้ไขปัญหาที่พบบ่อยอัตโนมัติ
"""

import os
import subprocess
from pathlib import Path

BOLD = '\033[1m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RED = '\033[91m'
RESET = '\033[0m'

def fix_all_gitignore():
    """แก้ไข .gitignore ทั้งหมด"""
    print(f"\n{BOLD}{BLUE}🔧 Fixing .gitignore files...{RESET}")
    
    result = subprocess.run(['python', 'refactor_and_clean.py', '--skip-formatting', '--skip-linting'], 
                          capture_output=True)
    
    if result.returncode == 0:
        print(f"{GREEN}✓ .gitignore files updated{RESET}")
    else:
        print(f"{YELLOW}⚠ Some issues encountered{RESET}")

def commit_package_locks():
    """Commit package-lock.json ที่ยังไม่ได้ commit"""
    print(f"\n{BOLD}{BLUE}📦 Committing package-lock.json files...{RESET}")
    
    repos = ['axionax-marketplace', 'axionax-deploy']
    
    for repo in repos:
        repo_path = Path(os.getcwd()) / repo
        package_lock = repo_path / 'package-lock.json'
        
        if package_lock.exists():
            try:
                subprocess.run(['git', 'add', 'package-lock.json'], cwd=repo_path, check=True)
                subprocess.run(['git', 'commit', '-m', 'chore: add package-lock.json'], cwd=repo_path)
                print(f"{GREEN}✓ Committed {repo}/package-lock.json{RESET}")
            except subprocess.CalledProcessError:
                print(f"{YELLOW}⚠ No changes or already committed in {repo}{RESET}")

def clean_git_artifacts():
    """ทำความสะอาด git artifacts"""
    print(f"\n{BOLD}{BLUE}🧹 Cleaning git artifacts...{RESET}")
    
    repos = ['axionax-core', 'axionax-sdk-ts', 'axionax-web', 
             'axionax-marketplace', 'axionax-docs', 'axionax-deploy', 'axionax-devtools']
    
    for repo in repos:
        repo_path = Path(os.getcwd()) / repo
        
        if repo_path.exists():
            try:
                # Run git prune
                subprocess.run(['git', 'prune'], cwd=repo_path, capture_output=True)
                
                # Run git gc
                subprocess.run(['git', 'gc', '--auto'], cwd=repo_path, capture_output=True)
                
                print(f"{GREEN}✓ Cleaned {repo}{RESET}")
            except Exception as e:
                print(f"{YELLOW}⚠ Error cleaning {repo}: {str(e)}{RESET}")

def install_all_dependencies():
    """Install dependencies ในทุก repo"""
    print(f"\n{BOLD}{BLUE}📥 Installing dependencies...{RESET}")
    
    # TypeScript repos
    ts_repos = ['axionax-sdk-ts', 'axionax-web', 'axionax-marketplace', 'axionax-deploy']
    
    for repo in ts_repos:
        repo_path = Path(os.getcwd()) / repo
        package_json = repo_path / 'package.json'
        
        if package_json.exists():
            print(f"  Installing in {repo}...")
            try:
                subprocess.run('npm install', cwd=repo_path, check=True, capture_output=True, shell=True)
                print(f"{GREEN}  ✓ {repo} dependencies installed{RESET}")
            except subprocess.CalledProcessError as e:
                print(f"{RED}  ✗ Error installing {repo} dependencies{RESET}")

def fix_line_endings():
    """แก้ไข line endings เป็น LF"""
    print(f"\n{BOLD}{BLUE}📝 Fixing line endings...{RESET}")
    
    repos = ['axionax-core', 'axionax-sdk-ts', 'axionax-web', 
             'axionax-marketplace', 'axionax-docs', 'axionax-deploy', 'axionax-devtools']
    
    for repo in repos:
        repo_path = Path(os.getcwd()) / repo
        gitattributes = repo_path / '.gitattributes'
        
        if not gitattributes.exists():
            # Create .gitattributes
            content = """* text=auto
*.ts text eol=lf
*.tsx text eol=lf
*.js text eol=lf
*.jsx text eol=lf
*.rs text eol=lf
*.toml text eol=lf
*.json text eol=lf
*.md text eol=lf
*.yml text eol=lf
*.yaml text eol=lf
"""
            with open(gitattributes, 'w', encoding='utf-8', newline='\n') as f:
                f.write(content)
            
            print(f"{GREEN}✓ Created .gitattributes for {repo}{RESET}")

def main():
    print(f"\n{BOLD}{BLUE}{'='*80}{RESET}")
    print(f"{BOLD}{BLUE}🚀 AXIONAX QUICK FIX{RESET}")
    print(f"{BOLD}{BLUE}{'='*80}{RESET}\n")
    
    print("Select fixes to apply:")
    print("  1. Fix all .gitignore files")
    print("  2. Commit package-lock.json files")
    print("  3. Clean git artifacts")
    print("  4. Install all dependencies")
    print("  5. Fix line endings")
    print("  6. Run all fixes")
    print("  0. Exit")
    
    choice = input("\nEnter choice (0-6): ").strip()
    
    if choice == '1':
        fix_all_gitignore()
    elif choice == '2':
        commit_package_locks()
    elif choice == '3':
        clean_git_artifacts()
    elif choice == '4':
        install_all_dependencies()
    elif choice == '5':
        fix_line_endings()
    elif choice == '6':
        print(f"\n{BOLD}Running all fixes...{RESET}")
        fix_all_gitignore()
        fix_line_endings()
        install_all_dependencies()
        clean_git_artifacts()
        commit_package_locks()
        print(f"\n{GREEN}{BOLD}✅ All fixes completed!{RESET}")
    elif choice == '0':
        print("Exiting...")
        return
    else:
        print(f"{RED}Invalid choice{RESET}")
        return
    
    print(f"\n{BOLD}{BLUE}{'='*80}{RESET}")
    print(f"{BOLD}💡 Next steps:{RESET}")
    print(f"  1. Review changes: git status")
    print(f"  2. Test: python test_repo_integration.py")
    print(f"  3. Commit: git add -A && git commit -m 'fix: apply quick fixes'")
    print(f"{BOLD}{BLUE}{'='*80}{RESET}\n")

if __name__ == '__main__':
    main()
