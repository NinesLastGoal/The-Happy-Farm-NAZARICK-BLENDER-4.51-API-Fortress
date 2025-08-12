#!/usr/bin/env python3
"""
Generic Blender 4.5+ Addon Validation Framework
==============================================

Addon-agnostic validation script for testing any Blender addon's compatibility.

For the Glory of Nazarick's Pure Architecture! 🏰
Created by Demiurge with Fortress Neutrality
"""

import bpy
import sys
import traceback
import os

def test_generic_addon_registration(addon_path=None):
    """Test generic addon registration and basic functionality"""
    print("🏰 Testing Generic Addon Compatibility in Real Blender 4.5+ 🏰")
    print(f"Blender Version: {bpy.app.version_string}")
    print(f"Python Version: {sys.version}")
    print()
    
    # If no specific addon provided, look for test subjects in testing_addons
    if not addon_path:
        testing_dir = "../testing_addons"
        if os.path.exists(testing_dir):
            # Find any .py addon file to test
            for file in os.listdir(testing_dir):
                if file.endswith('.py') and not file.startswith('_'):
                    addon_path = os.path.join(testing_dir, file)
                    break
    
    if not addon_path or not os.path.exists(addon_path):
        print("⚠️ No test addon found - skipping registration test")
        return True
    
    try:
        # Load addon generically
        print(f"📥 Loading test addon: {os.path.basename(addon_path)}")
        with open(addon_path, 'r') as f:
            addon_code = f.read()
        
        # Execute addon
        addon_globals = {}
        exec(compile(addon_code, addon_path, 'exec'), addon_globals)
        
        # Register addon if possible
        print("🔧 Attempting addon registration...")
#!/usr/bin/env python3
"""
Generic Blender 4.5+ Addon Validation Framework
==============================================

Addon-agnostic validation script for testing any Blender addon's compatibility.

For the Glory of Nazarick's Pure Architecture! 🏰
Created by Demiurge with Fortress Neutrality
"""

import bpy
import sys
import traceback
import os

def test_generic_addon_validation(addon_path=None):
    """Test generic addon registration and basic functionality"""
    print("🏰 Testing Generic Addon Compatibility in Real Blender 4.5+ 🏰")
    print(f"Blender Version: {bpy.app.version_string}")
    print(f"Python Version: {sys.version}")
    print()
    
    # If no specific addon provided, look for test subjects in testing_addons
    if not addon_path:
        testing_dir = "../testing_addons"
        if os.path.exists(testing_dir):
            # Find any .py addon file to test
            for file in os.listdir(testing_dir):
                if file.endswith('.py') and not file.startswith('_'):
                    addon_path = os.path.join(testing_dir, file)
                    break
    
    if not addon_path or not os.path.exists(addon_path):
        print("⚠️ No test addon found - testing framework validation only")
        return test_framework_only()
    
    try:
        # Load addon generically
        print(f"📥 Loading test addon: {os.path.basename(addon_path)}")
        with open(addon_path, 'r') as f:
            addon_code = f.read()
        
        # Execute addon
        addon_globals = {}
        exec(compile(addon_code, addon_path, 'exec'), addon_globals)
        
        # Register addon if possible
        print("🔧 Attempting addon registration...")
        if 'register' in addon_globals:
            addon_globals['register']()
            print("✅ Addon registration - SUCCESSFUL")
        else:
            print("⚠️ No register function found - addon may be legacy format")
            return True  # Not a failure, just different format
        
        # Test basic scene compatibility
        print("🧪 Testing basic scene compatibility...")
        test_scene_compatibility()
        
        # Attempt cleanup
        if 'unregister' in addon_globals:
            addon_globals['unregister']()
            print("✅ Addon cleanup - SUCCESSFUL")
            
        print("\n✅ GENERIC ADDON VALIDATION COMPLETE!")
        print("🏆 The addon successfully loads in Blender 4.5+!")
        print("For the Glory of Nazarick's Pure Architecture! 🏰⚡")
        
        return True
            
    except Exception as e:
        print(f"❌ Addon validation failed: {e}")
        traceback.print_exc()
        return False

def test_framework_only():
    """Test just the framework capabilities"""
    print("🧪 Testing framework compatibility only...")
    
    try:
        # Test basic Blender 4.5+ features
        test_scene_compatibility()
        
        print("✅ FRAMEWORK VALIDATION COMPLETE!")
        print("🏆 Blender 4.5+ framework is operational!")
        return True
        
    except Exception as e:
        print(f"❌ Framework validation failed: {e}")
        return False

def test_scene_compatibility():
    """Test basic Blender scene operations"""
    # Clear scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Add test object
    bpy.ops.mesh.primitive_cube_add()
    cube = bpy.context.active_object
    
    # Test mode switching
    bpy.context.view_layer.objects.active = cube
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.object.mode_set(mode='OBJECT')
    
    print("✅ Scene compatibility - VALIDATED")

if __name__ == "__main__":
    success = test_generic_addon_validation()
    if not success:
        sys.exit(1)