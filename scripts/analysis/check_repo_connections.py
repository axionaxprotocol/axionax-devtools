#!/usr/bin/env python3
"""
Repository Connection Checker
Analyzes dependencies and connections between axionax repositories
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Set, Tuple

class RepoConnectionChecker:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.repos = [
            'axionax-core',
            'axionax-web',
            'axionax-sdk-ts',
            'axionax-marketplace',
            'axionax-docs',
            'axionax-deploy',
            'axionax-devtools'
        ]
        self.connections = {}
        self.package_dependencies = {}
        self.import_dependencies = {}
        
    def check_repo_exists(self, repo_name: str) -> bool:
        """Check if repository directory exists"""
        repo_path = self.base_path / repo_name
        return repo_path.exists() and repo_path.is_dir()
    
    def get_git_info(self, repo_name: str) -> Dict:
        """Get git repository information"""
        repo_path = self.base_path / repo_name
        if not self.check_repo_exists(repo_name):
            return {"exists": False}
        
        try:
            os.chdir(repo_path)
            
            # Get current branch
            branch = subprocess.run(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                capture_output=True, text=True
            ).stdout.strip()
            
            # Get remote URL
            remote = subprocess.run(
                ['git', 'remote', 'get-url', 'origin'],
                capture_output=True, text=True
            ).stdout.strip()
            
            # Get last commit
            last_commit = subprocess.run(
                ['git', 'log', '-1', '--format=%h - %s'],
                capture_output=True, text=True
            ).stdout.strip()
            
            return {
                "exists": True,
                "branch": branch,
                "remote": remote,
                "last_commit": last_commit
            }
        except Exception as e:
            return {"exists": True, "error": str(e)}
    
    def analyze_package_json(self, repo_name: str) -> Dict:
        """Analyze package.json for dependencies"""
        repo_path = self.base_path / repo_name
        package_json = repo_path / "package.json"
        
        if not package_json.exists():
            return {}
        
        try:
            with open(package_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            deps = {}
            if 'dependencies' in data:
                deps['dependencies'] = data['dependencies']
            if 'devDependencies' in data:
                deps['devDependencies'] = data['devDependencies']
            
            # Check for axionax-related dependencies
            axionax_deps = []
            for dep_type in ['dependencies', 'devDependencies']:
                if dep_type in deps:
                    for dep_name in deps[dep_type].keys():
                        if 'axionax' in dep_name.lower():
                            axionax_deps.append({
                                'name': dep_name,
                                'version': deps[dep_type][dep_name],
                                'type': dep_type
                            })
            
            return {
                'has_package_json': True,
                'axionax_dependencies': axionax_deps,
                'total_dependencies': len(deps.get('dependencies', {})),
                'total_dev_dependencies': len(deps.get('devDependencies', {}))
            }
        except Exception as e:
            return {'has_package_json': True, 'error': str(e)}
    
    def analyze_cargo_toml(self, repo_name: str) -> Dict:
        """Analyze Cargo.toml for Rust dependencies"""
        repo_path = self.base_path / repo_name
        cargo_toml = repo_path / "Cargo.toml"
        
        if not cargo_toml.exists():
            return {}
        
        try:
            with open(cargo_toml, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple parsing for axionax-related dependencies
            axionax_deps = []
            in_dependencies = False
            for line in content.split('\n'):
                if line.strip().startswith('[dependencies'):
                    in_dependencies = True
                    continue
                if line.strip().startswith('['):
                    in_dependencies = False
                
                if in_dependencies and 'axionax' in line.lower():
                    axionax_deps.append(line.strip())
            
            return {
                'has_cargo_toml': True,
                'axionax_dependencies': axionax_deps
            }
        except Exception as e:
            return {'has_cargo_toml': True, 'error': str(e)}
    
    def scan_imports(self, repo_name: str) -> Set[str]:
        """Scan for axionax-related imports in source files"""
        repo_path = self.base_path / repo_name
        axionax_imports = set()
        
        # File extensions to scan
        extensions = ['.ts', '.tsx', '.js', '.jsx', '.rs', '.py', '.go']
        
        for ext in extensions:
            try:
                for file_path in repo_path.rglob(f'*{ext}'):
                    # Skip node_modules, target, dist, build directories
                    if any(skip in str(file_path) for skip in ['node_modules', 'target', 'dist', 'build', '.git']):
                        continue
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            
                        # Look for import/require statements with axionax
                        for line in content.split('\n'):
                            if 'axionax' in line.lower() and any(keyword in line for keyword in ['import', 'require', 'from', 'use']):
                                axionax_imports.add(line.strip()[:100])  # Truncate long lines
                    except:
                        continue
            except:
                continue
        
        return axionax_imports
    
    def analyze_readme(self, repo_name: str) -> Dict:
        """Analyze README.md for documentation and references"""
        repo_path = self.base_path / repo_name
        readme_path = repo_path / "README.md"
        
        if not readme_path.exists():
            return {'has_readme': False}
        
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Count references to other repos
            repo_references = {}
            for other_repo in self.repos:
                if other_repo != repo_name:
                    count = content.lower().count(other_repo.lower())
                    if count > 0:
                        repo_references[other_repo] = count
            
            return {
                'has_readme': True,
                'size': len(content),
                'repo_references': repo_references
            }
        except Exception as e:
            return {'has_readme': True, 'error': str(e)}
    
    def analyze_all_repos(self) -> Dict:
        """Analyze all repositories"""
        results = {}
        
        print("🔍 Analyzing repository connections...\n")
        
        for repo_name in self.repos:
            print(f"📦 Analyzing {repo_name}...")
            
            results[repo_name] = {
                'git_info': self.get_git_info(repo_name),
                'package_info': self.analyze_package_json(repo_name),
                'cargo_info': self.analyze_cargo_toml(repo_name),
                'readme_info': self.analyze_readme(repo_name),
                'imports': list(self.scan_imports(repo_name))
            }
        
        return results
    
    def generate_connection_graph(self, results: Dict) -> List[Tuple[str, str, str]]:
        """Generate connection graph from analysis results"""
        connections = []
        
        for repo_name, data in results.items():
            # From package.json dependencies
            if 'package_info' in data and 'axionax_dependencies' in data['package_info']:
                for dep in data['package_info']['axionax_dependencies']:
                    dep_name = dep['name']
                    for other_repo in self.repos:
                        if other_repo in dep_name:
                            connections.append((repo_name, other_repo, f"npm:{dep['type']}"))
            
            # From Cargo.toml dependencies
            if 'cargo_info' in data and 'axionax_dependencies' in data['cargo_info']:
                for dep in data['cargo_info']['axionax_dependencies']:
                    for other_repo in self.repos:
                        if other_repo in dep:
                            connections.append((repo_name, other_repo, "cargo:dependency"))
            
            # From README references
            if 'readme_info' in data and 'repo_references' in data['readme_info']:
                for other_repo, count in data['readme_info']['repo_references'].items():
                    connections.append((repo_name, other_repo, f"docs:reference({count})"))
        
        return connections
    
    def generate_mermaid_diagram(self, results: Dict, connections: List[Tuple[str, str, str]]) -> str:
        """Generate Mermaid flowchart diagram"""
        mermaid = ["```mermaid", "graph TD"]
        
        # Define nodes with status
        for repo_name, data in results.items():
            status = "✅" if data['git_info'].get('exists') else "❌"
            repo_id = repo_name.replace('-', '_')
            mermaid.append(f"    {repo_id}[\"{status} {repo_name}\"]")
        
        # Add connections
        for source, target, conn_type in connections:
            source_id = source.replace('-', '_')
            target_id = target.replace('-', '_')
            mermaid.append(f"    {source_id} -->|{conn_type}| {target_id}")
        
        # Add styling
        mermaid.append("")
        mermaid.append("    classDef coreStyle fill:#ff6b6b,stroke:#c92a2a,stroke-width:2px")
        mermaid.append("    classDef webStyle fill:#4ecdc4,stroke:#219a91,stroke-width:2px")
        mermaid.append("    classDef toolStyle fill:#ffe66d,stroke:#cca300,stroke-width:2px")
        mermaid.append("    classDef sdkStyle fill:#a8e6cf,stroke:#64b58b,stroke-width:2px")
        mermaid.append("")
        mermaid.append("    class axionax_core coreStyle")
        mermaid.append("    class axionax_web,axionax_marketplace webStyle")
        mermaid.append("    class axionax_devtools,axionax_deploy toolStyle")
        mermaid.append("    class axionax_sdk_ts,axionax_docs sdkStyle")
        mermaid.append("```")
        
        return "\n".join(mermaid)
    
    def generate_report(self, results: Dict, connections: List[Tuple[str, str, str]]) -> str:
        """Generate comprehensive text report"""
        report = []
        report.append("=" * 80)
        report.append("AXIONAX REPOSITORY CONNECTION ANALYSIS REPORT")
        report.append("=" * 80)
        report.append("")
        
        # Summary
        report.append("📊 REPOSITORY SUMMARY")
        report.append("-" * 80)
        total_repos = len(results)
        existing_repos = sum(1 for data in results.values() if data['git_info'].get('exists'))
        report.append(f"Total Repositories: {total_repos}")
        report.append(f"Existing Repositories: {existing_repos}")
        report.append(f"Total Connections Found: {len(connections)}")
        report.append("")
        
        # Detailed analysis per repo
        report.append("📦 DETAILED REPOSITORY ANALYSIS")
        report.append("-" * 80)
        
        for repo_name, data in results.items():
            report.append(f"\n### {repo_name.upper()}")
            report.append("-" * 40)
            
            git_info = data['git_info']
            if git_info.get('exists'):
                report.append(f"✅ Status: EXISTS")
                report.append(f"   Branch: {git_info.get('branch', 'N/A')}")
                report.append(f"   Remote: {git_info.get('remote', 'N/A')}")
                report.append(f"   Last Commit: {git_info.get('last_commit', 'N/A')}")
            else:
                report.append(f"❌ Status: NOT FOUND")
                continue
            
            # Package info
            pkg_info = data.get('package_info', {})
            if pkg_info.get('has_package_json'):
                report.append(f"\n📄 Package.json:")
                report.append(f"   Dependencies: {pkg_info.get('total_dependencies', 0)}")
                report.append(f"   Dev Dependencies: {pkg_info.get('total_dev_dependencies', 0)}")
                if pkg_info.get('axionax_dependencies'):
                    report.append(f"   Axionax Dependencies:")
                    for dep in pkg_info['axionax_dependencies']:
                        report.append(f"     - {dep['name']} ({dep['version']}) [{dep['type']}]")
            
            # Cargo info
            cargo_info = data.get('cargo_info', {})
            if cargo_info.get('has_cargo_toml'):
                report.append(f"\n📦 Cargo.toml:")
                if cargo_info.get('axionax_dependencies'):
                    report.append(f"   Axionax Dependencies:")
                    for dep in cargo_info['axionax_dependencies']:
                        report.append(f"     - {dep}")
            
            # README info
            readme_info = data.get('readme_info', {})
            if readme_info.get('has_readme'):
                report.append(f"\n📖 README.md:")
                report.append(f"   Size: {readme_info.get('size', 0)} bytes")
                if readme_info.get('repo_references'):
                    report.append(f"   References to other repos:")
                    for ref_repo, count in readme_info['repo_references'].items():
                        report.append(f"     - {ref_repo}: {count} mention(s)")
            
            # Imports
            if data.get('imports'):
                report.append(f"\n🔗 Import Statements ({len(data['imports'])} found):")
                for imp in list(data['imports'])[:5]:  # Show first 5
                    report.append(f"     {imp}")
                if len(data['imports']) > 5:
                    report.append(f"     ... and {len(data['imports']) - 5} more")
            
            report.append("")
        
        # Connection graph
        report.append("\n🔗 CONNECTION GRAPH")
        report.append("-" * 80)
        if connections:
            for source, target, conn_type in connections:
                report.append(f"{source} --> {target} ({conn_type})")
        else:
            report.append("No direct connections found between repositories.")
        
        report.append("")
        report.append("=" * 80)
        report.append("END OF REPORT")
        report.append("=" * 80)
        
        return "\n".join(report)

def main():
    # Get the base path (current directory)
    base_path = os.getcwd()
    
    print("🚀 axionax Repository Connection Checker")
    print("=" * 80)
    print(f"📁 Base Path: {base_path}\n")
    
    # Initialize checker
    checker = RepoConnectionChecker(base_path)
    
    # Analyze all repositories
    results = checker.analyze_all_repos()
    
    # Generate connection graph
    print("\n🔗 Generating connection graph...")
    connections = checker.generate_connection_graph(results)
    
    # Generate Mermaid diagram
    print("📊 Generating Mermaid diagram...")
    mermaid_diagram = checker.generate_mermaid_diagram(results, connections)
    
    # Generate report
    print("📝 Generating report...")
    report = checker.generate_report(results, connections)
    
    # Save Mermaid diagram
    mermaid_file = Path(base_path) / "REPOSITORY_FLOW.md"
    with open(mermaid_file, 'w', encoding='utf-8') as f:
        f.write("# axionax Repository Connection Flow\n\n")
        f.write("## Connection Diagram\n\n")
        f.write(mermaid_diagram)
        f.write("\n\n## Legend\n\n")
        f.write("- 🔴 **Core**: axionax-core (main protocol implementation)\n")
        f.write("- 🔵 **Web**: axionax-web, axionax-marketplace (web interfaces)\n")
        f.write("- 🟡 **Tools**: axionax-devtools, axionax-deploy (development & deployment)\n")
        f.write("- 🟢 **SDK/Docs**: axionax-sdk-ts, axionax-docs (libraries & documentation)\n")
    
    print(f"✅ Mermaid diagram saved to: {mermaid_file}")
    
    # Save full report
    report_file = Path(base_path) / "REPOSITORY_ANALYSIS.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ Full report saved to: {report_file}")
    
    # Display summary
    print("\n" + "=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    print(f"Total Repositories Analyzed: {len(results)}")
    print(f"Repositories Found: {sum(1 for data in results.values() if data['git_info'].get('exists'))}")
    print(f"Total Connections: {len(connections)}")
    print("\n✅ Analysis complete! Check the generated files for details.")

if __name__ == "__main__":
    main()
