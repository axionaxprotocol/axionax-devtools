#!/usr/bin/env python3
"""
Integration Tests for axionax DevTools
Tests cross-repository integration and connectivity
"""

import unittest
import os
import sys
from pathlib import Path
import subprocess


class TestRepositoryConnectivity(unittest.TestCase):
    """Test that repositories can connect to each other"""
    
    def setUp(self):
        """Set up test environment"""
        self.devtools_dir = Path(__file__).parent.parent
        self.workspace_root = self.devtools_dir.parent
        
    def test_core_repository_accessible(self):
        """Test that axionax-core repository is accessible"""
        core_path = self.workspace_root / "axionax-core"
        if core_path.exists():
            self.assertTrue(core_path.is_dir())
            self.assertTrue((core_path / "Cargo.toml").exists())
            self.assertTrue((core_path / "README.md").exists())
            
    def test_sdk_repository_accessible(self):
        """Test that axionax-sdk-ts repository is accessible"""
        sdk_path = self.workspace_root / "axionax-sdk-ts"
        if sdk_path.exists():
            self.assertTrue(sdk_path.is_dir())
            self.assertTrue((sdk_path / "package.json").exists())
            self.assertTrue((sdk_path / "README.md").exists())
            
    def test_web_repository_accessible(self):
        """Test that axionax-web repository is accessible"""
        web_path = self.workspace_root / "axionax-web"
        if web_path.exists():
            self.assertTrue(web_path.is_dir())
            self.assertTrue((web_path / "package.json").exists())
            self.assertTrue((web_path / "README.md").exists())


class TestGitIntegration(unittest.TestCase):
    """Test Git operations and repository state"""
    
    def setUp(self):
        """Set up test environment"""
        self.devtools_dir = Path(__file__).parent.parent
        
    def test_git_repository(self):
        """Test that this is a valid git repository"""
        git_dir = self.devtools_dir / ".git"
        self.assertTrue(git_dir.exists(), "Should be a git repository")
        
    def test_git_remote_configured(self):
        """Test that git remote is configured"""
        try:
            result = subprocess.run(
                ["git", "remote", "-v"],
                cwd=self.devtools_dir,
                capture_output=True,
                text=True,
                timeout=5
            )
            self.assertEqual(result.returncode, 0)
            self.assertIn("axionaxprotocol", result.stdout)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.skipTest("Git not available or timeout")
            
    def test_on_main_or_valid_branch(self):
        """Test that we're on a valid branch"""
        try:
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=self.devtools_dir,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                branch = result.stdout.strip()
                self.assertTrue(len(branch) > 0, "Should be on a valid branch")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.skipTest("Git not available or timeout")


class TestScriptExecution(unittest.TestCase):
    """Test that scripts can be executed"""
    
    def setUp(self):
        """Set up test environment"""
        self.devtools_dir = Path(__file__).parent.parent
        
    def test_run_tests_script_exists(self):
        """Test that run_tests.sh exists"""
        script = self.devtools_dir / "run_tests.sh"
        self.assertTrue(script.exists())
        
    def test_install_scripts_exist(self):
        """Test that installation scripts exist"""
        scripts = [
            "install_dependencies_linux.sh",
            "install_dependencies_macos.sh",
            "install_dependencies_windows.ps1"
        ]
        for script_name in scripts:
            script = self.devtools_dir / script_name
            self.assertTrue(script.exists(), f"{script_name} should exist")


class TestCrossRepoLinks(unittest.TestCase):
    """Test cross-repository documentation links"""
    
    def setUp(self):
        """Set up test environment"""
        self.devtools_dir = Path(__file__).parent.parent
        self.workspace_root = self.devtools_dir.parent
        
    def test_readme_references_core(self):
        """Test that README references axionax-core correctly"""
        readme = self.devtools_dir / "README.md"
        if readme.exists():
            content = readme.read_text(encoding='utf-8')
            # Should reference core repository
            self.assertTrue(
                "axionax-core" in content,
                "README should reference axionax-core"
            )
            
    def test_no_monorepo_references(self):
        """Test that there are no old monorepo references"""
        readme = self.devtools_dir / "README.md"
        if readme.exists():
            content = readme.read_text(encoding='utf-8')
            # Should NOT reference old monorepo
            self.assertNotIn(
                "axionaxiues",
                content,
                "README should not reference old monorepo"
            )


def run_integration_tests():
    """Run all integration tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestRepositoryConnectivity))
    suite.addTests(loader.loadTestsFromTestCase(TestGitIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestScriptExecution))
    suite.addTests(loader.loadTestsFromTestCase(TestCrossRepoLinks))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    print("=" * 70)
    print("axionax DevTools - Integration Tests")
    print("=" * 70)
    print()
    
    success = run_integration_tests()
    
    print()
    print("=" * 70)
    if success:
        print("All integration tests passed!")
        sys.exit(0)
    else:
        print("Some integration tests failed!")
        sys.exit(1)
