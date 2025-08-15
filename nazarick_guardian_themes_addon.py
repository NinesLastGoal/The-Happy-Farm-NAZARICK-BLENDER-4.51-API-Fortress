"""
🏰⚡ Nazarick Guardian Theme Switcher for Blender 4.5+ ⚡🏰

Supreme UI theme management inspired by the Floor Guardians of the Great Tomb of Nazarick.
Each Guardian's unique personality and powers are reflected in carefully crafted color palettes
that enhance workflow while preserving visual clarity and Blender's interface integrity.

Features:
- 8 Guardian-inspired themes: Albedo, Shalltear, Cocytus, Aura, Mare, Demiurge, Victim, Nazarick Core
- Safe theme snapshotting and restoration system
- Selective attribute modification to preserve legibility
- JSON export functionality for theme sharing
- Modular, extensible architecture for future enhancements
- Blender 4.5+ API compatibility with resilient error handling

For the eternal glory of Nazarick! 🏰⚡

Author: Supreme Being Ainz Ooal Gown & the Guardian Alliance
License: GPL v2+ (Same as Blender)
"""

bl_info = {
    "name": "Nazarick Guardian Theme Switcher",
    "author": "Supreme Being Ainz Ooal Gown & the Guardian Alliance",
    "version": (1, 0, 0),
    "blender": (4, 5, 0),
    "location": "3D Viewport > Sidebar (N) > Nazarick > Guardians",
    "description": "Guardian-inspired UI themes for enhanced Blender workflow experience",
    "warning": "Modifies Blender theme preferences - original theme is preserved",
    "doc_url": "https://github.com/NinesLastGoal/The-Happy-Farm-NAZARICK-BLENDER-4.51-API-Fortress/blob/main/nazarick_guardian_themes_addon.py",
    "tracker_url": "https://github.com/NinesLastGoal/The-Happy-Farm-NAZARICK-BLENDER-4.51-API-Fortress/issues",
    "category": "User Interface",
    "support": "COMMUNITY",
}

import bpy
import json
import os
from bpy.types import Panel, Operator, PropertyGroup
from bpy.props import EnumProperty, StringProperty, BoolProperty
from mathutils import Color


# ============================================================================
# GUARDIAN THEME PALETTES
# ============================================================================

