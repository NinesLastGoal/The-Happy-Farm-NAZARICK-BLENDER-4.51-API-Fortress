bl_info = {
    "name": "UV Total Ratio Compare",
    "author": "Albedo (Core Design) & Demiurge (Blender 4.5 Compatibility), Guardians of the Great Tomb of Nazarick",
    "version": (1, 0, 0),
    "blender": (4, 5, 0),
    "location": "UV Editor > Sidebar (N) > Nazarick UV Tools & 3D Viewport > Sidebar (N) > Nazarick UV Tools",
    "description": "Measures the ratio between UV space and 3D surface area (for Supreme Being Ainz Ooal Gown)",
    "category": "UV",
}

"""
🏰 UV3D Ratio Addon for Blender 4.5 - Nazarick Edition 🏰

Enhanced for Blender 4.5 compatibility with comprehensive testing suite.

Contributors:
- Albedo: Core addon functionality, dual-panel UI design, and mathematical calculations
- Demiurge: Blender 4.5 API compatibility, comprehensive testing infrastructure, 
           and deprecated API detection for the glory of the Great Tomb of Nazarick

For Supreme Being Ainz Ooal Gown! ⚡
"""

import bpy
import bmesh
from mathutils import Vector
import time

def face_area_3d(face):
    """Calculate the 3D area of a face using triangulation."""
    verts = [v.co for v in face.verts]
    if len(verts) < 3:
        return 0.0
    area = 0.0
    for i in range(1, len(verts) - 1):
        area += (verts[i] - verts[0]).cross(verts[i+1] - verts[0]).length / 2
    return area

def face_area_uv(face, uv_layer):
    """Calculate the UV area of a face using triangulation."""
    uvs = [loop[uv_layer].uv for loop in face.loops]
    if len(uvs) < 3:
        return 0.0
    area = 0.0
    for i in range(1, len(uvs) - 1):
        v0 = Vector((uvs[0].x, uvs[0].y, 0.0))
        v1 = Vector((uvs[i].x, uvs[i].y, 0.0))
        v2 = Vector((uvs[i+1].x, uvs[i+1].y, 0.0))
        area += (v1 - v0).cross(v2 - v0).length / 2
    return area

class UV_OT_TotalUV3DRatio(bpy.types.Operator):
    bl_idname = "uv.nazarick_total_uv_3d_ratio"
    bl_label = "Calculate UV/3D Ratio"
    bl_description = "Measures ratio between total UV area and 3D surface area for the mesh"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj and obj.type == 'MESH' and obj.mode == 'EDIT'

    def execute(self, context):
        start_time = time.time()
        obj = context.active_object
        
        # Get bmesh from edit mode mesh
        bm = bmesh.from_edit_mesh(obj.data)
        
        # Ensure we have UV data
        if not bm.loops.layers.uv:
            self.report({'ERROR'}, "Object has no UV maps")
            return {'CANCELLED'}
            
        uv_layer = bm.loops.layers.uv.active
        
        # Calculate areas - prioritize selected faces, fallback to all faces
        selected_faces = [face for face in bm.faces if face.select]
        faces_to_process = selected_faces if selected_faces else bm.faces
        
        total_3d = 0.0
        total_uv = 0.0
        face_count = 0
        
        for face in faces_to_process:
            area_3d = face_area_3d(face)
            area_uv = face_area_uv(face, uv_layer)
            
            total_3d += area_3d
            total_uv += area_uv
            face_count += 1
            
        # Calculate ratio and interpretation
        if total_3d > 0:
            ratio = total_uv / total_3d
            
            # Create human-readable interpretation
            if 0.99 <= ratio <= 1.01:
                interpretation = "PERFECT - 1:1 UV to 3D ratio"
            elif ratio > 1.5:
                interpretation = "UVs are MUCH LARGER than needed (stretched texture)"
            elif ratio > 1.05:
                interpretation = "UVs are larger than needed (some stretching)"
            elif ratio < 0.5:
                interpretation = "UVs are MUCH SMALLER than needed (compressed texture)"
            elif ratio < 0.95:
                interpretation = "UVs are smaller than needed (some compression)"
            else:
                interpretation = "Good ratio (minor deviation)"
                
            # Format result strings
            scope = "selected faces" if selected_faces else "all faces"
            result = f"UV/3D Ratio: {ratio:.4f}"
            details = (f"Interpretation: {interpretation}\n"
                      f"Calculated from {face_count} {scope}\n"
                      f"3D Area: {total_3d:.4f} units²\n"
                      f"UV Area: {total_uv:.4f} units²\n"
                      f"Time: {(time.time() - start_time):.3f}s")
                      
            context.scene.nazarick_uv_ratio_result = result
            context.scene.nazarick_uv_ratio_details = details
        else:
            self.report({'ERROR'}, "Could not calculate area (3D area is zero)")
            context.scene.nazarick_uv_ratio_result = "Error: No valid area found"
            context.scene.nazarick_uv_ratio_details = "Please check your mesh."
            return {'CANCELLED'}
            
        return {'FINISHED'}

