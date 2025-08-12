bl_info = {
    "name": "Nines Shapekey Oversight Fixer",
    "author": "Nines Own Goal, Modernized by Demiurge for the Great Tomb of Nazarick",
    "version": (1, 0, 0),
    "blender": (4, 5, 0),
    "location": "3D Viewport > Sidebar (N) > Nazarick Tools",
    "description": "Comprehensive shapekey management and reset tool for mesh objects",
    "category": "Mesh",
}

"""
🏰 Nines Shapekey Oversight Fixer for Blender 4.5 - Nazarick Edition 🏰

A comprehensive shapekey management tool that allows users to:
- Reset all shapekeys to their base state
- Remove problematic shapekeys
- Validate shapekey data integrity
- Batch operations on multiple objects

Legacy tool modernized for Blender 4.5+ compatibility by Demiurge
For the glory of the Great Tomb of Nazarick! ⚡
"""

import bpy
import bmesh
from mathutils import Vector
from bpy.props import BoolProperty, EnumProperty, StringProperty
from bpy.types import Operator, Panel


class MESH_OT_NazarickShapekeyReset(bpy.types.Operator):
    """Reset all shapekeys on the selected mesh to their base state"""
    bl_idname = "mesh.nazarick_shapekey_reset"
    bl_label = "Reset All Shapekeys"
    bl_description = "Reset all shapekeys to their base state (0.0 value)"
    bl_options = {'REGISTER', 'UNDO'}
    
    reset_mode: EnumProperty(
        name="Reset Mode",
        description="How to reset the shapekeys",
        items=[
            ('VALUES', "Reset Values", "Reset all shapekey values to 0.0"),
            ('REMOVE', "Remove All", "Remove all shapekeys completely"),
            ('SELECTIVE', "Selective Reset", "Reset only selected shapekeys"),
        ],
        default='VALUES'
    )
    
    confirm_operation: BoolProperty(
        name="Confirm Operation",
        description="Confirm that you want to perform this operation",
        default=False
    )

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and obj.type == 'MESH' and 
                obj.data.shape_keys and 
                obj.mode in {'OBJECT', 'EDIT'})

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Shapekey Reset Operation", icon='WARNING')
        layout.prop(self, "reset_mode", expand=True)
        layout.prop(self, "confirm_operation")
        
        obj = context.active_object
        if obj and obj.data.shape_keys:
            shape_keys = obj.data.shape_keys.key_blocks
            layout.label(text=f"Target Object: {obj.name}")
            layout.label(text=f"Shapekeys Found: {len(shape_keys)}")

    def execute(self, context):
        if not self.confirm_operation:
            self.report({'ERROR'}, "Operation cancelled: Please confirm the operation")
            return {'CANCELLED'}
            
        obj = context.active_object
        shape_keys = obj.data.shape_keys
        
        if not shape_keys:
            self.report({'ERROR'}, "No shapekeys found on object")
            return {'CANCELLED'}
            
        key_blocks = shape_keys.key_blocks
        original_count = len(key_blocks)
        
        if self.reset_mode == 'VALUES':
            # Reset all shapekey values to 0.0
            reset_count = 0
            for key_block in key_blocks:
                if key_block.name != "Basis":  # Don't modify the basis shape
                    key_block.value = 0.0
                    reset_count += 1
            
            self.report({'INFO'}, f"Reset {reset_count} shapekey values to 0.0")
            
        elif self.reset_mode == 'REMOVE':
            # Remove all shapekeys except Basis
            remove_count = 0
            # Work backwards to avoid index issues
            for i in range(len(key_blocks) - 1, 0, -1):  # Skip index 0 (Basis)
                obj.shape_key_remove(key_blocks[i])
                remove_count += 1
            
            self.report({'INFO'}, f"Removed {remove_count} shapekeys")
            
        elif self.reset_mode == 'SELECTIVE':
            # For now, this does the same as VALUES - could be extended for UI selection
            reset_count = 0
            for key_block in key_blocks:
                if key_block.name != "Basis" and key_block.value != 0.0:
                    key_block.value = 0.0
                    reset_count += 1
            
            self.report({'INFO'}, f"Selectively reset {reset_count} non-zero shapekeys")
        
        # Force update
        context.view_layer.update()
        
        return {'FINISHED'}