class NazarickGuardianPalettes:
    """
    Curated color palettes for each Floor Guardian of Nazarick.
    Each palette contains carefully selected colors that reflect the Guardian's
    personality, powers, and aesthetic while maintaining visual clarity.
    """
    
    ALBEDO = {
        "name": "Albedo - Overseer of Excellence",
        "description": "Pure white elegance with golden accents reflecting absolute perfection",
        "primary": (0.95, 0.95, 0.98, 1.0),      # Pure white
        "secondary": (0.85, 0.75, 0.25, 1.0),    # Royal gold
        "accent": (0.2, 0.2, 0.25, 1.0),         # Deep charcoal
        "selection": (1.0, 0.85, 0.3, 1.0),      # Bright gold
        "background": (0.12, 0.12, 0.15, 1.0),   # Dark elegant
        "text": (0.95, 0.95, 0.98, 1.0),         # White text
        "grid": (0.4, 0.35, 0.15, 1.0),          # Subtle gold grid
    },
    
    SHALLTEAR = {
        "name": "Shalltear - Crimson Countess",
        "description": "Blood-red elegance with silver highlights for the vampire noble",
        "primary": (0.8, 0.15, 0.2, 1.0),        # Crimson red
        "secondary": (0.75, 0.75, 0.8, 1.0),     # Silver
        "accent": (0.15, 0.05, 0.08, 1.0),       # Dark crimson
        "selection": (0.9, 0.2, 0.3, 1.0),       # Bright red
        "background": (0.08, 0.05, 0.06, 1.0),   # Deep dark
        "text": (0.9, 0.85, 0.87, 1.0),          # Light silver
        "grid": (0.4, 0.1, 0.15, 1.0),           # Dark red grid
    },
    
    COCYTUS = {
        "name": "Cocytus - Frozen Warrior",
        "description": "Icy blues and crystalline whites for the honorable insect warrior",
        "primary": (0.2, 0.4, 0.8, 1.0),         # Ice blue
        "secondary": (0.7, 0.85, 0.95, 1.0),     # Pale ice
        "accent": (0.05, 0.15, 0.3, 1.0),        # Deep ice
        "selection": (0.3, 0.6, 1.0, 1.0),       # Bright ice blue
        "background": (0.05, 0.08, 0.12, 1.0),   # Frozen dark
        "text": (0.85, 0.92, 0.98, 1.0),         # Ice white
        "grid": (0.15, 0.25, 0.4, 1.0),          # Ice grid
    },
    
    AURA = {
        "name": "Aura - Forest Guardian",
        "description": "Natural greens with earth tones for the beast tamer",
        "primary": (0.2, 0.6, 0.25, 1.0),        # Forest green
        "secondary": (0.4, 0.3, 0.15, 1.0),      # Earth brown
        "accent": (0.1, 0.25, 0.12, 1.0),        # Dark forest
        "selection": (0.4, 0.8, 0.45, 1.0),      # Bright green
        "background": (0.06, 0.08, 0.06, 1.0),   # Forest shadow
        "text": (0.85, 0.9, 0.85, 1.0),          # Natural white
        "grid": (0.15, 0.3, 0.18, 1.0),          # Forest grid
    },
    
    MARE = {
        "name": "Mare - Nature's Mage",
        "description": "Soft nature tones with magical purple accents",
        "primary": (0.4, 0.5, 0.3, 1.0),         # Sage green
        "secondary": (0.5, 0.3, 0.6, 1.0),       # Magic purple
        "accent": (0.2, 0.25, 0.15, 1.0),        # Dark sage
        "selection": (0.6, 0.4, 0.8, 1.0),       # Bright purple
        "background": (0.08, 0.09, 0.07, 1.0),   # Natural dark
        "text": (0.9, 0.92, 0.88, 1.0),          # Soft white
        "grid": (0.25, 0.3, 0.2, 1.0),           # Natural grid
    },
    
    DEMIURGE = {
        "name": "Demiurge - Infernal Strategist",
        "description": "Sophisticated dark tones with fiery orange accents",
        "primary": (0.15, 0.12, 0.1, 1.0),       # Dark sophistication
        "secondary": (0.8, 0.4, 0.1, 1.0),       # Hellfire orange
        "accent": (0.05, 0.04, 0.03, 1.0),       # Deep darkness
        "selection": (1.0, 0.5, 0.2, 1.0),       # Bright flame
        "background": (0.03, 0.02, 0.02, 1.0),   # Void black
        "text": (0.9, 0.8, 0.7, 1.0),            # Warm white
        "grid": (0.3, 0.2, 0.1, 1.0),            # Dark fire grid
    },
    
    VICTIM = {
        "name": "Victim - Angelic Sacrifice",
        "description": "Pure whites with soft golden halos and gentle warmth",
        "primary": (0.98, 0.98, 1.0, 1.0),       # Angel white
        "secondary": (0.9, 0.85, 0.6, 1.0),      # Soft gold
        "accent": (0.8, 0.8, 0.85, 1.0),         # Light gray
        "selection": (1.0, 0.9, 0.7, 1.0),       # Golden glow
        "background": (0.15, 0.15, 0.18, 1.0),   # Gentle dark
        "text": (0.95, 0.95, 1.0, 1.0),          # Pure white
        "grid": (0.5, 0.45, 0.3, 1.0),           # Golden grid
    },
    
    NAZARICK_CORE = {
        "name": "Nazarick Core - Tomb Essence",
        "description": "Deep mystical purples with ancient gold for the heart of Nazarick",
        "primary": (0.3, 0.15, 0.4, 1.0),        # Mystical purple
        "secondary": (0.7, 0.6, 0.2, 1.0),       # Ancient gold
        "accent": (0.15, 0.08, 0.2, 1.0),        # Deep purple
        "selection": (0.8, 0.7, 0.3, 1.0),       # Tomb gold
        "background": (0.05, 0.03, 0.06, 1.0),   # Tomb depths
        "text": (0.9, 0.85, 0.95, 1.0),          # Mystical white
        "grid": (0.2, 0.15, 0.25, 1.0),          # Purple grid
    }


