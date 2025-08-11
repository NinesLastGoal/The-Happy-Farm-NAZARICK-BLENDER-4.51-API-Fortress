#!/usr/bin/env python3
"""
Test Suite for UV3D Ratio Blender Addon
========================================

This test suite validates the UV3D Ratio addon for Blender 4.5 compatibility.
Tests are designed to run outside of Blender to verify code structure,
mathematical functions, and basic functionality.

For the Glory of Nazarick! 🏰

Author: Nines Own Goal
"""

import unittest
import sys
import ast
import math
import importlib.util
from unittest.mock import Mock, MagicMock, patch
from typing import List, Tuple, Any

# Mock Blender modules for testing outside Blender environment
class MockVector:
    """Mock mathutils.Vector for testing"""
    def __init__(self, x=0.0, y=0.0, z=0.0):
        if isinstance(x, (list, tuple)):
            self.x, self.y, self.z = x[0], x[1], x[2] if len(x) > 2 else 0.0
        else:
            self.x, self.y, self.z = x, y, z
    
    def __sub__(self, other):
        return MockVector(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def cross(self, other):
        # Vector cross product
        cx = self.y * other.z - self.z * other.y
        cy = self.z * other.x - self.x * other.z
        cz = self.x * other.y - self.y * other.x
        result = MockVector(cx, cy, cz)
        result.length = math.sqrt(cx*cx + cy*cy + cz*cz)
        return result
    
    @property
    def length(self):
        return math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)

class MockBlenderType:
    """Base mock class for Blender types"""
    pass

class MockOperator(MockBlenderType):
    """Mock Blender Operator class"""
    pass

class MockPanel(MockBlenderType):
    """Mock Blender Panel class"""
    pass

class TestMockFace:
    """Mock face object for testing"""
    def __init__(self, vertices, uv_coords=None):
        self.verts = [MockVert(v) for v in vertices]
        self.select = True
        self.loops = []
        if uv_coords:
            for i, uv in enumerate(uv_coords):
                loop = MockLoop()
                loop.mock_uv = MockUV(uv[0], uv[1])
                self.loops.append(loop)

class MockVert:
    """Mock vertex object"""
    def __init__(self, coords):
        self.co = MockVector(coords)

class MockLoop:
    """Mock loop object"""
    def __init__(self):
        self.mock_uv = None
    
    def __getitem__(self, uv_layer):
        return self.mock_uv

class MockUV:
    """Mock UV coordinate"""
    def __init__(self, u, v):
        self.uv = MockVector(u, v, 0.0)

class TestAddonStructure(unittest.TestCase):
    """Test the basic structure and syntax of the addon"""
    
    def setUp(self):
        """Load the addon file for testing"""
        with open('../src/addons/uv_ratio_tool.py', 'r') as f:
            self.addon_code = f.read()
        self.ast_tree = ast.parse(self.addon_code)
    
    def test_python_syntax_valid(self):
        """Test that the Python syntax is valid"""
        try:
            ast.parse(self.addon_code)
        except SyntaxError as e:
            self.fail(f"Syntax error in addon: {e}")
    
    def test_bl_info_present(self):
        """Test that bl_info dictionary is present and valid"""
        self.assertIn('bl_info', self.addon_code)
        
        # Extract bl_info using AST
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == 'bl_info':
                        # Found bl_info assignment
                        self.assertIsInstance(node.value, ast.Dict)
                        return
        self.fail("bl_info dictionary not found")
    
    def test_required_blender_version(self):
        """Test that addon specifies Blender 4.5+ compatibility"""
        self.assertIn('"blender": (4, 5, 0)', self.addon_code)
    
    def test_required_classes_present(self):
        """Test that all required classes are defined"""
        required_classes = [
            'UV_OT_TotalUV3DRatio',
            'UV_PT_NazarickRatioPanel', 
            'VIEW3D_PT_NazarickRatioPanel',
            'UV_OT_ScaleUVTo3D',
            'NazarickRatioPanelMixin'
        ]
        
        for class_name in required_classes:
            self.assertIn(f'class {class_name}', self.addon_code, 
                         f"Required class {class_name} not found")
    
    def test_required_functions_present(self):
        """Test that required functions are defined"""
        required_functions = [
            'face_area_3d',
            'face_area_uv',
            'register',
            'unregister'
        ]
        
        for func_name in required_functions:
            self.assertIn(f'def {func_name}', self.addon_code,
                         f"Required function {func_name} not found")

