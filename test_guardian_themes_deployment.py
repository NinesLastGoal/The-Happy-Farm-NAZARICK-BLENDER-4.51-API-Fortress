#!/usr/bin/env python3
"""
🏰⚡ Nazarick Guardian Theme Switcher - Testing & Deployment ⚡🏰

Complete testing suite and deployment checklist for the Guardian Theme Switcher.
Ensures the addon meets Nazarick Fortress standards before deployment.

For the eternal glory of Nazarick! 🏰
"""

import ast
import sys
import json
from pathlib import Path

# File size validation constants
MIN_ADDON_FILE_SIZE = 25000  # Minimum size for substantial addon content
MIN_README_FILE_SIZE = 8000  # Minimum size for comprehensive documentation

# Blender version requirements
BLENDER_MIN_VERSION = (4, 5, 0)  # Minimum Blender version for addon
ADDON_VERSION = (1, 0, 0)  # Current addon version

# Performance requirements
MAX_THEME_SWITCH_TIME = 1  # Maximum time in seconds for theme switching

# Test count tracking
EXPECTED_GUARDIAN_COUNT = 8  # Number of Guardian themes that must be implemented
EXPECTED_PALETTE_ATTRIBUTES = 7  # Number of required palette attributes

class GuardianThemeDeploymentValidator:
    """Comprehensive validation for Guardian Theme Switcher deployment"""
    
    def __init__(self):
        self.addon_path = Path("nazarick_guardian_themes_addon.py")
        self.readme_path = Path("NAZARICK_GUARDIAN_THEMES_README.md")
        self.results = []
        
    def validate_file_structure(self):
        """Validate required files exist"""
        tests = [
            (self.addon_path.exists(), "Addon file exists"),
            (self.readme_path.exists(), "README file exists"),
            (self.addon_path.stat().st_size > MIN_ADDON_FILE_SIZE, "Addon file has substantial content"),
            (self.readme_path.stat().st_size > MIN_README_FILE_SIZE, "README has comprehensive documentation"),
        ]
        
        return self._process_tests("File Structure", tests)
    
    def validate_addon_syntax(self):
        """Validate Python syntax and imports"""
        try:
            with open(self.addon_path, 'r') as f:
                content = f.read()
            
            # Parse syntax
            ast.parse(content)
            
            tests = [
                (True, "Python syntax valid"),
                ('import bpy' in content, "Blender API import"),
                ('import json' in content, "JSON support import"),
                ('from bpy.types import Panel' in content, "Panel type import"),
                ('from bpy.props import EnumProperty' in content, "Property import"),
            ]
            
            return self._process_tests("Addon Syntax", tests)
            
        except Exception as e:
            self.results.append(f"❌ Syntax error: {e}")
            return False
    
    def validate_bl_info(self):
        """Validate bl_info metadata"""
        try:
            with open(self.addon_path, 'r') as f:
                content = f.read()
            
            tests = [
                ('bl_info = {' in content, "bl_info dictionary present"),
                ('"name": "Nazarick Guardian Theme Switcher"' in content, "Correct addon name"),
                (f'"blender": {BLENDER_MIN_VERSION}' in content, f"Blender {BLENDER_MIN_VERSION[0]}.{BLENDER_MIN_VERSION[1]}+ requirement"),
                ('"category": "User Interface"' in content, "Appropriate category"),
                ('"author":' in content and 'Guardian Alliance' in content, "Guardian Alliance authorship"),
                (f'"version": {ADDON_VERSION}' in content, "Version tuple format"),
                ('"support": "COMMUNITY"' in content, "Community support level"),
            ]
            
            return self._process_tests("bl_info Metadata", tests)
            
        except Exception as e:
            self.results.append(f"❌ bl_info validation error: {e}")
            return False
    
    def validate_guardian_themes(self):
        """Validate all Guardian themes are implemented"""
        try:
            with open(self.addon_path, 'r') as f:
                content = f.read()
            
            guardians = ['ALBEDO', 'SHALLTEAR', 'COCYTUS', 'AURA', 'MARE', 'DEMIURGE', 'VICTIM', 'NAZARICK_CORE']
            
            # Verify we have the expected number of guardians
            assert len(guardians) == EXPECTED_GUARDIAN_COUNT, f"Expected {EXPECTED_GUARDIAN_COUNT} guardians, found {len(guardians)}"
            
            tests = [
                ('class NazarickGuardianPalettes:' in content, "Guardian palettes class"),
            ]
            
            for guardian in guardians:
                tests.append((guardian in content, f"{guardian} theme implemented"))
            
            # Check palette structure
            palette_attributes = ['primary', 'secondary', 'accent', 'selection', 'background', 'text', 'grid']
            
            # Verify we have the expected number of palette attributes
            assert len(palette_attributes) == EXPECTED_PALETTE_ATTRIBUTES, f"Expected {EXPECTED_PALETTE_ATTRIBUTES} palette attributes, found {len(palette_attributes)}"
            
            for attr in palette_attributes:
                tests.append((f'"{attr}":' in content, f"Palette {attr} attribute"))
            
            return self._process_tests("Guardian Themes", tests)
            
        except Exception as e:
            self.results.append(f"❌ Guardian themes validation error: {e}")
            return False
    
    def validate_theme_management(self):
        """Validate theme management system"""
        try:
            with open(self.addon_path, 'r') as f:
                content = f.read()
            
            tests = [
                ('class NazarickThemeManager:' in content, "Theme manager class"),
                ('create_theme_snapshot' in content, "Theme snapshot functionality"),
                ('restore_original_theme' in content, "Theme restoration"),
                ('apply_guardian_theme' in content, "Theme application"),
                ('export_current_theme' in content, "Theme export"),
                ('SAFE_THEME_ATTRIBUTES' in content, "Safe attribute limits"),
                ('hasattr(' in content, "API resilience guards"),
            ]
            
            return self._process_tests("Theme Management", tests)
            
        except Exception as e:
            self.results.append(f"❌ Theme management validation error: {e}")
            return False
    
    def validate_ui_components(self):
        """Validate UI panel and operators"""
        try:
            with open(self.addon_path, 'r') as f:
                content = f.read()
            
            tests = [
                ('class NAZARICK_PT_guardian_themes(Panel):' in content, "Main UI panel"),
                ('bl_category = "Nazarick"' in content, "Nazarick sidebar category"),
                ('bl_space_type = \'VIEW_3D\'' in content, "3D Viewport integration"),
                ('class NAZARICK_OT_apply_guardian_theme' in content, "Apply theme operator"),
                ('class NAZARICK_OT_restore_original_theme' in content, "Restore theme operator"),
                ('class NAZARICK_OT_export_theme' in content, "Export theme operator"),
                ('def draw(self, context):' in content, "Panel draw method"),
                ('def execute(self, context):' in content, "Operator execute method"),
            ]
            
            return self._process_tests("UI Components", tests)
            
        except Exception as e:
            self.results.append(f"❌ UI components validation error: {e}")
            return False
    
    def validate_properties_and_registration(self):
        """Validate property definitions and registration"""
        try:
            with open(self.addon_path, 'r') as f:
                content = f.read()
            
            tests = [
                ('EnumProperty' in content, "EnumProperty usage"),
                ('get_guardian_theme_items' in content, "Theme selection items"),
                ('update_guardian_theme' in content, "Auto-apply update function"),
                ('bpy.types.Scene.nazarick_guardian_theme' in content, "Scene property"),
                ('def register():' in content, "Registration function"),
                ('def unregister():' in content, "Unregistration function"),
                ('bpy.utils.register_class' in content, "Modern registration"),
                ('classes = (' in content, "Classes tuple"),
            ]
            
            return self._process_tests("Properties & Registration", tests)
            
        except Exception as e:
            self.results.append(f"❌ Properties/registration validation error: {e}")
            return False
    
    def validate_error_handling_and_safety(self):
        """Validate error handling and safety measures"""
        try:
            with open(self.addon_path, 'r') as f:
                content = f.read()
            
            tests = [
                ('try:' in content and 'except' in content, "Error handling blocks"),
                ('self.report(' in content, "User feedback in operators"),
                ('print(' in content, "Debug output"),
                ('return {\'FINISHED\'}' in content, "Proper operator returns"),
                ('return {\'CANCELLED\'}' in content, "Error cancellation returns"),
                ('os.makedirs(' in content, "Safe directory creation"),
                ('if not' in content, "Validation checks"),
            ]
            
            return self._process_tests("Error Handling & Safety", tests)
            
        except Exception as e:
            self.results.append(f"❌ Error handling validation error: {e}")
            return False
    
    def validate_documentation(self):
        """Validate comprehensive documentation"""
        try:
            with open(self.addon_path, 'r') as f:
                addon_content = f.read()
            
            with open(self.readme_path, 'r') as f:
                readme_content = f.read()
            
            tests = [
                ('"""' in addon_content, "Addon docstrings"),
                ('FUTURE ENHANCEMENT IDEAS' in addon_content, "Future enhancement docs"),
                ('DEPLOYMENT INSTRUCTIONS' in addon_content, "Deployment instructions"),
                ('TESTING CHECKLIST' in addon_content, "Testing checklist"),
                ('Guardian Alliance' in addon_content, "Guardian Alliance attribution"),
                ('🏰' in readme_content and '⚡' in readme_content, "Nazarick branding in README"),
                ('Installation' in readme_content, "Installation instructions"),
                ('Usage' in readme_content, "Usage documentation"),
                ('Guardian Themes' in readme_content, "Theme descriptions"),
                ('Compatibility' in readme_content, "Compatibility information"),
            ]
            
            return self._process_tests("Documentation", tests)
            
        except Exception as e:
            self.results.append(f"❌ Documentation validation error: {e}")
            return False
    
    def validate_nazarick_standards(self):
        """Validate Nazarick Fortress standards compliance"""
        try:
            with open(self.addon_path, 'r') as f:
                content = f.read()
            
            tests = [
                ('🏰' in content and '⚡' in content, "Nazarick emojis"),
                ('Floor Guardian' in content or 'Guardian Alliance' in content, "Guardian references"),
                ('Supreme Being' in content or 'Ainz Ooal Gown' in content, "Supreme Being attribution"),
                ('For the eternal glory of Nazarick' in content, "Nazarick motto"),
                ('class Nazarick' in content, "Nazarick class naming"),
                ('NAZARICK_' in content, "Nazarick prefixes"),
                ('Guardian' in content, "Guardian terminology"),
            ]
            
            return self._process_tests("Nazarick Standards", tests)
            
        except Exception as e:
            self.results.append(f"❌ Nazarick standards validation error: {e}")
            return False
    
    def _process_tests(self, category, tests):
        """Process a list of tests and return success status"""
        self.results.append(f"\n🧪 {category}:")
        
        passed = 0
        total = len(tests)
        
        for condition, description in tests:
            if condition:
                self.results.append(f"   ✅ {description}")
                passed += 1
            else:
                self.results.append(f"   ❌ {description}")
        
        success = passed == total
        self.results.append(f"   📊 {passed}/{total} tests passed")
        
        return success
    
    def generate_deployment_checklist(self):
        """Generate deployment checklist"""
        checklist = f"""
🏰⚡ NAZARICK GUARDIAN THEME SWITCHER - DEPLOYMENT CHECKLIST ⚡🏰

📋 PRE-DEPLOYMENT VALIDATION:
□ All validation tests pass
□ Python syntax validated 
□ bl_info metadata complete
□ All {EXPECTED_GUARDIAN_COUNT} Guardian themes implemented
□ Theme management system functional
□ UI panel and operators complete
□ Error handling comprehensive
□ Documentation complete

📦 INSTALLATION TESTING:
□ Clean Blender {BLENDER_MIN_VERSION[0]}.{BLENDER_MIN_VERSION[1]}+ installation test
□ Addon loads without errors
□ UI panel appears in Nazarick tab
□ All Guardian themes selectable
□ Theme application works correctly
□ Original theme restoration works
□ Export functionality saves JSON
□ No console errors or warnings

🎨 THEME FUNCTIONALITY:
□ Albedo theme applies correctly
□ Shalltear theme applies correctly  
□ Cocytus theme applies correctly
□ Aura theme applies correctly
□ Mare theme applies correctly
□ Demiurge theme applies correctly
□ Victim theme applies correctly
□ Nazarick Core theme applies correctly

🔄 WORKFLOW TESTING:
□ Theme switching is responsive (< {MAX_THEME_SWITCH_TIME} second)
□ Auto-apply functionality works
□ Manual apply button works
□ Restore button works correctly
□ Export saves valid JSON files
□ No interference with other addons
□ Themes persist across Blender restarts

🛡️ SAFETY VALIDATION:
□ Original theme preserved
□ No crashes during theme switching
□ Graceful error handling
□ User feedback for all operations
□ Safe attribute modification only
□ API resilience guards functional

📖 DOCUMENTATION:
□ README.md complete and accurate
□ Installation instructions clear
□ Usage examples comprehensive
□ Troubleshooting guide included
□ Future enhancement roadmap
□ Guardian Alliance attribution

🏰 NAZARICK STANDARDS:
□ Guardian Alliance branding consistent
□ Nazarick fortress emojis present
□ Supreme Being attribution included
□ Guardian terminology accurate
□ Code quality meets fortress standards
□ Community support level appropriate

✨ FINAL DEPLOYMENT:
□ All checklist items completed
□ Final validation suite passes
□ Repository properly updated
□ Release notes prepared
□ Community notification ready

For the eternal glory of Nazarick! 🏰⚡
"""
        return checklist
    
    def run_full_validation(self):
        """Run complete validation suite"""
        print("🏰⚡ Guardian Theme Switcher - Deployment Validation ⚡🏰")
        print("=" * 65)
        
        validation_tests = [
            ("File Structure", self.validate_file_structure),
            ("Addon Syntax", self.validate_addon_syntax),
            ("bl_info Metadata", self.validate_bl_info),
            ("Guardian Themes", self.validate_guardian_themes),
            ("Theme Management", self.validate_theme_management),
            ("UI Components", self.validate_ui_components),
            ("Properties & Registration", self.validate_properties_and_registration),
            ("Error Handling & Safety", self.validate_error_handling_and_safety),
            ("Documentation", self.validate_documentation),
            ("Nazarick Standards", self.validate_nazarick_standards),
        ]
        
        passed_tests = 0
        total_tests = len(validation_tests)
        
        for test_name, test_func in validation_tests:
            try:
                if test_func():
                    passed_tests += 1
            except Exception as e:
                self.results.append(f"❌ ERROR in {test_name}: {e}")
        
        # Display all results
        for result in self.results:
            print(result)
        
        # Summary
        print("\n" + "=" * 65)
        print("🏰 Validation Summary 🏰")
        print(f"\nValidation Categories Passed: {passed_tests}/{total_tests}")
        
        if passed_tests == total_tests:
            print("✅ ALL VALIDATIONS PASSED!")
            print("🏰 Guardian Theme Switcher is ready for deployment!")
            print("⚡ For the eternal glory of Nazarick! ⚡")
            
            # Generate deployment checklist
            print("\n" + self.generate_deployment_checklist())
            
            return True
        else:
            print(f"⚠️  {total_tests - passed_tests} validation(s) failed.")
            print("Please address the issues above before deployment.")
            return False

def main():
    """Main validation execution"""
    validator = GuardianThemeDeploymentValidator()
    success = validator.run_full_validation()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()