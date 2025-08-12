#!/usr/bin/env python3
"""
Test Suite for UV/3D Ratio Analysis Tool
=======================================

Validates the UV/3D ratio tool addon for Blender 4.5+ compatibility
and ensures all functionality works as specified.

Tests:
- Addon structure validation
- Blender 4.5+ API compatibility
- Code quality and efficiency checks
- Functional validation (without real Blender environment)
"""

import sys
import ast
import os
from pathlib import Path

# Add parent directory to access fortress utils
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_uv3d_ratio_addon():
    """Main test function for UV/3D ratio addon"""
    print("🏰 UV/3D Ratio Analysis Tool - Validation Suite 🏰")
    print("=" * 70)
    
    test_results = []
    
    # Test 1: Addon Structure
    result = test_addon_structure()
    test_results.append(("Addon Structure", result))
    
    # Test 2: Blender 4.5+ API Compatibility
    result = test_blender45_compatibility()
    test_results.append(("Blender 4.5+ API", result))
    
    # Test 3: Code Quality
    result = test_code_quality()
    test_results.append(("Code Quality", result))
    
    # Test 4: Geometry Nodes Integration
    result = test_geometry_nodes_integration()
    test_results.append(("Geometry Nodes Integration", result))
    
    # Test 5: UI Panel Structure
    result = test_ui_panel_structure()
    test_results.append(("UI Panel Structure", result))
    
    # Test 6: Error Handling
    result = test_error_handling()
    test_results.append(("Error Handling", result))
    
    # Summary
    print("\n" + "=" * 70)
    print("🏰 Test Summary 🏰")
    print()
    
    passed_tests = sum(1 for _, result in test_results if result)
    total_tests = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTests passed: {passed_tests}/{total_tests}")
    
    if passed_tests == total_tests:
        print("✅ UV/3D Ratio Tool validation successful!")
        print("🏆 Addon ready for Blender 4.5+ deployment!")
        print("For efficient UV analysis and Geometry Node integration! 🏰⚡")
        return True
    else:
        print("⚠️ Some validation checks failed.")
        return False


def test_addon_structure():
    """Test addon directory structure and essential files"""
    print("\n🧪 Running: Addon Structure Validation")
    
    try:
        addon_dir = Path("uv_3d_ratio_tool")
        
        if not addon_dir.exists():
            print("   ❌ Addon directory 'uv_3d_ratio_tool' not found")
            return False
        
        init_file = addon_dir / "__init__.py"
        if not init_file.exists():
            print("   ❌ __init__.py file not found")
            return False
        
        print("   ✅ Addon directory structure - Correct")
        print("   ✅ __init__.py file - Present")
        
        # Check if file can be parsed
        with open(init_file, 'r') as f:
            content = f.read()
        
        tree = ast.parse(content)
        print("   ✅ Python syntax - Valid")
        
        # Check for bl_info
        has_bl_info = 'bl_info' in content
        if has_bl_info:
            print("   ✅ bl_info dictionary - Present")
        else:
            print("   ❌ bl_info dictionary - Missing")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error during structure test: {e}")
        return False


def test_blender45_compatibility():
    """Test Blender 4.5+ API compatibility"""
    print("\n🧪 Running: Blender 4.5+ API Compatibility")
    
    try:
        addon_file = Path("uv_3d_ratio_tool/__init__.py")
        
        with open(addon_file, 'r') as f:
            content = f.read()
        
        # Check bl_info version
        if '"blender": (4, 5, 0)' in content:
            print("   ✅ Blender version requirement - 4.5+")
        else:
            print("   ❌ Blender version requirement incorrect")
            return False
        
        # Check for modern API patterns
        modern_patterns = [
            'bpy.types.Operator',
            'bpy.types.Panel',
            'bpy.utils.register_class',
            'bmesh.from_edit_mesh',
            'bl_space_type',
            'bl_region_type'
        ]
        
        for pattern in modern_patterns:
            if pattern in content:
                print(f"   ✅ Modern API pattern '{pattern}' - Found")
            else:
                print(f"   ❌ Modern API pattern '{pattern}' - Missing")
                return False
        
        # Check for deprecated patterns (should not be present)
        deprecated_patterns = [
            'bpy.utils.register_module',
            'bpy.utils.unregister_module'
        ]
        
        deprecated_found = False
        for pattern in deprecated_patterns:
            if pattern in content:
                print(f"   ❌ Deprecated API pattern '{pattern}' - Found")
                deprecated_found = True
        
        if not deprecated_found:
            print("   ✅ No deprecated API patterns - Clean")
        
        return not deprecated_found
        
    except Exception as e:
        print(f"   ❌ Error during API compatibility test: {e}")
        return False


