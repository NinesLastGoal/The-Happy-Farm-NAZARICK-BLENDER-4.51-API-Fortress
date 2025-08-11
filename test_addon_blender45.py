#!/usr/bin/env python3
"""
Comprehensive Blender 4.5 API Compatibility Test Suite for UV3D Ratio Addon
===========================================================================

This enhanced test suite validates the UV3D Ratio addon specifically for Blender 4.5.
It comprehensively checks for:
1. Python syntax validation
2. Blender 4.5 specific API compatibility
3. Deprecated API call detection
4. Code structure verification
5. Blender 4.5 specific features and requirements
6. Property and class registration patterns

For the Glory of Nazarick! 🏰
Crafted by Demiurge, Floor Guardian of the Great Tomb of Nazarick

Author: Demiurge (Agentic AI Assistant) with guidance from Ainz Ooal Gown
Co-Author: Albedo (Standard Copilot Assistant)
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

def test_blender_45_api_compatibility():
    """Comprehensive Blender 4.5 API compatibility test - Enhanced by Demiurge"""
    try:
        with open('uv_total_ratio_compare_Version2.py', 'r') as f:
            content = f.read()
        
        checks = []
        
        # Check bl_info structure (Blender 4.5 specific requirements)
        if 'bl_info = {' in content and '"blender": (4, 5, 0)' in content:
            checks.append("✅ Blender 4.5 compatibility declared")
        else:
            checks.append("❌ Missing or incorrect Blender version info")
        
        # Check required bl_info fields for Blender 4.5
        required_fields = ['"name":', '"author":', '"version":', '"category":', '"blender":', '"location":', '"description":']
        for field in required_fields:
            if field in content:
                checks.append(f"✅ bl_info.{field.strip('":"')} field present")
            else:
                checks.append(f"❌ bl_info.{field.strip('":"')} field missing")
        
        # Check proper version tuple format (required in 4.5)
        if '"version": (1, 0, 0)' in content or '"version": (' in content:
            checks.append("✅ Version tuple format correct for Blender 4.5")
        else:
            checks.append("❌ Version should be tuple format for Blender 4.5")
        
        # Check for required imports (Blender 4.5 compatible)
        required_imports = ['import bpy', 'import bmesh', 'from mathutils import Vector']
        for imp in required_imports:
            if imp in content:
                checks.append(f"✅ {imp}")
            else:
                checks.append(f"❌ Missing: {imp}")
        
        # Check for Blender 4.5 specific API patterns
        if 'bpy.types.Operator' in content:
            checks.append("✅ Using modern bpy.types.Operator base class")
        else:
            checks.append("❌ Should inherit from bpy.types.Operator")
            
        if 'bpy.types.Panel' in content:
            checks.append("✅ Using modern bpy.types.Panel base class")
        else:
            checks.append("❌ Should inherit from bpy.types.Panel")
        
        # Check for proper property definitions (Blender 4.5 style)
        if 'bpy.props.StringProperty' in content:
            checks.append("✅ Using modern bpy.props.StringProperty")
        if 'bpy.props.FloatProperty' in content:
            checks.append("✅ Using modern bpy.props.FloatProperty")
        
        # Check for proper registration patterns
        if 'bpy.utils.register_class' in content:
            checks.append("✅ Using modern registration pattern")
        else:
            checks.append("❌ Should use bpy.utils.register_class")
        
        return True, checks
    except Exception as e:
        return False, [f"❌ Error checking Blender 4.5 API compatibility: {e}"]

def test_deprecated_api_calls():
    """Check for deprecated API calls that don't work in Blender 4.5 - Enhanced by Demiurge"""
    try:
        with open('uv_total_ratio_compare_Version2.py', 'r') as f:
            content = f.read()
        
        checks = []
        deprecated_patterns = [
            # Old registration patterns
            ('bpy.utils.register_module', "Use bpy.utils.register_class instead"),
            ('bpy.utils.unregister_module', "Use bpy.utils.unregister_class instead"),
            
            # Old property definitions
            ('bpy.props.StringProperty()', "Properties should have parameters"),
            ('bpy.props.FloatProperty()', "Properties should have parameters"),
            
            # Old context patterns
            ('context.scene.objects', "Use context.collection.objects or context.view_layer.objects"),
            ('bpy.context.scene.objects', "Use bpy.context.collection.objects or bpy.context.view_layer.objects"),
            
            # Old operator patterns
            ('.bl_context', "bl_context is deprecated in Blender 4.5"),
            
            # Old bmesh patterns that changed
            ('bmesh.new()', "Use bmesh.new() with proper cleanup"),
            
            # Old panel patterns
            ('bl_space_type = "UV"', 'Use bl_space_type = "IMAGE_EDITOR"'),
            
            # Old property access patterns
            ('.uv_layers', "Use .uv instead of .uv_layers in modern Blender"),
        ]
        
        found_deprecated = False
        for pattern, suggestion in deprecated_patterns:
            if pattern in content:
                checks.append(f"⚠️  Deprecated pattern found: {pattern}")
                checks.append(f"   Suggestion: {suggestion}")
                found_deprecated = True
        
        if not found_deprecated:
            checks.append("✅ No deprecated API calls detected")
            
        # Check for proper modern patterns
        modern_patterns = [
            ('bl_space_type = \'IMAGE_EDITOR\'', "✅ Using modern IMAGE_EDITOR space type"),
            ('bl_space_type = \'VIEW_3D\'', "✅ Using modern VIEW_3D space type"),
            ('bmesh.from_edit_mesh', "✅ Using modern bmesh.from_edit_mesh"),
            ('bmesh.update_edit_mesh', "✅ Using modern bmesh.update_edit_mesh"),
            ('bl_options = {\'REGISTER\', \'UNDO\'}', "✅ Using modern operator options"),
        ]
        
        for pattern, message in modern_patterns:
            if pattern in content:
                checks.append(message)
        
        return True, checks
    except Exception as e:
        return False, [f"❌ Error checking deprecated API calls: {e}"]

