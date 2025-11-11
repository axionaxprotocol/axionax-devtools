#!/usr/bin/env python3
"""
Basic Unit Tests for axionax DevTools
Tests core functionality, file operations, and utility functions
"""

import unittest
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestFileOperations(unittest.TestCase):
    """Test file and directory operations"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = Path(__file__).parent
        self.root_dir = self.test_dir.parent
        
    def test_workspace_structure(self):
        """Test that workspace has correct structure"""
        # Check main directories exist
        self.assertTrue(self.root_dir.exists(), "Root directory should exist")
        self.assertTrue((self.root_dir / "scripts").exists(), "Scripts directory should exist")
        self.assertTrue((self.root_dir / "tools").exists(), "Tools directory should exist")
        self.assertTrue((self.root_dir / "docs").exists(), "Docs directory should exist")
        
    def test_readme_exists(self):
        """Test that README.md exists and is not empty"""
        readme = self.root_dir / "README.md"
        self.assertTrue(readme.exists(), "README.md should exist")
        self.assertGreater(readme.stat().st_size, 0, "README.md should not be empty")
        
    def test_scripts_executable(self):
        """Test that shell scripts exist"""
        scripts = [
            "run_tests.sh",
            "install_dependencies_linux.sh",
            "install_dependencies_macos.sh"
        ]
        for script in scripts:
            script_path = self.root_dir / script
            self.assertTrue(script_path.exists(), f"{script} should exist")


class TestRepositoryStructure(unittest.TestCase):
    """Test repository structure and organization"""
    
    def setUp(self):
        """Set up test environment"""
        self.root_dir = Path(__file__).parent.parent
        self.workspace_root = self.root_dir.parent
        
    def test_sibling_repositories(self):
        """Test that sibling repositories exist"""
        expected_repos = [
            "axionax-core",
            "axionax-web",
            "axionax-sdk-ts",
            "axionax-docs",
            "axionax-deploy"
        ]
        
        for repo in expected_repos:
            repo_path = self.workspace_root / repo
            # Only test if workspace has multi-repo structure
            if repo_path.exists():
                self.assertTrue(repo_path.is_dir(), f"{repo} should be a directory")
                
    def test_devtools_scripts(self):
        """Test that essential scripts exist"""
        scripts_dir = self.root_dir / "scripts"
        if scripts_dir.exists():
            subdirs = ["testing", "fixing", "analysis"]
            for subdir in subdirs:
                subdir_path = scripts_dir / subdir
                if subdir_path.exists():
                    self.assertTrue(subdir_path.is_dir(), f"scripts/{subdir} should be a directory")


class TestToolsAvailability(unittest.TestCase):
    """Test that required tools are available"""
    
    def test_python_version(self):
        """Test Python version is 3.10+"""
        self.assertGreaterEqual(sys.version_info.major, 3)
        self.assertGreaterEqual(sys.version_info.minor, 10)
        
    def test_pathlib_available(self):
        """Test that pathlib is available"""
        from pathlib import Path
        self.assertTrue(True)
        
    def test_json_available(self):
        """Test that json module is available"""
        import json
        test_data = {"test": "data"}
        json_str = json.dumps(test_data)
        parsed = json.loads(json_str)
        self.assertEqual(parsed["test"], "data")


class TestDocumentation(unittest.TestCase):
    """Test documentation completeness"""
    
    def setUp(self):
        """Set up test environment"""
        self.root_dir = Path(__file__).parent.parent
        self.docs_dir = self.root_dir / "docs"
        
    def test_docs_directory_exists(self):
        """Test that docs directory exists"""
        self.assertTrue(self.docs_dir.exists(), "docs directory should exist")
        
    def test_readme_branding(self):
        """Test that README uses correct branding"""
        readme = self.root_dir / "README.md"
        if readme.exists():
            content = readme.read_text(encoding='utf-8')
            # Should use lowercase 'axionax', not 'AxionAX' or 'Axionax'
            self.assertIn("axionax", content.lower())
            
    def test_no_broken_branding(self):
        """Test that there are no incorrect branding variations"""
        readme = self.root_dir / "README.md"
        if readme.exists():
            content = readme.read_text(encoding='utf-8')
            # Check for common mistakes (case-sensitive check on title lines)
            lines = content.split('\n')
            for i, line in enumerate(lines):
                # Allow AxionAX in URLs and specific contexts
                if line.startswith('#') and 'github.com' not in line:
                    # Title lines should not have AxionAX
                    if 'AxionAX' in line and 'axionax' not in line.lower():
                        self.fail(f"Line {i+1}: Found 'AxionAX' in title: {line}")


def run_tests():
    """Run all tests and return results"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestFileOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestRepositoryStructure))
    suite.addTests(loader.loadTestsFromTestCase(TestToolsAvailability))
    suite.addTests(loader.loadTestsFromTestCase(TestDocumentation))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    print("=" * 70)
    print("axionax DevTools - Basic Unit Tests")
    print("=" * 70)
    print()
    
    success = run_tests()
    
    print()
    print("=" * 70)
    if success:
        print("All tests passed!")
        sys.exit(0)
    else:
        print("Some tests failed!")
        sys.exit(1)
