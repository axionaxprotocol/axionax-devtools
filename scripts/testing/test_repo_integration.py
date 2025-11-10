#!/usr/bin/env python3
"""
Repository Integration Testing Tool
Tests actual connections and integrations between axionax repositories
Generates comprehensive test results and fix recommendations
"""

import os
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

class RepoIntegrationTester:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.repos = {
            'axionax-core': {
                'type': 'rust',
                'main_files': ['Cargo.toml', 'src/lib.rs', 'src/main.rs'],
                'test_command': 'cargo check --lib',
                'dependencies': []
            },
            'axionax-sdk-ts': {
                'type': 'typescript',
                'main_files': ['package.json', 'src/index.ts', 'tsconfig.json'],
                'test_command': 'npm run build',
                'dependencies': []
            },
            'axionax-web': {
                'type': 'nextjs',
                'main_files': ['package.json', 'next.config.js', 'tsconfig.json'],
                'test_command': 'npm run build',
                'dependencies': ['axionax-sdk-ts']
            },
            'axionax-marketplace': {
                'type': 'react',
                'main_files': ['package.json', 'src/App.tsx', 'tsconfig.json'],
                'test_command': 'npm run build',
                'dependencies': ['axionax-sdk-ts']
            },
            'axionax-docs': {
                'type': 'documentation',
                'main_files': ['README.md', 'index.md'],
                'test_command': None,
                'dependencies': ['axionax-core', 'axionax-sdk-ts', 'axionax-web']
            },
            'axionax-deploy': {
                'type': 'deployment',
                'main_files': ['docker-compose.yaml', 'setup_validator.sh'],
                'test_command': None,
                'dependencies': ['axionax-core']
            },
            'axionax-devtools': {
                'type': 'tools',
                'main_files': ['README.md', 'tools/'],
                'test_command': None,
                'dependencies': ['axionax-core']
            }
        }
        self.test_results = {}
        self.issues = []
        self.recommendations = []
        
    def test_repo_exists(self, repo_name: str) -> Dict:
        """Test if repository exists and is accessible"""
        repo_path = self.base_path / repo_name
        
        result = {
            'test': 'Repository Existence',
            'repo': repo_name,
            'status': 'PASS',
            'details': {},
            'issues': []
        }
        
        if not repo_path.exists():
            result['status'] = 'FAIL'
            result['issues'].append(f"Repository directory not found: {repo_path}")
            return result
        
        # Check if it's a git repo
        git_dir = repo_path / '.git'
        if not git_dir.exists():
            result['status'] = 'WARN'
            result['issues'].append("Not a git repository")
        
        # Check main files
        missing_files = []
        for main_file in self.repos[repo_name]['main_files']:
            file_path = repo_path / main_file
            if not file_path.exists():
                missing_files.append(main_file)
        
        if missing_files:
            result['status'] = 'WARN' if result['status'] == 'PASS' else result['status']
            result['issues'].append(f"Missing expected files: {', '.join(missing_files)}")
        
        result['details']['path'] = str(repo_path)
        result['details']['is_git'] = git_dir.exists()
        result['details']['missing_files'] = missing_files
        
        return result
    
    def test_git_status(self, repo_name: str) -> Dict:
        """Test git repository status"""
        repo_path = self.base_path / repo_name
        
        result = {
            'test': 'Git Status',
            'repo': repo_name,
            'status': 'PASS',
            'details': {},
            'issues': []
        }
        
        if not repo_path.exists():
            result['status'] = 'SKIP'
            result['issues'].append("Repository not found")
            return result
        
        try:
            os.chdir(repo_path)
            
            # Check branch
            branch = subprocess.run(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                capture_output=True, text=True, timeout=10
            )
            result['details']['branch'] = branch.stdout.strip()
            
            # Check remote
            remote = subprocess.run(
                ['git', 'remote', 'get-url', 'origin'],
                capture_output=True, text=True, timeout=10
            )
            result['details']['remote'] = remote.stdout.strip()
            
            # Check uncommitted changes
            status = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True, text=True, timeout=10
            )
            
            if status.stdout.strip():
                result['status'] = 'WARN'
                result['issues'].append("Repository has uncommitted changes")
                result['details']['uncommitted_files'] = len(status.stdout.strip().split('\n'))
            
            # Check if remote is accessible
            if 'github.com' in result['details'].get('remote', ''):
                result['details']['remote_accessible'] = True
            
        except subprocess.TimeoutExpired:
            result['status'] = 'FAIL'
            result['issues'].append("Git command timeout")
        except Exception as e:
            result['status'] = 'FAIL'
            result['issues'].append(f"Git error: {str(e)}")
        
        return result
    
    def test_package_json(self, repo_name: str) -> Dict:
        """Test package.json validity and dependencies"""
        repo_path = self.base_path / repo_name
        package_json = repo_path / 'package.json'
        
        result = {
            'test': 'Package.json Validation',
            'repo': repo_name,
            'status': 'PASS',
            'details': {},
            'issues': []
        }
        
        if not package_json.exists():
            result['status'] = 'SKIP'
            result['issues'].append("No package.json found")
            return result
        
        try:
            with open(package_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            result['details']['name'] = data.get('name', 'N/A')
            result['details']['version'] = data.get('version', 'N/A')
            
            # Check for required fields
            required_fields = ['name', 'version', 'scripts']
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                result['status'] = 'WARN'
                result['issues'].append(f"Missing required fields: {', '.join(missing_fields)}")
            
            # Count dependencies
            deps = data.get('dependencies', {})
            dev_deps = data.get('devDependencies', {})
            
            result['details']['total_dependencies'] = len(deps)
            result['details']['total_dev_dependencies'] = len(dev_deps)
            
            # Check for axionax dependencies
            axionax_deps = [dep for dep in deps.keys() if 'axionax' in dep.lower()]
            if axionax_deps:
                result['details']['axionax_dependencies'] = axionax_deps
            
            # Check if node_modules exists
            node_modules = repo_path / 'node_modules'
            if not node_modules.exists() and (deps or dev_deps):
                result['status'] = 'WARN'
                result['issues'].append("Dependencies defined but node_modules not found. Run 'npm install'")
            
        except json.JSONDecodeError as e:
            result['status'] = 'FAIL'
            result['issues'].append(f"Invalid JSON: {str(e)}")
        except Exception as e:
            result['status'] = 'FAIL'
            result['issues'].append(f"Error reading package.json: {str(e)}")
        
        return result
    
    def test_cargo_toml(self, repo_name: str) -> Dict:
        """Test Cargo.toml validity"""
        repo_path = self.base_path / repo_name
        cargo_toml = repo_path / 'Cargo.toml'
        
        result = {
            'test': 'Cargo.toml Validation',
            'repo': repo_name,
            'status': 'PASS',
            'details': {},
            'issues': []
        }
        
        if not cargo_toml.exists():
            result['status'] = 'SKIP'
            result['issues'].append("No Cargo.toml found")
            return result
        
        try:
            with open(cargo_toml, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic validation - check for [workspace] or [package]
            is_workspace = '[workspace]' in content
            is_package = '[package]' in content
            
            if not is_workspace and not is_package:
                result['status'] = 'FAIL'
                result['issues'].append("Missing [package] or [workspace] section")
            elif is_workspace:
                result['details']['is_workspace'] = True
                # Workspace is valid, not a failure
            
            # Check for dependencies
            if '[dependencies]' in content:
                result['details']['has_dependencies'] = True
                
                # Count axionax-related dependencies
                axionax_deps = []
                lines = content.split('\n')
                in_deps = False
                for line in lines:
                    if line.strip().startswith('[dependencies'):
                        in_deps = True
                        continue
                    if line.strip().startswith('['):
                        in_deps = False
                    if in_deps and 'axionax' in line.lower():
                        axionax_deps.append(line.strip())
                
                if axionax_deps:
                    result['details']['axionax_dependencies'] = axionax_deps
            
            # Check if target directory exists (indicates previous build)
            target_dir = repo_path / 'target'
            result['details']['has_target_dir'] = target_dir.exists()
            
        except Exception as e:
            result['status'] = 'FAIL'
            result['issues'].append(f"Error reading Cargo.toml: {str(e)}")
        
        return result
    
    def test_dependency_links(self, repo_name: str) -> Dict:
        """Test if dependencies between repos are properly linked"""
        repo_path = self.base_path / repo_name
        dependencies = self.repos[repo_name]['dependencies']
        
        result = {
            'test': 'Dependency Links',
            'repo': repo_name,
            'status': 'PASS',
            'details': {'dependencies': dependencies},
            'issues': []
        }
        
        if not dependencies:
            result['status'] = 'SKIP'
            result['issues'].append("No dependencies defined")
            return result
        
        broken_links = []
        for dep in dependencies:
            dep_path = self.base_path / dep
            if not dep_path.exists():
                broken_links.append(dep)
        
        if broken_links:
            result['status'] = 'FAIL'
            result['issues'].append(f"Missing dependency repositories: {', '.join(broken_links)}")
        
        result['details']['broken_links'] = broken_links
        result['details']['valid_links'] = [d for d in dependencies if d not in broken_links]
        
        return result
    
    def test_import_statements(self, repo_name: str) -> Dict:
        """Test if import statements can be resolved"""
        repo_path = self.base_path / repo_name
        
        result = {
            'test': 'Import Resolution',
            'repo': repo_name,
            'status': 'PASS',
            'details': {},
            'issues': []
        }
        
        # Scan for import issues
        unresolved_imports = []
        files_scanned = 0
        
        extensions = {
            'rust': ['.rs'],
            'typescript': ['.ts', '.tsx'],
            'nextjs': ['.ts', '.tsx', '.js', '.jsx'],
            'react': ['.ts', '.tsx', '.js', '.jsx']
        }
        
        repo_type = self.repos[repo_name]['type']
        scan_extensions = extensions.get(repo_type, [])
        
        if not scan_extensions:
            result['status'] = 'SKIP'
            result['issues'].append(f"No import scanning for type: {repo_type}")
            return result
        
        try:
            for ext in scan_extensions:
                for file_path in repo_path.rglob(f'*{ext}'):
                    # Skip build directories
                    if any(skip in str(file_path) for skip in ['node_modules', 'target', 'dist', '.next', 'build']):
                        continue
                    
                    files_scanned += 1
                    if files_scanned > 100:  # Limit scanning
                        break
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                        
                        # Look for axionax imports that might be broken
                        lines = content.split('\n')
                        for i, line in enumerate(lines, 1):
                            if 'import' in line or 'require' in line or 'from' in line:
                                if 'axionax' in line.lower():
                                    # Check if it's a relative import that might be broken
                                    if ('../' in line or './' in line) and 'axionax' in line:
                                        unresolved_imports.append({
                                            'file': str(file_path.relative_to(repo_path)),
                                            'line': i,
                                            'import': line.strip()[:80]
                                        })
                    except:
                        continue
            
            result['details']['files_scanned'] = files_scanned
            result['details']['potential_issues'] = len(unresolved_imports)
            
            if unresolved_imports:
                result['status'] = 'WARN'
                result['issues'].append(f"Found {len(unresolved_imports)} potential import issues")
                result['details']['sample_issues'] = unresolved_imports[:5]
            
        except Exception as e:
            result['status'] = 'FAIL'
            result['issues'].append(f"Error scanning imports: {str(e)}")
        
        return result
    
    def test_build_system(self, repo_name: str) -> Dict:
        """Test if build system is properly configured"""
        repo_path = self.base_path / repo_name
        test_command = self.repos[repo_name]['test_command']
        
        result = {
            'test': 'Build System',
            'repo': repo_name,
            'status': 'PASS',
            'details': {},
            'issues': []
        }
        
        if not test_command:
            result['status'] = 'SKIP'
            result['issues'].append("No build command defined for this repo type")
            return result
        
        if not repo_path.exists():
            result['status'] = 'SKIP'
            result['issues'].append("Repository not found")
            return result
        
        try:
            os.chdir(repo_path)
            
            # Check for lock files
            if 'npm' in test_command:
                lock_file = repo_path / 'package-lock.json'
                if not lock_file.exists():
                    result['status'] = 'WARN'
                    result['issues'].append("package-lock.json not found. Run 'npm install' first")
                result['details']['has_lock_file'] = lock_file.exists()
            
            elif 'cargo' in test_command:
                lock_file = repo_path / 'Cargo.lock'
                result['details']['has_lock_file'] = lock_file.exists()
            
            result['details']['build_command'] = test_command
            result['details']['ready_to_build'] = True
            
            # Don't actually run build (too time-consuming), just check prerequisites
            
        except Exception as e:
            result['status'] = 'FAIL'
            result['issues'].append(f"Build system check error: {str(e)}")
        
        return result
    
    def run_all_tests(self) -> Dict:
        """Run all tests for all repositories"""
        print("🧪 Starting Repository Integration Tests")
        print("=" * 80)
        
        all_results = {}
        
        for repo_name in self.repos.keys():
            print(f"\n📦 Testing {repo_name}...")
            repo_results = []
            
            # Run all tests for this repo
            tests = [
                self.test_repo_exists,
                self.test_git_status,
                self.test_package_json,
                self.test_cargo_toml,
                self.test_dependency_links,
                self.test_import_statements,
                self.test_build_system
            ]
            
            for test_func in tests:
                try:
                    result = test_func(repo_name)
                    repo_results.append(result)
                    
                    # Print test result
                    status_symbol = {
                        'PASS': '✅',
                        'WARN': '⚠️',
                        'FAIL': '❌',
                        'SKIP': '⏭️'
                    }.get(result['status'], '❓')
                    
                    print(f"  {status_symbol} {result['test']}: {result['status']}")
                    
                    if result['issues']:
                        for issue in result['issues']:
                            print(f"     → {issue}")
                    
                except Exception as e:
                    print(f"  ❌ {test_func.__name__}: ERROR - {str(e)}")
            
            all_results[repo_name] = repo_results
        
        return all_results
    
    def generate_summary(self, all_results: Dict) -> Dict:
        """Generate test summary statistics"""
        summary = {
            'total_repos': len(all_results),
            'total_tests': 0,
            'passed': 0,
            'warnings': 0,
            'failed': 0,
            'skipped': 0,
            'critical_issues': [],
            'warnings_list': [],
            'by_repo': {}
        }
        
        for repo_name, results in all_results.items():
            repo_summary = {
                'total': len(results),
                'passed': 0,
                'warnings': 0,
                'failed': 0,
                'skipped': 0,
                'health_score': 0
            }
            
            for result in results:
                summary['total_tests'] += 1
                
                if result['status'] == 'PASS':
                    summary['passed'] += 1
                    repo_summary['passed'] += 1
                elif result['status'] == 'WARN':
                    summary['warnings'] += 1
                    repo_summary['warnings'] += 1
                    summary['warnings_list'].extend([
                        f"{repo_name}: {issue}" for issue in result['issues']
                    ])
                elif result['status'] == 'FAIL':
                    summary['failed'] += 1
                    repo_summary['failed'] += 1
                    summary['critical_issues'].extend([
                        f"{repo_name}: {issue}" for issue in result['issues']
                    ])
                elif result['status'] == 'SKIP':
                    summary['skipped'] += 1
                    repo_summary['skipped'] += 1
            
            # Calculate health score (0-100)
            if repo_summary['total'] > 0:
                health_score = (
                    (repo_summary['passed'] * 100 + 
                     repo_summary['warnings'] * 50 - 
                     repo_summary['failed'] * 100) / 
                    (repo_summary['total'] * 100)
                ) * 100
                repo_summary['health_score'] = max(0, min(100, health_score))
            
            summary['by_repo'][repo_name] = repo_summary
        
        return summary
    
    def generate_recommendations(self, all_results: Dict, summary: Dict) -> List[Dict]:
        """Generate fix recommendations based on test results"""
        recommendations = []
        
        # Critical issues first
        if summary['critical_issues']:
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Critical Issues',
                'issues': summary['critical_issues'],
                'actions': [
                    "Fix repository structure issues immediately",
                    "Ensure all required files exist",
                    "Verify git repository configuration"
                ]
            })
        
        # Dependency issues
        dependency_issues = []
        for repo_name, results in all_results.items():
            for result in results:
                if result['test'] == 'Dependency Links' and result['status'] == 'FAIL':
                    dependency_issues.append(f"{repo_name}: {', '.join(result['issues'])}")
        
        if dependency_issues:
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Dependency Links',
                'issues': dependency_issues,
                'actions': [
                    "Verify all dependent repositories are cloned",
                    "Check dependency paths in package.json/Cargo.toml",
                    "Consider using workspace configuration for monorepo setup"
                ]
            })
        
        # Build system issues
        build_issues = []
        for repo_name, results in all_results.items():
            for result in results:
                if result['test'] == 'Build System' and result['status'] in ['WARN', 'FAIL']:
                    build_issues.append(f"{repo_name}: {', '.join(result['issues'])}")
        
        if build_issues:
            recommendations.append({
                'priority': 'MEDIUM',
                'category': 'Build System',
                'issues': build_issues,
                'actions': [
                    "Run 'npm install' in TypeScript/Node.js projects",
                    "Run 'cargo build' in Rust projects",
                    "Ensure all build dependencies are installed"
                ]
            })
        
        # Import issues
        import_issues = []
        for repo_name, results in all_results.items():
            for result in results:
                if result['test'] == 'Import Resolution' and result['status'] == 'WARN':
                    import_issues.append(f"{repo_name}: {result['details'].get('potential_issues', 0)} potential issues")
        
        if import_issues:
            recommendations.append({
                'priority': 'MEDIUM',
                'category': 'Import Statements',
                'issues': import_issues,
                'actions': [
                    "Review import paths for consistency",
                    "Update import statements after package restructuring",
                    "Consider using path aliases in tsconfig.json"
                ]
            })
        
        # Git status warnings
        git_warnings = []
        for repo_name, results in all_results.items():
            for result in results:
                if result['test'] == 'Git Status' and result['status'] == 'WARN':
                    git_warnings.append(f"{repo_name}: Uncommitted changes")
        
        if git_warnings:
            recommendations.append({
                'priority': 'LOW',
                'category': 'Git Status',
                'issues': git_warnings,
                'actions': [
                    "Commit or stash uncommitted changes",
                    "Ensure working directory is clean before major operations",
                    "Review changes before committing"
                ]
            })
        
        return recommendations
    
    def generate_report(self, all_results: Dict, summary: Dict, recommendations: List[Dict]) -> str:
        """Generate comprehensive text report"""
        lines = []
        lines.append("=" * 80)
        lines.append("AXIONAX REPOSITORY INTEGRATION TEST REPORT")
        lines.append("=" * 80)
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        
        # Executive Summary
        lines.append("📊 EXECUTIVE SUMMARY")
        lines.append("-" * 80)
        lines.append(f"Total Repositories Tested: {summary['total_repos']}")
        lines.append(f"Total Tests Executed: {summary['total_tests']}")
        lines.append(f"✅ Passed: {summary['passed']} ({summary['passed']/summary['total_tests']*100:.1f}%)")
        lines.append(f"⚠️  Warnings: {summary['warnings']} ({summary['warnings']/summary['total_tests']*100:.1f}%)")
        lines.append(f"❌ Failed: {summary['failed']} ({summary['failed']/summary['total_tests']*100:.1f}%)")
        lines.append(f"⏭️  Skipped: {summary['skipped']} ({summary['skipped']/summary['total_tests']*100:.1f}%)")
        lines.append("")
        
        # Repository Health Scores
        lines.append("🏥 REPOSITORY HEALTH SCORES")
        lines.append("-" * 80)
        for repo_name, repo_summary in summary['by_repo'].items():
            health_score = repo_summary['health_score']
            health_symbol = '🟢' if health_score >= 80 else '🟡' if health_score >= 60 else '🔴'
            lines.append(f"{health_symbol} {repo_name}: {health_score:.1f}/100")
            lines.append(f"   Passed: {repo_summary['passed']}, Warnings: {repo_summary['warnings']}, Failed: {repo_summary['failed']}, Skipped: {repo_summary['skipped']}")
        lines.append("")
        
        # Detailed Test Results
        lines.append("🧪 DETAILED TEST RESULTS")
        lines.append("-" * 80)
        for repo_name, results in all_results.items():
            lines.append(f"\n### {repo_name.upper()}")
            lines.append("-" * 40)
            
            for result in results:
                status_symbol = {
                    'PASS': '✅',
                    'WARN': '⚠️',
                    'FAIL': '❌',
                    'SKIP': '⏭️'
                }.get(result['status'], '❓')
                
                lines.append(f"\n{status_symbol} {result['test']}: {result['status']}")
                
                if result['details']:
                    lines.append("   Details:")
                    for key, value in result['details'].items():
                        if isinstance(value, list) and len(value) > 3:
                            lines.append(f"     {key}: {len(value)} items")
                        else:
                            lines.append(f"     {key}: {value}")
                
                if result['issues']:
                    lines.append("   Issues:")
                    for issue in result['issues']:
                        lines.append(f"     • {issue}")
        
        lines.append("")
        
        # Recommendations
        lines.append("\n💡 RECOMMENDATIONS & FIX ACTIONS")
        lines.append("=" * 80)
        
        if not recommendations:
            lines.append("✅ No critical issues found! All systems appear healthy.")
        else:
            for i, rec in enumerate(recommendations, 1):
                priority_symbol = {
                    'HIGH': '🔴',
                    'MEDIUM': '🟡',
                    'LOW': '🟢'
                }.get(rec['priority'], '❓')
                
                lines.append(f"\n{i}. {priority_symbol} {rec['category']} (Priority: {rec['priority']})")
                lines.append("-" * 40)
                
                if rec['issues']:
                    lines.append("Issues Found:")
                    for issue in rec['issues'][:5]:  # Limit to 5
                        lines.append(f"  • {issue}")
                    if len(rec['issues']) > 5:
                        lines.append(f"  ... and {len(rec['issues']) - 5} more")
                
                lines.append("\nRecommended Actions:")
                for action in rec['actions']:
                    lines.append(f"  ✓ {action}")
        
        lines.append("")
        lines.append("=" * 80)
        lines.append("END OF REPORT")
        lines.append("=" * 80)
        
        return "\n".join(lines)
    
    def generate_fix_script(self, recommendations: List[Dict]) -> str:
        """Generate automated fix script"""
        script_lines = []
        script_lines.append("#!/bin/bash")
        script_lines.append("# Automated Fix Script for axionax Repositories")
        script_lines.append("# Generated: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        script_lines.append("")
        script_lines.append("set -e  # Exit on error")
        script_lines.append("")
        script_lines.append("echo '🔧 Starting automated fixes...'")
        script_lines.append("echo ''")
        script_lines.append("")
        
        for i, rec in enumerate(recommendations, 1):
            script_lines.append(f"# {i}. {rec['category']} ({rec['priority']} Priority)")
            script_lines.append(f"echo '📝 Fixing: {rec['category']}'")
            
            if 'Build System' in rec['category']:
                script_lines.append("")
                script_lines.append("# Install dependencies for Node.js projects")
                script_lines.append("for repo in axionax-web axionax-sdk-ts axionax-marketplace; do")
                script_lines.append("  if [ -d \"$repo\" ] && [ -f \"$repo/package.json\" ]; then")
                script_lines.append("    echo \"  Installing dependencies for $repo...\"")
                script_lines.append("    cd $repo")
                script_lines.append("    npm install")
                script_lines.append("    cd ..")
                script_lines.append("  fi")
                script_lines.append("done")
                script_lines.append("")
            
            if 'Git Status' in rec['category']:
                script_lines.append("")
                script_lines.append("# Check git status")
                script_lines.append("for repo in axionax-*; do")
                script_lines.append("  if [ -d \"$repo/.git\" ]; then")
                script_lines.append("    echo \"  Checking $repo...\"")
                script_lines.append("    cd $repo")
                script_lines.append("    git status --short")
                script_lines.append("    cd ..")
                script_lines.append("  fi")
                script_lines.append("done")
                script_lines.append("")
            
            script_lines.append("")
        
        script_lines.append("echo ''")
        script_lines.append("echo '✅ Automated fixes completed!'")
        script_lines.append("echo 'Please review changes and run tests again.'")
        
        return "\n".join(script_lines)

def main():
    print("🚀 axionax Repository Integration Tester")
    print("=" * 80)
    
    base_path = os.getcwd()
    print(f"📁 Base Path: {base_path}\n")
    
    tester = RepoIntegrationTester(base_path)
    
    # Run all tests
    all_results = tester.run_all_tests()
    
    # Generate summary
    print("\n" + "=" * 80)
    print("📊 Generating Summary...")
    summary = tester.generate_summary(all_results)
    
    # Generate recommendations
    print("💡 Generating Recommendations...")
    recommendations = tester.generate_recommendations(all_results, summary)
    
    # Generate report
    print("📝 Generating Report...")
    report = tester.generate_report(all_results, summary, recommendations)
    
    # Save report
    report_file = Path(base_path) / "INTEGRATION_TEST_REPORT.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"✅ Report saved to: {report_file}")
    
    # Save detailed results as JSON
    results_file = Path(base_path) / "integration_test_results.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'summary': summary,
            'results': all_results,
            'recommendations': recommendations
        }, f, indent=2, default=str)
    print(f"✅ Detailed results saved to: {results_file}")
    
    # Generate fix script
    if recommendations:
        fix_script = tester.generate_fix_script(recommendations)
        fix_script_file = Path(base_path) / "auto_fix.sh"
        with open(fix_script_file, 'w', encoding='utf-8') as f:
            f.write(fix_script)
        print(f"✅ Fix script saved to: {fix_script_file}")
        print("   Run: bash auto_fix.sh (on Linux/Mac) or review manually")
    
    # Print summary
    print("\n" + "=" * 80)
    print("📊 FINAL SUMMARY")
    print("=" * 80)
    print(f"Total Tests: {summary['total_tests']}")
    print(f"✅ Passed: {summary['passed']} ({summary['passed']/summary['total_tests']*100:.1f}%)")
    print(f"⚠️  Warnings: {summary['warnings']} ({summary['warnings']/summary['total_tests']*100:.1f}%)")
    print(f"❌ Failed: {summary['failed']} ({summary['failed']/summary['total_tests']*100:.1f}%)")
    
    if summary['failed'] > 0:
        print("\n🔴 Critical issues detected! Review INTEGRATION_TEST_REPORT.txt for details.")
    elif summary['warnings'] > 0:
        print("\n🟡 Some warnings found. Review INTEGRATION_TEST_REPORT.txt for recommendations.")
    else:
        print("\n🟢 All tests passed! Repositories are healthy.")
    
    print("\n✅ Integration testing complete!")

if __name__ == "__main__":
    main()
