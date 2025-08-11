#!/usr/bin/env python3
"""
Quick Test Runner for UV3D Ratio Addon
======================================

This script runs basic validation tests on the UV3D Ratio addon
before deployment to Blender 4.5.

Usage:
    python3 run_tests.py

For the Glory of Nazarick! 🏰
"""

import subprocess
import sys
import os

def main():
    """Run all available tests"""
    print("🏰 UV3D Ratio Addon - Test Runner 🏰")
    print("=" * 50)
    
    # Check if test files exist
    test_files = [
        'test_addon_blender45.py',
        'test_uv_addon.py'  # Backup comprehensive test
    ]
    
    # Run the primary Blender 4.5 compatibility test
    primary_test = 'test_addon_blender45.py'
    
    if os.path.exists(primary_test):
        print(f"🧪 Running primary test suite: {primary_test}")
        try:
            result = subprocess.run([sys.executable, primary_test], 
                                  capture_output=True, text=True)
            
            print(result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)
                
            if result.returncode == 0:
                print("\n🎉 All tests passed! Addon is ready for Blender 4.5!")
                return True
            else:
                print("\n⚠️ Some tests failed. Check output above.")
                return False
                
        except Exception as e:
            print(f"❌ Error running tests: {e}")
            return False
    else:
        print(f"❌ Test file not found: {primary_test}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)