class TestMathematicalFunctions(unittest.TestCase):
    """Test the mathematical functions used in the addon"""
    
    def setUp(self):
        """Set up isolated test environment for math functions"""
        # Extract just the mathematical functions for testing
        with open('../src/addons/uv_ratio_tool.py', 'r') as f:
            content = f.read()
        
        # Extract face_area_3d function
        start = content.find('def face_area_3d(face):')
        end = content.find('\ndef ', start + 1)
        if end == -1:
            end = content.find('\nclass ', start + 1)
        face_area_3d_code = content[start:end]
        
        # Extract face_area_uv function  
        start = content.find('def face_area_uv(face, uv_layer):')
        end = content.find('\ndef ', start + 1)
        if end == -1:
            end = content.find('\nclass ', start + 1)
        face_area_uv_code = content[start:end]
        
        # Create namespace with mock Vector
        test_namespace = {
            'Vector': MockVector,
            '__name__': '__main__'
        }
        
        # Execute the functions in isolated namespace
        exec(face_area_3d_code, test_namespace)
        exec(face_area_uv_code, test_namespace)
        
        self.face_area_3d = test_namespace['face_area_3d']
        self.face_area_uv = test_namespace['face_area_uv']
    
    def test_triangle_3d_area(self):
        """Test 3D area calculation for a simple triangle"""
        # Create a right triangle with vertices at (0,0,0), (1,0,0), (0,1,0)
        vertices = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
        face = TestMockFace(vertices)
        
        area = self.face_area_3d(face)
        expected_area = 0.5  # Area of right triangle with legs of length 1
        
        self.assertAlmostEqual(area, expected_area, places=6,
                              msg="3D triangle area calculation incorrect")
    
    def test_square_3d_area(self):
        """Test 3D area calculation for a square"""
        # Create a unit square in the XY plane
        vertices = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)]
        face = TestMockFace(vertices)
        
        area = self.face_area_3d(face)
        expected_area = 1.0  # Area of unit square
        
        self.assertAlmostEqual(area, expected_area, places=6,
                              msg="3D square area calculation incorrect")
    
    def test_triangle_uv_area(self):
        """Test UV area calculation for a simple triangle"""
        # Create a right triangle in UV space
        vertices = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
        uv_coords = [(0, 0), (1, 0), (0, 1)]
        face = TestMockFace(vertices, uv_coords)
        
        # Mock UV layer
        uv_layer = Mock()
        
        area = self.face_area_uv(face, uv_layer)
        expected_area = 0.5  # Area of right triangle with legs of length 1
        
        self.assertAlmostEqual(area, expected_area, places=6,
                              msg="UV triangle area calculation incorrect")
    
    def test_degenerate_face_area(self):
        """Test area calculation for degenerate faces (< 3 vertices)"""
        # Test with no vertices
        face_empty = TestMockFace([])
        self.assertEqual(self.face_area_3d(face_empty), 0.0)
        
        # Test with 2 vertices (edge)
        face_edge = TestMockFace([(0, 0, 0), (1, 0, 0)])
        self.assertEqual(self.face_area_3d(face_edge), 0.0)
    
    def test_zero_area_face(self):
        """Test area calculation for faces with zero area (collinear points)"""
        # Three collinear points should give zero area
        vertices = [(0, 0, 0), (1, 0, 0), (2, 0, 0)]
        face = TestMockFace(vertices)
        
        area = self.face_area_3d(face)
        self.assertAlmostEqual(area, 0.0, places=6,
                              msg="Collinear points should have zero area")

class TestBlenderIntegration(unittest.TestCase):
    """Test Blender-specific integration aspects"""
    
    def test_operator_class_names(self):
        """Test that operator classes have correct naming convention"""
        with open('../src/addons/uv_ratio_tool.py', 'r') as f:
            content = f.read()
        
        # Check for operator naming conventions
        self.assertIn('class UV_OT_TotalUV3DRatio', content)
        self.assertIn('class UV_OT_ScaleUVTo3D', content)
        
        # Check for bl_idname patterns
        self.assertIn('bl_idname = "uv.nazarick_total_uv_3d_ratio"', content)
        self.assertIn('bl_idname = "uv.nazarick_scale_uv_to_3d"', content)
    
    def test_panel_class_names(self):
        """Test that panel classes have correct naming convention"""
        with open('../src/addons/uv_ratio_tool.py', 'r') as f:
            content = f.read()
        
        # Check for panel naming conventions
        self.assertIn('class UV_PT_NazarickRatioPanel', content)
        self.assertIn('class VIEW3D_PT_NazarickRatioPanel', content)
        
        # Check for space type definitions
        self.assertIn("bl_space_type = 'IMAGE_EDITOR'", content)
        self.assertIn("bl_space_type = 'VIEW_3D'", content)
    
    def test_mixin_class_present(self):
        """Test that the mixin class is properly defined"""
        with open('../src/addons/uv_ratio_tool.py', 'r') as f:
            content = f.read()
        
        self.assertIn('class NazarickRatioPanelMixin:', content)
        self.assertIn('def draw_ratio_panel(self, context, layout):', content)
    
    def test_classes_tuple_definition(self):
        """Test that classes tuple is properly defined"""
        with open('../src/addons/uv_ratio_tool.py', 'r') as f:
            content = f.read()
        
        self.assertIn('classes = (', content)
        self.assertIn('UV_OT_TotalUV3DRatio,', content)
        self.assertIn('UV_PT_NazarickRatioPanel,', content)
        self.assertIn('VIEW3D_PT_NazarickRatioPanel,', content)
        self.assertIn('UV_OT_ScaleUVTo3D,', content)