# ============================================================================
# THEME MANAGEMENT SYSTEM
# ============================================================================

class NazarickThemeManager:
    """
    Core theme management system for safely applying and restoring Guardian themes.
    Uses selective attribute modification to preserve Blender's interface integrity.
    """
    
    # Original theme snapshot for restoration
    _original_theme_snapshot = None
    _snapshot_created = False
    
    # Safe theme attributes to modify (preserves legibility and functionality)
    SAFE_THEME_ATTRIBUTES = {
        'view_3d': [
            'back', 'grid', 'wire', 'wire_edit', 'select', 'vertex_select', 
            'edge_select', 'face_select', 'empty', 'camera', 'lamp'
        ],
        'user_interface': [
            'wcol_regular', 'wcol_tool', 'wcol_menu', 'wcol_box'
        ],
        'properties': [
            'back'
        ]
    }
    
    @classmethod
    def create_theme_snapshot(cls):
        """
        Create a snapshot of the current theme for safe restoration.
        Only captures attributes that will be modified.
        """
        if cls._snapshot_created:
            return True
            
        try:
            theme = bpy.context.preferences.themes[0]
            snapshot = {}
            
            for area_name, attributes in cls.SAFE_THEME_ATTRIBUTES.items():
                if hasattr(theme, area_name):
                    area = getattr(theme, area_name)
                    snapshot[area_name] = {}
                    
                    for attr in attributes:
                        if hasattr(area, attr):
                            attr_value = getattr(area, attr)
                            
                            # Handle color values
                            if hasattr(attr_value, '__len__') and len(attr_value) >= 3:
                                snapshot[area_name][attr] = tuple(attr_value[:4] if len(attr_value) >= 4 else list(attr_value) + [1.0])
                            elif hasattr(attr_value, 'inner'):
                                # Handle widget color structures
                                widget_colors = {}
                                for color_attr in ['outline', 'inner', 'inner_sel', 'item', 'text', 'text_sel']:
                                    if hasattr(attr_value, color_attr):
                                        color_val = getattr(attr_value, color_attr)
                                        if hasattr(color_val, '__len__') and len(color_val) >= 3:
                                            widget_colors[color_attr] = tuple(color_val[:4] if len(color_val) >= 4 else list(color_val) + [1.0])
                                snapshot[area_name][attr] = widget_colors
            
            cls._original_theme_snapshot = snapshot
            cls._snapshot_created = True
            return True
            
        except Exception as e:
            print(f"🚨 Nazarick Theme Manager: Failed to create snapshot - {e}")
            return False
    
    @classmethod
    def apply_guardian_theme(cls, guardian_name):
        """
        Apply a Guardian theme with safe attribute modification.
        
        Args:
            guardian_name (str): Name of the Guardian theme to apply
        """
        try:
            # Ensure we have a snapshot
            if not cls.create_theme_snapshot():
                return False
            
            # Get the palette
            palette = getattr(NazarickGuardianPalettes, guardian_name.upper(), None)
            if not palette:
                print(f"🚨 Guardian theme '{guardian_name}' not found")
                return False
            
            theme = bpy.context.preferences.themes[0]
            
            # Apply View 3D colors
            if hasattr(theme, 'view_3d'):
                view_3d = theme.view_3d
                
                # Safe color applications with hasattr guards
                if hasattr(view_3d, 'back'):
                    view_3d.back = palette["background"][:3]
                
                if hasattr(view_3d, 'grid'):
                    view_3d.grid = palette["grid"][:3]
                
                if hasattr(view_3d, 'select'):
                    view_3d.select = palette["selection"][:3]
                
                if hasattr(view_3d, 'wire'):
                    view_3d.wire = palette["accent"][:3]
                
                if hasattr(view_3d, 'wire_edit'):
                    view_3d.wire_edit = palette["primary"][:3]
                
                if hasattr(view_3d, 'vertex_select'):
                    view_3d.vertex_select = palette["selection"][:3]
                
                if hasattr(view_3d, 'edge_select'):
                    view_3d.edge_select = palette["selection"][:3]
                
                if hasattr(view_3d, 'face_select'):
                    # Use a more subtle version for face selection
                    face_color = [c * 0.3 for c in palette["selection"][:3]]
                    view_3d.face_select = face_color
            
            # Apply minimal UI colors (very conservative)
            if hasattr(theme, 'user_interface'):
                ui = theme.user_interface
                
                # Only modify regular widget colors slightly
                if hasattr(ui, 'wcol_regular') and hasattr(ui.wcol_regular, 'inner_sel'):
                    ui.wcol_regular.inner_sel = [c * 0.8 for c in palette["primary"][:3]] + [0.5]
            
            print(f"✨ Applied Guardian theme: {palette['name']}")
            return True
            
        except Exception as e:
            print(f"🚨 Failed to apply Guardian theme '{guardian_name}': {e}")
            return False
    
    @classmethod
    def restore_original_theme(cls):
        """
        Restore the original theme from snapshot.
        """
        if not cls._snapshot_created or not cls._original_theme_snapshot:
            print("⚠️ No theme snapshot available for restoration")
            return False
        
        try:
            theme = bpy.context.preferences.themes[0]
            
            for area_name, attributes in cls._original_theme_snapshot.items():
                if hasattr(theme, area_name):
                    area = getattr(theme, area_name)
                    
                    for attr_name, attr_value in attributes.items():
                        if hasattr(area, attr_name):
                            attr_obj = getattr(area, attr_name)
                            
                            if isinstance(attr_value, dict):
                                # Restore widget colors
                                for color_attr, color_value in attr_value.items():
                                    if hasattr(attr_obj, color_attr):
                                        setattr(attr_obj, color_attr, color_value)
                            else:
                                # Restore direct color values
                                setattr(area, attr_name, attr_value)
            
            print("✨ Original theme restored successfully")
            return True
            
        except Exception as e:
            print(f"🚨 Failed to restore original theme: {e}")
            return False
    
    @classmethod
    def export_current_theme(cls, filepath):
        """
        Export current theme attributes to JSON file.
        
        Args:
            filepath (str): Path to save the theme file
        """
        try:
            theme = bpy.context.preferences.themes[0]
            export_data = {
                'nazarick_theme_export': True,
                'version': '1.0',
                'theme_data': {}
            }
            
            for area_name, attributes in cls.SAFE_THEME_ATTRIBUTES.items():
                if hasattr(theme, area_name):
                    area = getattr(theme, area_name)
                    export_data['theme_data'][area_name] = {}
                    
                    for attr in attributes:
                        if hasattr(area, attr):
                            attr_value = getattr(area, attr)
                            
                            if hasattr(attr_value, '__len__') and len(attr_value) >= 3:
                                export_data['theme_data'][area_name][attr] = list(attr_value)
                            elif hasattr(attr_value, 'inner'):
                                # Export widget colors
                                widget_colors = {}
                                for color_attr in ['outline', 'inner', 'inner_sel', 'item', 'text', 'text_sel']:
                                    if hasattr(attr_value, color_attr):
                                        color_val = getattr(attr_value, color_attr)
                                        if hasattr(color_val, '__len__') and len(color_val) >= 3:
                                            widget_colors[color_attr] = list(color_val)
                                export_data['theme_data'][area_name][attr] = widget_colors
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            print(f"✨ Theme exported to: {filepath}")
            return True
            
        except Exception as e:
            print(f"🚨 Failed to export theme: {e}")
            return False