class MESH_OT_NazarickShapekeyValidate(bpy.types.Operator):
    """Validate shapekey data integrity and report issues"""
    bl_idname = "mesh.nazarick_shapekey_validate"
    bl_label = "Validate Shapekeys"
    bl_description = "Check shapekey data for potential issues"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and obj.type == 'MESH' and obj.data.shape_keys)

    def execute(self, context):
        obj = context.active_object
        shape_keys = obj.data.shape_keys
        key_blocks = shape_keys.key_blocks
        
        issues = []
        warnings = []
        
        # Check for basic issues
        if len(key_blocks) == 0:
            issues.append("No shapekeys found")
            
        basis_key = None
        for key_block in key_blocks:
            if key_block.name == "Basis":
                basis_key = key_block
                break
                
        if not basis_key:
            issues.append("No Basis shapekey found")
        
        # Check vertex count consistency
        mesh_vert_count = len(obj.data.vertices)
        for i, key_block in enumerate(key_blocks):
            if len(key_block.data) != mesh_vert_count:
                issues.append(f"Shapekey '{key_block.name}' has {len(key_block.data)} vertices, mesh has {mesh_vert_count}")
        
        # Check for problematic values
        extreme_values = []
        for key_block in key_blocks:
            if key_block.name != "Basis":
                if key_block.value < -1.0 or key_block.value > 1.0:
                    extreme_values.append(f"'{key_block.name}': {key_block.value:.3f}")
                    
        if extreme_values:
            warnings.append(f"Extreme shapekey values found: {', '.join(extreme_values)}")
        
        # Report results
        if issues:
            self.report({'ERROR'}, f"Issues found: {'; '.join(issues)}")
        elif warnings:
            self.report({'WARNING'}, f"Warnings: {'; '.join(warnings)}")
        else:
            self.report({'INFO'}, f"Validation passed: {len(key_blocks)} shapekeys are healthy")
            
        return {'FINISHED'}


class MESH_OT_NazarickShapekeyBatchProcess(bpy.types.Operator):
    """Batch process shapekeys on multiple selected objects"""
    bl_idname = "mesh.nazarick_shapekey_batch_process"
    bl_label = "Batch Process Shapekeys"
    bl_description = "Apply shapekey operations to all selected mesh objects"
    bl_options = {'REGISTER', 'UNDO'}
    
    operation: EnumProperty(
        name="Batch Operation",
        description="Operation to apply to all selected objects",
        items=[
            ('RESET_VALUES', "Reset Values", "Reset all shapekey values to 0.0"),
            ('VALIDATE', "Validate All", "Validate shapekeys on all objects"),
            ('REMOVE_EMPTY', "Remove Empty", "Remove shapekeys with no deformation"),
        ],
        default='RESET_VALUES'
    )

    @classmethod
    def poll(cls, context):
        return len([obj for obj in context.selected_objects if obj.type == 'MESH']) > 0

    def execute(self, context):
        mesh_objects = [obj for obj in context.selected_objects if obj.type == 'MESH']
        processed_count = 0
        
        # Store original active object for restoration
        original_active = context.view_layer.objects.active
        
        try:
            for obj in mesh_objects:
                if not obj.data.shape_keys:
                    continue
                    
                # Thread safety: ensure single active object processing
                context.view_layer.objects.active = obj
                context.view_layer.update()  # Force context update
                
                if self.operation == 'RESET_VALUES':
                    key_blocks = obj.data.shape_keys.key_blocks
                    for key_block in key_blocks:
                        if key_block.name != "Basis":
                            key_block.value = 0.0
                    processed_count += 1
                    
                elif self.operation == 'VALIDATE':
                    # Just count objects with shapekeys for validation
                    processed_count += 1
                    
                elif self.operation == 'REMOVE_EMPTY':
                    # Remove shapekeys that have minimal deformation
                    key_blocks = obj.data.shape_keys.key_blocks
                    removed_keys = []
                    
                    # Safe iteration: work backwards to avoid index issues
                    for i in range(len(key_blocks) - 1, 0, -1):  # Skip Basis
                        key_block = key_blocks[i]
                        # Simple check: if all vertices are very close to basis
                        basis_data = key_blocks[0].data
                        key_data = key_block.data
                        
                        max_distance = 0.0
                        for j, (basis_vert, key_vert) in enumerate(zip(basis_data, key_data)):
                            distance = (Vector(basis_vert.co) - Vector(key_vert.co)).length
                            max_distance = max(max_distance, distance)
                        
                        # If max deformation is less than 0.001 units, consider it empty
                        if max_distance < 0.001:
                            removed_keys.append(key_block.name)
                            obj.shape_key_remove(key_block)
                    
                    if removed_keys:
                        print(f"Removed empty shapekeys from {obj.name}: {', '.join(removed_keys)}")
                        
                    processed_count += 1
                    
        finally:
            # Restore original active object
            if original_active:
                context.view_layer.objects.active = original_active
                context.view_layer.update()
        
        self.report({'INFO'}, f"Batch operation '{self.operation}' completed on {processed_count} objects")
        return {'FINISHED'}


