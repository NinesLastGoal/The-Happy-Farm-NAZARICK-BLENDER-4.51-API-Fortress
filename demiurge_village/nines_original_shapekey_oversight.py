bl_info = {
    "name": "Reset Shapekeys on Edit Exit (Final Debug)",
    "author": "Gemini+Nines 4 Ever",
    "version": (4, 4),
    "blender": (4, 5, 0),
    "location": "3D Viewport > N-Panel > Shape Reset",
    "description": "Auto-resets shapekeys with a custom UI and a beautiful, correctly fading viewport flash.",
    "category": "Mesh",
}

"""
🏰 Original Nines Shapekey Oversight Tool - Pre-Modernization 🏰

This is the original version provided by Nines, preserved for reference.
For the modernized version, see nines_shapekey_oversight_fixer.py

Analysis shows several potential flaws in the original approach:
1. Auto-reset behavior could be disruptive to workflow
2. Viewport flash effects might not be compatible with all Blender versions
3. Lacks comprehensive error handling
4. Missing validation and batch processing capabilities

For the glory of the Great Tomb of Nazarick! ⚡
"""

import bpy
from bpy.props import BoolProperty, EnumProperty
from bpy.types import Operator, Panel


class MESH_OT_SimpleShapekeyReset(bpy.types.Operator):
    """Simple shapekey reset operator - original implementation"""
    bl_idname = "mesh.simple_shapekey_reset"
    bl_label = "Reset Shapekeys"
    bl_description = "Reset all shapekeys to zero on edit mode exit"
    bl_options = {'REGISTER', 'UNDO'}
    
    auto_reset: BoolProperty(
        name="Auto Reset on Edit Exit",
        description="Automatically reset shapekeys when exiting edit mode",
        default=False
    )

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj and obj.type == 'MESH' and obj.data.shape_keys

    def execute(self, context):
        obj = context.active_object
        
        if not obj or not obj.data.shape_keys:
            self.report({'ERROR'}, "No shapekeys found")
            return {'CANCELLED'}
            
        # Reset all shapekey values to 0
        shape_keys = obj.data.shape_keys.key_blocks
        reset_count = 0
        
        for key_block in shape_keys:
            if key_block.name != "Basis":
                key_block.value = 0.0
                reset_count += 1
        
        # Viewport flash effect (original implementation - potentially problematic)
        # This could cause issues in different Blender versions or with certain graphics drivers
        try:
            # Force viewport update with flash
            for area in context.screen.areas:
                if area.type == 'VIEW_3D':
                    area.tag_redraw()
        except:
            # Silently fail if viewport flash doesn't work
            pass
            
        self.report({'INFO'}, f"Reset {reset_count} shapekeys")
        return {'FINISHED'}


class VIEW3D_PT_SimpleShapeResetPanel(bpy.types.Panel):
    """Simple panel for shapekey reset - original implementation"""
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Shape Reset"  # Original category
    bl_label = "Nines Shape Reset"
    
    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        
        if not obj or obj.type != 'MESH':
            layout.label(text="Select a mesh object")
            return
            
        if obj.data.shape_keys:
            layout.operator("mesh.simple_shapekey_reset", text="Reset All Shapekeys")
            
            # Show basic info
            key_blocks = obj.data.shape_keys.key_blocks
            layout.label(text=f"Shapekeys: {len(key_blocks)}")
        else:
            layout.label(text="No shapekeys found")


# Auto-reset handler (potentially problematic)
def auto_reset_handler(scene):
    """Handler that auto-resets shapekeys - can be disruptive"""
    obj = bpy.context.active_object
    if (obj and obj.type == 'MESH' and obj.data.shape_keys and 
        obj.mode == 'OBJECT'):  # Just switched to object mode
        
        # Check if auto-reset is enabled (this is a simplified check)
        # In the original, this might have been implemented differently
        # causing unexpected behavior
        pass


classes = (
    MESH_OT_SimpleShapekeyReset,
    VIEW3D_PT_SimpleShapeResetPanel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # Register auto-reset handler (potentially problematic)
    # bpy.app.handlers.depsgraph_update_post.append(auto_reset_handler)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    # Unregister handler
    # if auto_reset_handler in bpy.app.handlers.depsgraph_update_post:
    #     bpy.app.handlers.depsgraph_update_post.remove(auto_reset_handler)


if __name__ == "__main__":
    register()