#!/usr/bin/env python3
"""
🏰 Demiurge Village Addon Testing Suite 🏰

Comprehensive testing for all modernized Blender addons in the demiurge_village:
- Nines Shapekey Oversight Fixer (modernized)
- UV Total Ratio Compare (modernized) 
- Nazarick Stitch Tool (new)

Architected by Demiurge for the Great Tomb of Nazarick
"""

import unittest
import ast
import os
import sys
import time
from unittest.mock import Mock, MagicMock, patch


class MockBpy:
    """Mock Blender Python API for testing"""
    def __init__(self):
        self.types = Mock()
        self.types.Operator = type('Operator', (), {})
        self.types.Panel = type('Panel', (), {})
        self.types.Scene = type('Scene', (), {})
        
        self.props = Mock()
        self.props.BoolProperty = Mock(return_value=Mock())
        self.props.IntProperty = Mock(return_value=Mock())
        self.props.FloatProperty = Mock(return_value=Mock())
        self.props.StringProperty = Mock(return_value=Mock())
        self.props.EnumProperty = Mock(return_value=Mock())
        
        self.utils = Mock()
        self.utils.register_class = Mock()
        self.utils.unregister_class = Mock()
        
        self.context = Mock()
        self.context.active_object = Mock()
        self.context.selected_objects = []
        self.context.scene = Mock()
        self.context.view_layer = Mock()
        
        self.data = Mock()
        self.ops = Mock()


class MockBmesh:
    """Mock bmesh module for testing"""
    def __init__(self):
        self.from_edit_mesh = Mock()
        self.update_edit_mesh = Mock()
        self.ops = Mock()


class MockMathutils:
    """Mock mathutils module for testing"""
    class Vector:
        def __init__(self, coords):
            self.x, self.y, self.z = coords if len(coords) >= 3 else (coords + [0, 0])[:3]
            
        def __sub__(self, other):
            return MockMathutils.Vector([self.x - other.x, self.y - other.y, self.z - other.z])
            
        def cross(self, other):
            return MockMathutils.Vector([0, 0, 1])  # Simplified
            
        def normalized(self):
            return self
            
        @property
        def length(self):
            return 1.0
    
    Matrix = Mock()


# Mock Blender modules globally
sys.modules['bpy'] = MockBpy()
sys.modules['bmesh'] = MockBmesh()
sys.modules['mathutils'] = MockMathutils()


class TestDemiurgeVillageStructure(unittest.TestCase):
    """Test the structure and organization of the demiurge_village"""
    
    def setUp(self):
        self.village_path = "demiurge_village"
        
    def test_village_directory_exists(self):
        """Test that the demiurge_village directory exists"""
        self.assertTrue(os.path.exists(self.village_path), 
                       "demiurge_village directory should exist")
        
    def test_required_addons_present(self):
        """Test that all required addon files are present"""
        required_files = [
            "nines_shapekey_oversight_fixer.py",
            "uv_total_ratio_compare_modernized.py", 
            "nazarick_stitch_tool.py"
        ]
        
        for file_name in required_files:
            file_path = os.path.join(self.village_path, file_name)
            self.assertTrue(os.path.exists(file_path), 
                          f"Required addon file {file_name} should exist in demiurge_village")


class TestShapekeyAddonModernization(unittest.TestCase):
    """Test the modernized Nines Shapekey Oversight Fixer addon"""
    
    def setUp(self):
        self.addon_path = os.path.join("demiurge_village", "nines_shapekey_oversight_fixer.py")
        with open(self.addon_path, 'r') as f:
            self.addon_code = f.read()
        self.addon_ast = ast.parse(self.addon_code)
        
    def test_python_syntax_valid(self):
        """Test that the shapekey addon has valid Python syntax"""
        try:
            compile(self.addon_code, self.addon_path, 'exec')
        except SyntaxError as e:
            self.fail(f"Syntax error in shapekey addon: {e}")
            
    def test_bl_info_structure(self):
        """Test that bl_info is properly structured for Blender 4.5"""
        self.assertIn("bl_info", self.addon_code)
        
        # Check required bl_info fields
        required_fields = ["name", "author", "version", "blender", "location", "description", "category"]
        for field in required_fields:
            self.assertIn(f'"{field}"', self.addon_code, 
                         f"bl_info should contain {field} field")
                         
        # Check Blender version requirement
        self.assertIn("(4, 5, 0)", self.addon_code, 
                     "Should require Blender 4.5.0 or newer")
                     
    def test_modern_api_usage(self):
        """Test that the addon uses modern Blender 4.5 API patterns"""
        # Should use modern operator base class
        self.assertIn("bpy.types.Operator", self.addon_code)
        self.assertIn("bpy.types.Panel", self.addon_code)
        
        # Should use modern property definitions  
        has_props = ("bpy.props." in self.addon_code or 
                    "from bpy.props import" in self.addon_code)
        self.assertTrue(has_props, "Should use modern property definitions")
        
        # Should have poll methods for operators
        self.assertIn("def poll(cls, context):", self.addon_code)
        
    def test_required_classes_present(self):
        """Test that required operator and panel classes are present"""
        class_names = []
        for node in ast.walk(self.addon_ast):
            if isinstance(node, ast.ClassDef):
                class_names.append(node.name)
                
        # Should have shapekey-related operators
        shapekey_classes = [name for name in class_names if 'Shapekey' in name or 'MESH_OT_' in name]
        self.assertGreater(len(shapekey_classes), 0, 
                          "Should have shapekey operator classes")
                          
        # Should have panel class
        panel_classes = [name for name in class_names if 'Panel' in name or '_PT_' in name]
        self.assertGreater(len(panel_classes), 0, 
                          "Should have panel classes")
                          
    def test_no_deprecated_patterns(self):
        """Test that no deprecated API patterns are used"""
        deprecated_patterns = [
            "bpy.utils.register_module",
            "context.scene.objects",
            "bl_space_type = 'UV'",  # Should be IMAGE_EDITOR
        ]
        
        for pattern in deprecated_patterns:
            self.assertNotIn(pattern, self.addon_code, 
                           f"Should not use deprecated pattern: {pattern}")


