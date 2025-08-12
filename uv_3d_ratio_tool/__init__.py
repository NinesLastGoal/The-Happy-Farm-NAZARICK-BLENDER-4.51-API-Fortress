"""
UV/3D Ratio Analysis Tool - Blender 4.5+ Addon
=============================================

A sleek and efficient addon for analyzing 3D surface area to UV area ratios
with optional Geometry Nodes integration.

Features:
- Calculate 3D surface area to UV area ratio for active mesh objects
- Minimal UI panel in 3D View sidebar (N-panel)
- Toggle switch for Geometry Nodes custom attribute integration
- Efficient code with Blender 4.5 API compatibility
- Minimal dependencies and overhead

Author: Created for Blender 4.5+ API compatibility
License: Same as Blender (GPL v2 or later)
"""

bl_info = {
    "name": "UV/3D Ratio Analysis Tool",
    "author": "Blender 4.5+ Development Team",
    "version": (1, 0, 0),
    "blender": (4, 5, 0),
    "location": "3D Viewport > Sidebar (N) > UV/3D Ratio",
    "description": "Analyze 3D surface area to UV area ratios with optional Geometry Nodes integration",
    "category": "UV",
    "doc_url": "",
    "tracker_url": "",
    "support": "COMMUNITY",
}

import bpy
import bmesh
import math
from mathutils import Vector


def calculate_3d_surface_area(mesh_object):
    """
    Calculate the total 3D surface area of a mesh object.
    
    Args:
        mesh_object: Blender mesh object in edit mode
        
    Returns:
        float: Total 3D surface area in Blender units squared
    """
    # Get bmesh representation from edit mode
    bm = bmesh.from_edit_mesh(mesh_object.data)
    
    total_area = 0.0
    
    # Calculate area for each face
    for face in bm.faces:
        if face.is_valid and len(face.verts) >= 3:
            # Calculate face area using triangulation
            verts = [v.co for v in face.verts]
            face_area = 0.0
            
            # Triangulate the face and sum triangle areas
            for i in range(1, len(verts) - 1):
                # Vector cross product gives twice the triangle area
                v1 = verts[i] - verts[0]
                v2 = verts[i + 1] - verts[0]
                triangle_area = v1.cross(v2).length * 0.5
                face_area += triangle_area
            
            total_area += face_area
    
    return total_area


def calculate_uv_area(mesh_object):
    """
    Calculate the total UV area of a mesh object.
    
    Args:
        mesh_object: Blender mesh object in edit mode
        
    Returns:
        float: Total UV area in UV space units squared
    """
    # Get bmesh representation from edit mode
    bm = bmesh.from_edit_mesh(mesh_object.data)
    
    # Check if UV data exists
    if not bm.loops.layers.uv.active:
        return 0.0
    
    uv_layer = bm.loops.layers.uv.active
    total_uv_area = 0.0
    
    # Calculate UV area for each face
    for face in bm.faces:
        if face.is_valid and len(face.loops) >= 3:
            # Get UV coordinates for this face
            uv_coords = [loop[uv_layer].uv for loop in face.loops]
            face_uv_area = 0.0
            
            # Triangulate the UV face and sum triangle areas
            for i in range(1, len(uv_coords) - 1):
                # Convert to 3D vectors for cross product calculation
                uv0 = Vector((uv_coords[0].x, uv_coords[0].y, 0.0))
                uv1 = Vector((uv_coords[i].x, uv_coords[i].y, 0.0))
                uv2 = Vector((uv_coords[i + 1].x, uv_coords[i + 1].y, 0.0))
                
                # Calculate triangle area using cross product
                v1 = uv1 - uv0
                v2 = uv2 - uv0
                triangle_area = v1.cross(v2).length * 0.5
                face_uv_area += triangle_area
            
            total_uv_area += face_uv_area
    
    return total_uv_area


class UV3D_OT_CalculateRatio(bpy.types.Operator):
    """Calculate UV to 3D surface area ratio for the active mesh object"""
    bl_idname = "uv3d.calculate_ratio"
    bl_label = "Calculate UV/3D Ratio"
    bl_description = "Calculate the ratio between UV area and 3D surface area"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        """Check if operator can be executed"""
        return (context.active_object and 
                context.active_object.type == 'MESH' and 
                context.active_object.mode == 'EDIT')

    def execute(self, context):
        """Execute the ratio calculation"""
        mesh_obj = context.active_object
        
        try:
            # Calculate areas
            surface_area_3d = calculate_3d_surface_area(mesh_obj)
            uv_area = calculate_uv_area(mesh_obj)
            
            # Validate results
            if surface_area_3d <= 0:
                self.report({'ERROR'}, "Invalid 3D surface area (zero or negative)")
                return {'CANCELLED'}
            
            if uv_area <= 0:
                self.report({'ERROR'}, "Invalid UV area - check if object has UV mapping")
                return {'CANCELLED'}
            
            # Calculate ratio
            ratio = uv_area / surface_area_3d
            
            # Store results in scene properties
            scene = context.scene
            scene.uv3d_ratio_value = ratio
            scene.uv3d_surface_area = surface_area_3d
            scene.uv3d_uv_area = uv_area
            
            # Update custom attribute if toggle is enabled
            if scene.uv3d_enable_geonode_attr:
                self._update_geometry_node_attribute(mesh_obj, ratio)
            
            self.report({'INFO'}, f"UV/3D Ratio: {ratio:.4f}")
            
        except Exception as e:
            self.report({'ERROR'}, f"Calculation failed: {str(e)}")
            return {'CANCELLED'}
        
        return {'FINISHED'}
    
    def _update_geometry_node_attribute(self, mesh_obj, ratio_value):
        """Update the custom attribute for Geometry Nodes"""
        try:
            # Ensure we're in object mode to modify attributes
            current_mode = mesh_obj.mode
            if current_mode != 'OBJECT':
                bpy.ops.object.mode_set(mode='OBJECT')
            
            # Get or create the custom attribute
            mesh_data = mesh_obj.data
            attr_name = "UV_3D_Ratio"
            
            # Remove existing attribute if it exists
            if attr_name in mesh_data.attributes:
                mesh_data.attributes.remove(mesh_data.attributes[attr_name])
            
            # Create new float attribute
            attribute = mesh_data.attributes.new(attr_name, 'FLOAT', 'FACE')
            
            # Set the ratio value for all faces
            for i in range(len(mesh_data.polygons)):
                attribute.data[i].value = ratio_value
            
            # Return to original mode
            if current_mode != 'OBJECT':
                bpy.ops.object.mode_set(mode=current_mode)
                
        except Exception as e:
            print(f"Warning: Failed to update Geometry Node attribute: {e}")


