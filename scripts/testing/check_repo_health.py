#!/usr/bin/env python3
"""
Repository Health Checker
ตรวจสอบสุขภาพและความพร้อมของทุก repository
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

# ANSI Colors
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

class RepoHealthChecker:
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.repos = [
            'axionax-core',
            'axionax-sdk-ts',
            'axionax-web',
            'axionax-marketplace',
            'axionax-docs',
            'axionax-deploy',
            'axionax-devtools'
        ]
        self.issues = []
        self.recommendations = []

    def print_header(self):
        print(f"\n{BOLD}{'='*80}{RESET}")
        print(f"{BOLD}{BLUE}🏥 AXIONAX REPOSITORY HEALTH CHECK{RESET}")
        print(f"{BOLD}{'='*80}{RESET}")
        print(f"เวลา: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Workspace: {self.workspace_root}")
        print(f"{BOLD}{'='*80}{RESET}\n")

    def check_gitignore(self, repo_name: str) -> Dict:
        """ตรวจสอบ .gitignore files"""
        repo_path = self.workspace_root / repo_name
        gitignore_path = repo_path / '.gitignore'
        
        result = {
            'repo': repo_name,
            'check': 'gitignore',
            'status': 'pass',
            'issues': []
        }
        
        if not gitignore_path.exists():
            result['status'] = 'fail'
            result['issues'].append('ไม่มีไฟล์ .gitignore')
            self.issues.append(f"{repo_name}: ไม่มี .gitignore")
            self.recommendations.append(f"สร้าง .gitignore ใน {repo_name}")
            return result
        
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # ตรวจสอบ patterns ที่ควรมี
        required_patterns = {
            'rust': ['target/', 'Cargo.lock', '*.swp', '*.swo'],
            'typescript': ['node_modules/', 'dist/', 'build/', '.next/', '.env', '*.log'],
            'documentation': ['.venv/', '__pycache__/', '*.pyc'],
            'deployment': ['node_modules/', '.env', '*.log'],
            'tools': ['*.log', '.venv/']
        }
        
        # กำหนดประเภท repo
        repo_type = None
        if repo_name == 'axionax-core':
            repo_type = 'rust'
        elif repo_name in ['axionax-sdk-ts', 'axionax-web', 'axionax-marketplace']:
            repo_type = 'typescript'
        elif repo_name == 'axionax-docs':
            repo_type = 'documentation'
        elif repo_name == 'axionax-deploy':
            repo_type = 'deployment'
        elif repo_name == 'axionax-devtools':
            repo_type = 'tools'
        
        if repo_type:
            missing_patterns = []
            for pattern in required_patterns[repo_type]:
                if pattern not in content:
                    missing_patterns.append(pattern)
            
            if missing_patterns:
                result['status'] = 'warn'
                result['issues'].append(f'ควรเพิ่ม patterns: {", ".join(missing_patterns)}')
                self.recommendations.append(f"เพิ่ม {', '.join(missing_patterns)} ใน {repo_name}/.gitignore")
        
        return result

    def check_uncommitted_files(self, repo_name: str) -> Dict:
        """ตรวจสอบไฟล์ที่ยังไม่ได้ commit"""
        import subprocess
        
        repo_path = self.workspace_root / repo_name
        result = {
            'repo': repo_name,
            'check': 'uncommitted_files',
            'status': 'pass',
            'issues': []
        }
        
        try:
            # ดึง git status
            cmd_result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=repo_path,
                capture_output=True,
                text=True
            )
            
            if cmd_result.returncode == 0:
                lines = cmd_result.stdout.strip().split('\n')
                lines = [l for l in lines if l.strip()]
                
                if lines:
                    # แยกประเภทไฟล์
                    untracked = []
                    modified = []
                    
                    for line in lines:
                        status = line[:2]
                        filename = line[3:].strip()
                        
                        if status.strip() == '??':
                            untracked.append(filename)
                        else:
                            modified.append(filename)
                    
                    # ตรวจสอบว่าเป็นไฟล์ที่ควร ignore หรือไม่
                    should_ignore = []
                    should_commit = []
                    
                    for file in untracked + modified:
                        if any(pattern in file for pattern in ['target/', 'node_modules/', '__pycache__', '.pyc', '.log', '.swp', '.swo']):
                            should_ignore.append(file)
                        else:
                            should_commit.append(file)
                    
                    if should_ignore:
                        result['status'] = 'warn'
                        result['issues'].append(f'มีไฟล์ที่ควร ignore: {len(should_ignore)} ไฟล์')
                        self.issues.append(f"{repo_name}: มี {len(should_ignore)} ไฟล์ที่ควร ignore")
                        self.recommendations.append(f"ปรับปรุง .gitignore ใน {repo_name}")
                    
                    if should_commit:
                        result['status'] = 'warn'
                        result['issues'].append(f'มีไฟล์ยังไม่ commit: {", ".join(should_commit[:3])}{"..." if len(should_commit) > 3 else ""}')
                        self.recommendations.append(f"Commit ไฟล์ใน {repo_name}: {', '.join(should_commit)}")
        
        except Exception as e:
            result['status'] = 'fail'
            result['issues'].append(f'เกิดข้อผิดพลาด: {str(e)}')
        
        return result

    def check_package_lock(self, repo_name: str) -> Dict:
        """ตรวจสอบ package-lock.json"""
        repo_path = self.workspace_root / repo_name
        package_json = repo_path / 'package.json'
        package_lock = repo_path / 'package-lock.json'
        
        result = {
            'repo': repo_name,
            'check': 'package_lock',
            'status': 'pass',
            'issues': []
        }
        
        if not package_json.exists():
            result['status'] = 'skip'
            return result
        
        if not package_lock.exists():
            result['status'] = 'warn'
            result['issues'].append('ไม่มี package-lock.json (ควร commit)')
            self.recommendations.append(f"Run 'npm install' และ commit package-lock.json ใน {repo_name}")
        
        return result

    def check_dependency_versions(self, repo_name: str) -> Dict:
        """ตรวจสอบ dependency versions"""
        repo_path = self.workspace_root / repo_name
        package_json = repo_path / 'package.json'
        
        result = {
            'repo': repo_name,
            'check': 'dependency_versions',
            'status': 'pass',
            'issues': []
        }
        
        if not package_json.exists():
            result['status'] = 'skip'
            return result
        
        try:
            with open(package_json, 'r', encoding='utf-8') as f:
                pkg = json.load(f)
            
            deps = pkg.get('dependencies', {})
            
            # ตรวจสอบ @axionax/sdk
            if '@axionax/sdk' in deps:
                version = deps['@axionax/sdk']
                
                if not version.startswith('file:'):
                    result['status'] = 'fail'
                    result['issues'].append(f'@axionax/sdk ใช้ {version} แทน file: link')
                    self.issues.append(f"{repo_name}: @axionax/sdk ไม่ได้ใช้ file: link")
                    self.recommendations.append(f"เปลี่ยน @axionax/sdk เป็น 'file:../axionax-sdk-ts' ใน {repo_name}")
                elif not version.endswith('axionax-sdk-ts'):
                    result['status'] = 'warn'
                    result['issues'].append(f'@axionax/sdk path อาจไม่ถูกต้อง: {version}')
        
        except Exception as e:
            result['status'] = 'fail'
            result['issues'].append(f'เกิดข้อผิดพลาด: {str(e)}')
        
        return result

    def check_readme(self, repo_name: str) -> Dict:
        """ตรวจสอบ README.md"""
        repo_path = self.workspace_root / repo_name
        readme_path = repo_path / 'README.md'
        
        result = {
            'repo': repo_name,
            'check': 'readme',
            'status': 'pass',
            'issues': []
        }
        
        if not readme_path.exists():
            result['status'] = 'warn'
            result['issues'].append('ไม่มี README.md')
            self.recommendations.append(f"สร้าง README.md ใน {repo_name}")
            return result
        
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # ตรวจสอบเนื้อหาพื้นฐาน
        if len(content.strip()) < 100:
            result['status'] = 'warn'
            result['issues'].append('README.md มีเนื้อหาน้อยเกินไป')
            self.recommendations.append(f"เพิ่มเนื้อหาใน {repo_name}/README.md")
        
        # ตรวจสอบว่ามี sections สำคัญหรือไม่
        important_sections = ['installation', 'usage', 'development']
        missing_sections = []
        
        for section in important_sections:
            if section.lower() not in content.lower():
                missing_sections.append(section)
        
        if missing_sections:
            result['status'] = 'info'
            result['issues'].append(f'ควรเพิ่ม sections: {", ".join(missing_sections)}')
        
        return result

    def run_all_checks(self):
        """รันการตรวจสอบทั้งหมด"""
        self.print_header()
        
        all_results = []
        
        for repo_name in self.repos:
            repo_path = self.workspace_root / repo_name
            
            if not repo_path.exists():
                print(f"{RED}⚠ ข้าม {repo_name}: ไม่พบ directory{RESET}")
                continue
            
            print(f"\n{BOLD}{BLUE}Checking: {repo_name}{RESET}")
            print(f"{'─'*80}")
            
            # Run checks
            checks = [
                self.check_gitignore(repo_name),
                self.check_uncommitted_files(repo_name),
                self.check_package_lock(repo_name),
                self.check_dependency_versions(repo_name),
                self.check_readme(repo_name)
            ]
            
            for check_result in checks:
                all_results.append(check_result)
                self.print_check_result(check_result)
        
        return all_results

    def print_check_result(self, result: Dict):
        """พิมพ์ผลการตรวจสอบ"""
        status = result['status']
        
        if status == 'pass':
            icon = '✅'
            color = GREEN
        elif status == 'warn':
            icon = '⚠️'
            color = YELLOW
        elif status == 'fail':
            icon = '❌'
            color = RED
        elif status == 'info':
            icon = 'ℹ️'
            color = BLUE
        else:  # skip
            icon = '⏭️'
            color = RESET
        
        print(f"  {icon} {result['check'].replace('_', ' ').title()}: {color}{status.upper()}{RESET}")
        
        if result['issues']:
            for issue in result['issues']:
                print(f"     • {issue}")

    def print_summary(self):
        """พิมพ์สรุป"""
        print(f"\n{BOLD}{'='*80}{RESET}")
        print(f"{BOLD}📊 สรุปผลการตรวจสอบ{RESET}")
        print(f"{BOLD}{'='*80}{RESET}")
        
        if not self.issues:
            print(f"{GREEN}✅ ไม่พบปัญหาร้ายแรง!{RESET}")
        else:
            print(f"{RED}❌ พบปัญหา {len(self.issues)} จุด:{RESET}")
            for i, issue in enumerate(self.issues, 1):
                print(f"  {i}. {issue}")
        
        if self.recommendations:
            print(f"\n{BOLD}💡 คำแนะนำในการแก้ไข ({len(self.recommendations)} จุด):{RESET}")
            for i, rec in enumerate(self.recommendations, 1):
                print(f"  {i}. {rec}")
        
        print(f"\n{BOLD}{'='*80}{RESET}\n")

def main():
    workspace = os.getcwd()
    
    print(f"{BOLD}🏥 Repository Health Checker{RESET}")
    print(f"Workspace: {workspace}\n")
    
    checker = RepoHealthChecker(workspace)
    checker.run_all_checks()
    checker.print_summary()

if __name__ == '__main__':
    main()