class TestStitchToolAddon(unittest.TestCase):
    """Test the new Nazarick Stitch Tool addon"""
    
    def setUp(self):
        self.addon_path = os.path.join("demiurge_village", "nazarick_stitch_tool.py")
        with open(self.addon_path, 'r') as f:
            self.addon_code = f.read()
        self.addon_ast = ast.parse(self.addon_code)
        
    def test_python_syntax_valid(self):
        """Test that the stitch tool has valid Python syntax"""
        try:
            compile(self.addon_code, self.addon_path, 'exec')
        except SyntaxError as e:
            self.fail(f"Syntax error in stitch tool: {e}")
            
    def test_bl_info_blender45_compatible(self):
        """Test that bl_info declares Blender 4.5 compatibility"""
        self.assertIn("(4, 5, 0)", self.addon_code, 
                     "Should require Blender 4.5.0 or newer")
        self.assertIn('"category": "Mesh"', self.addon_code,
                     "Should be categorized as Mesh addon")
                     
    def test_stitch_functionality_present(self):
        """Test that stitch-specific functionality is implemented"""
        # Should have stitch creation operator
        self.assertIn("CreateStitches", self.addon_code)
        self.assertIn("vertex_group", self.addon_code)
        self.assertIn("stitch_count", self.addon_code)
        self.assertIn("stitch_size", self.addon_code)
        
        # Should have different stitch styles
        self.assertIn("STRAIGHT", self.addon_code)
        self.assertIn("CROSS", self.addon_code)
        self.assertIn("ZIGZAG", self.addon_code)
        
    def test_vertex_group_integration(self):
        """Test that the addon properly integrates with vertex groups"""
        self.assertIn("vertex_groups", self.addon_code)
        self.assertIn("deform_layer", self.addon_code)
        self.assertIn("vg_index", self.addon_code)
        
    def test_modern_bmesh_usage(self):
        """Test that modern bmesh patterns are used"""
        self.assertIn("bmesh.from_edit_mesh", self.addon_code)
        self.assertIn("bmesh.update_edit_mesh", self.addon_code)
        
    def test_ui_panel_implementation(self):
        """Test that UI panel is properly implemented"""
        self.assertIn("VIEW3D_PT_", self.addon_code)
        self.assertIn("bl_space_type = 'VIEW_3D'", self.addon_code)
        self.assertIn("bl_category", self.addon_code)


class TestUVAddonModernization(unittest.TestCase):
    """Test the modernized UV addon"""
    
    def setUp(self):
        self.addon_path = os.path.join("demiurge_village", "uv_total_ratio_compare_modernized.py")
        with open(self.addon_path, 'r') as f:
            self.addon_code = f.read()
            
    def test_python_syntax_valid(self):
        """Test that the modernized UV addon has valid Python syntax"""
        try:
            compile(self.addon_code, self.addon_path, 'exec')
        except SyntaxError as e:
            self.fail(f"Syntax error in modernized UV addon: {e}")
            
    def test_modern_space_types(self):
        """Test that modern space types are used"""
        self.assertIn("'IMAGE_EDITOR'", self.addon_code)
        self.assertIn("'VIEW_3D'", self.addon_code)
        # Should not use deprecated 'UV' space type
        self.assertNotIn("bl_space_type = 'UV'", self.addon_code)
        
    def test_dual_panel_architecture(self):
        """Test that dual-panel architecture is maintained"""
        self.assertIn("UV_PT_", self.addon_code)
        self.assertIn("VIEW3D_PT_", self.addon_code)
        self.assertIn("NazarickRatioPanelMixin", self.addon_code)


