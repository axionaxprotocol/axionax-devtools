#!/usr/bin/env python3
"""
Performance and Build Tests for axionax DevTools
Tests performance characteristics and build processes
"""

import unittest
import os
import sys
from pathlib import Path
import time
import subprocess


class TestPerformance(unittest.TestCase):
    """Test performance characteristics"""
    
    def setUp(self):
        """Set up test environment"""
        self.devtools_dir = Path(__file__).parent.parent
        
    def test_file_operations_performance(self):
        """Test that file operations are reasonably fast"""
        start_time = time.time()
        
        # Count all Python files
        python_files = list(self.devtools_dir.rglob("*.py"))
        
        elapsed = time.time() - start_time
        
        # Should complete in reasonable time (< 5 seconds)
        self.assertLess(elapsed, 5.0, "File enumeration should be fast")
        self.assertGreater(len(python_files), 0, "Should find some Python files")
        
    def test_readme_parsing_performance(self):
        """Test that README parsing is fast"""
        readme = self.devtools_dir / "README.md"
        if not readme.exists():
            self.skipTest("README.md not found")
            
        start_time = time.time()
        
        # Read and parse README
        content = readme.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        elapsed = time.time() - start_time
        
        # Should be very fast (< 1 second)
        self.assertLess(elapsed, 1.0, "README parsing should be very fast")
        self.assertGreater(len(lines), 10, "README should have content")


class TestBuildProcesses(unittest.TestCase):
    """Test build and compilation processes"""
    
    def setUp(self):
        """Set up test environment"""
        self.devtools_dir = Path(__file__).parent.parent
        self.workspace_root = self.devtools_dir.parent
        
    def test_python_syntax_validation(self):
        """Test that all Python files have valid syntax"""
        python_files = list(self.devtools_dir.rglob("*.py"))
        
        syntax_errors = []
        for py_file in python_files:
            if '__pycache__' in str(py_file):
                continue
                
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    compile(f.read(), py_file.name, 'exec')
            except SyntaxError as e:
                syntax_errors.append(f"{py_file.name}: {e}")
                
        self.assertEqual(len(syntax_errors), 0, f"Found syntax errors: {syntax_errors}")
        
    def test_core_project_buildable(self):
        """Test that axionax-core can be checked for build"""
        core_path = self.workspace_root / "axionax-core"
        if not core_path.exists():
            self.skipTest("axionax-core not found")
            
        cargo_toml = core_path / "Cargo.toml"
        self.assertTrue(cargo_toml.exists(), "Cargo.toml should exist")
        
    def test_sdk_project_structure(self):
        """Test that axionax-sdk-ts has proper structure"""
        sdk_path = self.workspace_root / "axionax-sdk-ts"
        if not sdk_path.exists():
            self.skipTest("axionax-sdk-ts not found")
            
        package_json = sdk_path / "package.json"
        self.assertTrue(package_json.exists(), "package.json should exist")


class TestScriptIntegrity(unittest.TestCase):
    """Test script integrity and executability"""
    
    def setUp(self):
        """Set up test environment"""
        self.devtools_dir = Path(__file__).parent.parent
        
    def test_powershell_scripts_syntax(self):
        """Test that PowerShell scripts have basic syntax correctness"""
        ps_scripts = list(self.devtools_dir.rglob("*.ps1"))
        
        for ps_script in ps_scripts:
            try:
                content = ps_script.read_text(encoding='utf-8')
                
                # Basic checks
                self.assertGreater(len(content), 0, f"{ps_script.name} should not be empty")
                
                # Should not have obvious syntax errors
                self.assertNotIn('<<<<<<', content, f"{ps_script.name} has merge conflict markers")
                self.assertNotIn('>>>>>>', content, f"{ps_script.name} has merge conflict markers")
            except Exception as e:
                self.fail(f"Error reading {ps_script.name}: {e}")
                
    def test_bash_scripts_syntax(self):
        """Test that Bash scripts have basic syntax correctness"""
        sh_scripts = list(self.devtools_dir.rglob("*.sh"))
        
        for sh_script in sh_scripts:
            try:
                content = sh_script.read_text(encoding='utf-8')
                
                # Basic checks
                self.assertGreater(len(content), 0, f"{sh_script.name} should not be empty")
                
                # Should start with shebang
                first_line = content.split('\n')[0]
                self.assertTrue(
                    first_line.startswith('#!'),
                    f"{sh_script.name} should have shebang"
                )
                
                # Should not have merge conflicts
                self.assertNotIn('<<<<<<', content, f"{sh_script.name} has merge conflict markers")
                self.assertNotIn('>>>>>>', content, f"{sh_script.name} has merge conflict markers")
            except Exception as e:
                self.fail(f"Error reading {sh_script.name}: {e}")


class TestCrossRepositoryIntegration(unittest.TestCase):
    """Test cross-repository integration"""
    
    def setUp(self):
        """Set up test environment"""
        self.devtools_dir = Path(__file__).parent.parent
        self.workspace_root = self.devtools_dir.parent
        
    def test_all_repos_have_readme(self):
        """Test that all repositories have README"""
        expected_repos = [
            "axionax-core",
            "axionax-web",
            "axionax-sdk-ts",
            "axionax-docs",
            "axionax-devtools"
        ]
        
        repos_without_readme = []
        for repo in expected_repos:
            repo_path = self.workspace_root / repo
            if repo_path.exists():
                readme = repo_path / "README.md"
                if not readme.exists():
                    repos_without_readme.append(repo)
                    
        self.assertEqual(
            len(repos_without_readme),
            0,
            f"Repositories without README: {repos_without_readme}"
        )
        
    def test_all_repos_are_git_repositories(self):
        """Test that all repositories are git repositories"""
        expected_repos = [
            "axionax-core",
            "axionax-web",
            "axionax-sdk-ts",
            "axionax-docs",
            "axionax-devtools"
        ]
        
        non_git_repos = []
        for repo in expected_repos:
            repo_path = self.workspace_root / repo
            if repo_path.exists():
                git_dir = repo_path / ".git"
                if not git_dir.exists():
                    non_git_repos.append(repo)
                    
        self.assertEqual(
            len(non_git_repos),
            0,
            f"Repositories without .git: {non_git_repos}"
        )


def run_performance_tests():
    """Run all performance tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestPerformance))
    suite.addTests(loader.loadTestsFromTestCase(TestBuildProcesses))
    suite.addTests(loader.loadTestsFromTestCase(TestScriptIntegrity))
    suite.addTests(loader.loadTestsFromTestCase(TestCrossRepositoryIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    print("=" * 70)
    print("axionax DevTools - Performance & Build Tests")
    print("=" * 70)
    print()
    
    success = run_performance_tests()
    
    print()
    print("=" * 70)
    if success:
        print("ทดสอบเรียบร้อย - All performance tests passed!")
        sys.exit(0)
    else:
        print("พบข้อผิดพลาด - Some tests failed!")
        sys.exit(1)
