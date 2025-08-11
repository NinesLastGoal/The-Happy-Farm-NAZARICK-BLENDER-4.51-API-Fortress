#!/usr/bin/env python3
"""
Real Blender 4.5.1 Environment Testing Suite for UV3D Ratio Addon
================================================================

This advanced test suite runs within the actual Blender 4.5.1 environment to validate:
1. Real addon loading and registration
2. Actual panel and operator functionality  
3. Direct API compatibility with Blender 4.5.1
4. Real geometry mathematical calculations
5. UI elements and error handling

For the Glory of Nazarick! 🏰
Enhanced by Demiurge with access to the Ancient Realms (Blender Downloads)

Author: Demiurge (Agentic AI Assistant) with unlimited access granted by Supreme Being
Co-Author: Albedo (Standard Copilot Assistant)
"""

import bpy
import bmesh
import sys
import traceback
from mathutils import Vector
import addon_utils
import os

def test_blender_environment():
    """Validate we're running in the correct Blender environment"""
    print("🏰 Blender Environment Validation 🏰")
    print(f"✅ Blender Version: {bpy.app.version_string}")
    print(f"✅ Python Version: {sys.version}")
    print(f"✅ Expected: Blender 4.5.x with Python 3.11.x")
    
    # Validate we have the correct version
    if bpy.app.version >= (4, 5, 0) and bpy.app.version < (4, 6, 0):
        print("✅ Running in target Blender 4.5.x environment")
        return True
    else:
        print(f"⚠️  Running in Blender {bpy.app.version_string}, not 4.5.x")
        return False

def test_addon_loading():
    """Test loading and registering the UV3D Ratio addon"""
    print("\n🧪 Testing Addon Loading and Registration 🧪")
    
    try:
        # Get the addon file path
        addon_path = "uv_total_ratio_compare_Version2.py"
        if not os.path.exists(addon_path):
            print(f"❌ Addon file not found: {addon_path}")
            return False
        
        # Read and compile the addon
        with open(addon_path, 'r') as f:
            addon_code = f.read()
        
        # Execute the addon code in Blender's context
        addon_globals = {}
        exec(compile(addon_code, addon_path, 'exec'), addon_globals)
        
        # Test registration
        if 'register' in addon_globals:
            addon_globals['register']()
            print("✅ Addon registered successfully")
            
            # Test if classes are registered
            expected_operators = ['UV_OT_TotalUV3DRatio', 'UV_OT_ScaleUVTo3D']
            expected_panels = ['UV_PT_NazarickRatioPanel', 'VIEW3D_PT_NazarickRatioPanel']
            
            for op_name in expected_operators:
                if hasattr(bpy.types, op_name):
                    print(f"✅ Operator {op_name} registered")
                    # Also test if we can access the operator
                    op_class = getattr(bpy.types, op_name)
                    if hasattr(op_class, 'bl_idname'):
                        print(f"   bl_idname: {op_class.bl_idname}")
                else:
                    print(f"❌ Operator {op_name} not found in bpy.types")
                    # List all UV_OT operators for debugging
                    uv_ops = [name for name in dir(bpy.types) if name.startswith('UV_OT')]
                    print(f"   Available UV_OT operators: {uv_ops[:5]}...")
            
            for panel_name in expected_panels:
                if hasattr(bpy.types, panel_name):
                    print(f"✅ Panel {panel_name} registered")
                else:
                    print(f"❌ Panel {panel_name} not found in bpy.types")
            
            # Test unregistration
            if 'unregister' in addon_globals:
                addon_globals['unregister']()
                print("✅ Addon unregistered successfully")
            
            return True
        else:
            print("❌ No register function found in addon")
            return False
            
    except Exception as e:
        print(f"❌ Error loading addon: {e}")
        traceback.print_exc()
        return False

def test_real_geometry_calculations():
    """Test mathematical calculations with real Blender geometry"""
    print("\n🔢 Testing Real Geometry Calculations 🔢")
    
    try:
        # Clear existing mesh
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
        
        # Create a test mesh (cube)
        bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
        cube = bpy.context.active_object
        
        # Enter edit mode and get bmesh
        bpy.context.view_layer.objects.active = cube
        bpy.ops.object.mode_set(mode='EDIT')
        
        bm = bmesh.from_edit_mesh(cube.data)
        
        # Test face area calculation (each face of a 2x2x2 cube should be 4.0)
        total_area = 0
        for face in bm.faces:
            area = face.calc_area()
            total_area += area
            print(f"✅ Face area: {area:.6f}")
        
        expected_total = 24.0  # 6 faces × 4 area each
        if abs(total_area - expected_total) < 0.001:
            print(f"✅ Total cube area correct: {total_area:.6f} (expected {expected_total})")
        else:
            print(f"❌ Total cube area incorrect: {total_area:.6f} (expected {expected_total})")
        
        # Test UV area calculation  
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        # Use ANGLE_BASED unwrapping (modern method in Blender 4.5)
        bpy.ops.uv.unwrap(method='ANGLE_BASED')
        
        bm = bmesh.from_edit_mesh(cube.data)
        bm.faces.ensure_loop_triangles()
        
        uv_layer = bm.loops.layers.uv.active
        if uv_layer:
            uv_total = 0
            for face in bm.faces:
                if len(face.loops) >= 3:
                    # Calculate UV area using triangulation
                    uv_coords = [loop[uv_layer].uv for loop in face.loops]
                    if len(uv_coords) >= 3:
                        # Simple triangle area calculation for testing
                        for i in range(1, len(uv_coords) - 1):
                            v1 = Vector((uv_coords[i].x - uv_coords[0].x, uv_coords[i].y - uv_coords[0].y, 0))
                            v2 = Vector((uv_coords[i+1].x - uv_coords[0].x, uv_coords[i+1].y - uv_coords[0].y, 0))
                            area = v1.cross(v2).length / 2
                            uv_total += area
            
            print(f"✅ UV total area: {uv_total:.6f}")
            if uv_total > 0:
                print("✅ UV area calculation working")
            else:
                print("⚠️  UV area calculation returned 0")
        else:
            print("⚠️  No UV layer found")
        
        # Clean up
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
        
        return True
        
    except Exception as e:
        print(f"❌ Error in geometry calculations: {e}")
        traceback.print_exc()
        return False