# ============================================================================
# BLENDER OPERATORS
# ============================================================================

class NAZARICK_OT_apply_guardian_theme(Operator):
    """Apply selected Guardian theme to Blender interface"""
    bl_idname = "nazarick.apply_guardian_theme"
    bl_label = "Apply Guardian Theme"
    bl_description = "Apply the selected Guardian's theme to enhance your Blender experience"
    bl_options = {'REGISTER', 'UNDO'}
    
    guardian_name: StringProperty(
        name="Guardian Name",
        description="Name of the Guardian theme to apply",
        default=""
    )
    
    def execute(self, context):
        if not self.guardian_name:
            self.report({'ERROR'}, "No Guardian theme specified")
            return {'CANCELLED'}
        
        success = NazarickThemeManager.apply_guardian_theme(self.guardian_name)
        
        if success:
            # Update the scene property to reflect the change
            context.scene.nazarick_guardian_theme = self.guardian_name
            self.report({'INFO'}, f"Applied Guardian theme: {self.guardian_name}")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, f"Failed to apply Guardian theme: {self.guardian_name}")
            return {'CANCELLED'}


class NAZARICK_OT_restore_original_theme(Operator):
    """Restore the original Blender theme"""
    bl_idname = "nazarick.restore_original_theme"
    bl_label = "Restore Original Theme"
    bl_description = "Restore Blender's original theme before Guardian modifications"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        success = NazarickThemeManager.restore_original_theme()
        
        if success:
            context.scene.nazarick_guardian_theme = 'ORIGINAL'
            self.report({'INFO'}, "Original theme restored successfully")
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "No original theme snapshot available")
            return {'CANCELLED'}


