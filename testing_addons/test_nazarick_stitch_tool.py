#!/usr/bin/env python3
"""
🏰⚡ NAZARICK STITCH TOOL COMPREHENSIVE TEST SUITE ⚡🏰
======================================================

Tests for the enhanced Nazarick Stitch Tool featuring:
- Reliable stitch geometry tagging system
- Auto-sizing based on mesh scale  
- Multiple removal modes with session tracking
- Error handling and robustness

Architect: Demiurge | Creator: Albedo | Overlord: Ainz Ooal Gown
For the Glory of the Great Tomb of Nazarick! 🏰
"""

import sys
import os
import ast
import re
from pathlib import Path

def test_stitch_tool_syntax():
    """Test that the stitch tool has valid Python syntax"""
    try:
        with open('./examples/stitch_tool/nazarick_stitch_tool.py', 'r') as f:
            code = f.read()
        ast.parse(code)
        return True, "✅ Python syntax is valid"
    except SyntaxError as e:
        return False, f"❌ Syntax error: {e}"
    except Exception as e:
        return False, f"❌ Error parsing file: {e}"

def test_enhanced_features():
    """Test that enhanced features are implemented"""
    try:
        with open('./examples/stitch_tool/nazarick_stitch_tool.py', 'r') as f:
            content = f.read()
        
        checks = []
        
        # Check for StitchGeometryManager class
        if 'class StitchGeometryManager:' in content:
            checks.append("✅ StitchGeometryManager class found")
        else:
            checks.append("❌ StitchGeometryManager class missing")
        
        # Check for tagging constants
        if 'STITCH_TAG_VERTEX_GROUP = "NAZARICK_STITCHES"' in content:
            checks.append("✅ Stitch tagging vertex group constant found")
        else:
            checks.append("❌ Stitch tagging vertex group constant missing")
        
        if 'STITCH_TAG_ATTRIBUTE = "nazarick_stitch_id"' in content:
            checks.append("✅ Stitch tagging attribute constant found")
        else:
            checks.append("❌ Stitch tagging attribute constant missing")
        
        # Check for auto-sizing functionality
        if 'get_mesh_scale_info' in content:
            checks.append("✅ Auto-sizing mesh scale calculation found")
        else:
            checks.append("❌ Auto-sizing mesh scale calculation missing")
        
        if 'use_auto_sizing: BoolProperty' in content:
            checks.append("✅ Auto-sizing property found")
        else:
            checks.append("❌ Auto-sizing property missing")
        
        # Check for enhanced removal modes
        if 'ALL_TAGGED' in content and 'LAST_SESSION' in content:
            checks.append("✅ Enhanced removal modes found")
        else:
            checks.append("❌ Enhanced removal modes missing")
        
        # Check for session tracking
        if 'create_stitch_session_id' in content:
            checks.append("✅ Session tracking functionality found")
        else:
            checks.append("❌ Session tracking functionality missing")
        
        # Check for new operator
        if 'MESH_OT_NazarickCalculateAutoSize' in content:
            checks.append("✅ Auto-size calculation operator found")
        else:
            checks.append("❌ Auto-size calculation operator missing")
        
        # Check for improved parameter ranges
        if 'soft_min=' in content and 'soft_max=' in content:
            checks.append("✅ Improved parameter ranges found")
        else:
            checks.append("❌ Improved parameter ranges missing")
        
        success = all('✅' in check for check in checks)
        return success, checks
        
    except Exception as e:
        return False, [f"❌ Error analyzing file: {e}"]

def test_error_handling():
    """Test that proper error handling is implemented"""
    try:
        with open('./examples/stitch_tool/nazarick_stitch_tool.py', 'r') as f:
            content = f.read()
        
        checks = []
        
        # Check for try-except blocks
        try_count = content.count('try:')
        except_count = content.count('except')
        
        if try_count >= 3 and except_count >= 3:
            checks.append(f"✅ Error handling found ({try_count} try blocks, {except_count} except blocks)")
        else:
            checks.append(f"❌ Insufficient error handling ({try_count} try blocks, {except_count} except blocks)")
        
        # Check for validation patterns
        if 'if not obj or obj.type != \'MESH\':' in content:
            checks.append("✅ Object type validation found")
        else:
            checks.append("❌ Object type validation missing")
        
        if 'if obj.mode != \'EDIT\':' in content:
            checks.append("✅ Edit mode validation found")
        else:
            checks.append("❌ Edit mode validation missing")
        
        # Check for proper error reporting
        if 'self.report({\'ERROR\'}' in content:
            checks.append("✅ Error reporting found")
        else:
            checks.append("❌ Error reporting missing")
        
        success = all('✅' in check for check in checks)
        return success, checks
        
    except Exception as e:
        return False, [f"❌ Error analyzing file: {e}"]

def test_ui_enhancements():
    """Test that UI enhancements are properly implemented"""
    try:
        with open('./examples/stitch_tool/nazarick_stitch_tool.py', 'r') as f:
            content = f.read()
        
        checks = []
        
        # Check for auto-sizing UI
        if 'nazarick_stitch_auto_sizing' in content:
            checks.append("✅ Auto-sizing UI property found")
        else:
            checks.append("❌ Auto-sizing UI property missing")
        
        # Check for removal mode UI
        if 'nazarick_stitch_remove_mode' in content:
            checks.append("✅ Removal mode UI property found")
        else:
            checks.append("❌ Removal mode UI property missing")
        
        # Check for improved tooltips
        tooltip_count = content.count('description=')
        if tooltip_count >= 10:
            checks.append(f"✅ Enhanced tooltips found ({tooltip_count} descriptions)")
        else:
            checks.append(f"❌ Insufficient tooltips ({tooltip_count} descriptions)")
        
        # Check for stitch info display
        if 'Tagged stitches:' in content:
            checks.append("✅ Stitch information display found")
        else:
            checks.append("❌ Stitch information display missing")
        
        success = all('✅' in check for check in checks)
        return success, checks
        
    except Exception as e:
        return False, [f"❌ Error analyzing file: {e}"]