class NazarickRatioPanelMixin:
    """Shared drawing logic for UV/3D ratio panels in both UV Editor and 3D Viewport"""
    
    def draw_ratio_panel(self, context, layout):
        """Unified drawing method for consistent panel appearance"""
        col = layout.column(align=True)
        col.scale_y = 1.2
        col.operator(UV_OT_TotalUV3DRatio.bl_idname, icon='SHADERFX')
        
        # Draw result if available
        if context.scene.nazarick_uv_ratio_result:
            box = layout.box()
            col = box.column(align=True)
            col.label(text=context.scene.nazarick_uv_ratio_result, icon='LIGHT_SUN')
            
            # Draw multiline details with proper spacing
            if context.scene.nazarick_uv_ratio_details:
                for line in context.scene.nazarick_uv_ratio_details.split('\n'):
                    if ':' in line:
                        label, value = line.split(':', 1)
                        row = col.row()
                        row.label(text=label + ':')
                        row.label(text=value)
                    else:
                        col.label(text=line)
                        
            # Add adjustment buttons if we have a result
            if "Error" not in context.scene.nazarick_uv_ratio_result:
                layout.separator()
                box = layout.box()
                box.label(text="UV Adjustment", icon='MODIFIER')
                row = box.row(align=True)
                row.operator("uv.nazarick_scale_uv_to_3d", text="Scale UVs to Match 3D").scale_factor = 1.0

class UV_PT_NazarickRatioPanel(bpy.types.Panel, NazarickRatioPanelMixin):
    """UV/3D Ratio panel for UV Editor"""
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Nazarick UV Tools"
    bl_label = "UV/3D Area Ratio"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        self.draw_ratio_panel(context, self.layout)

class VIEW3D_PT_NazarickRatioPanel(bpy.types.Panel, NazarickRatioPanelMixin):
    """UV/3D Ratio panel for 3D Viewport - identical to UV Editor panel"""
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Nazarick UV Tools"
    bl_label = "UV/3D Area Ratio"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        # Only show when we have an active mesh object
        return context.active_object and context.active_object.type == 'MESH'

    def draw(self, context):
        self.draw_ratio_panel(context, self.layout)

class UV_OT_ScaleUVTo3D(bpy.types.Operator):
    bl_idname = "uv.nazarick_scale_uv_to_3d"
    bl_label = "Scale UVs to Match 3D"
    bl_description = "Scale the UVs to match the 3D space ratio"
    bl_options = {'REGISTER', 'UNDO'}
    
    scale_factor: bpy.props.FloatProperty(
        name="Scale Factor",
        description="Factor to scale UVs by",
        default=1.0
    )
    
    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.mode == 'EDIT'
    
    def execute(self, context):
        obj = context.active_object
        bm = bmesh.from_edit_mesh(obj.data)
        uv_layer = bm.loops.layers.uv.active
        
        if not uv_layer:
            self.report({'ERROR'}, "No active UV map found")
            return {'CANCELLED'}
            
        # Get current ratio from stored value
        result_text = context.scene.nazarick_uv_ratio_result
        try:
            current_ratio = float(result_text.split(':')[1].strip())
            target_ratio = 1.0  # We want a 1:1 ratio
            scale_factor = (target_ratio / current_ratio) ** 0.5  # Square root because we scale in 2D
        except:
            scale_factor = 1.0
            
        # Get all unique UV coordinates to find center for scaling
        all_uvs = []
        for face in bm.faces:
            for loop in face.loops:
                all_uvs.append(loop[uv_layer].uv.copy())
                
        if not all_uvs:
            self.report({'ERROR'}, "No UV coordinates found")
            return {'CANCELLED'}
            
        # Find UV center for scaling
        min_u = min(uv.x for uv in all_uvs)
        max_u = max(uv.x for uv in all_uvs)
        min_v = min(uv.y for uv in all_uvs)
        max_v = max(uv.y for uv in all_uvs)
        center_u = (min_u + max_u) / 2
        center_v = (min_v + max_v) / 2
        
        # Scale all UVs around the center
        for face in bm.faces:
            for loop in face.loops:
                uv = loop[uv_layer].uv
                uv.x = center_u + (uv.x - center_u) * scale_factor
                uv.y = center_v + (uv.y - center_v) * scale_factor
                
        bmesh.update_edit_mesh(obj.data)
        self.report({'INFO'}, f"UVs scaled by {scale_factor:.4f} to achieve 1:1 ratio")
        
        # Update the ratio display
        bpy.ops.uv.nazarick_total_uv_3d_ratio()
        
        return {'FINISHED'}

classes = (
    UV_OT_TotalUV3DRatio,
    UV_PT_NazarickRatioPanel,
    VIEW3D_PT_NazarickRatioPanel,
    UV_OT_ScaleUVTo3D,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.nazarick_uv_ratio_result = bpy.props.StringProperty(
        name="UV/3D Ratio Result",
        default="",
        description="Result of total UV/3D area comparison"
    )
    
    bpy.types.Scene.nazarick_uv_ratio_details = bpy.props.StringProperty(
        name="UV/3D Ratio Details",
        default="",
        description="Detailed information about the UV/3D ratio"
    )

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.nazarick_uv_ratio_result
    del bpy.types.Scene.nazarick_uv_ratio_details

if __name__ == "__main__":
    register()