class NAZARICK_OT_export_theme(Operator):
    """Export current theme settings to JSON file"""
    bl_idname = "nazarick.export_theme"
    bl_label = "Export Current Theme"
    bl_description = "Export current theme attributes to a JSON file for sharing"
    bl_options = {'REGISTER'}
    
    filepath: StringProperty(
        name="File Path",
        description="Path to save the theme file",
        subtype='FILE_PATH',
        default="nazarick_theme_export.json"
    )
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
    def execute(self, context):
        success = NazarickThemeManager.export_current_theme(self.filepath)
        
        if success:
            self.report({'INFO'}, f"Theme exported to: {self.filepath}")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "Failed to export theme")
            return {'CANCELLED'}


# ============================================================================
# USER INTERFACE PANEL
# ============================================================================

class NAZARICK_PT_guardian_themes(Panel):
    """Main Guardian Themes panel in the Nazarick sidebar tab"""
    bl_label = "Guardians"
    bl_idname = "NAZARICK_PT_guardian_themes"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Nazarick"
    bl_context = "objectmode"
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='SHADING_RENDERED')
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Header with Nazarick branding
        box = layout.box()
        col = box.column(align=True)
        col.label(text="🏰 Guardian Theme Switcher ⚡", icon='WORLD')
        col.separator(factor=0.5)
        
        # Theme selection dropdown
        col.label(text="Select Guardian Theme:")
        col.prop(scene, "nazarick_guardian_theme", text="")
        col.separator()
        
        # Control buttons
        row = col.row(align=True)
        row.scale_y = 1.2
        
        # Apply theme button
        apply_op = row.operator("nazarick.apply_guardian_theme", text="Apply Theme", icon='CHECKMARK')
        apply_op.guardian_name = scene.nazarick_guardian_theme
        
        # Restore original button
        row.operator("nazarick.restore_original_theme", text="Restore", icon='RECOVER_LAST')
        
        col.separator()
        
        # Export functionality
        export_box = col.box()
        export_col = export_box.column(align=True)
        export_col.label(text="Export Current Theme:", icon='EXPORT')
        export_col.operator("nazarick.export_theme", text="Save Theme as JSON", icon='FILE_TICK')
        
        col.separator()
        
        # Information about current theme
        if hasattr(scene, 'nazarick_guardian_theme') and scene.nazarick_guardian_theme != 'ORIGINAL':
            current_theme = scene.nazarick_guardian_theme
            if hasattr(NazarickGuardianPalettes, current_theme):
                palette = getattr(NazarickGuardianPalettes, current_theme)
                
                info_box = col.box()
                info_col = info_box.column(align=True)
                info_col.label(text="Current Theme:", icon='INFO')
                info_col.label(text=palette["name"])
                
                # Description with word wrapping
                desc_lines = self.wrap_text(palette["description"], 35)
                for line in desc_lines:
                    info_col.label(text=line)
        
        col.separator()
        
        # Footer
        footer_box = col.box()
        footer_col = footer_box.column(align=True)
        footer_col.scale_y = 0.8
        footer_col.label(text="For the Glory of Nazarick! 🏰⚡")
        footer_col.label(text="Guardian Alliance v1.0")
    
    def wrap_text(self, text, max_length):
        """Simple text wrapping for descriptions"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + word) <= max_length:
                current_line += word + " "
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        
        if current_line:
            lines.append(current_line.strip())
        
        return lines


# ============================================================================
# PROPERTY DEFINITIONS
# ============================================================================

def get_guardian_theme_items(self, context):
    """Generate theme selection items for EnumProperty"""
    return [
        ('ORIGINAL', 'Original Blender', 'Restore default Blender theme', 'BLENDER', 0),
        ('ALBEDO', 'Albedo', 'Pure white elegance with golden accents', 'LIGHT_SUN', 1),
        ('SHALLTEAR', 'Shalltear', 'Blood-red elegance with silver highlights', 'HEART', 2),
        ('COCYTUS', 'Cocytus', 'Icy blues and crystalline whites', 'FREEZE', 3),
        ('AURA', 'Aura', 'Natural greens with earth tones', 'OUTLINER_OB_HAIR', 4),
        ('MARE', 'Mare', 'Soft nature tones with magical purple accents', 'OUTLINER_OB_FORCE_FIELD', 5),
        ('DEMIURGE', 'Demiurge', 'Sophisticated dark tones with fiery orange accents', 'FIRE', 6),
        ('VICTIM', 'Victim', 'Pure whites with soft golden halos', 'LIGHT_HEMI', 7),
        ('NAZARICK_CORE', 'Nazarick Core', 'Deep mystical purples with ancient gold', 'SHADERFX', 8),
    ]


def update_guardian_theme(self, context):
    """Auto-apply theme when selection changes"""
    if self.nazarick_guardian_theme == 'ORIGINAL':
        bpy.ops.nazarick.restore_original_theme()
    else:
        bpy.ops.nazarick.apply_guardian_theme(guardian_name=self.nazarick_guardian_theme)


# ============================================================================
# REGISTRATION
# ============================================================================

classes = (
    NAZARICK_OT_apply_guardian_theme,
    NAZARICK_OT_restore_original_theme,
    NAZARICK_OT_export_theme,
    NAZARICK_PT_guardian_themes,
)


def register():
    """Register addon classes and properties"""
    try:
        # Register classes
        for cls in classes:
            bpy.utils.register_class(cls)
        
        # Add scene properties
        bpy.types.Scene.nazarick_guardian_theme = EnumProperty(
            name="Guardian Theme",
            description="Select a Guardian-inspired theme for Blender",
            items=get_guardian_theme_items,
            default='ORIGINAL',
            update=update_guardian_theme
        )
        
        print("✨ Nazarick Guardian Theme Switcher registered successfully")
        
    except Exception as e:
        print(f"🚨 Failed to register Nazarick Guardian Theme Switcher: {e}")


def unregister():
    """Unregister addon classes and properties"""
    try:
        # Restore original theme before unregistering
        NazarickThemeManager.restore_original_theme()
        
        # Remove scene properties
        if hasattr(bpy.types.Scene, 'nazarick_guardian_theme'):
            del bpy.types.Scene.nazarick_guardian_theme
        
        # Unregister classes
        for cls in reversed(classes):
            bpy.utils.unregister_class(cls)
        
        print("✨ Nazarick Guardian Theme Switcher unregistered successfully")
        
    except Exception as e:
        print(f"🚨 Failed to unregister Nazarick Guardian Theme Switcher: {e}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    register()


# ============================================================================
# FUTURE ENHANCEMENT IDEAS & DOCUMENTATION
# ============================================================================

"""
🚀 FUTURE CUSTOMIZATION POSSIBILITIES 🚀