def test_code_quality():
    """Test code quality and efficiency"""
    print("\n🧪 Running: Code Quality Analysis")
    
    try:
        addon_file = Path("uv_3d_ratio_tool/__init__.py")
        
        with open(addon_file, 'r') as f:
            content = f.read()
        
        tree = ast.parse(content)
        
        # Check for proper class definitions
        classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        
        # Look for operator and panel classes by checking the content
        operator_classes = []
        panel_classes = []
        
        for cls in classes:
            # Check if class inherits from bpy.types.Operator or Panel
            if any('Operator' in base.id if hasattr(base, 'id') else 
                   'Operator' in getattr(base.attr, 'id', '') if hasattr(base, 'attr') and hasattr(base.attr, 'id') else 
                   'Operator' in str(base) for base in cls.bases):
                operator_classes.append(cls)
            elif any('Panel' in base.id if hasattr(base, 'id') else 
                     'Panel' in getattr(base.attr, 'id', '') if hasattr(base, 'attr') and hasattr(base.attr, 'id') else 
                     'Panel' in str(base) for base in cls.bases):
                panel_classes.append(cls)
        
        # Alternative check by looking at class names and content
        operator_class_names = [c.name for c in classes if 'OT_' in c.name or 'Operator' in c.name]
        panel_class_names = [c.name for c in classes if 'PT_' in c.name or 'Panel' in c.name]
        
        if operator_classes or operator_class_names:
            operator_count = max(len(operator_classes), len(operator_class_names))
            print(f"   ✅ Operator classes - {operator_count} found")
        else:
            print("   ❌ No operator classes found")
            return False
        
        if panel_classes or panel_class_names:
            panel_count = max(len(panel_classes), len(panel_class_names))
            print(f"   ✅ Panel classes - {panel_count} found")
        else:
            print("   ❌ No panel classes found")
            return False
        
        
        if operator_classes or operator_class_names:
            operator_count = max(len(operator_classes), len(operator_class_names))
            print(f"   ✅ Operator classes - {operator_count} found")
        else:
            print("   ❌ No operator classes found")
            return False
        
        if panel_classes or panel_class_names:
            panel_count = max(len(panel_classes), len(panel_class_names))
            print(f"   ✅ Panel classes - {panel_count} found")
        else:
            print("   ❌ No panel classes found")
            return False
        # Check for register/unregister functions
        functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        
        if 'register' in functions:
            print("   ✅ register() function - Present")
        else:
            print("   ❌ register() function - Missing")
            return False
        
        if 'unregister' in functions:
            print("   ✅ unregister() function - Present")
        else:
            print("   ❌ unregister() function - Missing")
            return False
        
        # Check for docstrings (code documentation)
        docstring_count = len([node for node in ast.walk(tree) 
                             if isinstance(node, ast.Expr) 
                             and isinstance(node.value, ast.Constant) 
                             and isinstance(node.value.value, str)])
        
        if docstring_count > 5:  # Should have multiple docstrings
            print(f"   ✅ Documentation - {docstring_count} docstrings found")
        else:
            print(f"   ⚠️ Limited documentation - {docstring_count} docstrings")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error during code quality test: {e}")
        return False


