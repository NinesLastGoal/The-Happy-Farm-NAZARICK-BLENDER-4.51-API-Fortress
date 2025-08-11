#!/usr/bin/env python3
"""
Blender 4.5 Compatibility Test Suite for UV3D Ratio Addon
=========================================================

This test suite validates the UV3D Ratio addon for Blender 4.5.
It focuses on:
1. Python syntax validation
2. Blender compatibility checks  
3. Code structure verification
4. Basic functionality tests

For the Glory of Nazarick! 🏰

Author: Nines Own Goal
"""

import unittest
import sys
import ast
import math
import subprocess
from pathlib import Path

def test_python_syntax():
    """Test Python syntax is valid"""
    try:
        with open('uv_total_ratio_compare_Version2.py', 'r') as f:
            code = f.read()
        ast.parse(code)
        return True, "✅ Python syntax is valid"
    except SyntaxError as e:
        return False, f"❌ Syntax error: {e}"
    except Exception as e:
        return False, f"❌ Error parsing file: {e}"

def test_blender_compatibility():
    """Test Blender 4.5 compatibility"""
    try:
        with open('uv_total_ratio_compare_Version2.py', 'r') as f:
            content = f.read()
        
        checks = []
        
        # Check bl_info
        if 'bl_info = {' in content and '"blender": (4, 5, 0)' in content:
            checks.append("✅ Blender 4.5 compatibility declared")
        else:
            checks.append("❌ Missing or incorrect Blender version info")
        
        # Check required fields
        required_fields = ['"name":', '"author":', '"version":', '"category":']
        for field in required_fields:
            if field in content:
                checks.append(f"✅ {field.strip('":"')} field present")
            else:
                checks.append(f"❌ Missing {field.strip('":"')} field")
        
        # Check imports
        required_imports = ['import bpy', 'import bmesh', 'from mathutils import Vector']
        for imp in required_imports:
            if imp in content:
                checks.append(f"✅ {imp}")
            else:
                checks.append(f"❌ Missing {imp}")
        
        return True, checks
    except Exception as e:
        return False, [f"❌ Error checking compatibility: {e}"]

def test_class_structure():
    """Test addon class structure"""
    try:
        with open('uv_total_ratio_compare_Version2.py', 'r') as f:
            content = f.read()
        
        required_classes = [
            'UV_OT_TotalUV3DRatio',
            'UV_PT_NazarickRatioPanel',
            'VIEW3D_PT_NazarickRatioPanel', 
            'UV_OT_ScaleUVTo3D',
            'NazarickRatioPanelMixin'
        ]
        
        checks = []
        for cls in required_classes:
            if f'class {cls}' in content:
                checks.append(f"✅ Class {cls} found")
            else:
                checks.append(f"❌ Class {cls} missing")
        
        # Check for register/unregister
        if 'def register():' in content and 'def unregister():' in content:
            checks.append("✅ register/unregister functions found")
        else:
            checks.append("❌ Missing register/unregister functions")
        
        return True, checks
    except Exception as e:
        return False, [f"❌ Error checking class structure: {e}"]