The modular architecture of this addon allows for numerous enhancements:

1. ICON OVERLAYS:
   - Custom Guardian icons for buttons and panels
   - Animated Guardian emblems in the interface
   - Context-sensitive Guardian imagery

2. ANIMATED TRANSITIONS:
   - Smooth color transitions between themes
   - Fade effects when switching themes
   - Animated accents and highlights

3. PER-WORKSPACE THEMING:
   - Different Guardian themes for different workspaces
   - Automatic theme switching based on workspace context
   - Workflow-specific color schemes

4. ACCENT COLOR SLIDERS:
   - User-customizable accent colors within Guardian themes
   - Real-time color adjustment with live preview
   - Save custom Guardian variations

5. EXTENDED THEME ELEMENTS:
   - Custom node editor colors
   - Shader editor enhancements
   - Compositor theming integration

6. SEASONAL VARIATIONS:
   - Holiday-themed Guardian palettes
   - Time-of-day adaptive themes
   - Special event commemorative themes

7. GUARDIAN VOICE INTEGRATION:
   - Theme selection confirmation messages
   - Guardian-specific status notifications
   - Audio feedback for theme changes

8. ADVANCED EXPORT/IMPORT:
   - Share Guardian themes with the community
   - Import custom Guardian variations
   - Theme marketplace integration

