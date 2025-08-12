#!/usr/bin/env python3
"""
🏰⚡ NAZARICK BLENDER ADDON PACKAGER ⚡🏰

Supreme Overlord's Automated Tool for Creating Blender-Compatible ZIP Files

This tool creates properly structured ZIP files for Blender addon installation,
ensuring compliance with Nazarick Fortress specifications.
"""

import os
import sys
import zipfile
import shutil
from pathlib import Path
from typing import List, Optional


class AddonPackager:
    """
    Creates Blender-compatible ZIP packages for addons.
    """
    
    def __init__(self):
        self.excluded_patterns = [
            '__pycache__',
            '*.pyc',
            '*.pyo',
            '.DS_Store',
            'Thumbs.db',
            '.git',
            '.svn',
            '*.tmp',
            '*.temp',
            '.pytest_cache',
            '*.log'
        ]
    
    def package_addon(self, addon_path: str, output_path: Optional[str] = None) -> str:
        """
        Package an addon into a Blender-compatible ZIP file.
        
        Args:
            addon_path: Path to addon directory or Python file
            output_path: Optional output ZIP path (defaults to addon_name.zip)
            
        Returns:
            Path to created ZIP file
        """
        addon_path = Path(addon_path)
        
        if not addon_path.exists():
            raise FileNotFoundError(f"Addon path does not exist: {addon_path}")
        
        # Determine output path
        if output_path is None:
            if addon_path.is_dir():
                output_path = f"{addon_path.name}.zip"
            else:
                output_path = f"{addon_path.stem}.zip"
        
        output_path = Path(output_path)
        
        print(f"🏰 Packaging Blender addon...")
        print(f"Source: {addon_path}")
        print(f"Output: {output_path}")
        
        # Validate addon before packaging
        self._validate_addon(addon_path)
        
        # Create ZIP file
        if addon_path.is_dir():
            self._package_directory_addon(addon_path, output_path)
        else:
            self._package_single_file_addon(addon_path, output_path)
        
        # Validate the created ZIP
        self._validate_zip(output_path)
        
        file_size = output_path.stat().st_size
        print(f"✅ Addon packaged successfully!")
        print(f"📦 ZIP file: {output_path} ({file_size:,} bytes)")
        
        return str(output_path)
    
    def _validate_addon(self, addon_path: Path):
        """Validate addon structure before packaging."""
        print("🔍 Validating addon structure...")
        
        if addon_path.is_dir():
            # Multi-file addon validation
            init_file = addon_path / "__init__.py"
            if not init_file.exists():
                raise ValueError(f"Multi-file addon missing __init__.py: {addon_path}")
            
            # Check for bl_info
            with open(init_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'bl_info' not in content:
                    raise ValueError(f"__init__.py missing bl_info dictionary: {init_file}")
        
        elif addon_path.suffix == '.py':
            # Single file addon validation
            with open(addon_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'bl_info' not in content:
                    raise ValueError(f"Addon file missing bl_info dictionary: {addon_path}")
        
        else:
            raise ValueError(f"Invalid addon format: {addon_path}")
        
        print("✅ Addon structure validated")
    
    def _package_directory_addon(self, addon_dir: Path, output_path: Path):
        """Package a directory-based addon."""
        files_added = 0
        
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file_path in addon_dir.rglob('*'):
                if file_path.is_file() and not self._should_exclude(file_path):
                    # Calculate archive path (relative to parent of addon directory)
                    arcname = file_path.relative_to(addon_dir.parent)
                    zip_file.write(file_path, arcname)
                    files_added += 1
                    print(f"  Added: {arcname}")
        
        print(f"📁 Packaged {files_added} files from directory addon")
    
    def _package_single_file_addon(self, addon_file: Path, output_path: Path):
        """Package a single-file addon."""
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.write(addon_file, addon_file.name)
            print(f"  Added: {addon_file.name}")
        
        print("📄 Packaged single-file addon")
    
    def _should_exclude(self, file_path: Path) -> bool:
        """Check if file should be excluded from package."""
        import fnmatch
        
        file_str = str(file_path)
        
        for pattern in self.excluded_patterns:
            if fnmatch.fnmatch(file_str, f"*{pattern}*"):
                return True
            if fnmatch.fnmatch(file_path.name, pattern):
                return True
        
        return False
    
    def _validate_zip(self, zip_path: Path):
        """Validate the created ZIP file."""
        print("🔍 Validating created ZIP file...")
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_file:
                # Test ZIP integrity
                zip_file.testzip()
                
                # Check contents
                file_list = zip_file.namelist()
                if not file_list:
                    raise ValueError("ZIP file is empty")
                
                # Verify structure
                if len(file_list) == 1 and file_list[0].endswith('.py'):
                    # Single file addon
                    print("✅ Single-file addon structure validated")
                elif any(f.endswith('__init__.py') for f in file_list):
                    # Multi-file addon
                    print("✅ Multi-file addon structure validated")
                else:
                    raise ValueError("Invalid addon structure in ZIP")
        
        except zipfile.BadZipFile as e:
            raise ValueError(f"Invalid ZIP file created: {e}")
        
        print("✅ ZIP file validated")


def main():
    """Main CLI interface for addon packaging."""
    if len(sys.argv) < 2:
        print("🏰⚡ NAZARICK BLENDER ADDON PACKAGER ⚡🏰")
        print("Usage: python package_blender_addon.py <addon_path> [output_path]")
        print("       addon_path: Path to addon directory or .py file")
        print("       output_path: Optional output ZIP path (defaults to addon_name.zip)")
        print("")
        print("Examples:")
        print("  python package_blender_addon.py my_addon/")
        print("  python package_blender_addon.py my_addon.py")
        print("  python package_blender_addon.py my_addon/ custom_name.zip")
        sys.exit(1)
    
    addon_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        packager = AddonPackager()
        zip_path = packager.package_addon(addon_path, output_path)
        
        print("")
        print("🎯 INSTALLATION INSTRUCTIONS:")
        print("1. Open Blender 4.5.0 or higher")
        print("2. Go to Edit > Preferences > Add-ons")
        print("3. Click 'Install...' and select the ZIP file")
        print("4. Enable the addon by checking the checkbox")
        print("")
        print("🏰 For the eternal glory of Nazarick! ⚡")
        
    except Exception as e:
        print(f"❌ Error packaging addon: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()