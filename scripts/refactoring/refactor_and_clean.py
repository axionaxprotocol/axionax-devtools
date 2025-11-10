#!/usr/bin/env python3
"""
Axionax Protocol Code Refactoring and Cleaning Tool
เครื่องมือสำหรับ refactor และทำความสะอาด code ทั้ง protocol
"""

import os
import sys
import re
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Set

# ANSI Colors
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'

class CodeRefactorCleaner:
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.repos = {
            'axionax-core': {'type': 'rust', 'path': self.workspace_root / 'axionax-core'},
            'axionax-sdk-ts': {'type': 'typescript', 'path': self.workspace_root / 'axionax-sdk-ts'},
            'axionax-web': {'type': 'typescript', 'path': self.workspace_root / 'axionax-web'},
            'axionax-marketplace': {'type': 'typescript', 'path': self.workspace_root / 'axionax-marketplace'},
            'axionax-docs': {'type': 'documentation', 'path': self.workspace_root / 'axionax-docs'},
            'axionax-deploy': {'type': 'deployment', 'path': self.workspace_root / 'axionax-deploy'},
            'axionax-devtools': {'type': 'tools', 'path': self.workspace_root / 'axionax-devtools'}
        }
        self.changes = []
        self.errors = []

    def print_header(self):
        print(f"\n{BOLD}{'='*80}{RESET}")
        print(f"{BOLD}{MAGENTA}🔧 AXIONAX PROTOCOL CODE REFACTOR & CLEAN{RESET}")
        print(f"{BOLD}{'='*80}{RESET}")
        print(f"เวลา: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Workspace: {self.workspace_root}")
        print(f"{BOLD}{'='*80}{RESET}\n")

    # ==================== GITIGNORE MANAGEMENT ====================
    
    def create_or_update_gitignore(self, repo_name: str, repo_info: dict):
        """สร้างหรืออัพเดท .gitignore"""
        print(f"\n{CYAN}📝 Updating .gitignore for {repo_name}...{RESET}")
        
        gitignore_path = repo_info['path'] / '.gitignore'
        
        # กำหนด patterns ตามประเภท
        patterns = {
            'rust': [
                '# Rust',
                'target/',
                'Cargo.lock',
                '**/*.rs.bk',
                '*.pdb',
                '',
                '# IDE',
                '*.swp',
                '*.swo',
                '*~',
                '.vscode/',
                '.idea/',
                '',
                '# OS',
                '.DS_Store',
                'Thumbs.db',
                '',
                '# Node (for tools)',
                'node_modules/',
                'package-lock.json',
                '',
                '# Logs',
                '*.log',
                'npm-debug.log*',
                'yarn-debug.log*',
                'yarn-error.log*'
            ],
            'typescript': [
                '# Dependencies',
                'node_modules/',
                '',
                '# Build outputs',
                'dist/',
                'build/',
                '.next/',
                'out/',
                '',
                '# Environment',
                '.env',
                '.env.local',
                '.env.development.local',
                '.env.test.local',
                '.env.production.local',
                '',
                '# Logs',
                '*.log',
                'npm-debug.log*',
                'yarn-debug.log*',
                'yarn-error.log*',
                'lerna-debug.log*',
                '',
                '# IDE',
                '.vscode/',
                '.idea/',
                '*.swp',
                '*.swo',
                '*~',
                '',
                '# OS',
                '.DS_Store',
                'Thumbs.db',
                '',
                '# Testing',
                'coverage/',
                '.nyc_output/',
                '',
                '# Cache',
                '.cache/',
                '.parcel-cache/',
                '.eslintcache/'
            ],
            'documentation': [
                '# Python',
                '__pycache__/',
                '*.py[cod]',
                '*$py.class',
                '*.so',
                '.Python',
                '',
                '# Virtual Environment',
                'venv/',
                'env/',
                'ENV/',
                '.venv/',
                '',
                '# Build',
                'build/',
                'dist/',
                '_build/',
                '',
                '# IDE',
                '.vscode/',
                '.idea/',
                '*.swp',
                '*.swo',
                '',
                '# OS',
                '.DS_Store',
                'Thumbs.db',
                '',
                '# Logs',
                '*.log'
            ],
            'deployment': [
                '# Dependencies',
                'node_modules/',
                '',
                '# Environment',
                '.env',
                '.env.local',
                '.env.*.local',
                '',
                '# Logs',
                '*.log',
                'npm-debug.log*',
                '',
                '# Docker',
                '*.pid',
                '',
                '# IDE',
                '.vscode/',
                '.idea/',
                '',
                '# OS',
                '.DS_Store',
                'Thumbs.db',
                '',
                '# Certificates',
                '*.pem',
                '*.key',
                '*.crt'
            ],
            'tools': [
                '# Python',
                '__pycache__/',
                '*.py[cod]',
                '.venv/',
                'venv/',
                '',
                '# Node',
                'node_modules/',
                '',
                '# Logs',
                '*.log',
                '',
                '# IDE',
                '.vscode/',
                '.idea/',
                '',
                '# OS',
                '.DS_Store',
                'Thumbs.db'
            ]
        }
        
        repo_type = repo_info['type']
        new_content = '\n'.join(patterns.get(repo_type, ['node_modules/', '*.log']))
        
        # ตรวจสอบว่ามี .gitignore อยู่แล้วหรือไม่
        if gitignore_path.exists():
            with open(gitignore_path, 'r', encoding='utf-8') as f:
                old_content = f.read()
            
            if old_content.strip() == new_content.strip():
                print(f"  ⏭️  ไม่ต้องเปลี่ยนแปลง")
                return
        
        # เขียนไฟล์
        with open(gitignore_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(new_content)
        
        self.changes.append(f"{repo_name}: อัพเดท .gitignore")
        print(f"  {GREEN}✓{RESET} อัพเดท .gitignore แล้ว")

    # ==================== TYPESCRIPT/JAVASCRIPT CLEANING ====================
    
    def clean_typescript_code(self, repo_name: str, repo_info: dict):
        """ทำความสะอาด TypeScript/JavaScript code"""
        if repo_info['type'] != 'typescript':
            return
        
        print(f"\n{CYAN}🧹 Cleaning TypeScript code in {repo_name}...{RESET}")
        
        src_dir = repo_info['path'] / 'src'
        if not src_dir.exists():
            print(f"  ⏭️  ไม่มี src directory")
            return
        
        changes_made = 0
        
        # หาไฟล์ .ts และ .tsx ทั้งหมด
        ts_files = list(src_dir.glob('**/*.ts')) + list(src_dir.glob('**/*.tsx'))
        
        for file_path in ts_files:
            if file_path.name.endswith('.d.ts'):
                continue  # ข้าม type definition files
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # 1. ลบ console.log ที่เหลือค้าง (แต่เก็บ console.error และ console.warn)
                content = re.sub(r'^(\s*)console\.log\([^)]*\);?\s*$', '', content, flags=re.MULTILINE)
                
                # 2. ลบ debugger statements
                content = re.sub(r'^(\s*)debugger;?\s*$', '', content, flags=re.MULTILINE)
                
                # 3. ลบ empty lines ที่ซ้อนกันเกิน 2 บรรทัด
                content = re.sub(r'\n{3,}', '\n\n', content)
                
                # 4. ลบ trailing whitespace
                content = re.sub(r'[ \t]+$', '', content, flags=re.MULTILINE)
                
                # 5. ตรวจสอบ unused imports (basic check)
                # Note: การตรวจสอบ unused imports ที่แม่นยำต้องใช้ AST parser
                
                # 6. แน่ใจว่าไฟล์ลงท้ายด้วย newline
                if content and not content.endswith('\n'):
                    content += '\n'
                
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
                        f.write(content)
                    changes_made += 1
                    
            except Exception as e:
                self.errors.append(f"{repo_name}/{file_path.name}: {str(e)}")
        
        if changes_made > 0:
            self.changes.append(f"{repo_name}: ทำความสะอาด {changes_made} ไฟล์ TypeScript")
            print(f"  {GREEN}✓{RESET} ทำความสะอาด {changes_made} ไฟล์")
        else:
            print(f"  ⏭️  ไม่มีการเปลี่ยนแปลง")

    # ==================== RUST CODE CLEANING ====================
    
    def clean_rust_code(self, repo_name: str, repo_info: dict):
        """ทำความสะอาด Rust code"""
        if repo_info['type'] != 'rust':
            return
        
        print(f"\n{CYAN}🧹 Cleaning Rust code in {repo_name}...{RESET}")
        
        # หา .rs files ทั้งหมด
        rs_files = list(repo_info['path'].glob('**/*.rs'))
        
        changes_made = 0
        
        for file_path in rs_files:
            # ข้าม target directory
            if 'target' in str(file_path):
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # 1. ลบ println! ที่ใช้สำหรับ debug (แต่เก็บ error! และ warn!)
                # Note: นี่คือการทำความสะอาดเบื้องต้น ควรใช้ proper logging แทน
                
                # 2. ลบ empty lines ที่ซ้อนกันเกิน 2 บรรทัด
                content = re.sub(r'\n{3,}', '\n\n', content)
                
                # 3. ลบ trailing whitespace
                content = re.sub(r'[ \t]+$', '', content, flags=re.MULTILINE)
                
                # 4. แน่ใจว่าไฟล์ลงท้ายด้วย newline
                if content and not content.endswith('\n'):
                    content += '\n'
                
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
                        f.write(content)
                    changes_made += 1
                    
            except Exception as e:
                self.errors.append(f"{repo_name}/{file_path.name}: {str(e)}")
        
        if changes_made > 0:
            self.changes.append(f"{repo_name}: ทำความสะอาด {changes_made} ไฟล์ Rust")
            print(f"  {GREEN}✓{RESET} ทำความสะอาด {changes_made} ไฟล์")
        else:
            print(f"  ⏭️  ไม่มีการเปลี่ยนแปลง")

    # ==================== FORMATTING ====================
    
    def run_prettier(self, repo_name: str, repo_info: dict):
        """รัน Prettier สำหรับ TypeScript repos"""
        if repo_info['type'] != 'typescript':
            return
        
        print(f"\n{CYAN}💅 Running Prettier on {repo_name}...{RESET}")
        
        package_json = repo_info['path'] / 'package.json'
        if not package_json.exists():
            print(f"  ⏭️  ไม่มี package.json")
            return
        
        # ตรวจสอบว่ามี prettier หรือไม่
        try:
            with open(package_json, 'r', encoding='utf-8') as f:
                pkg = json.load(f)
            
            dev_deps = pkg.get('devDependencies', {})
            if 'prettier' not in dev_deps:
                print(f"  ⏭️  ไม่มี Prettier ใน devDependencies")
                return
            
            # รัน prettier
            result = subprocess.run(
                ['npx', 'prettier', '--write', 'src/**/*.{ts,tsx,js,jsx,json}'],
                cwd=repo_info['path'],
                capture_output=True,
                text=True,
                shell=True
            )
            
            if result.returncode == 0:
                self.changes.append(f"{repo_name}: รัน Prettier")
                print(f"  {GREEN}✓{RESET} รัน Prettier สำเร็จ")
            else:
                print(f"  {YELLOW}⚠{RESET}  Prettier: {result.stderr[:100]}")
                
        except Exception as e:
            self.errors.append(f"{repo_name} Prettier: {str(e)}")
            print(f"  {RED}✗{RESET} เกิดข้อผิดพลาด: {str(e)}")

    def run_rustfmt(self, repo_name: str, repo_info: dict):
        """รัน rustfmt สำหรับ Rust repos"""
        if repo_info['type'] != 'rust':
            return
        
        print(f"\n{CYAN}💅 Running rustfmt on {repo_name}...{RESET}")
        
        try:
            result = subprocess.run(
                ['cargo', 'fmt', '--all'],
                cwd=repo_info['path'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.changes.append(f"{repo_name}: รัน rustfmt")
                print(f"  {GREEN}✓{RESET} รัน rustfmt สำเร็จ")
            else:
                print(f"  {YELLOW}⚠{RESET}  rustfmt: {result.stderr[:100]}")
                
        except FileNotFoundError:
            print(f"  {YELLOW}⚠{RESET}  rustfmt ไม่ได้ติดตั้ง")
        except Exception as e:
            self.errors.append(f"{repo_name} rustfmt: {str(e)}")
            print(f"  {RED}✗{RESET} เกิดข้อผิดพลาด: {str(e)}")

    # ==================== LINTING ====================
    
    def run_eslint_fix(self, repo_name: str, repo_info: dict):
        """รัน ESLint --fix สำหรับ TypeScript repos"""
        if repo_info['type'] != 'typescript':
            return
        
        print(f"\n{CYAN}🔍 Running ESLint --fix on {repo_name}...{RESET}")
        
        package_json = repo_info['path'] / 'package.json'
        if not package_json.exists():
            print(f"  ⏭️  ไม่มี package.json")
            return
        
        try:
            # รัน eslint --fix
            result = subprocess.run(
                ['npx', 'eslint', 'src', '--ext', '.ts,.tsx,.js,.jsx', '--fix'],
                cwd=repo_info['path'],
                capture_output=True,
                text=True,
                shell=True
            )
            
            # ESLint อาจ return non-zero ถ้ายังมี errors หลัง fix
            if "error" not in result.stdout.lower() or result.returncode == 0:
                self.changes.append(f"{repo_name}: รัน ESLint --fix")
                print(f"  {GREEN}✓{RESET} รัน ESLint --fix สำเร็จ")
            else:
                print(f"  {YELLOW}⚠{RESET}  ESLint พบ errors บางส่วนที่ไม่สามารถ fix อัตโนมัติได้")
                
        except Exception as e:
            print(f"  {YELLOW}⚠{RESET}  ข้าม ESLint (อาจไม่มีติดตั้ง)")

    def run_clippy_fix(self, repo_name: str, repo_info: dict):
        """รัน clippy --fix สำหรับ Rust repos"""
        if repo_info['type'] != 'rust':
            return
        
        print(f"\n{CYAN}🔍 Running cargo clippy --fix on {repo_name}...{RESET}")
        
        try:
            result = subprocess.run(
                ['cargo', 'clippy', '--fix', '--allow-dirty', '--allow-staged'],
                cwd=repo_info['path'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.changes.append(f"{repo_name}: รัน clippy --fix")
                print(f"  {GREEN}✓{RESET} รัน clippy --fix สำเร็จ")
            else:
                print(f"  {YELLOW}⚠{RESET}  clippy: {result.stderr[:100]}")
                
        except FileNotFoundError:
            print(f"  {YELLOW}⚠{RESET}  cargo clippy ไม่ได้ติดตั้ง")
        except Exception as e:
            self.errors.append(f"{repo_name} clippy: {str(e)}")
            print(f"  {RED}✗{RESET} เกิดข้อผิดพลาด: {str(e)}")

    # ==================== UNUSED CODE DETECTION ====================
    
    def detect_unused_files(self, repo_name: str, repo_info: dict):
        """ตรวจหาไฟล์ที่ไม่ได้ใช้งาน"""
        print(f"\n{CYAN}🔎 Detecting unused files in {repo_name}...{RESET}")
        
        unused = []
        
        # ตรวจสอบไฟล์ที่น่าสงสัย
        suspicious_patterns = [
            '*.backup',
            '*.bak',
            '*.old',
            '*.tmp',
            '*~',
            '*.swp',
            '*.swo'
        ]
        
        for pattern in suspicious_patterns:
            for file_path in repo_info['path'].glob(f'**/{pattern}'):
                # ข้าม node_modules และ target
                if 'node_modules' in str(file_path) or 'target' in str(file_path):
                    continue
                unused.append(file_path)
        
        if unused:
            print(f"  {YELLOW}⚠{RESET}  พบไฟล์ที่น่าจะไม่ได้ใช้: {len(unused)} ไฟล์")
            for file_path in unused[:5]:  # แสดงแค่ 5 ไฟล์แรก
                print(f"     - {file_path.relative_to(repo_info['path'])}")
            if len(unused) > 5:
                print(f"     ... และอีก {len(unused) - 5} ไฟล์")
        else:
            print(f"  {GREEN}✓{RESET} ไม่พบไฟล์ที่น่าสงสัย")

    # ==================== DOCUMENTATION ====================
    
    def check_documentation(self, repo_name: str, repo_info: dict):
        """ตรวจสอบ documentation"""
        print(f"\n{CYAN}📚 Checking documentation in {repo_name}...{RESET}")
        
        readme = repo_info['path'] / 'README.md'
        issues = []
        
        if not readme.exists():
            issues.append("ไม่มี README.md")
        else:
            with open(readme, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # ตรวจสอบ sections สำคัญ
            required_sections = ['installation', 'usage', 'development']
            missing = [s for s in required_sections if s.lower() not in content.lower()]
            
            if missing:
                issues.append(f"ขาด sections: {', '.join(missing)}")
            
            if len(content) < 200:
                issues.append("README.md สั้นเกินไป")
        
        if issues:
            print(f"  {YELLOW}⚠{RESET}  พบปัญหา:")
            for issue in issues:
                print(f"     - {issue}")
        else:
            print(f"  {GREEN}✓{RESET} Documentation ดูดี")

    # ==================== MAIN EXECUTION ====================
    
    def run_all_refactoring(self, skip_formatting: bool = False, skip_linting: bool = False):
        """รัน refactoring และ cleaning ทั้งหมด"""
        self.print_header()
        
        for repo_name, repo_info in self.repos.items():
            if not repo_info['path'].exists():
                print(f"{RED}⚠ ข้าม {repo_name}: ไม่พบ directory{RESET}")
                continue
            
            print(f"\n{BOLD}{BLUE}{'='*80}{RESET}")
            print(f"{BOLD}{BLUE}Processing: {repo_name}{RESET}")
            print(f"{BOLD}{BLUE}{'='*80}{RESET}")
            
            # 1. Update .gitignore
            self.create_or_update_gitignore(repo_name, repo_info)
            
            # 2. Clean code
            if repo_info['type'] == 'typescript':
                self.clean_typescript_code(repo_name, repo_info)
            elif repo_info['type'] == 'rust':
                self.clean_rust_code(repo_name, repo_info)
            
            # 3. Format code
            if not skip_formatting:
                if repo_info['type'] == 'typescript':
                    self.run_prettier(repo_name, repo_info)
                elif repo_info['type'] == 'rust':
                    self.run_rustfmt(repo_name, repo_info)
            
            # 4. Lint and fix
            if not skip_linting:
                if repo_info['type'] == 'typescript':
                    self.run_eslint_fix(repo_name, repo_info)
                elif repo_info['type'] == 'rust':
                    self.run_clippy_fix(repo_name, repo_info)
            
            # 5. Detect unused files
            self.detect_unused_files(repo_name, repo_info)
            
            # 6. Check documentation
            self.check_documentation(repo_name, repo_info)

    def print_summary(self):
        """พิมพ์สรุปผล"""
        print(f"\n{BOLD}{'='*80}{RESET}")
        print(f"{BOLD}📊 สรุปผลการ Refactor & Clean{RESET}")
        print(f"{BOLD}{'='*80}{RESET}")
        
        if self.changes:
            print(f"\n{GREEN}✅ การเปลี่ยนแปลง ({len(self.changes)} รายการ):{RESET}")
            for i, change in enumerate(self.changes, 1):
                print(f"  {i}. {change}")
        else:
            print(f"\n{YELLOW}⚠  ไม่มีการเปลี่ยนแปลง{RESET}")
        
        if self.errors:
            print(f"\n{RED}❌ ข้อผิดพลาด ({len(self.errors)} รายการ):{RESET}")
            for i, error in enumerate(self.errors, 1):
                print(f"  {i}. {error}")
        
        print(f"\n{BOLD}{'='*80}{RESET}")
        print(f"{BOLD}💡 คำแนะนำถัดไป:{RESET}")
        print(f"  1. ตรวจสอบการเปลี่ยนแปลงด้วย: git diff")
        print(f"  2. ทดสอบ build: npm run build (TypeScript) หรือ cargo build (Rust)")
        print(f"  3. รัน tests: npm test หรือ cargo test")
        print(f"  4. Commit การเปลี่ยนแปลง: git add -A && git commit -m 'refactor: clean and format code'")
        print(f"{BOLD}{'='*80}{RESET}\n")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Axionax Protocol Code Refactoring & Cleaning Tool')
    parser.add_argument('--skip-formatting', action='store_true', help='ข้ามการ format code')
    parser.add_argument('--skip-linting', action='store_true', help='ข้ามการ lint และ fix')
    parser.add_argument('--repo', type=str, help='ระบุ repo ที่ต้องการ refactor (ถ้าไม่ระบุจะทำทั้งหมด)')
    
    args = parser.parse_args()
    
    workspace = os.getcwd()
    
    print(f"{BOLD}{MAGENTA}🔧 Axionax Protocol Refactor & Clean Tool{RESET}")
    print(f"Workspace: {workspace}\n")
    
    cleaner = CodeRefactorCleaner(workspace)
    
    if args.repo:
        # Refactor เฉพาะ repo ที่ระบุ
        if args.repo in cleaner.repos:
            repo_info = cleaner.repos[args.repo]
            print(f"Refactoring only: {args.repo}")
            # TODO: Implement single repo refactoring
        else:
            print(f"{RED}Error: ไม่พบ repo '{args.repo}'{RESET}")
            sys.exit(1)
    else:
        # Refactor ทั้งหมด
        cleaner.run_all_refactoring(
            skip_formatting=args.skip_formatting,
            skip_linting=args.skip_linting
        )
    
    cleaner.print_summary()

if __name__ == '__main__':
    main()
