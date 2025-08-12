#!/usr/bin/env python3
"""
🏰⚡ NAZARICK BLENDER ADDON COMPLIANCE VALIDATOR ⚡🏰

Supreme Overlord's Automated Tool for Addon Quality Assurance

This tool validates Blender addons against the Nazarick Fortress specifications
to ensure legendary quality standards are maintained.
"""

import os
import sys
import ast
import re
import zipfile
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional


class AddonComplianceValidator:
    """
    Comprehensive validator for Blender addon compliance with Nazarick standards.
    """
    
    def __init__(self):
        self.results = {
            'passed': [],
            'warnings': [],
            'errors': [],
            'score': 0,
            'max_score': 0
        }
        
        # Valid Blender categories from specifications
        self.valid_categories = {
            "3D View", "Add Mesh", "Animation", "Development", "Game Engine",
            "Import-Export", "Mesh", "Material", "Object", "Render", "Rigging",
            "Sculpting", "Sequencer", "System", "Text Editor", "UV", "User Interface"
        }
        
        # Valid support levels
        self.valid_support_levels = {"COMMUNITY", "OFFICIAL", "TESTING"}
        
    def validate_addon(self, addon_path: str) -> Dict[str, Any]:
        """
        Validate an addon against Nazarick specifications.
        
        Args:
            addon_path: Path to addon file (.py) or directory
            
        Returns:
            Dict containing validation results
        """
        self.results = {
            'passed': [],
            'warnings': [],
            'errors': [],
            'score': 0,
            'max_score': 0
        }
        
        addon_path = Path(addon_path)
        
        if not addon_path.exists():
            self._add_error(f"Addon path does not exist: {addon_path}")
            return self.results
            
        # Handle ZIP files
        if addon_path.suffix.lower() == '.zip':
            return self._validate_zip_addon(addon_path)
        
        # Handle directories
        elif addon_path.is_dir():
            return self._validate_directory_addon(addon_path)
            
        # Handle single Python files
        elif addon_path.suffix.lower() == '.py':
            return self._validate_single_file_addon(addon_path)
            
        else:
            self._add_error(f"Unsupported addon format: {addon_path}")
            return self.results
    
    def _validate_zip_addon(self, zip_path: Path) -> Dict[str, Any]:
        """Validate a ZIP-packaged addon."""
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                with zipfile.ZipFile(zip_path, 'r') as zip_file:
                    zip_file.extractall(temp_dir)
                
                # Check ZIP structure
                self._validate_zip_structure(temp_dir, zip_path.stem)
                
                # Find and validate the main addon
                addon_dir = Path(temp_dir)
                extracted_items = list(addon_dir.iterdir())
                
                if len(extracted_items) == 1 and extracted_items[0].is_dir():
                    # Multi-file addon
                    return self._validate_directory_addon(extracted_items[0])
                elif len(extracted_items) == 1 and extracted_items[0].suffix == '.py':
                    # Single file addon
                    return self._validate_single_file_addon(extracted_items[0])
                else:
                    self._add_error("Invalid ZIP structure - should contain single addon folder or Python file")
                    
        except Exception as e:
            self._add_error(f"Failed to process ZIP file: {e}")
            
        return self.results
    
    def _validate_zip_structure(self, temp_dir: str, expected_name: str):
        """Validate ZIP file structure requirements."""
        self._add_test("ZIP Structure Validation")
        
        temp_path = Path(temp_dir)
        items = list(temp_path.iterdir())
        
        # Should contain exactly one item
        if len(items) != 1:
            self._add_error(f"ZIP should contain exactly one item, found {len(items)}")
            return
            
        item = items[0]
        
        # Check naming convention
        if item.is_dir():
            if item.name != expected_name:
                self._add_warning(f"Directory name '{item.name}' doesn't match ZIP name '{expected_name}'")
            
            # Check for __init__.py
            init_file = item / "__init__.py"
            if not init_file.exists():
                self._add_error("Multi-file addon missing __init__.py")
            else:
                self._add_passed("Found required __init__.py")
        
        elif item.suffix == '.py':
            if item.stem != expected_name:
                self._add_warning(f"Python file name '{item.stem}' doesn't match ZIP name '{expected_name}'")
        
        # Check for hidden/unwanted files
        unwanted_patterns = ['.DS_Store', '__pycache__', '*.pyc', '.git', '.svn']
        for pattern in unwanted_patterns:
            if any(temp_path.glob(f"**/{pattern}")):
                self._add_warning(f"ZIP contains unwanted files matching '{pattern}'")
    
    def _validate_directory_addon(self, addon_dir: Path) -> Dict[str, Any]:
        """Validate a directory-based addon."""
        self._add_test("Directory Addon Validation")
        
        # Check for __init__.py
        init_file = addon_dir / "__init__.py"
        if not init_file.exists():
            self._add_error("Multi-file addon missing __init__.py")
            return self.results
        
        self._add_passed("Found required __init__.py")
        
        # Validate the main __init__.py file
        self._validate_python_file(init_file, is_main=True)
        
        # Check file structure
        self._validate_file_structure(addon_dir)
        
        # Validate additional Python files
        for py_file in addon_dir.glob("*.py"):
            if py_file.name != "__init__.py":
                self._validate_python_file(py_file, is_main=False)
        
        return self.results
    
    def _validate_single_file_addon(self, addon_file: Path) -> Dict[str, Any]:
        """Validate a single-file addon."""
        self._add_test("Single File Addon Validation")
        
        if not addon_file.exists():
            self._add_error(f"Addon file does not exist: {addon_file}")
            return self.results
            
        self._validate_python_file(addon_file, is_main=True)
        return self.results
    
    def _validate_file_structure(self, addon_dir: Path):
        """Validate addon directory structure."""
        self._add_test("File Structure Validation")
        
        # Check naming convention (lowercase, underscores only)
        dir_name = addon_dir.name
        if not re.match(r'^[a-z][a-z0-9_]*$', dir_name):
            self._add_error(f"Directory name '{dir_name}' should be lowercase with underscores only")
        else:
            self._add_passed(f"Directory name '{dir_name}' follows naming convention")
        
        # Check for recommended files
        recommended_files = ['README.md', 'operators.py', 'panels.py']
        for rec_file in recommended_files:
            if (addon_dir / rec_file).exists():
                self._add_passed(f"Found recommended file: {rec_file}")
        
        # Check for unwanted files
        unwanted_patterns = ['.DS_Store', '__pycache__', '*.pyc']
        for pattern in unwanted_patterns:
            if list(addon_dir.glob(pattern)):
                self._add_warning(f"Found unwanted files matching '{pattern}'")
    
    def _validate_python_file(self, py_file: Path, is_main: bool = False):
        """Validate a Python file for compliance."""
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse the AST
            tree = ast.parse(content)
            
            if is_main:
                self._validate_bl_info(tree, py_file)
                self._validate_registration_functions(tree, content)
            
            self._validate_code_quality(tree, content, py_file)
            
        except SyntaxError as e:
            self._add_error(f"Syntax error in {py_file}: {e}")
        except Exception as e:
            self._add_error(f"Failed to validate {py_file}: {e}")
    
    def _validate_bl_info(self, tree: ast.AST, file_path: Path):
        """Validate bl_info dictionary compliance."""
        self._add_test("bl_info Dictionary Validation")
        
        bl_info = None
        
        # Find bl_info assignment
        for node in ast.walk(tree):
            if (isinstance(node, ast.Assign) and 
                len(node.targets) == 1 and
                isinstance(node.targets[0], ast.Name) and
                node.targets[0].id == 'bl_info'):
                bl_info = node.value
                break
        
        if not bl_info:
            self._add_error("Missing bl_info dictionary")
            return
        
        if not isinstance(bl_info, ast.Dict):
            self._add_error("bl_info must be a dictionary")
            return
        
        self._add_passed("Found bl_info dictionary")
        
        # Extract bl_info data
        bl_info_data = {}
        try:
            for key, value in zip(bl_info.keys, bl_info.values):
                if isinstance(key, ast.Constant):
                    key_name = key.value
                elif isinstance(key, ast.Str):  # Python < 3.8 compatibility
                    key_name = key.s
                else:
                    continue
                
                if isinstance(value, ast.Constant):
                    bl_info_data[key_name] = value.value
                elif isinstance(value, ast.Str):
                    bl_info_data[key_name] = value.s
                elif isinstance(value, ast.Tuple):
                    # Handle version tuple
                    tuple_values = []
                    for elt in value.elts:
                        if isinstance(elt, ast.Constant):
                            tuple_values.append(elt.value)
                        elif isinstance(elt, ast.Num):  # Python < 3.8 compatibility
                            tuple_values.append(elt.n)
                    bl_info_data[key_name] = tuple(tuple_values)
        
        except Exception as e:
            self._add_error(f"Failed to parse bl_info: {e}")
            return
        
        # Validate required fields
        required_fields = ["name", "author", "version", "blender", "location", "description", "category"]
        
        for field in required_fields:
            if field not in bl_info_data:
                self._add_error(f"Missing required bl_info field: {field}")
            else:
                self._add_passed(f"Found required field: {field}")
        
        # Validate field values
        self._validate_bl_info_fields(bl_info_data)
    
    def _validate_bl_info_fields(self, bl_info_data: Dict[str, Any]):
        """Validate individual bl_info field values."""
        
        # Validate name
        if "name" in bl_info_data:
            name = bl_info_data["name"]
            if not isinstance(name, str) or not (3 <= len(name) <= 50):
                self._add_error("bl_info['name'] must be 3-50 characters")
            elif not re.match(r'^[a-zA-Z0-9\s\-_/().]+$', name):
                self._add_error("bl_info['name'] contains invalid characters")
            else:
                self._add_passed(f"Valid addon name: '{name}'")
        
        # Validate version
        if "version" in bl_info_data:
            version = bl_info_data["version"]
            if not isinstance(version, tuple) or len(version) != 3:
                self._add_error("bl_info['version'] must be a tuple of 3 integers")
            elif not all(isinstance(v, int) and v >= 0 for v in version):
                self._add_error("bl_info['version'] must contain non-negative integers")
            else:
                self._add_passed(f"Valid version: {version}")
        
        # Validate Blender version
        if "blender" in bl_info_data:
            blender_version = bl_info_data["blender"]
            if not isinstance(blender_version, tuple) or len(blender_version) != 3:
                self._add_error("bl_info['blender'] must be a tuple of 3 integers")
            elif blender_version < (4, 5, 0):
                self._add_error("bl_info['blender'] must be (4, 5, 0) or higher for this fortress")
            else:
                self._add_passed(f"Valid Blender version requirement: {blender_version}")
        
        # Validate description
        if "description" in bl_info_data:
            desc = bl_info_data["description"]
            if not isinstance(desc, str) or not (10 <= len(desc) <= 200):
                self._add_error("bl_info['description'] must be 10-200 characters")
            else:
                self._add_passed(f"Valid description length: {len(desc)} characters")
        
        # Validate category
        if "category" in bl_info_data:
            category = bl_info_data["category"]
            if category not in self.valid_categories:
                self._add_error(f"bl_info['category'] '{category}' is not a valid Blender category")
            else:
                self._add_passed(f"Valid category: '{category}'")
        
        # Validate support level
        if "support" in bl_info_data:
            support = bl_info_data["support"]
            if support not in self.valid_support_levels:
                self._add_error(f"bl_info['support'] '{support}' must be one of: {self.valid_support_levels}")
            else:
                self._add_passed(f"Valid support level: '{support}'")
    
    def _validate_registration_functions(self, tree: ast.AST, content: str):
        """Validate register/unregister functions."""
        self._add_test("Registration Functions Validation")
        
        functions = {}
        
        # Find function definitions
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions[node.name] = node
        
        # Check for required functions
        if 'register' not in functions:
            self._add_error("Missing register() function")
        else:
            self._add_passed("Found register() function")
            
        if 'unregister' not in functions:
            self._add_error("Missing unregister() function")
        else:
            self._add_passed("Found unregister() function")
        
        # Check for classes tuple
        if 'classes' in content or 'CLASSES' in content:
            self._add_passed("Found classes collection for registration")
        
        # Check for __main__ block
        if 'if __name__ == "__main__":' in content:
            self._add_passed("Found __main__ testing block")
        else:
            self._add_warning("Missing __main__ testing block (recommended)")
    
    def _validate_code_quality(self, tree: ast.AST, content: str, file_path: Path):
        """Validate code quality standards."""
        self._add_test(f"Code Quality Validation ({file_path.name})")
        
        # Check for classes with proper naming
        class_count = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_count += 1
                
                # Check bl_idname and bl_label for Blender classes
                if any(base.id in ['Operator', 'Panel', 'PropertyGroup'] 
                      for base in node.bases if isinstance(base, ast.Name)):
                    
                    has_bl_idname = False
                    has_bl_label = False
                    
                    for item in node.body:
                        if isinstance(item, ast.Assign):
                            for target in item.targets:
                                if isinstance(target, ast.Name):
                                    if target.id == 'bl_idname':
                                        has_bl_idname = True
                                    elif target.id == 'bl_label':
                                        has_bl_label = True
                    
                    if not has_bl_idname:
                        self._add_error(f"Class {node.name} missing bl_idname")
                    if not has_bl_label:
                        self._add_error(f"Class {node.name} missing bl_label")
                    
                    if has_bl_idname and has_bl_label:
                        self._add_passed(f"Class {node.name} has required bl_idname and bl_label")
        
        if class_count > 0:
            self._add_passed(f"Found {class_count} class definitions")
        
        # Check for basic error handling patterns
        if 'try:' in content and 'except' in content:
            self._add_passed("Found error handling (try/except blocks)")
        else:
            self._add_warning("No error handling found (recommended)")
        
        # Check for docstrings
        docstring_count = content.count('"""') + content.count("'''")
        if docstring_count >= 2:  # At least one docstring pair
            self._add_passed("Found documentation strings")
        else:
            self._add_warning("Limited documentation (consider adding docstrings)")
    
    def _add_test(self, test_name: str):
        """Start a new test category."""
        pass  # Just for organization
    
    def _add_passed(self, message: str):
        """Add a passed validation."""
        self.results['passed'].append(message)
        self.results['score'] += 1
        self.results['max_score'] += 1
    
    def _add_warning(self, message: str):
        """Add a warning (non-critical issue)."""
        self.results['warnings'].append(message)
        self.results['max_score'] += 1
    
    def _add_error(self, message: str):
        """Add an error (critical issue)."""
        self.results['errors'].append(message)
        self.results['max_score'] += 1
    
    def generate_report(self) -> str:
        """Generate a comprehensive validation report."""
        total_tests = len(self.results['passed']) + len(self.results['warnings']) + len(self.results['errors'])
        
        if total_tests == 0:
            return "No validation tests were performed."
        
        success_rate = (self.results['score'] / self.results['max_score']) * 100 if self.results['max_score'] > 0 else 0
        
        report = []
        report.append("🏰⚡ NAZARICK ADDON VALIDATION REPORT ⚡🏰")
        report.append("=" * 50)
        report.append(f"Overall Score: {self.results['score']}/{self.results['max_score']} ({success_rate:.1f}%)")
        report.append("")
        
        # Status determination
        if success_rate >= 95:
            status = "✅ READY FOR PRODUCTION"
            status_desc = "Meets legendary Nazarick standards!"
        elif success_rate >= 80:
            status = "⚠️ MINOR ISSUES"
            status_desc = "Review recommended before deployment"
        else:
            status = "❌ NOT READY"
            status_desc = "Critical issues must be resolved"
        
        report.append(f"Status: {status}")
        report.append(f"Assessment: {status_desc}")
        report.append("")
        
        # Passed tests
        if self.results['passed']:
            report.append(f"✅ PASSED TESTS ({len(self.results['passed'])}):")
            for test in self.results['passed']:
                report.append(f"  • {test}")
            report.append("")
        
        # Warnings
        if self.results['warnings']:
            report.append(f"⚠️ WARNINGS ({len(self.results['warnings'])}):")
            for warning in self.results['warnings']:
                report.append(f"  • {warning}")
            report.append("")
        
        # Errors
        if self.results['errors']:
            report.append(f"❌ ERRORS ({len(self.results['errors'])}):")
            for error in self.results['errors']:
                report.append(f"  • {error}")
            report.append("")
        
        report.append("📋 RECOMMENDATIONS:")
        if success_rate >= 95:
            report.append("  • Addon meets all requirements for production deployment")
        elif success_rate >= 80:
            report.append("  • Address warnings to improve quality")
            report.append("  • Consider additional testing")
        else:
            report.append("  • CRITICAL: Fix all errors before deployment")
            report.append("  • Review Blender addon specifications")
            report.append("  • Test thoroughly in Blender environment")
        
        report.append("")
        report.append("For detailed specifications, see:")
        report.append("docs/BLENDER_ADDON_SPECIFICATIONS.md")
        
        return "\n".join(report)


def main():
    """Main CLI interface for addon validation."""
    if len(sys.argv) != 2:
        print("🏰⚡ NAZARICK ADDON COMPLIANCE VALIDATOR ⚡🏰")
        print("Usage: python validate_addon_compliance.py <addon_path>")
        print("       addon_path: Path to .py file, addon directory, or .zip file")
        sys.exit(1)
    
    addon_path = sys.argv[1]
    validator = AddonComplianceValidator()
    
    print("🏰 Validating addon against Nazarick specifications...")
    print(f"Target: {addon_path}")
    print()
    
    results = validator.validate_addon(addon_path)
    report = validator.generate_report()
    
    print(report)
    
    # Exit with appropriate code
    success_rate = (results['score'] / results['max_score']) * 100 if results['max_score'] > 0 else 0
    if success_rate >= 95:
        sys.exit(0)  # Success
    elif success_rate >= 80:
        sys.exit(1)  # Warnings
    else:
        sys.exit(2)  # Errors


if __name__ == "__main__":
    main()