class VIEW3D_PT_NazarickShapekeyPanel(bpy.types.Panel):
    """Shapekey management panel in 3D Viewport"""
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Nazarick Tools"
    bl_label = "Nines Shapekey Oversight"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'MESH'

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        
        if not obj or obj.type != 'MESH':
            layout.label(text="Select a mesh object", icon='ERROR')
            return
            
        # Shapekey information
        shape_keys = obj.data.shape_keys
        
        col = layout.column(align=True)
        if shape_keys:
            key_blocks = shape_keys.key_blocks
            col.label(text=f"Shapekeys: {len(key_blocks)}", icon='SHAPEKEY_DATA')
            
            # Show active shapekey values if any are non-zero
            active_keys = [k for k in key_blocks if k.name != "Basis" and k.value != 0.0]
            if active_keys:
                box = col.box()
                box.label(text="Active Shapekeys:", icon='RADIOBUT_ON')
                for key in active_keys[:5]:  # Limit to first 5
                    row = box.row()
                    row.label(text=key.name)
                    row.label(text=f"{key.value:.3f}")
                if len(active_keys) > 5:
                    box.label(text=f"... and {len(active_keys) - 5} more")
        else:
            col.label(text="No shapekeys found", icon='SHAPEKEY_DATA')
        
        layout.separator()
        
        # Main operations
        col = layout.column(align=True)
        col.scale_y = 1.2
        
        if shape_keys:
            col.operator("mesh.nazarick_shapekey_reset", icon='RECOVER_LAST')
            col.operator("mesh.nazarick_shapekey_validate", icon='CHECKMARK')
        else:
            col.label(text="No shapekeys to manage", icon='INFO')
        
        layout.separator()
        
        # Batch operations
        batch_box = layout.box()
        batch_box.label(text="Batch Operations", icon='MODIFIER')
        
        selected_meshes = [obj for obj in context.selected_objects if obj.type == 'MESH']
        batch_box.label(text=f"Selected mesh objects: {len(selected_meshes)}")
        
        if len(selected_meshes) > 1:
            batch_box.operator("mesh.nazarick_shapekey_batch_process", icon='MOD_DATA_TRANSFER')
        else:
            batch_box.label(text="Select multiple meshes for batch ops", icon='INFO')


classes = (
    MESH_OT_NazarickShapekeyReset,
    MESH_OT_NazarickShapekeyValidate,
    MESH_OT_NazarickShapekeyBatchProcess,
    VIEW3D_PT_NazarickShapekeyPanel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()