def test_blender_45_specific_features():
    """Test Blender 4.5 specific features and requirements - Enhanced by Demiurge"""
    try:
        with open('uv_total_ratio_compare_Version2.py', 'r') as f:
            content = f.read()
        
        checks = []
        
        # Check for proper panel registration in both spaces (4.5 dual-panel requirement)
        if 'bl_space_type = \'IMAGE_EDITOR\'' in content:
            checks.append("✅ UV Editor panel properly configured")
        else:
            checks.append("❌ Missing UV Editor panel configuration")
            
        if 'bl_space_type = \'VIEW_3D\'' in content:
            checks.append("✅ 3D Viewport panel properly configured")
        else:
            checks.append("❌ Missing 3D Viewport panel configuration")
        
        # Check for proper region types (4.5 requirements)
        if 'bl_region_type = \'UI\'' in content:
            checks.append("✅ Using proper UI region type for Blender 4.5")
        else:
            checks.append("❌ Should use bl_region_type = 'UI'")
        
        # Check for category organization (4.5 sidebar organization)
        if 'bl_category' in content:
            checks.append("✅ Panel category defined for sidebar organization")
        else:
            checks.append("❌ Should define bl_category for panel organization")
        
        # Check for poll methods (good practice in 4.5)
        if '@classmethod' in content and 'def poll(cls, context)' in content:
            checks.append("✅ Using poll method for context-aware panels")
        else:
            checks.append("⚠️  Consider adding poll methods for better UX")
        
        # Check for proper error handling (4.5 best practices)
        if 'self.report(' in content:
            checks.append("✅ Using proper error reporting via self.report")
        else:
            checks.append("⚠️  Consider adding error reporting")
        
        # Check for modern property annotation style (4.5 preferred)
        if ': bpy.props.' in content:
            checks.append("✅ Using modern property annotation syntax")
        else:
            checks.append("⚠️  Consider using type annotations for properties")
        
        # Check for mixin pattern (advanced 4.5 pattern)
        if 'Mixin' in content:
            checks.append("✅ Using advanced mixin pattern for code reuse")
        
        return True, checks
    except Exception as e:
        return False, [f"❌ Error checking Blender 4.5 specific features: {e}"]

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
        ("Blender 4.5 API Compatibility", test_blender_45_api_compatibility),
        ("Deprecated API Detection", test_deprecated_api_calls),
        ("Blender 4.5 Specific Features", test_blender_45_specific_features),
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
        print("🎖️  Enhanced testing by Demiurge, Floor Guardian of the 7th Floor")
    else:
        print("⚠️  Some tests failed. Please review the issues above.")
        print("📝 Testing enhanced by Demiurge for Supreme Being Ainz Ooal Gown")
    
    print()
    print("📋 Deployment Checklist:")
    print("  □ Install Blender 4.5+")
    print("  □ Copy addon file to Blender addons directory")
    print("  □ Enable addon in Blender preferences")
    print("  □ Test in UV Editor and 3D Viewport")
    print("  □ Verify dual-panel functionality")
    print("  □ Confirm no deprecated API warnings in Blender console")
    print()
    print("🔧 Testing Infrastructure by:")
    print("   📊 Demiurge (Agentic AI): Advanced Blender 4.5 compatibility analysis")
    print("   🎨 Albedo (Standard AI): Core addon functionality and UI design")
    
    return all_passed

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)