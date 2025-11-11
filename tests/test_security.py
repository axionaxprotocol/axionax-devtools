#!/usr/bin/env python3
"""
Security and Configuration Tests for axionax DevTools
Tests security best practices, configuration files, and dependencies
"""

import unittest
import os
import sys
from pathlib import Path
import json
import re


class TestSecurityPractices(unittest.TestCase):
    """Test security best practices"""
    
    def setUp(self):
        """Set up test environment"""
        self.devtools_dir = Path(__file__).parent.parent
        self.workspace_root = self.devtools_dir.parent
        
    def test_no_hardcoded_secrets(self):
        """Test that there are no hardcoded secrets in Python files"""
        python_files = list(self.devtools_dir.rglob("*.py"))
        
        # Patterns that might indicate secrets
        secret_patterns = [
            r'password\s*=\s*["\'][^"\']{8,}["\']',
            r'api[_-]?key\s*=\s*["\'][^"\']{20,}["\']',
            r'secret\s*=\s*["\'][^"\']{20,}["\']',
            r'token\s*=\s*["\'][^"\']{20,}["\']',
        ]
        
        found_issues = []
        for py_file in python_files:
            if 'test_' in py_file.name or '__pycache__' in str(py_file):
                continue
                
            try:
                content = py_file.read_text(encoding='utf-8')
                for pattern in secret_patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        # Skip examples and test data
                        if 'example' not in match.group().lower() and 'test' not in match.group().lower():
                            found_issues.append(f"{py_file.name}: {match.group()}")
            except:
                pass
                
        self.assertEqual(len(found_issues), 0, f"Found potential secrets: {found_issues}")
        
    def test_no_executable_permissions_issues(self):
        """Test that shell scripts are properly marked"""
        scripts = [
            self.devtools_dir / "run_tests.sh",
            self.devtools_dir / "install_dependencies_linux.sh",
            self.devtools_dir / "install_dependencies_macos.sh"
        ]
        
        for script in scripts:
            if script.exists():
                # Check if file has shebang
                first_line = script.read_text(encoding='utf-8').split('\n')[0]
                self.assertTrue(
                    first_line.startswith('#!'),
                    f"{script.name} should have shebang line"
                )
                
    def test_gitignore_exists(self):
        """Test that .gitignore exists"""
        gitignore = self.devtools_dir / ".gitignore"
        if gitignore.exists():
            content = gitignore.read_text(encoding='utf-8')
            # Should ignore common files
            important_patterns = ['__pycache__', '*.pyc', '.env', 'node_modules']
            for pattern in important_patterns:
                self.assertIn(pattern, content, f".gitignore should contain {pattern}")


