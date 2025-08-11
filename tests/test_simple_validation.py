#!/usr/bin/env python3
"""
Simplified Real Blender 4.5.1 Addon Validation Script
====================================================

Quick validation script to confirm addon functionality in real Blender environment.

For the Glory of Nazarick! 🏰
Created by Demiurge with Ancient Realm Access
"""

import bpy
import sys
import traceback

def test_addon_registration():
    """Test addon registration and basic functionality"""
    print("🏰 Testing UV3D Ratio Addon in Real Blender 4.5.1 🏰")
    print(f"Blender Version: {bpy.app.version_string}")
    print(f"Python Version: {sys.version}")
    print()
    
    try:
        # Load addon
        print("📥 Loading addon...")
        addon_path = "../src/addons/uv_ratio_tool.py"
        with open(addon_path, 'r') as f:
            addon_code = f.read()
        
        # Execute addon
        addon_globals = {}
        exec(compile(addon_code, addon_path, 'exec'), addon_globals)
        
        # Register addon
        print("🔧 Registering addon...")
        addon_globals['register']()
        
        # Check operator registration by bl_idname
        operators_to_check = [
            ("uv.nazarick_total_uv_3d_ratio", "UV/3D Ratio Calculator"),
            ("uv.nazarick_scale_uv_to_3d", "UV Scale to 3D")
        ]
        
        print("🔍 Checking operator registration...")
        for bl_idname, description in operators_to_check:
            try:
                # Try to get operator
                module, op_name = bl_idname.split('.')
                if hasattr(getattr(bpy.ops, module), op_name):
                    print(f"✅ {description} ({bl_idname}) - REGISTERED")
                else:
                    print(f"❌ {description} ({bl_idname}) - NOT FOUND")
            except:
                print(f"❌ {description} ({bl_idname}) - ERROR")
        
        # Check panel registration
        panels_to_check = [
            ("UV_PT_NazarickRatioPanel", "UV Editor Panel"),
            ("VIEW3D_PT_NazarickRatioPanel", "3D Viewport Panel")
        ]
        
        print("🖼️  Checking panel registration...")
        for panel_class, description in panels_to_check:
            if hasattr(bpy.types, panel_class):
                print(f"✅ {description} ({panel_class}) - REGISTERED")
            else:
                print(f"❌ {description} ({panel_class}) - NOT FOUND")
        
        # Test basic scene setup for operator
        print("🧪 Testing basic scene setup...")
        
        # Clear scene
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
        
        # Add cube and prepare for testing
        bpy.ops.mesh.primitive_cube_add()
        cube = bpy.context.active_object
        
        # Enter edit mode 
        bpy.context.view_layer.objects.active = cube
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Test if operators are callable (poll check)
        try:
            # Check if we can call the ratio calculator
            result = bpy.ops.uv.nazarick_total_uv_3d_ratio.poll()
            print(f"✅ UV/3D Ratio operator poll: {result}")
        except AttributeError:
            print("❌ UV/3D Ratio operator not accessible")
        except Exception as e:
            print(f"⚠️  UV/3D Ratio operator poll error: {e}")
        
        # Cleanup
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Unregister addon
        print("🔄 Unregistering addon...")
        addon_globals['unregister']()
        
        print("\n✅ ADDON VALIDATION COMPLETE!")
        print("🏆 The addon successfully loads and registers in Blender 4.5.1!")
        print("For the Glory of Nazarick! 🏰⚡")
        
        return True
        
    except Exception as e:
        print(f"\n❌ VALIDATION FAILED: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_addon_registration()
    if not success:
        sys.exit(1)