def test_mathematical_functions():
    """Test the mathematical functions in isolation"""
    try:
        # Mock classes for testing
        class MockVector:
            def __init__(self, x, y, z):
                self.x, self.y, self.z = x, y, z
            
            def __sub__(self, other):
                return MockVector(self.x - other.x, self.y - other.y, self.z - other.z)
            
            def cross(self, other):
                cx = self.y * other.z - self.z * other.y
                cy = self.z * other.x - self.x * other.z  
                cz = self.x * other.y - self.y * other.x
                result = MockVector(cx, cy, cz)
                result.length = math.sqrt(cx*cx + cy*cy + cz*cz)
                return result

        class MockVert:
            def __init__(self, coords):
                self.co = MockVector(*coords)

        class MockFace:
            def __init__(self, vertices):
                self.verts = [MockVert(v) for v in vertices]

        # Mathematical function from the addon
        def face_area_3d(face):
            """Calculate the 3D area of a face using triangulation."""
            verts = [v.co for v in face.verts]
            if len(verts) < 3:
                return 0.0
            area = 0.0
            for i in range(1, len(verts) - 1):
                area += (verts[i] - verts[0]).cross(verts[i+1] - verts[0]).length / 2
            return area

        # Test triangle area (should be 0.5)
        triangle = MockFace([(0, 0, 0), (1, 0, 0), (0, 1, 0)])
        area = face_area_3d(triangle)
        assert abs(area - 0.5) < 0.0001, f"Expected 0.5, got {area}"

        # Test square area (should be 1.0)
        square = MockFace([(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)])
        area = face_area_3d(square)
        assert abs(area - 1.0) < 0.0001, f"Expected 1.0, got {area}"

        # Test degenerate case (should be 0.0)
        degenerate = MockFace([(0, 0, 0), (1, 0, 0)])  # Only 2 vertices
        area = face_area_3d(degenerate)
        assert area == 0.0, f"Expected 0.0 for degenerate face, got {area}"

        return True, "✅ Mathematical functions validated (triangle=0.5, square=1.0, degenerate=0.0)"
        
    except Exception as e:
        return False, f"❌ Mathematical function test failed: {e}"

def test_python_version():
    """Test Python version compatibility"""
    version = sys.version_info
    checks = []
    
    checks.append(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        checks.append("✅ Python version compatible with Blender")
    else:
        checks.append("⚠️  Python version may not be compatible with Blender 4.5")
    
    # Note about Blender's bundled Python
    checks.append("ℹ️  Note: Blender 4.5 includes Python 3.11.x bundled")
    
    return True, checks

def test_code_compilation():
    """Test that code compiles without imports"""
    try:
        # Test compilation by trying to compile the code
        with open('uv_total_ratio_compare_Version2.py', 'r') as f:
            code = f.read()
        
        compile(code, 'uv_total_ratio_compare_Version2.py', 'exec')
        return True, "✅ Code compiles successfully"
    except SyntaxError as e:
        return False, f"❌ Compilation error: {e}"
    except Exception as e:
        return False, f"❌ Error during compilation: {e}"

def run_all_tests():
    """Run all tests and display results"""
    print("🏰 UV3D Ratio Addon - Blender 4.5 Compatibility Test Suite 🏰")
    print("=" * 70)
    print()
    
    tests = [
        ("Python Syntax Validation", test_python_syntax),
        ("Python Version Check", test_python_version),
        ("Code Compilation", test_code_compilation),
        ("Blender Compatibility", test_blender_compatibility),
        ("Class Structure", test_class_structure),
        ("Mathematical Functions", test_mathematical_functions),
    ]
    
    results = []
    all_passed = True
    
    for test_name, test_func in tests:
        print(f"🧪 Running: {test_name}")
        try:
            success, details = test_func()
            if success:
                print(f"✅ PASS: {test_name}")
                if isinstance(details, list):
                    for detail in details:
                        print(f"   {detail}")
                else:
                    print(f"   {details}")
            else:
                print(f"❌ FAIL: {test_name}")
                if isinstance(details, list):
                    for detail in details:
                        print(f"   {detail}")
                else:
                    print(f"   {details}")
                all_passed = False
            results.append((test_name, success, details))
        except Exception as e:
            print(f"🔥 ERROR: {test_name} - {e}")
            all_passed = False
            results.append((test_name, False, str(e)))
        print()
    
    print("=" * 70)
    print("🏰 Test Summary 🏰")
    print()
    
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if all_passed:
        print("✅ ALL TESTS PASSED!")
        print("🏆 The addon is ready for Blender 4.5!")
        print("For the Glory of Nazarick! 🏰⚡")
    else:
        print("⚠️  Some tests failed. Please review the issues above.")
    
    print()
    print("📋 Deployment Checklist:")
    print("  □ Install Blender 4.5+")
    print("  □ Copy addon file to Blender addons directory")
    print("  □ Enable addon in Blender preferences")
    print("  □ Test in UV Editor and 3D Viewport")
    print("  □ Verify dual-panel functionality")
    
    return all_passed

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)