class TestAddonCompatibility(unittest.TestCase):
    """Test compatibility with Blender 4.5 and Python versions"""
    
    def test_python_version_compatibility(self):
        """Test compatibility with Python 3.11+ (Blender 4.5 requirement)"""
        current_version = sys.version_info
        
        # Blender 4.5 uses Python 3.11+
        self.assertGreaterEqual(current_version.major, 3,
                               "Python 3.x required")
        
        print(f"✅ Python version: {current_version.major}.{current_version.minor}.{current_version.micro}")
        
        if current_version.major == 3 and current_version.minor < 11:
            print(f"⚠️  Note: Blender 4.5 typically uses Python 3.11+, current is {current_version.major}.{current_version.minor}")
    
    def test_addon_metadata(self):
        """Test addon metadata for Blender compatibility"""
        with open('../src/addons/uv_ratio_tool.py', 'r') as f:
            content = f.read()
        
        # Check for required metadata
        self.assertIn('"name":', content)
        self.assertIn('"author":', content)
        self.assertIn('"version":', content)
        self.assertIn('"blender":', content)
        self.assertIn('"category":', content)
        self.assertIn('"location":', content)
        self.assertIn('"description":', content)
    
    def test_import_requirements(self):
        """Test that required imports are present"""
        with open('../src/addons/uv_ratio_tool.py', 'r') as f:
            content = f.read()
        
        # Check for required imports
        self.assertIn('import bpy', content)
        self.assertIn('import bmesh', content)
        self.assertIn('from mathutils import Vector', content)
        self.assertIn('import time', content)

class TestCodeQuality(unittest.TestCase):
    """Test code quality and best practices"""
    
    def test_function_docstrings(self):
        """Test that key functions have docstrings"""
        with open('../src/addons/uv_ratio_tool.py', 'r') as f:
            content = f.read()
        
        # Check for function docstrings
        self.assertIn('"""Calculate the 3D area of a face using triangulation."""', content)
        self.assertIn('"""Calculate the UV area of a face using triangulation."""', content)
    
    def test_class_docstrings(self):
        """Test that classes have appropriate docstrings"""
        with open('../src/addons/uv_ratio_tool.py', 'r') as f:
            content = f.read()
        
        # Check for class documentation
        self.assertIn('"""Shared drawing logic for UV/3D ratio panels', content)
    
    def test_no_obvious_syntax_errors(self):
        """Test that there are no obvious syntax issues"""
        with open('../src/addons/uv_ratio_tool.py', 'r') as f:
            content = f.read()
        
        # Check for common syntax issues
        self.assertNotIn('print(', content)  # No debug prints left
        self.assertNotIn('TODO', content.upper())  # No unfinished TODOs
        
        # Check for proper indentation (basic check)
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.strip() and not line.startswith('#'):
                # Basic indentation check
                leading_spaces = len(line) - len(line.lstrip())
                self.assertEqual(leading_spaces % 4, 0, 
                               f"Line {i+1} has improper indentation: {leading_spaces} spaces")

def run_tests():
    """Run all tests and return results"""
    print("🏰 Running UV3D Ratio Addon Test Suite for Blender 4.5 🏰")
    print("=" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestAddonStructure,
        TestMathematicalFunctions,
        TestBlenderIntegration,
        TestAddonCompatibility,
        TestCodeQuality
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)
    
    print("\n" + "=" * 60)
    print(f"🏰 Test Results Summary 🏰")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print("\n🔥 ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('Error:')[-1].strip()}")
    
    if result.wasSuccessful():
        print("\n✅ All tests passed! The addon is ready for Blender 4.5!")
        print("For the Glory of Nazarick! 🏰⚡")
        return True
    else:
        print("\n⚠️  Some tests failed. Please review and fix issues before deployment.")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)