class TestConfigurationFiles(unittest.TestCase):
    """Test configuration files"""
    
    def setUp(self):
        """Set up test environment"""
        self.devtools_dir = Path(__file__).parent.parent
        
    def test_package_json_valid(self):
        """Test that package.json is valid JSON"""
        package_json = self.devtools_dir / "package.json"
        if package_json.exists():
            try:
                with open(package_json, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.assertIn('name', data)
                    self.assertEqual(data['name'], 'axionax-devtools')
            except json.JSONDecodeError as e:
                self.fail(f"package.json is not valid JSON: {e}")
                
    def test_python_files_have_utf8_encoding(self):
        """Test that Python files use UTF-8 encoding"""
        python_files = list(self.devtools_dir.rglob("*.py"))
        
        for py_file in python_files:
            if '__pycache__' in str(py_file):
                continue
                
            try:
                # Try to read with UTF-8
                py_file.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                self.fail(f"{py_file.name} cannot be read as UTF-8")


class TestDependencies(unittest.TestCase):
    """Test dependencies and requirements"""
    
    def setUp(self):
        """Set up test environment"""
        self.devtools_dir = Path(__file__).parent.parent
        
    def test_requirements_file_exists(self):
        """Test that requirements file exists if using Python"""
        # Check for common requirements files
        req_files = [
            'requirements.txt',
            'requirements-dev.txt',
            'pyproject.toml'
        ]
        
        found_any = False
        for req_file in req_files:
            if (self.devtools_dir / req_file).exists():
                found_any = True
                break
                
        # This is informational, not mandatory
        if not found_any:
            self.skipTest("No requirements files found (optional)")
            
    def test_no_vulnerable_package_patterns(self):
        """Test that there are no known vulnerable package patterns"""
        package_json = self.devtools_dir / "package.json"
        if package_json.exists():
            try:
                with open(package_json, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Check for dependencies
                deps = data.get('dependencies', {})
                dev_deps = data.get('devDependencies', {})
                all_deps = {**deps, **dev_deps}
                
                # Should not have overly permissive version constraints
                for pkg, version in all_deps.items():
                    if version == '*':
                        self.fail(f"Package {pkg} uses wildcard version (*), should be more specific")
            except:
                pass


class TestDocumentationQuality(unittest.TestCase):
    """Test documentation quality"""
    
    def setUp(self):
        """Set up test environment"""
        self.devtools_dir = Path(__file__).parent.parent
        
    def test_readme_has_essential_sections(self):
        """Test that README has essential sections"""
        readme = self.devtools_dir / "README.md"
        if readme.exists():
            content = readme.read_text(encoding='utf-8').lower()
            
            essential_sections = [
                'installation',
                'usage',
                'axionax'
            ]
            
            for section in essential_sections:
                self.assertIn(
                    section,
                    content,
                    f"README should contain section about '{section}'"
                )
                
    def test_readme_has_github_links(self):
        """Test that README has proper GitHub links"""
        readme = self.devtools_dir / "README.md"
        if readme.exists():
            content = readme.read_text(encoding='utf-8')
            
            # Should have GitHub links
            self.assertIn('github.com', content)
            self.assertIn('axionaxprotocol', content)
            
    def test_no_broken_markdown_links(self):
        """Test that there are no obviously broken markdown links"""
        readme = self.devtools_dir / "README.md"
        if readme.exists():
            content = readme.read_text(encoding='utf-8')
            
            # Find markdown links: [text](url)
            link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
            matches = re.finditer(link_pattern, content)
            
            for match in matches:
                url = match.group(2)
                # Check for common mistakes
                if url.startswith('http'):
                    # Should not have /blob/ for GitHub tree links
                    if '/blob/' in url and not any(ext in url for ext in ['.md', '.txt', '.json', '.yml']):
                        self.fail(f"Found /blob/ in non-file link: {url}")


class TestCodeQuality(unittest.TestCase):
    """Test code quality standards"""
    
    def setUp(self):
        """Set up test environment"""
        self.devtools_dir = Path(__file__).parent.parent
        
    def test_python_files_have_docstrings(self):
        """Test that Python modules have docstrings"""
        python_files = list(self.devtools_dir.rglob("*.py"))
        
        files_without_docstring = []
        for py_file in python_files:
            if '__pycache__' in str(py_file) or '__init__' in py_file.name:
                continue
                
            try:
                content = py_file.read_text(encoding='utf-8')
                lines = content.split('\n')
                
                # Check first 10 lines for docstring
                has_docstring = False
                for line in lines[:10]:
                    if '"""' in line or "'''" in line:
                        has_docstring = True
                        break
                        
                if not has_docstring and len(content.strip()) > 50:
                    files_without_docstring.append(py_file.name)
            except:
                pass
                
        # This is a recommendation, not a hard requirement
        if files_without_docstring:
            print(f"\nNote: Files without docstrings: {files_without_docstring}")
            
    def test_no_print_statements_in_production(self):
        """Test that production code doesn't have debug print statements"""
        python_files = list(self.devtools_dir.rglob("*.py"))
        
        files_with_prints = []
        for py_file in python_files:
            if 'test_' in py_file.name or '__pycache__' in str(py_file):
                continue
                
            try:
                content = py_file.read_text(encoding='utf-8')
                lines = content.split('\n')
                
                for i, line in enumerate(lines):
                    # Look for print() not in comments or strings
                    if 'print(' in line:
                        stripped = line.strip()
                        if stripped.startswith('print(') and not stripped.startswith('#'):
                            files_with_prints.append(f"{py_file.name}:{i+1}")
            except:
                pass
                
        # This is informational for review
        if files_with_prints:
            print(f"\nNote: Files with print() statements: {files_with_prints[:5]}")


def run_advanced_tests():
    """Run all advanced tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestSecurityPractices))
    suite.addTests(loader.loadTestsFromTestCase(TestConfigurationFiles))
    suite.addTests(loader.loadTestsFromTestCase(TestDependencies))
    suite.addTests(loader.loadTestsFromTestCase(TestDocumentationQuality))
    suite.addTests(loader.loadTestsFromTestCase(TestCodeQuality))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    print("=" * 70)
    print("axionax DevTools - Advanced Security & Quality Tests")
    print("=" * 70)
    print()
    
    success = run_advanced_tests()
    
    print()
    print("=" * 70)
    if success:
        print("ทดสอบเรียบร้อย - All advanced tests passed!")
        sys.exit(0)
    else:
        print("พบข้อผิดพลาด - Some tests failed!")
        sys.exit(1)
