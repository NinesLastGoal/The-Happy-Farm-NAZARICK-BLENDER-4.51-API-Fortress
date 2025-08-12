#!/usr/bin/env python3
"""
🏰⚡ NAZARICK FORTRESS TEST RUNNER ⚡🏰
====================================

Supreme test orchestration for all fortress validation systems.
Ensures every component meets the exacting standards of Nazarick.

Usage:
    python3 run_tests.py

Architect: Demiurge | Creator: Albedo | Overlord: Ainz Ooal Gown
For the Glory of the Great Tomb of Nazarick! 🏰
"""

import subprocess
import sys
import os
# Add parent directory to path to import from src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.utils.fortress_banner import display_fortress_banner, display_testing_header

def main():
    """Run all fortress validation tests"""
    # Display the magnificent fortress banner
    display_fortress_banner(compact=True)
    print()
    
    display_testing_header("FORTRESS COMPREHENSIVE VALIDATION")
    
    # Available fortress testing components
    test_suites = [
        {
            'name': 'Comprehensive Framework Testing',
            'file': 'test_comprehensive_addon_framework.py',
            'description': 'Extensible framework for testing any Blender addon compatibility'
        },
        {
            'name': 'Primary Compatibility Validation',
            'file': 'test_addon_blender45.py',
            'description': 'Main Blender 4.5+ API compatibility validation framework'
        },
        {
            'name': 'Legacy Tool Validation',
            'file': 'test_nazarick_stitch_tool.py',
            'description': 'Legacy test structure validation (addon-specific, to be sanitized)'
        },
        {
            'name': 'Real Environment Testing', 
            'file': 'test_blender_real_environment.py',
            'description': 'Real Blender 4.5+ environment compatibility testing'
        },
        {
            'name': 'Quick Validation Framework',
            'file': 'test_simple_validation.py', 
            'description': 'Rapid generic compatibility verification'
        },
        {
            'name': 'Advanced Testing Framework',
            'file': 'test_uv_addon.py',
            'description': 'Comprehensive addon testing with generic mocking (to be sanitized)'
        }
    ]
    
    total_tests = 0
    successful_tests = 0
    
    for suite in test_suites:
        if os.path.exists(suite['file']):
            print(f"\n⚡ Activating: {suite['name']}")
            print(f"📋 Description: {suite['description']}")
            print(f"🔧 Test File: {suite['file']}")
            print("─" * 60)
            
            try:
                result = subprocess.run([sys.executable, suite['file']], 
                                      capture_output=True, text=True)
                
                total_tests += 1
                
                # Display output
                if result.stdout:
                    print(result.stdout)
                if result.stderr and result.stderr.strip():
                    print("⚠️ Warnings/Errors:", result.stderr)
                
                if result.returncode == 0:
                    print(f"✅ {suite['name']} - VALIDATION SUCCESSFUL")
                    successful_tests += 1
                else:
                    print(f"❌ {suite['name']} - VALIDATION FAILED (Exit code: {result.returncode})")
                    
            except Exception as e:
                print(f"💥 Error executing {suite['name']}: {e}")
                total_tests += 1
        else:
            print(f"\n🔍 {suite['name']} - Test file not found: {suite['file']}")
    
    # Display fortress validation summary
    print("\n" + "🏰" + "="*78 + "🏰")
    print("⚡ FORTRESS VALIDATION SUMMARY ⚡")
    print("🏰" + "="*78 + "🏰")
    
    print(f"📊 Total Test Suites: {total_tests}")
    print(f"✅ Successful Validations: {successful_tests}")
    print(f"❌ Failed Validations: {total_tests - successful_tests}")
    
    if successful_tests == total_tests and total_tests > 0:
        print("\n🏆 FORTRESS STATUS: SUPREMELY OPERATIONAL ⚡")
        print("🎉 All fortress components validated successfully!")
        print("🏰 The fortress stands ready to validate all future addons!")
        print("\nFOR THE ETERNAL GLORY OF NAZARICK! 🏰⚡🏰")
        return True
    elif successful_tests > 0:
        print(f"\n⚠️ FORTRESS STATUS: PARTIALLY OPERATIONAL")
        print(f"🔧 {successful_tests}/{total_tests} fortress components operational")
        print("🛠️ Some fortress systems require attention")
        return False
    else:
        print("\n💥 FORTRESS STATUS: REQUIRES IMMEDIATE ATTENTION")
        print("🚨 Critical fortress systems need investigation")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)