class UV3D_PT_RatioPanel(bpy.types.Panel):
    """UI Panel for UV/3D Ratio Analysis in 3D Viewport sidebar"""
    bl_label = "UV/3D Ratio"
    bl_idname = "UV3D_PT_ratio_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "UV/3D Ratio"
    
    @classmethod
    def poll(cls, context):
        """Only show panel when there's an active mesh object"""
        return (context.active_object and 
                context.active_object.type == 'MESH')

    def draw(self, context):
        """Draw the panel UI"""
        layout = self.layout
        scene = context.scene
        
        # Main calculation button
        col = layout.column(align=True)
        col.scale_y = 1.2
        col.operator("uv3d_ratio.calculate", icon='UV')
        
        # Geometry Nodes integration toggle
        layout.separator()
        box = layout.box()
        box.label(text="Geometry Nodes Integration", icon='GEOMETRY_NODES')
        box.prop(scene, "uv3d_enable_geonode_attr", 
                text="Write to Custom Attribute")
        
        # Show attribute name when enabled
        if scene.uv3d_enable_geonode_attr:
            sub = box.box()
            sub.label(text="Attribute: UV_3D_Ratio", icon='TOOL_SETTINGS')
            sub.label(text="Type: Float (per face)")
        
        # Display results if available
        if scene.uv3d_ratio_value > 0:
            layout.separator()
            
            # Results box
            result_box = layout.box()
            result_box.label(text="Analysis Results", icon='INFO')
            
            # Main ratio value
            col = result_box.column(align=True)
            col.label(text=f"UV/3D Ratio: {scene.uv3d_ratio_value:.4f}")
            
            # Interpretation
            ratio = scene.uv3d_ratio_value
            if 0.95 <= ratio <= 1.05:
                interpretation = "Optimal (1:1 ratio)"
                icon = 'CHECKMARK'
            elif ratio > 1.5:
                interpretation = "UV Stretched"
                icon = 'ERROR'
            elif ratio < 0.5:
                interpretation = "UV Compressed"
                icon = 'ERROR'
            elif ratio > 1.05:
                interpretation = "Slightly Stretched"
                icon = 'QUESTION'
            else:
                interpretation = "Slightly Compressed"
                icon = 'QUESTION'
            
            col.label(text=f"Status: {interpretation}", icon=icon)
            
            # Detailed values (smaller text)
            col.separator()
            sub = col.column(align=True)
            sub.scale_y = 0.8
            sub.label(text=f"3D Area: {scene.uv3d_surface_area:.6f}")
            sub.label(text=f"UV Area: {scene.uv3d_uv_area:.6f}")


# Registration
classes = (
    UV3D_OT_CalculateRatio,
    UV3D_PT_RatioPanel,
)


def register():
    """Register addon classes and properties"""
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # Scene properties for storing results
    bpy.types.Scene.uv3d_ratio_value = bpy.props.FloatProperty(
        name="UV/3D Ratio",
        description="Calculated UV to 3D surface area ratio",
        default=0.0,
        min=0.0
    )
    
    bpy.types.Scene.uv3d_surface_area = bpy.props.FloatProperty(
        name="3D Surface Area",
        description="Total 3D surface area",
        default=0.0,
        min=0.0
    )
    
    bpy.types.Scene.uv3d_uv_area = bpy.props.FloatProperty(
        name="UV Area",
        description="Total UV area",
        default=0.0,
        min=0.0
    )
    
    bpy.types.Scene.uv3d_enable_geonode_attr = bpy.props.BoolProperty(
        name="Enable Geometry Node Attribute",
        description="Write ratio to custom attribute for Geometry Nodes access",
        default=False
    )


def unregister():
    """Unregister addon classes and properties"""
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    # Remove scene properties
    del bpy.types.Scene.uv3d_ratio_value
    del bpy.types.Scene.uv3d_surface_area
    del bpy.types.Scene.uv3d_uv_area
    del bpy.types.Scene.uv3d_enable_geonode_attr


if __name__ == "__main__":
    register()