#!/usr/bin/env python3
"""
Repository Quality Analyzer
ตรวจสอบและให้คะแนนคุณภาพของ repository ตาม 4 เกณฑ์:
1. ความยาก-ง่าย (Ease of Use)
2. ประสิทธิภาพ (Performance)
3. ระเบียบ (Organization)
4. ความเข้ากันได้ (Compatibility)
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict

# ANSI Colors
BOLD = '\033[1m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RED = '\033[91m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
RESET = '\033[0m'


@dataclass
class QualityScore:
    """คะแนนคุณภาพของแต่ละด้าน"""
    ease_of_use: float = 0.0
    performance: float = 0.0
    organization: float = 0.0
    compatibility: float = 0.0
    total: float = 0.0
    grade: str = "F"
    
    def calculate_total(self):
        """คำนวณคะแนนรวม (ถ่วงน้ำหนักเท่ากัน)"""
        self.total = (
            self.ease_of_use * 0.25 +
            self.performance * 0.25 +
            self.organization * 0.25 +
            self.compatibility * 0.25
        )
        self.grade = self._calculate_grade()
    
    def _calculate_grade(self) -> str:
        """คำนวณเกรด"""
        if self.total >= 90:
            return "A+"
        elif self.total >= 85:
            return "A"
        elif self.total >= 80:
            return "B+"
        elif self.total >= 75:
            return "B"
        elif self.total >= 70:
            return "C+"
        elif self.total >= 65:
            return "C"
        elif self.total >= 60:
            return "D"
        else:
            return "F"


class RepositoryQualityAnalyzer:
    """วิเคราะห์คุณภาพของ repository"""
    
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.repo_name = repo_path.name
        self.metrics = {}
        self.issues = []
        self.recommendations = []
    
    # ============================================
    # 1. ความยาก-ง่าย (Ease of Use)
    # ============================================
    
    def analyze_ease_of_use(self) -> float:
        """วิเคราะห์ความยาก-ง่ายในการใช้งาน (100 คะแนน)"""
        score = 0.0
        max_score = 100.0
        
        print(f"  {CYAN}📖 Analyzing Ease of Use...{RESET}")
        
        # 1. README.md quality (25 points)
        readme_score = self._check_readme_quality()
        score += readme_score
        print(f"    README Quality: {readme_score:.1f}/25")
        
        # 2. Documentation coverage (25 points)
        doc_score = self._check_documentation_coverage()
        score += doc_score
        print(f"    Documentation: {doc_score:.1f}/25")
        
        # 3. Quick start guide (15 points)
        quickstart_score = self._check_quickstart_guide()
        score += quickstart_score
        print(f"    Quick Start: {quickstart_score:.1f}/15")
        
        # 4. Examples and tutorials (15 points)
        examples_score = self._check_examples()
        score += examples_score
        print(f"    Examples: {examples_score:.1f}/15")
        
        # 5. Installation simplicity (10 points)
        install_score = self._check_installation_scripts()
        score += install_score
        print(f"    Installation: {install_score:.1f}/10")
        
        # 6. Configuration templates (10 points)
        config_score = self._check_config_templates()
        score += config_score
        print(f"    Config Templates: {config_score:.1f}/10")
        
        return score
    
    def _check_readme_quality(self) -> float:
        """ตรวจสอบคุณภาพ README (25 คะแนน)"""
        readme = self.repo_path / "README.md"
        if not readme.exists():
            self.issues.append("Missing README.md")
            return 0.0
        
        try:
            content = readme.read_text(encoding='utf-8')
            score = 0.0
            
            # Title (3 points)
            if content.startswith('#'):
                score += 3
            
            # Description (5 points)
            if len(content) > 500:
                score += 5
            elif len(content) > 200:
                score += 3
            
            # Installation section (5 points)
            if 'install' in content.lower():
                score += 5
            
            # Usage section (5 points)
            if 'usage' in content.lower() or 'getting started' in content.lower():
                score += 5
            
            # Examples (4 points)
            if 'example' in content.lower():
                score += 4
            
            # Links to docs (3 points)
            if 'docs' in content.lower() or 'documentation' in content.lower():
                score += 3
            
            return min(score, 25.0)
        except:
            return 0.0
    
    def _check_documentation_coverage(self) -> float:
        """ตรวจสอบความครอบคลุมของเอกสาร (25 คะแนน)"""
        score = 0.0
        
        # Check for docs directory (10 points)
        docs_dir = self.repo_path / "docs"
        if docs_dir.exists() and docs_dir.is_dir():
            doc_files = list(docs_dir.rglob("*.md"))
            if len(doc_files) >= 10:
                score += 10
            elif len(doc_files) >= 5:
                score += 7
            elif len(doc_files) >= 3:
                score += 5
            elif len(doc_files) >= 1:
                score += 3
        
        # Check for API reference (8 points)
        api_docs = [
            self.repo_path / "docs" / "API_REFERENCE.md",
            self.repo_path / "API.md",
            self.repo_path / "docs" / "api.md"
        ]
        if any(doc.exists() for doc in api_docs):
            score += 8
        
        # Check for architecture docs (7 points)
        arch_docs = [
            self.repo_path / "docs" / "ARCHITECTURE.md",
            self.repo_path / "ARCHITECTURE.md"
        ]
        if any(doc.exists() for doc in arch_docs):
            score += 7
        
        return min(score, 25.0)
    
    def _check_quickstart_guide(self) -> float:
        """ตรวจสอบ Quick Start Guide (15 คะแนน)"""
        quickstart_files = [
            self.repo_path / "QUICKSTART.md",
            self.repo_path / "QUICK_START.md",
            self.repo_path / "docs" / "QUICKSTART.md",
            self.repo_path / "docs" / "GETTING_STARTED.md"
        ]
        
        for qsfile in quickstart_files:
            if qsfile.exists():
                try:
                    content = qsfile.read_text(encoding='utf-8')
                    score = 5.0  # Base score for existing
                    
                    # Check for step-by-step instructions (5 points)
                    if any(marker in content.lower() for marker in ['step 1', '1.', '## step']):
                        score += 5
                    
                    # Check for code examples (5 points)
                    if '```' in content:
                        score += 5
                    
                    return min(score, 15.0)
                except:
                    return 5.0
        
        return 0.0
    
    def _check_examples(self) -> float:
        """ตรวจสอบ Examples และ Tutorials (15 คะแนน)"""
        score = 0.0
        
        # Check for examples directory (8 points)
        examples_dir = self.repo_path / "examples"
        if examples_dir.exists() and examples_dir.is_dir():
            example_files = list(examples_dir.rglob("*"))
            example_files = [f for f in example_files if f.is_file()]
            
            if len(example_files) >= 5:
                score += 8
            elif len(example_files) >= 3:
                score += 6
            elif len(example_files) >= 1:
                score += 4
        
        # Check for tests directory (7 points)
        tests_dir = self.repo_path / "tests"
        if tests_dir.exists() and tests_dir.is_dir():
            test_files = list(tests_dir.rglob("test_*.py")) + list(tests_dir.rglob("*_test.rs"))
            
            if len(test_files) >= 10:
                score += 7
            elif len(test_files) >= 5:
                score += 5
            elif len(test_files) >= 1:
                score += 3
        
        return min(score, 15.0)
    
    def _check_installation_scripts(self) -> float:
        """ตรวจสอบ Installation Scripts (10 คะแนน)"""
        score = 0.0
        
        install_files = [
            "install.sh",
            "setup.sh",
            "install.py",
            "Makefile"
        ]
        
        for ifile in install_files:
            if (self.repo_path / ifile).exists():
                score += 5
                break
        
        # Check for package manager files (5 points)
        pkg_files = ["package.json", "Cargo.toml", "pyproject.toml", "setup.py"]
        for pfile in pkg_files:
            if (self.repo_path / pfile).exists():
                score += 5
                break
        
        return min(score, 10.0)
    
    def _check_config_templates(self) -> float:
        """ตรวจสอบ Configuration Templates (10 คะแนน)"""
        score = 0.0
        
        config_files = [
            "config.example.yaml",
            "config.example.toml",
            "config.example.json",
            ".env.example",
            "environments"
        ]
        
        for cfile in config_files:
            path = self.repo_path / cfile
            if path.exists():
                score += 5
        
        return min(score, 10.0)
    
    # ============================================
    # 2. ประสิทธิภาพ (Performance)
    # ============================================
    
    def analyze_performance(self) -> float:
        """วิเคราะห์ประสิทธิภาพ (100 คะแนน)"""
        score = 0.0
        
        print(f"  {MAGENTA}⚡ Analyzing Performance...{RESET}")
        
        # 1. Code optimization indicators (25 points)
        opt_score = self._check_optimization_indicators()
        score += opt_score
        print(f"    Code Optimization: {opt_score:.1f}/25")
        
        # 2. Dependency management (20 points)
        dep_score = self._check_dependency_efficiency()
        score += dep_score
        print(f"    Dependencies: {dep_score:.1f}/20")
        
        # 3. Build configuration (20 points)
        build_score = self._check_build_config()
        score += build_score
        print(f"    Build Config: {build_score:.1f}/20")
        
        # 4. Performance tests (15 points)
        perf_test_score = self._check_performance_tests()
        score += perf_test_score
        print(f"    Perf Tests: {perf_test_score:.1f}/15")
        
        # 5. Benchmarking (10 points)
        bench_score = self._check_benchmarks()
        score += bench_score
        print(f"    Benchmarks: {bench_score:.1f}/10")
        
        # 6. Caching strategies (10 points)
        cache_score = self._check_caching()
        score += cache_score
        print(f"    Caching: {cache_score:.1f}/10")
        
        return score
    
    def _check_optimization_indicators(self) -> float:
        """ตรวจสอบ indicators ของการ optimize code (25 คะแนน)"""
        score = 0.0
        
        # Rust: Release profile optimization (10 points)
        cargo_toml = self.repo_path / "Cargo.toml"
        if cargo_toml.exists():
            try:
                content = cargo_toml.read_text(encoding='utf-8')
                if '[profile.release]' in content:
                    score += 5
                    if 'lto = true' in content or 'lto = "fat"' in content:
                        score += 3
                    if 'codegen-units = 1' in content:
                        score += 2
            except:
                pass
        
        # TypeScript: Production build config (8 points)
        tsconfig = self.repo_path / "tsconfig.json"
        if tsconfig.exists():
            try:
                with open(tsconfig, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    compiler_opts = config.get('compilerOptions', {})
                    
                    if compiler_opts.get('target') in ['ES2020', 'ES2021', 'ESNext']:
                        score += 4
                    if compiler_opts.get('module') in ['ES2020', 'ESNext']:
                        score += 2
                    if compiler_opts.get('strict') == True:
                        score += 2
            except:
                pass
        
        # Check for async/await usage (7 points)
        src_files = list(self.repo_path.rglob("*.rs")) + list(self.repo_path.rglob("*.ts"))
        async_count = 0
        for src_file in src_files[:10]:  # Sample first 10 files
            try:
                content = src_file.read_text(encoding='utf-8', errors='ignore')
                if 'async' in content and 'await' in content:
                    async_count += 1
            except:
                pass
        
        if async_count >= 5:
            score += 7
        elif async_count >= 3:
            score += 5
        elif async_count >= 1:
            score += 3
        
        return min(score, 25.0)
    
    def _check_dependency_efficiency(self) -> float:
        """ตรวจสอบประสิทธิภาพของ dependencies (20 คะแนน)"""
        score = 0.0
        
        # Check package.json (10 points)
        package_json = self.repo_path / "package.json"
        if package_json.exists():
            try:
                with open(package_json, 'r', encoding='utf-8') as f:
                    pkg = json.load(f)
                    
                    deps = pkg.get('dependencies', {})
                    dev_deps = pkg.get('devDependencies', {})
                    
                    # Reasonable number of dependencies (6 points)
                    total_deps = len(deps) + len(dev_deps)
                    if total_deps < 20:
                        score += 6
                    elif total_deps < 40:
                        score += 4
                    elif total_deps < 60:
                        score += 2
                    
                    # No wildcards in versions (4 points)
                    has_wildcards = any('*' in v for v in list(deps.values()) + list(dev_deps.values()))
                    if not has_wildcards:
                        score += 4
            except:
                pass
        
        # Check Cargo.toml (10 points)
        cargo_toml = self.repo_path / "Cargo.toml"
        if cargo_toml.exists():
            try:
                content = cargo_toml.read_text(encoding='utf-8')
                
                # Workspace optimization (5 points)
                if '[workspace]' in content:
                    score += 5
                
                # Feature flags usage (5 points)
                if 'features' in content.lower():
                    score += 5
            except:
                pass
        
        return min(score, 20.0)
    
    def _check_build_config(self) -> float:
        """ตรวจสอบ Build Configuration (20 คะแนน)"""
        score = 0.0
        
        # Makefile (8 points)
        if (self.repo_path / "Makefile").exists():
            score += 8
        
        # CI/CD configuration (7 points)
        ci_files = [
            ".github/workflows",
            ".gitlab-ci.yml",
            "azure-pipelines.yml"
        ]
        for ci_file in ci_files:
            if (self.repo_path / ci_file).exists():
                score += 7
                break
        
        # Docker optimization (5 points)
        dockerfile = self.repo_path / "Dockerfile"
        if dockerfile.exists():
            try:
                content = dockerfile.read_text(encoding='utf-8')
                if 'multi-stage' in content.lower() or 'AS builder' in content:
                    score += 5
                elif 'FROM' in content:
                    score += 3
            except:
                pass
        
        return min(score, 20.0)
    
    def _check_performance_tests(self) -> float:
        """ตรวจสอบ Performance Tests (15 คะแนน)"""
        score = 0.0
        
        # Check for benchmark files
        bench_files = list(self.repo_path.rglob("*bench*.rs")) + \
                     list(self.repo_path.rglob("*benchmark*.py")) + \
                     list(self.repo_path.rglob("*perf*.js"))
        
        if len(bench_files) >= 5:
            score += 15
        elif len(bench_files) >= 3:
            score += 10
        elif len(bench_files) >= 1:
            score += 7
        
        return score
    
    def _check_benchmarks(self) -> float:
        """ตรวจสอบ Benchmarking Tools (10 คะแนน)"""
        score = 0.0
        
        # Rust: Criterion (5 points)
        cargo_toml = self.repo_path / "Cargo.toml"
        if cargo_toml.exists():
            try:
                content = cargo_toml.read_text(encoding='utf-8')
                if 'criterion' in content.lower():
                    score += 5
            except:
                pass
        
        # JS: benchmark.js or similar (5 points)
        package_json = self.repo_path / "package.json"
        if package_json.exists():
            try:
                with open(package_json, 'r', encoding='utf-8') as f:
                    pkg = json.load(f)
                    all_deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}
                    
                    if any('benchmark' in dep.lower() for dep in all_deps.keys()):
                        score += 5
            except:
                pass
        
        return min(score, 10.0)
    
    def _check_caching(self) -> float:
        """ตรวจสอบ Caching Strategies (10 คะแนน)"""
        score = 0.0
        
        # Check for cache-related files
        cache_indicators = ['redis', 'memcache', 'cache', 'memoize']
        
        all_files = list(self.repo_path.rglob("*.rs")) + \
                   list(self.repo_path.rglob("*.ts")) + \
                   list(self.repo_path.rglob("*.py"))
        
        for src_file in all_files[:20]:  # Sample
            try:
                content = src_file.read_text(encoding='utf-8', errors='ignore').lower()
                if any(indicator in content for indicator in cache_indicators):
                    score += 5
                    break
            except:
                pass
        
        # Docker layer caching (5 points)
        dockerfile = self.repo_path / "Dockerfile"
        if dockerfile.exists():
            try:
                content = dockerfile.read_text(encoding='utf-8')
                # Good layer ordering
                if 'COPY package' in content and content.index('COPY package') < content.index('COPY .'):
                    score += 5
            except:
                pass
        
        return min(score, 10.0)
    
    # ============================================
    # 3. ระเบียบ (Organization)
    # ============================================
    
    def analyze_organization(self) -> float:
        """วิเคราะห์ความเป็นระเบียบ (100 คะแนน)"""
        score = 0.0
        
        print(f"  {YELLOW}📁 Analyzing Organization...{RESET}")
        
        # 1. Directory structure (25 points)
        struct_score = self._check_directory_structure()
        score += struct_score
        print(f"    Directory Structure: {struct_score:.1f}/25")
        
        # 2. File naming conventions (20 points)
        naming_score = self._check_naming_conventions()
        score += naming_score
        print(f"    Naming Conventions: {naming_score:.1f}/20")
        
        # 3. Code organization (20 points)
        code_org_score = self._check_code_organization()
        score += code_org_score
        print(f"    Code Organization: {code_org_score:.1f}/20")
        
        # 4. Version control (15 points)
        vcs_score = self._check_version_control()
        score += vcs_score
        print(f"    Version Control: {vcs_score:.1f}/15")
        
        # 5. Licensing and legal (10 points)
        legal_score = self._check_licensing()
        score += legal_score
        print(f"    Licensing: {legal_score:.1f}/10")
        
        # 6. Project metadata (10 points)
        meta_score = self._check_project_metadata()
        score += meta_score
        print(f"    Project Metadata: {meta_score:.1f}/10")
        
        return score
    
    def _check_directory_structure(self) -> float:
        """ตรวจสอบโครงสร้างไดเรกทอรี (25 คะแนน)"""
        score = 0.0
        
        expected_dirs = {
            'src': 8,
            'tests': 5,
            'docs': 5,
            'examples': 4,
            'core': 3
        }
        
        for dir_name, points in expected_dirs.items():
            dir_path = self.repo_path / dir_name
            if dir_path.exists() and dir_path.is_dir():
                score += points
        
        return min(score, 25.0)
    
    def _check_naming_conventions(self) -> float:
        """ตรวจสอบ Naming Conventions (20 คะแนน)"""
        score = 20.0  # Start with full score, deduct for issues
        
        # Check for inconsistent naming
        files = list(self.repo_path.rglob("*"))
        files = [f for f in files if f.is_file() and not any(skip in str(f) for skip in ['.git', 'node_modules', 'target'])]
        
        inconsistencies = 0
        for file in files[:50]:  # Sample first 50
            name = file.name
            # Check for mixed case (bad)
            if '_' in name and any(c.isupper() for c in name):
                inconsistencies += 1
        
        # Deduct points for inconsistencies
        deduction = min(inconsistencies * 2, 10)
        score -= deduction
        
        return max(score, 0.0)
    
    def _check_code_organization(self) -> float:
        """ตรวจสอบการจัดระเบียบโค้ด (20 คะแนน)"""
        score = 0.0
        
        # Modular structure (10 points)
        src_dir = self.repo_path / "src"
        if src_dir.exists():
            subdirs = [d for d in src_dir.iterdir() if d.is_dir()]
            if len(subdirs) >= 5:
                score += 10
            elif len(subdirs) >= 3:
                score += 7
            elif len(subdirs) >= 1:
                score += 4
        
        # Separation of concerns (10 points)
        concern_dirs = ['models', 'controllers', 'services', 'utils', 'lib', 'core']
        found_concerns = sum(1 for cd in concern_dirs if (self.repo_path / "src" / cd).exists() or (self.repo_path / cd).exists())
        
        if found_concerns >= 4:
            score += 10
        elif found_concerns >= 2:
            score += 7
        elif found_concerns >= 1:
            score += 4
        
        return min(score, 20.0)
    
    def _check_version_control(self) -> float:
        """ตรวจสอบ Version Control (15 คะแนน)"""
        score = 0.0
        
        # .gitignore (5 points)
        if (self.repo_path / ".gitignore").exists():
            score += 5
        
        # .gitattributes (3 points)
        if (self.repo_path / ".gitattributes").exists():
            score += 3
        
        # CHANGELOG (4 points)
        changelog_files = ["CHANGELOG.md", "HISTORY.md", "CHANGES.md"]
        if any((self.repo_path / cf).exists() for cf in changelog_files):
            score += 4
        
        # GitHub templates (3 points)
        if (self.repo_path / ".github").exists():
            score += 3
        
        return min(score, 15.0)
    
    def _check_licensing(self) -> float:
        """ตรวจสอบ Licensing (10 คะแนน)"""
        score = 0.0
        
        # LICENSE file (7 points)
        if (self.repo_path / "LICENSE").exists():
            score += 7
        
        # COPYRIGHT or NOTICE (3 points)
        if (self.repo_path / "COPYRIGHT").exists() or (self.repo_path / "NOTICE").exists():
            score += 3
        
        return min(score, 10.0)
    
    def _check_project_metadata(self) -> float:
        """ตรวจสอบ Project Metadata (10 คะแนน)"""
        score = 0.0
        
        # Package metadata
        pkg_files = {
            "package.json": 4,
            "Cargo.toml": 4,
            "pyproject.toml": 4
        }
        
        for pkg_file, points in pkg_files.items():
            if (self.repo_path / pkg_file).exists():
                score += points
                break  # Count only one
        
        # Version file (3 points)
        version_files = ["VERSION", "version.txt", ".version"]
        if any((self.repo_path / vf).exists() for vf in version_files):
            score += 3
        
        # Contributors file (3 points)
        if (self.repo_path / "CONTRIBUTORS.md").exists() or (self.repo_path / "AUTHORS").exists():
            score += 3
        
        return min(score, 10.0)
    
    # ============================================
    # 4. ความเข้ากันได้ (Compatibility)
    # ============================================
    
    def analyze_compatibility(self) -> float:
        """วิเคราะห์ความเข้ากันได้ (100 คะแนน)"""
        score = 0.0
        
        print(f"  {BLUE}🔗 Analyzing Compatibility...{RESET}")
        
        # 1. Cross-platform support (25 points)
        platform_score = self._check_platform_support()
        score += platform_score
        print(f"    Platform Support: {platform_score:.1f}/25")
        
        # 2. API compatibility (20 points)
        api_score = self._check_api_compatibility()
        score += api_score
        print(f"    API Compatibility: {api_score:.1f}/20")
        
        # 3. Version compatibility (20 points)
        version_score = self._check_version_compatibility()
        score += version_score
        print(f"    Version Compat: {version_score:.1f}/20")
        
        # 4. Standards compliance (15 points)
        standards_score = self._check_standards_compliance()
        score += standards_score
        print(f"    Standards: {standards_score:.1f}/15")
        
        # 5. Interoperability (10 points)
        interop_score = self._check_interoperability()
        score += interop_score
        print(f"    Interoperability: {interop_score:.1f}/10")
        
        # 6. Backwards compatibility (10 points)
        backward_score = self._check_backwards_compatibility()
        score += backward_score
        print(f"    Backwards Compat: {backward_score:.1f}/10")
        
        return score
    
    def _check_platform_support(self) -> float:
        """ตรวจสอบการรองรับหลาย platform (25 คะแนน)"""
        score = 0.0
        
        # Installation scripts for multiple platforms (15 points)
        install_scripts = {
            "install_dependencies_linux.sh": 5,
            "install_dependencies_macos.sh": 5,
            "install_dependencies_windows.ps1": 5
        }
        
        for script, points in install_scripts.items():
            if (self.repo_path / script).exists():
                score += points
        
        # Docker support (5 points)
        if (self.repo_path / "Dockerfile").exists():
            score += 5
        
        # CI for multiple platforms (5 points)
        ci_dir = self.repo_path / ".github" / "workflows"
        if ci_dir.exists():
            ci_files = list(ci_dir.rglob("*.yml"))
            for ci_file in ci_files:
                try:
                    content = ci_file.read_text(encoding='utf-8')
                    platforms = ['ubuntu', 'macos', 'windows']
                    found_platforms = sum(1 for p in platforms if p in content.lower())
                    if found_platforms >= 2:
                        score += 5
                        break
                except:
                    pass
        
        return min(score, 25.0)
    
    def _check_api_compatibility(self) -> float:
        """ตรวจสอบ API Compatibility (20 คะแนน)"""
        score = 0.0
        
        # OpenAPI/Swagger spec (8 points)
        api_specs = ["openapi.yaml", "swagger.yaml", "api.yaml"]
        if any((self.repo_path / spec).exists() for spec in api_specs):
            score += 8
        
        # JSON-RPC compliance (6 points)
        src_files = list(self.repo_path.rglob("*.rs")) + list(self.repo_path.rglob("*.ts"))
        for src_file in src_files[:20]:
            try:
                content = src_file.read_text(encoding='utf-8', errors='ignore')
                if 'json-rpc' in content.lower() or 'jsonrpc' in content.lower():
                    score += 6
                    break
            except:
                pass
        
        # API versioning (6 points)
        for src_file in src_files[:20]:
            try:
                content = src_file.read_text(encoding='utf-8', errors='ignore')
                if any(v in content for v in ['/v1/', '/v2/', 'api/v1', 'api/v2']):
                    score += 6
                    break
            except:
                pass
        
        return min(score, 20.0)
    
    def _check_version_compatibility(self) -> float:
        """ตรวจสอบ Version Compatibility (20 คะแนน)"""
        score = 0.0
        
        # Semantic versioning (8 points)
        package_json = self.repo_path / "package.json"
        cargo_toml = self.repo_path / "Cargo.toml"
        
        if package_json.exists():
            try:
                with open(package_json, 'r', encoding='utf-8') as f:
                    pkg = json.load(f)
                    version = pkg.get('version', '')
                    # Check semver format (x.y.z)
                    if version and version.count('.') == 2:
                        score += 8
            except:
                pass
        elif cargo_toml.exists():
            try:
                content = cargo_toml.read_text(encoding='utf-8')
                if 'version =' in content:
                    score += 8
            except:
                pass
        
        # Engine/runtime version specs (7 points)
        if package_json.exists():
            try:
                with open(package_json, 'r', encoding='utf-8') as f:
                    pkg = json.load(f)
                    if 'engines' in pkg:
                        score += 7
            except:
                pass
        
        # Rust edition specification (5 points)
        if cargo_toml.exists():
            try:
                content = cargo_toml.read_text(encoding='utf-8')
                if 'edition =' in content:
                    score += 5
            except:
                pass
        
        return min(score, 20.0)
    
    def _check_standards_compliance(self) -> float:
        """ตรวจสอบการปฏิบัติตามมาตรฐาน (15 คะแนน)"""
        score = 0.0
        
        # ESLint/Prettier for TS (5 points)
        if (self.repo_path / ".eslintrc.json").exists() or (self.repo_path / ".prettierrc").exists():
            score += 5
        
        # Clippy for Rust (5 points)
        if (self.repo_path / "clippy.toml").exists() or (self.repo_path / ".clippy.toml").exists():
            score += 5
        
        # EditorConfig (5 points)
        if (self.repo_path / ".editorconfig").exists():
            score += 5
        
        return min(score, 15.0)
    
    def _check_interoperability(self) -> float:
        """ตรวจสอบ Interoperability (10 คะแนน)"""
        score = 0.0
        
        # FFI/Bindings (5 points)
        bridge_indicators = ['bridge', 'bindings', 'ffi', 'pyo3']
        for indicator in bridge_indicators:
            if (self.repo_path / indicator).exists():
                score += 5
                break
        
        # Protocol definitions (5 points)
        proto_files = list(self.repo_path.rglob("*.proto")) + \
                     list(self.repo_path.rglob("*.thrift"))
        if len(proto_files) > 0:
            score += 5
        
        return min(score, 10.0)
    
    def _check_backwards_compatibility(self) -> float:
        """ตรวจสอบ Backwards Compatibility (10 คะแนน)"""
        score = 0.0
        
        # Migration guides (5 points)
        migration_files = ["MIGRATION.md", "UPGRADE.md", "BREAKING_CHANGES.md"]
        if any((self.repo_path / mf).exists() for mf in migration_files):
            score += 5
        
        # Deprecation warnings in code (5 points)
        src_files = list(self.repo_path.rglob("*.rs")) + list(self.repo_path.rglob("*.ts"))
        for src_file in src_files[:20]:
            try:
                content = src_file.read_text(encoding='utf-8', errors='ignore')
                if 'deprecated' in content.lower() or '@deprecated' in content:
                    score += 5
                    break
            except:
                pass
        
        return min(score, 10.0)
    
    # ============================================
    # Main Analysis
    # ============================================
    
    def analyze(self) -> QualityScore:
        """วิเคราะห์คุณภาพทั้งหมด"""
        print(f"\n{BOLD}{GREEN}{'='*70}{RESET}")
        print(f"{BOLD}{GREEN}📊 Analyzing: {self.repo_name}{RESET}")
        print(f"{BOLD}{GREEN}{'='*70}{RESET}\n")
        
        score = QualityScore()
        
        # Analyze each dimension
        score.ease_of_use = self.analyze_ease_of_use()
        score.performance = self.analyze_performance()
        score.organization = self.analyze_organization()
        score.compatibility = self.analyze_compatibility()
        
        # Calculate total
        score.calculate_total()
        
        return score
    
    def generate_recommendations(self, score: QualityScore):
        """สร้างคำแนะนำสำหรับการปรับปรุง"""
        recommendations = []
        
        if score.ease_of_use < 70:
            recommendations.append("📖 Improve documentation: Add more examples and tutorials")
            recommendations.append("📝 Create a comprehensive QUICKSTART.md guide")
        
        if score.performance < 70:
            recommendations.append("⚡ Optimize build configuration: Enable LTO and reduce codegen-units")
            recommendations.append("🔬 Add performance benchmarks using Criterion or similar")
        
        if score.organization < 70:
            recommendations.append("📁 Restructure directories: Follow standard project layout")
            recommendations.append("🏷️ Improve naming conventions consistency")
        
        if score.compatibility < 70:
            recommendations.append("🔗 Add cross-platform installation scripts")
            recommendations.append("📋 Document API versioning and compatibility")
        
        return recommendations


def analyze_all_repositories(base_path: Path) -> Dict[str, QualityScore]:
    """วิเคราะห์ทุก repository"""
    repos = [
        'axionax-core',
        'axionax-sdk-ts',
        'axionax-web',
        'axionax-marketplace',
        'axionax-docs',
        'axionax-deploy',
        'axionax-devtools'
    ]
    
    results = {}
    
    for repo_name in repos:
        repo_path = base_path / repo_name
        if repo_path.exists():
            analyzer = RepositoryQualityAnalyzer(repo_path)
            score = analyzer.analyze()
            results[repo_name] = score
            
            # Generate and display recommendations
            recommendations = analyzer.generate_recommendations(score)
            if recommendations:
                print(f"\n{YELLOW}💡 Recommendations:{RESET}")
                for rec in recommendations:
                    print(f"  {rec}")
        else:
            print(f"{RED}❌ Repository not found: {repo_name}{RESET}")
    
    return results


def print_summary_report(results: Dict[str, QualityScore]):
    """พิมพ์รายงานสรุป"""
    print(f"\n{BOLD}{BLUE}{'='*70}{RESET}")
    print(f"{BOLD}{BLUE}📊 QUALITY ANALYSIS SUMMARY{RESET}")
    print(f"{BOLD}{BLUE}{'='*70}{RESET}\n")
    
    # Table header
    print(f"{BOLD}{'Repository':<25} {'Ease':<8} {'Perf':<8} {'Org':<8} {'Compat':<8} {'Total':<8} {'Grade':<6}{RESET}")
    print("-" * 70)
    
    # Sort by total score
    sorted_results = sorted(results.items(), key=lambda x: x[1].total, reverse=True)
    
    for repo_name, score in sorted_results:
        grade_color = GREEN if score.grade.startswith('A') else YELLOW if score.grade.startswith('B') else RED
        print(f"{repo_name:<25} {score.ease_of_use:>6.1f}  {score.performance:>6.1f}  {score.organization:>6.1f}  {score.compatibility:>6.1f}  {score.total:>6.1f}  {grade_color}{score.grade:<6}{RESET}")
    
    # Calculate averages
    avg_ease = sum(s.ease_of_use for s in results.values()) / len(results)
    avg_perf = sum(s.performance for s in results.values()) / len(results)
    avg_org = sum(s.organization for s in results.values()) / len(results)
    avg_compat = sum(s.compatibility for s in results.values()) / len(results)
    avg_total = sum(s.total for s in results.values()) / len(results)
    
    print("-" * 70)
    print(f"{BOLD}{'AVERAGE':<25} {avg_ease:>6.1f}  {avg_perf:>6.1f}  {avg_org:>6.1f}  {avg_compat:>6.1f}  {avg_total:>6.1f}{RESET}")
    
    # Best and worst
    best = max(results.items(), key=lambda x: x[1].total)
    worst = min(results.items(), key=lambda x: x[1].total)
    
    print(f"\n{GREEN}🏆 Best: {best[0]} ({best[1].total:.1f} - {best[1].grade}){RESET}")
    print(f"{YELLOW}⚠️  Needs Improvement: {worst[0]} ({worst[1].total:.1f} - {worst[1].grade}){RESET}")


def save_json_report(results: Dict[str, QualityScore], output_path: Path):
    """บันทึกรายงานเป็น JSON"""
    json_data = {
        repo_name: asdict(score)
        for repo_name, score in results.items()
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2)
    
    print(f"\n{GREEN}✅ JSON report saved: {output_path}{RESET}")


def main():
    print(f"\n{BOLD}{CYAN}{'='*70}{RESET}")
    print(f"{BOLD}{CYAN}🔍 AXIONAX REPOSITORY QUALITY ANALYZER{RESET}")
    print(f"{BOLD}{CYAN}{'='*70}{RESET}")
    
    # Get base path
    base_path = Path.cwd()
    
    print(f"\n{BOLD}Base Path:{RESET} {base_path}")
    print(f"{BOLD}Analyzing repositories...{RESET}\n")
    
    # Analyze all repositories
    results = analyze_all_repositories(base_path)
    
    # Print summary
    print_summary_report(results)
    
    # Save JSON report
    json_path = base_path / "QUALITY_ANALYSIS.json"
    save_json_report(results, json_path)
    
    print(f"\n{BOLD}{GREEN}{'='*70}{RESET}")
    print(f"{BOLD}{GREEN}✅ Analysis Complete!{RESET}")
    print(f"{BOLD}{GREEN}{'='*70}{RESET}\n")


if __name__ == "__main__":
    main()