9. PERFORMANCE MONITORING:
   - Theme performance impact analysis
   - Memory usage optimization
   - GPU rendering enhancement tracking

10. COLLABORATION FEATURES:
    - Team-synchronized theme preferences
    - Project-specific Guardian themes
    - Multi-user workflow integration

DEPLOYMENT INSTRUCTIONS:
=======================

1. Installation:
   - Copy nazarick_guardian_themes_addon.py to Blender's addons folder
   - Enable in Preferences > Add-ons > User Interface
   - Restart Blender for full compatibility

2. Usage:
   - Open 3D Viewport sidebar (N key)
   - Navigate to "Nazarick" tab
   - Select desired Guardian theme from dropdown
   - Use "Apply Theme" or auto-apply will engage
   - "Restore" button returns to original theme

3. Export/Import:
   - Export current theme settings via "Save Theme as JSON"
   - Share theme files with other Nazarick users
   - Import requires manual JSON loading (future enhancement)

TESTING CHECKLIST:
=================

□ Addon loads without errors in Blender 4.5+
□ All Guardian themes apply correctly
□ Original theme restoration works
□ Theme export functionality saves valid JSON
□ UI panel displays properly in 3D Viewport sidebar
□ EnumProperty updates trigger theme changes
□ No interference with other Blender functionality
□ Theme changes preserve across Blender sessions
□ Error handling prevents crashes
□ Console messages provide clear feedback

GUARDIAN ALLIANCE COMPATIBILITY:
===============================

This addon follows all Nazarick Fortress development standards:

✅ Blender 4.5+ API compliance
✅ Comprehensive error handling with hasattr guards
✅ Modular, extensible architecture
✅ Guardian Alliance naming conventions
✅ Safe theme attribute modification
✅ Original theme preservation
✅ User-friendly interface design
✅ Future enhancement documentation
✅ Deployment and testing guidelines
✅ Community sharing capabilities

For the eternal glory of Nazarick! 🏰⚡

"In theme design, as in all endeavors, we pursue the absolute perfection
befitting the Great Tomb of Nazarick. Every color, every accent, every
visual element must contribute to the supreme user experience worthy
of the Floor Guardians themselves."

- Supreme Being Ainz Ooal Gown
"""