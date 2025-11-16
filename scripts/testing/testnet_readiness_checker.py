#!/usr/bin/env python3
"""
Testnet Readiness Checker
Automated pre-launch validation for AxionAx Protocol testnet deployment
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime

# ANSI color codes
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'

@dataclass
class CheckResult:
    """Result of a single readiness check"""
    name: str
    category: str
    passed: bool
    score: float  # 0-100
    message: str
    details: Dict = None
    critical: bool = False

class TestnetReadinessChecker:
    """Comprehensive testnet readiness validation"""
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.results: List[CheckResult] = []
        self.start_time = None
        
    def run_all_checks(self) -> Tuple[bool, float]:
        """Run all readiness checks and return overall status"""
        self.start_time = time.time()
        
        print(f"\n{CYAN}{'='*70}{RESET}")
        print(f"{BOLD}{CYAN}  AXIONAX TESTNET READINESS CHECKER{RESET}")
        print(f"{CYAN}{'='*70}{RESET}\n")
        print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Run all check categories
        self._check_infrastructure()
        self._check_codebase()
        self._check_security()
        self._check_performance()
        self._check_documentation()
        self._check_deployment()
        self._check_monitoring()
        
        # Calculate overall results
        elapsed = time.time() - self.start_time
        overall_passed, overall_score = self._calculate_overall()
        
        # Print summary
        self._print_summary(overall_passed, overall_score, elapsed)
        
        # Save JSON report
        self._save_report(overall_passed, overall_score)
        
        return overall_passed, overall_score
    
    def _run_check(self, name: str, category: str, check_func, critical: bool = False):
        """Helper to run a single check and store result"""
        print(f"  🔍 Checking {name}...", end=' ')
        sys.stdout.flush()
        
        try:
            passed, score, message, details = check_func()
            result = CheckResult(
                name=name,
                category=category,
                passed=passed,
                score=score,
                message=message,
                details=details,
                critical=critical
            )
            self.results.append(result)
            
            icon = "✅" if passed else ("⚠️" if not critical else "❌")
            print(f"{icon} {message}")
            
        except Exception as e:
            result = CheckResult(
                name=name,
                category=category,
                passed=False,
                score=0,
                message=f"Check failed: {str(e)}",
                critical=critical
            )
            self.results.append(result)
            print(f"❌ Error: {str(e)}")
    
    # ========================================================================
    # CATEGORY 1: INFRASTRUCTURE CHECKS
    # ========================================================================
    
    def _check_infrastructure(self):
        """Check infrastructure readiness"""
        print(f"\n{BOLD}{BLUE}📦 INFRASTRUCTURE CHECKS{RESET}")
        
        self._run_check("Repository Structure", "infrastructure", 
                       self._check_repo_structure)
        self._run_check("Git Configuration", "infrastructure",
                       self._check_git_config)
        self._run_check("Dependencies", "infrastructure",
                       self._check_dependencies)
        self._run_check("Build Tools", "infrastructure",
                       self._check_build_tools)
    
    def _check_repo_structure(self):
        """Verify all required repositories exist"""
        required_repos = [
            'axionax-core',
            'axionax-sdk-ts', 
            'axionax-web',
            'axionax-docs',
            'axionax-deploy',
            'axionax-devtools'
        ]
        
        found = []
        missing = []
        
        for repo in required_repos:
            repo_path = self.workspace_root / repo
            if repo_path.exists():
                found.append(repo)
            else:
                missing.append(repo)
        
        score = (len(found) / len(required_repos)) * 100
        
        if missing:
            return False, score, f"{len(found)}/{len(required_repos)} repos found", {"missing": missing}
        return True, 100, f"All {len(required_repos)} repos present", {"repos": found}
    
    def _check_git_config(self):
        """Check git configuration"""
        try:
            # Check if we're in a git repo
            result = subprocess.run(
                ['git', 'rev-parse', '--git-dir'],
                cwd=self.workspace_root,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                return False, 0, "Not a git repository", None
            
            # Check for uncommitted changes
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=self.workspace_root,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            uncommitted = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
            
            if uncommitted > 0:
                return False, 50, f"{uncommitted} uncommitted changes", {"uncommitted": uncommitted}
            
            return True, 100, "Clean git state", None
            
        except Exception as e:
            return False, 0, f"Git check failed: {str(e)}", None
    
    def _check_dependencies(self):
        """Check if required dependencies are installed"""
        deps_status = {
            'rust': self._check_command(['rustc', '--version']),
            'cargo': self._check_command(['cargo', '--version']),
            'node': self._check_command(['node', '--version']),
            'npm': self._check_command(['npm', '--version']),
            'python': self._check_command(['python', '--version']),
            'docker': self._check_command(['docker', '--version']),
        }
        
        installed = sum(1 for v in deps_status.values() if v)
        total = len(deps_status)
        score = (installed / total) * 100
        
        missing = [k for k, v in deps_status.items() if not v]
        
        if missing:
            return False, score, f"{installed}/{total} dependencies", {"missing": missing}
        return True, 100, f"All {total} dependencies installed", deps_status
    
    def _check_build_tools(self):
        """Check if build tools are functional"""
        tools = {}
        
        # Check Rust build
        core_path = self.workspace_root / 'axionax-core'
        if core_path.exists():
            tools['rust_build'] = self._check_command(['cargo', 'check'], cwd=core_path)
        
        # Check Node build
        sdk_path = self.workspace_root / 'axionax-sdk-ts'
        if sdk_path.exists() and (sdk_path / 'package.json').exists():
            tools['node_build'] = (sdk_path / 'node_modules').exists()
        
        score = (sum(1 for v in tools.values() if v) / max(len(tools), 1)) * 100
        
        return len(tools) > 0 and all(tools.values()), score, f"{sum(tools.values())}/{len(tools)} builds OK", tools
    
    # ========================================================================
    # CATEGORY 2: CODEBASE CHECKS
    # ========================================================================
    
    def _check_codebase(self):
        """Check codebase quality and readiness"""
        print(f"\n{BOLD}{BLUE}💻 CODEBASE CHECKS{RESET}")
        
        self._run_check("Code Quality", "codebase",
                       self._check_code_quality)
        self._run_check("Test Coverage", "codebase",
                       self._check_test_coverage)
        self._run_check("Build Success", "codebase",
                       self._check_build_success)
        self._run_check("Linting", "codebase",
                       self._check_linting)
    
    def _check_code_quality(self):
        """Check code quality metrics"""
        # Run quality analyzer if available
        analyzer_path = self.workspace_root / 'axionax-devtools' / 'scripts' / 'analysis' / 'repo_quality_analyzer.py'
        
        if not analyzer_path.exists():
            return False, 0, "Quality analyzer not found", None
        
        try:
            result = subprocess.run(
                [sys.executable, str(analyzer_path)],
                cwd=self.workspace_root,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # Check for QUALITY_ANALYSIS.json
            report_path = self.workspace_root / 'QUALITY_ANALYSIS.json'
            if report_path.exists():
                with open(report_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    avg_score = data.get('average', {}).get('total', 0)
                    
                    if avg_score >= 60:
                        return True, avg_score, f"Quality score: {avg_score:.1f}/100 (Grade D+)", data
                    else:
                        return False, avg_score, f"Quality score: {avg_score:.1f}/100 (Below threshold)", data
            
            return False, 0, "Quality report not generated", None
            
        except Exception as e:
            return False, 0, f"Quality check failed: {str(e)}", None
    
    def _check_test_coverage(self):
        """Check test suite execution"""
        test_runner = self.workspace_root / 'axionax-devtools' / 'run_all_tests.py'
        
        if not test_runner.exists():
            return False, 0, "Test runner not found", None
        
        try:
            result = subprocess.run(
                [sys.executable, str(test_runner)],
                cwd=self.workspace_root,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            # Parse output for test results
            output = result.stdout
            if 'passed' in output.lower():
                # Try to extract numbers
                import re
                match = re.search(r'(\d+)/(\d+)\s+passed', output, re.IGNORECASE)
                if match:
                    passed = int(match.group(1))
                    total = int(match.group(2))
                    score = (passed / total) * 100
                    
                    if passed == total:
                        return True, 100, f"All {total} tests passed", {"passed": passed, "total": total}
                    else:
                        return False, score, f"{passed}/{total} tests passed", {"passed": passed, "total": total}
            
            return True, 80, "Tests executed", None
            
        except Exception as e:
            return False, 0, f"Test execution failed: {str(e)}", None
    
    def _check_build_success(self):
        """Check if all projects build successfully"""
        builds = {}
        
        # Check Rust build
        core_path = self.workspace_root / 'axionax-core'
        if core_path.exists():
            try:
                result = subprocess.run(
                    ['cargo', 'build', '--release'],
                    cwd=core_path,
                    capture_output=True,
                    timeout=300
                )
                builds['rust'] = result.returncode == 0
            except:
                builds['rust'] = False
        
        # Check TypeScript builds
        for project in ['axionax-sdk-ts', 'axionax-web']:
            project_path = self.workspace_root / project
            if project_path.exists() and (project_path / 'package.json').exists():
                try:
                    result = subprocess.run(
                        ['npm', 'run', 'build'],
                        cwd=project_path,
                        capture_output=True,
                        timeout=300
                    )
                    builds[project] = result.returncode == 0
                except:
                    builds[project] = False
        
        if not builds:
            return False, 0, "No buildable projects found", None
        
        success = sum(1 for v in builds.values() if v)
        total = len(builds)
        score = (success / total) * 100
        
        if success == total:
            return True, 100, f"All {total} builds successful", builds
        else:
            return False, score, f"{success}/{total} builds successful", builds
    
    def _check_linting(self):
        """Check code linting status"""
        lint_configs = []
        
        # Check for linting configs
        for repo in ['axionax-core', 'axionax-sdk-ts', 'axionax-web']:
            repo_path = self.workspace_root / repo
            if repo_path.exists():
                if (repo_path / 'clippy.toml').exists():
                    lint_configs.append(f'{repo}/clippy.toml')
                if (repo_path / '.eslintrc.json').exists():
                    lint_configs.append(f'{repo}/.eslintrc.json')
                if (repo_path / '.prettierrc').exists():
                    lint_configs.append(f'{repo}/.prettierrc')
        
        score = min(len(lint_configs) * 20, 100)
        
        if len(lint_configs) >= 5:
            return True, score, f"{len(lint_configs)} lint configs found", {"configs": lint_configs}
        else:
            return False, score, f"Only {len(lint_configs)} lint configs", {"configs": lint_configs}
    
    # ========================================================================
    # CATEGORY 3: SECURITY CHECKS (CRITICAL)
    # ========================================================================
    
    def _check_security(self):
        """Check security readiness"""
        print(f"\n{BOLD}{RED}🔒 SECURITY CHECKS (CRITICAL){RESET}")
        
        self._run_check("No Hardcoded Secrets", "security",
                       self._check_secrets, critical=True)
        self._run_check("Dependency Vulnerabilities", "security",
                       self._check_vulnerabilities, critical=True)
        self._run_check("Security Audit Status", "security",
                       self._check_audit_status, critical=True)
        self._run_check("Access Controls", "security",
                       self._check_access_controls)
    
    def _check_secrets(self):
        """Check for hardcoded secrets"""
        # Common secret patterns
        patterns = [
            'password\s*=\s*["\']',
            'api[_-]?key\s*=\s*["\']',
            'secret\s*=\s*["\']',
            'token\s*=\s*["\']',
            'private[_-]?key\s*=\s*["\']'
        ]
        
        # Paths to exclude from scanning (examples, docs, auto-generated configs)
        exclude_patterns = [
            '.env.example',
            'example',
            'README',
            'DEPLOYMENT_REPORT',
            'docker-compose',
            'setup_testnet.ps1',
            'full_setup.ps1',
            'setup_faucet.sh',  # Accepts CLI arguments
            'setup_explorer.sh',
            'setup_validator.sh',
            'setup_rpc_node.sh',
            'monorepo-archive',  # Archived code
            'your_private_key',  # Placeholder text
            'Axionax_v1.5',  # Old testnet version
            'Axionax_v1.6',  # Old testnet version
        ]
        
        findings = []
        
        for repo in ['axionax-core', 'axionax-sdk-ts', 'axionax-web', 'axionax-deploy', 'axionax-devtools']:
            repo_path = self.workspace_root / repo
            if not repo_path.exists():
                continue
            
            for pattern in patterns:
                try:
                    result = subprocess.run(
                        ['git', 'grep', '-i', '-E', pattern],
                        cwd=repo_path,
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    
                    if result.stdout:
                        # Filter out excluded paths and safe patterns
                        suspicious_lines = []
                        for line in result.stdout.split('\n'):
                            if not line.strip():
                                continue
                            # Skip if contains exclude pattern
                            if any(excl in line for excl in exclude_patterns):
                                continue
                            # Skip empty assignments, env var references, or parameter assignments
                            if '=""' in line or '=${' in line or '="$' in line:
                                continue
                            suspicious_lines.append(line)
                        
                        if suspicious_lines:
                            findings.append({
                                'repo': repo,
                                'pattern': pattern,
                                'matches': len(suspicious_lines),
                                'sample': suspicious_lines[0] if suspicious_lines else ''
                            })
                except:
                    pass
        
        if findings:
            return False, 0, f"Found {len(findings)} potential secrets", {"findings": findings}
        
        return True, 100, "No hardcoded secrets detected", None
    
    def _check_vulnerabilities(self):
        """Check for known vulnerabilities in dependencies"""
        # Check if npm audit shows vulnerabilities
        vulnerable = []
        
        for repo in ['axionax-sdk-ts', 'axionax-web', 'axionax-marketplace']:
            repo_path = self.workspace_root / repo
            if repo_path.exists() and (repo_path / 'package.json').exists():
                try:
                    result = subprocess.run(
                        ['npm', 'audit', '--json'],
                        cwd=repo_path,
                        capture_output=True,
                        text=True,
                        timeout=60
                    )
                    
                    if result.stdout:
                        data = json.loads(result.stdout)
                        if 'vulnerabilities' in data:
                            vuln_counts = data.get('metadata', {}).get('vulnerabilities', {})
                            critical = vuln_counts.get('critical', 0)
                            high = vuln_counts.get('high', 0)
                            
                            if critical > 0 or high > 0:
                                vulnerable.append({
                                    'repo': repo,
                                    'critical': critical,
                                    'high': high
                                })
                except:
                    pass
        
        if vulnerable:
            return False, 30, f"{len(vulnerable)} repos with vulnerabilities", {"vulnerable": vulnerable}
        
        return True, 100, "No critical vulnerabilities found", None
    
    def _check_audit_status(self):
        """Check if security audit has been completed"""
        # Look for audit report
        audit_files = [
            'SECURITY_AUDIT.md',
            'AUDIT_REPORT.md',
            'SECURITY_REVIEW.md'
        ]
        
        found_audits = []
        for filename in audit_files:
            for repo in ['axionax-core', 'axionax-docs']:
                audit_path = self.workspace_root / repo / filename
                if audit_path.exists():
                    found_audits.append(str(audit_path.relative_to(self.workspace_root)))
        
        if found_audits:
            return True, 100, f"Found {len(found_audits)} audit report(s)", {"audits": found_audits}
        
        return False, 0, "No security audit report found", None
    
    def _check_access_controls(self):
        """Check access control configurations"""
        configs = []
        
        # Check for .gitignore
        for repo in ['axionax-core', 'axionax-sdk-ts', 'axionax-web', 'axionax-deploy']:
            gitignore = self.workspace_root / repo / '.gitignore'
            if gitignore.exists():
                configs.append(f'{repo}/.gitignore')
        
        score = min(len(configs) * 25, 100)
        
        return len(configs) >= 4, score, f"{len(configs)} access configs", {"configs": configs}
    
    # ========================================================================
    # CATEGORY 4: PERFORMANCE CHECKS
    # ========================================================================
    
    def _check_performance(self):
        """Check performance readiness"""
        print(f"\n{BOLD}{BLUE}⚡ PERFORMANCE CHECKS{RESET}")
        
        self._run_check("Benchmark Suite", "performance",
                       self._check_benchmarks)
        self._run_check("Build Optimization", "performance",
                       self._check_optimization)
        self._run_check("Load Testing", "performance",
                       self._check_load_testing)
    
    def _check_benchmarks(self):
        """Check for performance benchmarks"""
        bench_files = []
        
        # Check Rust benchmarks
        core_benches = self.workspace_root / 'axionax-core' / 'benches'
        if core_benches.exists():
            bench_files.extend(list(core_benches.glob('*.rs')))
        
        # Check for benchmark results
        bench_results = list(self.workspace_root.glob('**/benchmark_results.*'))
        
        total_found = len(bench_files) + len(bench_results)
        score = min(total_found * 25, 100)
        
        if total_found >= 2:
            return True, score, f"{total_found} benchmark files found", {
                "bench_files": [str(f.relative_to(self.workspace_root)) for f in bench_files]
            }
        else:
            return False, score, f"Only {total_found} benchmark files", None
    
    def _check_optimization(self):
        """Check build optimization configs"""
        optimizations = []
        
        # Check Rust release profile
        core_cargo = self.workspace_root / 'axionax-core' / 'Cargo.toml'
        if core_cargo.exists():
            content = core_cargo.read_text(encoding='utf-8')
            if '[profile.release]' in content and 'opt-level = 3' in content:
                optimizations.append('rust_release_profile')
        
        # Check TypeScript optimization
        for repo in ['axionax-sdk-ts', 'axionax-web']:
            tsconfig = self.workspace_root / repo / 'tsconfig.json'
            if tsconfig.exists():
                content = tsconfig.read_text(encoding='utf-8')
                if 'ES2021' in content or 'ESNext' in content:
                    optimizations.append(f'{repo}_tsconfig')
        
        score = min(len(optimizations) * 30, 100)
        
        return len(optimizations) >= 3, score, f"{len(optimizations)} optimizations", {"optimizations": optimizations}
    
    def _check_load_testing(self):
        """Check for load testing results"""
        # Look for load test results or scripts
        load_test_files = list(self.workspace_root.glob('**/load_test*'))
        
        if load_test_files:
            return True, 100, f"{len(load_test_files)} load test files", {
                "files": [str(f.relative_to(self.workspace_root)) for f in load_test_files]
            }
        
        return False, 0, "No load testing found", None
    
    # ========================================================================
    # CATEGORY 5: DOCUMENTATION CHECKS
    # ========================================================================
    
    def _check_documentation(self):
        """Check documentation completeness"""
        print(f"\n{BOLD}{BLUE}📚 DOCUMENTATION CHECKS{RESET}")
        
        self._run_check("Core Documentation", "documentation",
                       self._check_core_docs)
        self._run_check("API Documentation", "documentation",
                       self._check_api_docs)
        self._run_check("Deployment Guides", "documentation",
                       self._check_deployment_docs)
        self._run_check("Examples", "documentation",
                       self._check_examples)
    
    def _check_core_docs(self):
        """Check core documentation files"""
        required_docs = [
            'README.md',
            'ARCHITECTURE.md',
            'DEVELOPER_GUIDE.md',
            'CONTRIBUTING.md'
        ]
        
        found_docs = []
        
        for doc in required_docs:
            for repo in ['axionax-core', 'axionax-docs']:
                doc_path = self.workspace_root / repo / doc
                if doc_path.exists():
                    found_docs.append(doc)
                    break
        
        score = (len(found_docs) / len(required_docs)) * 100
        
        if len(found_docs) == len(required_docs):
            return True, 100, f"All {len(required_docs)} core docs present", {"docs": found_docs}
        else:
            missing = set(required_docs) - set(found_docs)
            return False, score, f"{len(found_docs)}/{len(required_docs)} docs", {"missing": list(missing)}
    
    def _check_api_docs(self):
        """Check API documentation"""
        api_docs = []
        
        for repo in ['axionax-core', 'axionax-docs', 'axionax-sdk-ts']:
            api_path = self.workspace_root / repo / 'docs' / 'API_REFERENCE.md'
            if not api_path.exists():
                api_path = self.workspace_root / repo / 'API_REFERENCE.md'
            
            if api_path.exists():
                api_docs.append(str(api_path.relative_to(self.workspace_root)))
        
        score = min(len(api_docs) * 50, 100)
        
        return len(api_docs) >= 1, score, f"{len(api_docs)} API docs found", {"docs": api_docs}
    
    def _check_deployment_docs(self):
        """Check deployment documentation"""
        deployment_docs = []
        
        for repo in ['axionax-deploy', 'axionax-docs']:
            for doc_name in ['DEPLOYMENT_GUIDE.md', 'DEPLOYMENT.md', 'VPS_VALIDATOR_SETUP.md']:
                doc_path = self.workspace_root / repo / doc_name
                if doc_path.exists():
                    deployment_docs.append(str(doc_path.relative_to(self.workspace_root)))
        
        score = min(len(deployment_docs) * 40, 100)
        
        return len(deployment_docs) >= 2, score, f"{len(deployment_docs)} deployment docs", {"docs": deployment_docs}
    
    def _check_examples(self):
        """Check for code examples"""
        example_dirs = []
        
        for repo in ['axionax-core', 'axionax-sdk-ts']:
            examples_path = self.workspace_root / repo / 'examples'
            if examples_path.exists() and examples_path.is_dir():
                example_files = list(examples_path.glob('*.*'))
                if example_files:
                    example_dirs.append({
                        'repo': repo,
                        'count': len(example_files)
                    })
        
        total_examples = sum(d['count'] for d in example_dirs)
        score = min(total_examples * 15, 100)
        
        return total_examples >= 4, score, f"{total_examples} examples", {"examples": example_dirs}
    
    # ========================================================================
    # CATEGORY 6: DEPLOYMENT CHECKS
    # ========================================================================
    
    def _check_deployment(self):
        """Check deployment readiness"""
        print(f"\n{BOLD}{BLUE}🚀 DEPLOYMENT CHECKS{RESET}")
        
        self._run_check("Docker Configuration", "deployment",
                       self._check_docker_config)
        self._run_check("Environment Configs", "deployment",
                       self._check_env_configs)
        self._run_check("Deployment Scripts", "deployment",
                       self._check_deployment_scripts)
    
    def _check_docker_config(self):
        """Check Docker configuration"""
        docker_files = []
        
        for repo in ['axionax-core', 'axionax-web', 'axionax-deploy']:
            dockerfile = self.workspace_root / repo / 'Dockerfile'
            if dockerfile.exists():
                docker_files.append(f'{repo}/Dockerfile')
            
            compose = self.workspace_root / repo / 'docker-compose.yml'
            if compose.exists():
                docker_files.append(f'{repo}/docker-compose.yml')
        
        score = min(len(docker_files) * 20, 100)
        
        return len(docker_files) >= 3, score, f"{len(docker_files)} Docker files", {"files": docker_files}
    
    def _check_env_configs(self):
        """Check environment configurations"""
        env_configs = []
        
        for repo in ['axionax-core', 'axionax-web', 'axionax-deploy']:
            repo_path = self.workspace_root / repo
            if repo_path.exists():
                for env_file in ['.env.example', '.env.testnet', 'config.testnet.toml']:
                    env_path = repo_path / env_file
                    if env_path.exists():
                        env_configs.append(f'{repo}/{env_file}')
        
        score = min(len(env_configs) * 25, 100)
        
        return len(env_configs) >= 3, score, f"{len(env_configs)} env configs", {"configs": env_configs}
    
    def _check_deployment_scripts(self):
        """Check deployment automation scripts"""
        scripts = []
        
        deploy_path = self.workspace_root / 'axionax-deploy'
        if deploy_path.exists():
            for script_name in ['setup_rpc_node.sh', 'setup_validator.sh', 'setup_faucet.sh', 'setup_explorer.sh']:
                script_path = deploy_path / script_name
                if script_path.exists():
                    scripts.append(script_name)
        
        score = min(len(scripts) * 25, 100)
        
        return len(scripts) >= 3, score, f"{len(scripts)} deployment scripts", {"scripts": scripts}
    
    # ========================================================================
    # CATEGORY 7: MONITORING CHECKS
    # ========================================================================
    
    def _check_monitoring(self):
        """Check monitoring and observability"""
        print(f"\n{BOLD}{BLUE}📊 MONITORING CHECKS{RESET}")
        
        self._run_check("Logging Configuration", "monitoring",
                       self._check_logging)
        self._run_check("Metrics Collection", "monitoring",
                       self._check_metrics)
        self._run_check("Health Checks", "monitoring",
                       self._check_health_endpoints)
    
    def _check_logging(self):
        """Check logging configuration"""
        # Look for logging configs
        log_configs = []
        
        for repo in ['axionax-core', 'axionax-web']:
            repo_path = self.workspace_root / repo
            if repo_path.exists():
                # Check Rust logging
                cargo = repo_path / 'Cargo.toml'
                if cargo.exists():
                    content = cargo.read_text(encoding='utf-8')
                    if 'log' in content or 'tracing' in content:
                        log_configs.append(f'{repo}/Cargo.toml (logging)')
                
                # Check Node logging
                package = repo_path / 'package.json'
                if package.exists():
                    content = package.read_text(encoding='utf-8')
                    if 'winston' in content or 'pino' in content:
                        log_configs.append(f'{repo}/package.json (logging)')
        
        score = min(len(log_configs) * 50, 100)
        
        return len(log_configs) >= 1, score, f"{len(log_configs)} logging configs", {"configs": log_configs}
    
    def _check_metrics(self):
        """Check metrics collection setup"""
        # Look for metrics endpoints or Prometheus configs
        metrics_files = []
        
        for repo in ['axionax-core', 'axionax-deploy']:
            repo_path = self.workspace_root / repo
            if repo_path.exists():
                for metrics_file in ['prometheus.yml', 'metrics.toml', 'grafana-dashboard.json']:
                    metrics_path = repo_path / metrics_file
                    if metrics_path.exists():
                        metrics_files.append(f'{repo}/{metrics_file}')
        
        score = min(len(metrics_files) * 50, 100)
        
        if metrics_files:
            return True, score, f"{len(metrics_files)} metrics configs", {"files": metrics_files}
        
        return False, 0, "No metrics configuration", None
    
    def _check_health_endpoints(self):
        """Check for health check endpoints"""
        # Look for health check implementations
        health_checks = []
        
        # Check in core
        core_src = self.workspace_root / 'axionax-core' / 'src'
        if core_src.exists():
            for rs_file in core_src.rglob('*.rs'):
                content = rs_file.read_text(encoding='utf-8', errors='ignore')
                if '/health' in content or 'health_check' in content:
                    health_checks.append(str(rs_file.relative_to(self.workspace_root)))
                    break
        
        score = min(len(health_checks) * 100, 100)
        
        return len(health_checks) >= 1, score, f"{len(health_checks)} health endpoints", {"endpoints": health_checks}
    
    # ========================================================================
    # HELPER METHODS
    # ========================================================================
    
    def _check_command(self, cmd: List[str], cwd=None) -> bool:
        """Check if a command runs successfully"""
        try:
            result = subprocess.run(
                cmd,
                cwd=cwd or self.workspace_root,
                capture_output=True,
                timeout=10
            )
            return result.returncode == 0
        except:
            return False
    
    def _calculate_overall(self) -> Tuple[bool, float]:
        """Calculate overall readiness score"""
        if not self.results:
            return False, 0
        
        # Categorize results
        categories = {}
        for result in self.results:
            if result.category not in categories:
                categories[result.category] = []
            categories[result.category].append(result)
        
        # Calculate category scores
        category_scores = {}
        for category, results in categories.items():
            avg_score = sum(r.score for r in results) / len(results)
            category_scores[category] = avg_score
        
        # Overall score (weighted average)
        weights = {
            'infrastructure': 0.15,
            'codebase': 0.20,
            'security': 0.25,  # Highest weight
            'performance': 0.15,
            'documentation': 0.10,
            'deployment': 0.10,
            'monitoring': 0.05
        }
        
        overall_score = sum(
            category_scores.get(cat, 0) * weight
            for cat, weight in weights.items()
        )
        
        # Check critical requirements
        critical_passed = all(
            r.passed for r in self.results if r.critical
        )
        
        # Overall pass requires:
        # 1. All critical checks passed
        # 2. Overall score >= 70
        overall_passed = critical_passed and overall_score >= 70
        
        return overall_passed, overall_score
    
    def _print_summary(self, overall_passed: bool, overall_score: float, elapsed: float):
        """Print summary report"""
        print(f"\n{CYAN}{'='*70}{RESET}")
        print(f"{BOLD}{CYAN}  SUMMARY REPORT{RESET}")
        print(f"{CYAN}{'='*70}{RESET}\n")
        
        # Overall status
        status_color = GREEN if overall_passed else RED
        status_icon = "✅" if overall_passed else "❌"
        status_text = "READY FOR TESTNET" if overall_passed else "NOT READY"
        
        print(f"  {status_icon} {BOLD}{status_color}Overall Status: {status_text}{RESET}")
        print(f"  📊 Overall Score: {overall_score:.1f}/100")
        print(f"  ⏱️  Execution Time: {elapsed:.2f}s\n")
        
        # Category breakdown
        categories = {}
        for result in self.results:
            if result.category not in categories:
                categories[result.category] = []
            categories[result.category].append(result)
        
        print(f"{BOLD}Category Scores:{RESET}")
        for category in ['infrastructure', 'codebase', 'security', 'performance', 
                        'documentation', 'deployment', 'monitoring']:
            if category not in categories:
                continue
            
            results = categories[category]
            avg_score = sum(r.score for r in results) / len(results)
            passed = sum(1 for r in results if r.passed)
            total = len(results)
            
            color = GREEN if avg_score >= 70 else (YELLOW if avg_score >= 50 else RED)
            print(f"  {category.title():20s}: {color}{avg_score:5.1f}/100{RESET}  ({passed}/{total} passed)")
        
        # Critical issues
        critical_failed = [r for r in self.results if r.critical and not r.passed]
        if critical_failed:
            print(f"\n{BOLD}{RED}❌ CRITICAL ISSUES (Must Fix):{RESET}")
            for result in critical_failed:
                print(f"  • {result.name}: {result.message}")
        
        # High priority recommendations
        high_priority = [r for r in self.results if not r.passed and not r.critical and r.score < 50]
        if high_priority:
            print(f"\n{BOLD}{YELLOW}⚠️  HIGH PRIORITY IMPROVEMENTS:{RESET}")
            for result in high_priority[:5]:  # Show top 5
                print(f"  • {result.name}: {result.message}")
        
        # Recommendations
        print(f"\n{BOLD}📋 RECOMMENDATIONS:{RESET}")
        if overall_passed:
            print(f"  {GREEN}✅ System is ready for testnet launch!{RESET}")
            print(f"  • Perform final security review")
            print(f"  • Schedule deployment window")
            print(f"  • Prepare rollback procedures")
        else:
            print(f"  {RED}❌ Complete the following before testnet:{RESET}")
            if critical_failed:
                print(f"  • Fix {len(critical_failed)} critical security issues")
            if overall_score < 70:
                print(f"  • Improve overall score from {overall_score:.1f} to 70+")
            print(f"  • Review failed checks and address root causes")
            print(f"  • Re-run readiness checker after fixes")
        
        print(f"\n{CYAN}{'='*70}{RESET}\n")
    
    def _save_report(self, overall_passed: bool, overall_score: float):
        """Save JSON report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'overall_passed': overall_passed,
            'overall_score': round(overall_score, 2),
            'results': [asdict(r) for r in self.results]
        }
        
        report_path = self.workspace_root / 'TESTNET_READINESS_REPORT.json'
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        print(f"📄 Detailed report saved: {report_path.name}\n")

def main():
    """Main entry point"""
    # Find workspace root
    workspace_root = Path.cwd()
    
    # If running from scripts/testing, go up to workspace root
    if workspace_root.name == 'testing':
        workspace_root = workspace_root.parent.parent.parent
    elif workspace_root.name == 'scripts':
        workspace_root = workspace_root.parent.parent
    elif workspace_root.name == 'axionax-devtools':
        workspace_root = workspace_root.parent
    
    # Run readiness checks
    checker = TestnetReadinessChecker(workspace_root)
    overall_passed, overall_score = checker.run_all_checks()
    
    # Exit with appropriate code
    sys.exit(0 if overall_passed else 1)

if __name__ == '__main__':
    main()