def test_class_structure():
    """Test that all required classes are properly defined"""
    try:
        with open('./examples/stitch_tool/nazarick_stitch_tool.py', 'r') as f:
            content = f.read()
        
        checks = []
        
        # Check for all required operator classes
        required_classes = [
            'MESH_OT_NazarickCreateStitches',
            'MESH_OT_NazarickRemoveStitches', 
            'MESH_OT_NazarickCalculateAutoSize',
            'VIEW3D_PT_NazarickStitchPanel'
        ]
        
        for class_name in required_classes:
            if f'class {class_name}' in content:
                checks.append(f"✅ {class_name} class found")
            else:
                checks.append(f"❌ {class_name} class missing")
        
        # Check classes tuple
        if 'classes = (' in content:
            checks.append("✅ Classes tuple found")
            # Count classes in tuple
            classes_section = re.search(r'classes = \((.*?)\)', content, re.DOTALL)
            if classes_section:
                class_count = len([line for line in classes_section.group(1).split('\n') if line.strip() and not line.strip().startswith('#')])
                if class_count >= 4:
                    checks.append(f"✅ Classes tuple has {class_count} classes")
                else:
                    checks.append(f"❌ Classes tuple only has {class_count} classes")
        else:
            checks.append("❌ Classes tuple missing")
        
        success = all('✅' in check for check in checks)
        return success, checks
        
    except Exception as e:
        return False, [f"❌ Error analyzing file: {e}"]

def test_blender_45_compatibility():
    """Test Blender 4.5+ compatibility"""
    try:
        with open('./examples/stitch_tool/nazarick_stitch_tool.py', 'r') as f:
            content = f.read()
        
        checks = []
        
        # Check bl_info
        if '"blender": (4, 5, 0)' in content:
            checks.append("✅ Blender 4.5+ compatibility declared")
        else:
            checks.append("❌ Blender version not set to 4.5+")
        
        # Check for modern API usage
        if 'edge.link_faces' in content:
            checks.append("✅ Modern edge.link_faces API used")
        else:
            checks.append("❌ Modern edge.link_faces API not found")
        
        # Check for deprecated API absence
        if 'edge.faces' not in content:
            checks.append("✅ No deprecated edge.faces API found")
        else:
            checks.append("❌ Deprecated edge.faces API still present")
        
        # Check for proper imports
        required_imports = ['import bpy', 'import bmesh', 'from mathutils']
        for imp in required_imports:
            if imp in content:
                checks.append(f"✅ {imp} found")
            else:
                checks.append(f"❌ {imp} missing")
        
        success = all('✅' in check for check in checks)
        return success, checks
        
    except Exception as e:
        return False, [f"❌ Error analyzing file: {e}"]

def run_all_tests():
    """Run all tests and display results"""
    print("🏰⚡ NAZARICK STITCH TOOL TEST SUITE ⚡🏰")
    print("=" * 60)
    
    tests = [
        ("Python Syntax Validation", test_stitch_tool_syntax),
        ("Enhanced Features", test_enhanced_features),
        ("Error Handling", test_error_handling),
        ("UI Enhancements", test_ui_enhancements), 
        ("Class Structure", test_class_structure),
        ("Blender 4.5+ Compatibility", test_blender_45_compatibility)
    ]
    
    total_tests = 0
    passed_tests = 0
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        try:
            success, result = test_func()
            total_tests += 1
            
            if success:
                passed_tests += 1
                print(f"✅ PASS: {test_name}")
                if isinstance(result, list):
                    for item in result:
                        print(f"   {item}")
                else:
                    print(f"   {result}")
            else:
                print(f"❌ FAIL: {test_name}")
                if isinstance(result, list):
                    for item in result:
                        print(f"   {item}")
                else:
                    print(f"   {result}")
                    
        except Exception as e:
            total_tests += 1
            print(f"💥 ERROR: {test_name} - {e}")
    
    print("\n" + "🏰" + "=" * 58 + "🏰")
    print("⚡ NAZARICK STITCH TOOL TEST SUMMARY ⚡")
    print("🏰" + "=" * 58 + "🏰")
    
    print(f"📊 Tests run: {total_tests}")
    print(f"✅ Passed: {passed_tests}")
    print(f"❌ Failed: {total_tests - passed_tests}")
    
    if passed_tests == total_tests:
        print("\n🏆 ALL TESTS PASSED!")
        print("🎉 The Nazarick Stitch Tool meets the Supreme Overlord's standards!")
        print("🏰 Enhanced with reliable tagging, auto-sizing, and robust error handling!")
        print("\nFOR THE ETERNAL GLORY OF NAZARICK! 🏰⚡🏰")
        return True
    else:
        print(f"\n⚠️ {total_tests - passed_tests} test(s) failed")
        print("🛠️ The fortress requires additional attention")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)