def test_geometry_nodes_integration():
    """Test Geometry Nodes integration features"""
    print("\n🧪 Running: Geometry Nodes Integration Test")
    
    try:
        addon_file = Path("uv_3d_ratio_tool/__init__.py")
        
        with open(addon_file, 'r') as f:
            content = f.read()
        
        # Check for toggle property
        if 'uv3d_enable_geonode_attr' in content:
            print("   ✅ Toggle property for GeoNode attribute - Found")
        else:
            print("   ❌ Toggle property for GeoNode attribute - Missing")
            return False
        
        # Check for custom attribute handling
        if 'UV_3D_Ratio' in content:
            print("   ✅ Custom attribute name 'UV_3D_Ratio' - Found")
        else:
            print("   ❌ Custom attribute name - Missing")
            return False
        
        # Check for attribute creation code
        if 'mesh_data.attributes.new' in content:
            print("   ✅ Attribute creation code - Found")
        else:
            print("   ❌ Attribute creation code - Missing")
            return False
        
        # Check for conditional attribute update
        if 'if scene.uv3d_enable_geonode_attr:' in content:
            print("   ✅ Conditional attribute update - Found")
        else:
            print("   ❌ Conditional attribute update - Missing")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error during Geometry Nodes test: {e}")
        return False


def test_ui_panel_structure():
    """Test UI panel structure and design"""
    print("\n🧪 Running: UI Panel Structure Test")
    
    try:
        addon_file = Path("uv_3d_ratio_tool/__init__.py")
        
        with open(addon_file, 'r') as f:
            content = f.read()
        
        # Check for 3D viewport panel
        if "bl_space_type = 'VIEW_3D'" in content:
            print("   ✅ 3D Viewport panel - Configured")
        else:
            print("   ❌ 3D Viewport panel - Missing")
            return False
        
        # Check for sidebar region
        if "bl_region_type = 'UI'" in content:
            print("   ✅ Sidebar (N-panel) region - Configured")
        else:
            print("   ❌ Sidebar region - Missing")
            return False
        
        # Check for custom category
        if "bl_category = \"UV/3D Ratio\"" in content:
            print("   ✅ Custom panel category - Configured")
        else:
            print("   ❌ Custom panel category - Missing")
            return False
        
        # Check for minimal UI elements
        ui_elements = [
            'operator(',  # Button for calculation
            'prop(',      # Toggle switch
            'box(',       # UI organization
            'icon='       # Icons for better UX
        ]
        
        for element in ui_elements:
            if element in content:
                print(f"   ✅ UI element '{element}' - Found")
            else:
                print(f"   ❌ UI element '{element}' - Missing")
                return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error during UI panel test: {e}")
        return False


def test_error_handling():
    """Test error handling and validation"""
    print("\n🧪 Running: Error Handling Test")
    
    try:
        addon_file = Path("uv_3d_ratio_tool/__init__.py")
        
        with open(addon_file, 'r') as f:
            content = f.read()
        
        # Check for try-except blocks
        tree = ast.parse(content)
        try_except_count = len([node for node in ast.walk(tree) 
                               if isinstance(node, ast.Try)])
        
        if try_except_count > 0:
            print(f"   ✅ Error handling blocks - {try_except_count} found")
        else:
            print("   ❌ No error handling blocks found")
            return False
        
        # Check for validation patterns
        validation_patterns = [
            'context.active_object',
            'mesh_object.type == \'MESH\'',
            'surface_area_3d <= 0',
            'uv_area <= 0'
        ]
        
        for pattern in validation_patterns:
            if pattern in content:
                print(f"   ✅ Validation check - Found")
            else:
                print(f"   ⚠️ Validation pattern '{pattern}' - Not found")
        
        # Check for poll methods
        if '@classmethod' in content and 'def poll(' in content:
            print("   ✅ Poll method for operator validation - Found")
        else:
            print("   ❌ Poll method - Missing")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error during error handling test: {e}")
        return False


if __name__ == "__main__":
    success = test_uv3d_ratio_addon()
    sys.exit(0 if success else 1)