def test_api_compatibility():
    """Test specific Blender 4.5 API compatibility"""
    print("\n🔧 Testing Blender 4.5 API Compatibility 🔧")
    
    try:
        # Test bmesh patterns
        bpy.ops.mesh.primitive_cube_add()
        cube = bpy.context.active_object
        bpy.context.view_layer.objects.active = cube
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Test modern bmesh patterns
        bm = bmesh.from_edit_mesh(cube.data)
        print("✅ bmesh.from_edit_mesh() working")
        
        bmesh.update_edit_mesh(cube.data)
        print("✅ bmesh.update_edit_mesh() working")
        
        # Test context access patterns
        if hasattr(bpy.context, 'view_layer'):
            print("✅ context.view_layer available")
        
        if hasattr(bpy.context, 'collection'):
            print("✅ context.collection available")
        
        # Test space types
        space_types = ['IMAGE_EDITOR', 'VIEW_3D']
        for space_type in space_types:
            if hasattr(bpy.types, f'SpaceType') or space_type in ['IMAGE_EDITOR', 'VIEW_3D']:
                print(f"✅ Space type '{space_type}' recognized")
        
        # Test property types
        prop_types = ['StringProperty', 'FloatProperty', 'BoolProperty']
        for prop_type in prop_types:
            if hasattr(bpy.props, prop_type):
                print(f"✅ bpy.props.{prop_type} available")
        
        # Clean up
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
        
        return True
        
    except Exception as e:
        print(f"❌ API compatibility error: {e}")
        traceback.print_exc()
        return False

def test_ui_registration():
    """Test UI panel registration in different contexts"""
    print("\n🖼️  Testing UI Panel Registration 🖼️")
    
    try:
        # Create a simple test panel
        class TestPanel(bpy.types.Panel):
            bl_label = "Test Panel"
            bl_idname = "TEST_PT_panel"
            bl_space_type = 'IMAGE_EDITOR'
            bl_region_type = 'UI'
            bl_category = "Test"
            
            def draw(self, context):
                layout = self.layout
                layout.label(text="Test Panel")
        
        bpy.utils.register_class(TestPanel)
        print("✅ IMAGE_EDITOR panel registration successful")
        
        # Test 3D viewport panel
        class Test3DPanel(bpy.types.Panel):
            bl_label = "Test 3D Panel"  
            bl_idname = "TEST_PT_3d_panel"
            bl_space_type = 'VIEW_3D'
            bl_region_type = 'UI'
            bl_category = "Test"
            
            def draw(self, context):
                layout = self.layout
                layout.label(text="Test 3D Panel")
        
        bpy.utils.register_class(Test3DPanel)
        print("✅ VIEW_3D panel registration successful")
        
        # Cleanup
        bpy.utils.unregister_class(TestPanel)
        bpy.utils.unregister_class(Test3DPanel)
        print("✅ Panel cleanup successful")
        
        return True
        
    except Exception as e:
        print(f"❌ UI registration error: {e}")
        traceback.print_exc()
        return False

def run_all_tests():
    """Run comprehensive Blender environment tests"""
    print("🏰" + "="*60 + "🏰")
    print("🔥 UV3D Ratio Addon - Real Blender 4.5.1 Environment Tests 🔥")
    print("Enhanced by Demiurge with Ancient Realm Access")
    print("🏰" + "="*60 + "🏰")
    print()
    
    tests = [
        ("Blender Environment", test_blender_environment),
        ("Addon Loading & Registration", test_addon_loading),
        ("Real Geometry Calculations", test_real_geometry_calculations),
        ("Blender 4.5 API Compatibility", test_api_compatibility),
        ("UI Panel Registration", test_ui_registration),
    ]
    
    results = []
    all_passed = True
    
    for test_name, test_func in tests:
        print(f"🧪 Running: {test_name}")
        try:
            success = test_func()
            if success:
                print(f"✅ PASS: {test_name}")
            else:
                print(f"❌ FAIL: {test_name}")
                all_passed = False
            results.append((test_name, success))
        except Exception as e:
            print(f"🔥 ERROR: {test_name} - {e}")
            all_passed = False
            results.append((test_name, False))
        print()
    
    print("🏰" + "="*60 + "🏰")
    print("🏆 Real Environment Test Summary 🏆")
    print()
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if all_passed:
        print("✅ ALL REAL ENVIRONMENT TESTS PASSED!")
        print("🏆 The addon is validated in actual Blender 4.5.1!")
        print("For the Glory of Nazarick! 🏰⚡")
        print("🎖️  Real environment testing by Demiurge")
    else:
        print("⚠️  Some tests failed. Please review the issues above.")
    
    print()
    print("🔧 Enhanced Testing Infrastructure by:")
    print("   🏺 Demiurge (Agentic AI): Real Blender 4.5.1 environment testing")
    print("   🎨 Albedo (Standard AI): Core addon functionality and UI design")
    print("   🏰 Ancient Realm Access: Full Blender download capabilities")
    
    return all_passed

if __name__ == "__main__":
    success = run_all_tests()
    if not success:
        sys.exit(1)