class TestBlender45Compatibility(unittest.TestCase):
    """Test Blender 4.5 compatibility across all addons"""
    
    def setUp(self):
        self.addon_files = [
            os.path.join("demiurge_village", "nines_shapekey_oversight_fixer.py"),
            os.path.join("demiurge_village", "uv_total_ratio_compare_modernized.py"),
            os.path.join("demiurge_village", "nazarick_stitch_tool.py")
        ]
        
    def test_all_addons_declare_blender45(self):
        """Test that all addons declare Blender 4.5 compatibility"""
        for addon_path in self.addon_files:
            with open(addon_path, 'r') as f:
                content = f.read()
            self.assertIn("(4, 5, 0)", content, 
                         f"{addon_path} should declare Blender 4.5 compatibility")
                         
    def test_no_deprecated_apis_used(self):
        """Test that no deprecated APIs are used in any addon"""
        deprecated_patterns = [
            "bpy.utils.register_module",
            "bl_space_type = 'UV'",
            "context.scene.objects",
        ]
        
        for addon_path in self.addon_files:
            with open(addon_path, 'r') as f:
                content = f.read()
            for pattern in deprecated_patterns:
                self.assertNotIn(pattern, content, 
                               f"{addon_path} should not use deprecated pattern: {pattern}")
                               
    def test_modern_property_definitions(self):
        """Test that all addons use modern property definitions"""
        for addon_path in self.addon_files:
            with open(addon_path, 'r') as f:
                content = f.read()
            if "Property" in content:  # Only test files that use properties
                has_modern_props = ("bpy.props." in content or 
                                  "from bpy.props import" in content)
                self.assertTrue(has_modern_props, 
                             f"{addon_path} should use modern property definitions")


class TestRegistrationPatterns(unittest.TestCase):
    """Test that all addons use proper registration patterns"""
    
    def setUp(self):
        self.addon_files = [
            os.path.join("demiurge_village", "nines_shapekey_oversight_fixer.py"),
            os.path.join("demiurge_village", "uv_total_ratio_compare_modernized.py"),
            os.path.join("demiurge_village", "nazarick_stitch_tool.py")
        ]
        
    def test_registration_functions_present(self):
        """Test that register/unregister functions are present"""
        for addon_path in self.addon_files:
            with open(addon_path, 'r') as f:
                content = f.read()
            self.assertIn("def register():", content, 
                         f"{addon_path} should have register() function")
            self.assertIn("def unregister():", content, 
                         f"{addon_path} should have unregister() function")
                         
    def test_classes_tuple_defined(self):
        """Test that classes tuple is properly defined"""
        for addon_path in self.addon_files:
            with open(addon_path, 'r') as f:
                content = f.read()
            self.assertIn("classes = (", content, 
                         f"{addon_path} should define classes tuple")


def run_demiurge_village_tests():
    """Run all tests for the demiurge village addons"""
    print("🏰⚡ DEMIURGE VILLAGE ADDON TESTING SUITE ⚡🏰")
    print("Supreme testing for all modernized Nazarick addons")
    print("🎖️ Architected by Demiurge for the Great Tomb of Nazarick")
    print("=" * 70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestDemiurgeVillageStructure,
        TestShapekeyAddonModernization, 
        TestStitchToolAddon,
        TestUVAddonModernization,
        TestBlender45Compatibility,
        TestRegistrationPatterns,
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    start_time = time.time()
    result = runner.run(suite)
    end_time = time.time()
    
    # Summary
    print("\n" + "=" * 70)
    print("🏰 DEMIURGE VILLAGE TEST SUMMARY 🏰")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print(f"Execution time: {end_time - start_time:.2f} seconds")
    
    if result.failures:
        print("\n🔥 FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError: ')[-1].strip()}")
    
    if result.errors:
        print("\n💥 ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('Error: ')[-1].strip()}")
    
    if result.testsRun > 0 and len(result.failures) == 0 and len(result.errors) == 0:
        print("\n✅ ALL DEMIURGE VILLAGE TESTS PASSED!")
        print("🏆 The modernized addons are ready for Blender 4.5!")
        print("For the Glory of the Great Tomb of Nazarick! 🏰⚡")
        return True
    else:
        print("\n⚠️ Some tests failed. Please review and fix issues before deployment.")
        return False


if __name__ == "__main__":
    success = run_demiurge_village_tests()
    sys.exit(0 if success else 1)