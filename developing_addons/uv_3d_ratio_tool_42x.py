bl_info = {
    "name": "UV/3D Area Ratio Tool",
    "author": "Developed for Blender 4.2.x LTS",
    "version": (1, 0, 0),
    "blender": (4, 2, 0),
    "location": "UV Editor > Sidebar (N) > UV Tools & 3D Viewport > Sidebar (N) > UV Tools",
    "description": "Measures UV area to 3D area ratios (UV÷3D). Ratio >1 = stretched, <1 = compressed, ≈1 = optimal",
    "category": "UV",
    "doc_url": "",
    "tracker_url": "",
    "support": "COMMUNITY",
}

"""
UV/3D Area Ratio Tool for Blender 4.2.x LTS
==========================================

A streamlined, production-ready addon that calculates the ratio of UV space 
area to 3D surface area (UV Area ÷ 3D Area) to help optimize texture mapping 
and identify UV stretching or compression issues.

Ratio Interpretation:
- Ratio > 1.0: UVs are STRETCHED (UV area larger than 3D area)
- Ratio < 1.0: UVs are COMPRESSED (UV area smaller than 3D area)  
- Ratio ≈ 1.0: OPTIMAL mapping (UV area matches 3D area)

Features:
- Calculate UV to 3D area ratios for selected faces or entire mesh
- Clear visual feedback with interpretation of ratio values
- One-click UV scaling to achieve optimal 1:1 ratio
- Dual-panel interface (UV Editor and 3D Viewport)
- Robust error handling and validation
- Compatible with Blender 4.2.x LTS standards

Installation:
1. Save this file as a .py file
2. In Blender: Edit > Preferences > Add-ons > Install...
3. Select the .py file and click Install Add-on
4. Enable the addon by checking the checkbox

Usage:
1. Select a mesh object and enter Edit Mode
2. Optionally select specific faces, or leave none selected to analyze the entire mesh
3. Open the UV Editor or 3D Viewport sidebar (N key)
4. Find the "UV Tools" panel
5. Click "Calculate UV/3D Ratio" to analyze the current UV mapping

Author: Production team for Blender 4.2.x LTS compatibility
"""

import bpy
import bmesh
import math
import time
from mathutils import Vector


def calculate_face_area_3d(face):
    """
    Calculate the 3D area of a face using triangulation.
    
    Args:
        face: Blender bmesh face object
        
    Returns:
        float: Area of the face in 3D space
    """
    if len(face.verts) < 3:
        return 0.0
    
    vertices = [vertex.co for vertex in face.verts]
    area = 0.0
    
    # Triangulate and sum areas
    for i in range(1, len(vertices) - 1):
        v1 = vertices[i] - vertices[0]
        v2 = vertices[i + 1] - vertices[0]
        triangle_area = v1.cross(v2).length * 0.5
        area += triangle_area
    
    return area


def calculate_face_area_uv(face, uv_layer):
    """
    Calculate the UV area of a face using triangulation.
    
    Args:
        face: Blender bmesh face object
        uv_layer: Active UV layer from bmesh
        
    Returns:
        float: Area of the face in UV space
    """
    if len(face.loops) < 3:
        return 0.0
    
    uv_coords = [loop[uv_layer].uv for loop in face.loops]
    area = 0.0
    
    # Triangulate UV coordinates and sum areas
    for i in range(1, len(uv_coords) - 1):
        uv0 = Vector((uv_coords[0].x, uv_coords[0].y, 0.0))
        uv1 = Vector((uv_coords[i].x, uv_coords[i].y, 0.0))
        uv2 = Vector((uv_coords[i + 1].x, uv_coords[i + 1].y, 0.0))
        
        triangle_area = (uv1 - uv0).cross(uv2 - uv0).length * 0.5
        area += triangle_area
    
    return area


class UV_OT_CalculateRatio(bpy.types.Operator):
    """Calculate the ratio between UV area and 3D surface area"""
    bl_idname = "uv.calculate_uv_3d_ratio"
    bl_label = "Calculate UV/3D Ratio"
    bl_description = ("Calculate UV Area ÷ 3D Area ratio. "
                     "Ratio > 1.0 = Stretched UVs, Ratio < 1.0 = Compressed UVs, Ratio ≈ 1.0 = Optimal mapping")
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        """Check if the operator can be executed"""
        active_object = context.active_object
        return (active_object and 
                active_object.type == 'MESH' and 
                active_object.mode == 'EDIT')

    def execute(self, context):
        """Execute the UV/3D ratio calculation"""
        start_time = time.time()
        
        try:
            result = self._calculate_ratio(context)
            calculation_time = time.time() - start_time
            
            if result['success']:
                self._store_results(context, result, calculation_time)
                self.report({'INFO'}, f"Ratio calculated: {result['ratio']:.4f}")
            else:
                self.report({'ERROR'}, result['error'])
                self._clear_results(context)
                
        except Exception as e:
            self.report({'ERROR'}, f"Calculation failed: {str(e)}")
            self._clear_results(context)
            return {'CANCELLED'}
        
        return {'FINISHED'}

    def _calculate_ratio(self, context):
        """Internal method to perform the ratio calculation"""
        active_object = context.active_object
        
        # Validate mesh object
        if not active_object or active_object.type != 'MESH':
            return {'success': False, 'error': "Active object must be a mesh"}
        
        if active_object.mode != 'EDIT':
            return {'success': False, 'error': "Object must be in Edit Mode"}
        
        # Get bmesh representation
        try:
            bmesh_data = bmesh.from_edit_mesh(active_object.data)
            if not bmesh_data.is_valid:
                return {'success': False, 'error': "Invalid mesh data"}
        except Exception as e:
            return {'success': False, 'error': f"Failed to access mesh data: {str(e)}"}
        
        # Validate UV data
        if not bmesh_data.loops.layers.uv:
            return {'success': False, 'error': "No UV maps found on the mesh"}
        
        uv_layer = bmesh_data.loops.layers.uv.active
        if not uv_layer:
            return {'success': False, 'error': "No active UV layer found"}
        
        # Determine faces to process (selected faces or all faces)
        selected_faces = [face for face in bmesh_data.faces if face.select and face.is_valid]
        faces_to_process = selected_faces if selected_faces else [face for face in bmesh_data.faces if face.is_valid]
        
        if not faces_to_process:
            return {'success': False, 'error': "No valid faces found to process"}
        
        # Calculate areas
        total_3d_area = 0.0
        total_uv_area = 0.0
        processed_faces = 0
        numerical_epsilon = 1e-10
        
        for face in faces_to_process:
            area_3d = calculate_face_area_3d(face)
            area_uv = calculate_face_area_uv(face, uv_layer)
            
            # Validate calculated areas
            if (area_3d < 0 or area_uv < 0 or 
                not math.isfinite(area_3d) or not math.isfinite(area_uv)):
                continue  # Skip invalid faces
            
            total_3d_area += area_3d
            total_uv_area += area_uv
            processed_faces += 1
        
        # Calculate final ratio
        if total_3d_area <= numerical_epsilon:
            return {'success': False, 'error': "3D area is zero or invalid - check mesh geometry"}
        
        ratio = total_uv_area / total_3d_area
        
        if not math.isfinite(ratio):
            return {'success': False, 'error': "Invalid ratio calculated (infinite or NaN)"}
        
        # Create interpretation
        interpretation = self._interpret_ratio(ratio)
        scope = "selected faces" if selected_faces else "entire mesh"
        
        return {
            'success': True,
            'ratio': ratio,
            'interpretation': interpretation,
            'total_3d_area': total_3d_area,
            'total_uv_area': total_uv_area,
            'processed_faces': processed_faces,
            'scope': scope
        }

    def _interpret_ratio(self, ratio):
        """Generate human-readable interpretation of the ratio value"""
        tolerance = 1e-6
        
        if abs(ratio - 1.0) < tolerance:
            return "OPTIMAL - Perfect 1:1 UV to 3D ratio"
        elif 0.99 <= ratio <= 1.01:
            return "EXCELLENT - Near-perfect ratio (within tolerance)"
        elif ratio > 2.0:
            return "SEVERE STRETCHING - UVs much larger than needed"
        elif ratio > 1.2:
            return "STRETCHED - UVs larger than needed"
        elif ratio > 1.05:
            return "SLIGHTLY STRETCHED - Minor stretching detected"
        elif ratio < 0.3:
            return "SEVERE COMPRESSION - UVs much smaller than needed"
        elif ratio < 0.8:
            return "COMPRESSED - UVs smaller than needed"
        elif ratio < 0.95:
            return "SLIGHTLY COMPRESSED - Minor compression detected"
        else:
            return "GOOD - Acceptable ratio with minor deviation"

    def _store_results(self, context, result, calculation_time):
        """Store calculation results in scene properties"""
        scene = context.scene
        
        # Main result
        scene.uv_ratio_result = f"UV/3D Ratio: {result['ratio']:.4f}"
        
        # Detailed information
        details = (
            f"Status: {result['interpretation']}\n"
            f"Scope: {result['processed_faces']} faces ({result['scope']})\n"
            f"3D Area: {result['total_3d_area']:.6f} units²\n"
            f"UV Area: {result['total_uv_area']:.6f} units²\n"
            f"Calculation Time: {calculation_time:.3f}s"
        )
        scene.uv_ratio_details = details
        
        # Store raw ratio for scaling operations
        scene.uv_ratio_value = result['ratio']

    def _clear_results(self, context):
        """Clear stored results"""
        scene = context.scene
        scene.uv_ratio_result = ""
        scene.uv_ratio_details = ""
        scene.uv_ratio_value = 1.0


class UV_OT_ScaleToOptimal(bpy.types.Operator):
    """Scale UVs to achieve optimal 1:1 ratio with 3D surface"""
    bl_idname = "uv.scale_uv_to_optimal"
    bl_label = "Scale UVs to Optimal Ratio"
    bl_description = ("Scale UV coordinates to achieve a 1:1 ratio (UV Area = 3D Area). "
                     "This provides optimal texture mapping without stretching or compression")
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        """Check if the operator can be executed"""
        active_object = context.active_object
        return (active_object and 
                active_object.type == 'MESH' and 
                active_object.mode == 'EDIT' and
                hasattr(context.scene, 'uv_ratio_value') and
                context.scene.uv_ratio_value > 0)

    def execute(self, context):
        """Execute UV scaling to optimal ratio"""
        try:
            active_object = context.active_object
            bmesh_data = bmesh.from_edit_mesh(active_object.data)
            uv_layer = bmesh_data.loops.layers.uv.active
            
            if not uv_layer:
                self.report({'ERROR'}, "No active UV layer found")
                return {'CANCELLED'}
            
            # Calculate scaling factor
            current_ratio = context.scene.uv_ratio_value
            target_ratio = 1.0
            # Scale factor is square root because we're scaling in 2D
            scale_factor = math.sqrt(target_ratio / current_ratio)
            
            # Find UV bounds for center-based scaling
            uv_coordinates = []
            for face in bmesh_data.faces:
                for loop in face.loops:
                    uv_coordinates.append(loop[uv_layer].uv.copy())
            
            if not uv_coordinates:
                self.report({'ERROR'}, "No UV coordinates found")
                return {'CANCELLED'}
            
            # Calculate UV center
            min_u = min(uv.x for uv in uv_coordinates)
            max_u = max(uv.x for uv in uv_coordinates)
            min_v = min(uv.y for uv in uv_coordinates)
            max_v = max(uv.y for uv in uv_coordinates)
            
            center_u = (min_u + max_u) * 0.5
            center_v = (min_v + max_v) * 0.5
            
            # Apply scaling around center point
            for face in bmesh_data.faces:
                for loop in face.loops:
                    uv_coord = loop[uv_layer].uv
                    uv_coord.x = center_u + (uv_coord.x - center_u) * scale_factor
                    uv_coord.y = center_v + (uv_coord.y - center_v) * scale_factor
            
            # Update the mesh
            bmesh.update_edit_mesh(active_object.data)
            
            self.report({'INFO'}, f"UVs scaled by factor {scale_factor:.4f} to achieve optimal ratio")
            
            # Recalculate ratio to update display
            bpy.ops.uv.calculate_uv_3d_ratio()
            
        except Exception as e:
            self.report({'ERROR'}, f"Scaling failed: {str(e)}")
            return {'CANCELLED'}
        
        return {'FINISHED'}


class UVRatioPanel:
    """Shared panel drawing functionality for both UV Editor and 3D Viewport"""
    
    def draw_panel_content(self, context, layout):
        """Draw the main panel content"""
        column = layout.column(align=True)
        
        # Add explanation text about ratio calculation
        info_box = layout.box()
        info_column = info_box.column(align=True)
        info_column.label(text="UV/3D Ratio Analysis:", icon='INFO')
        info_column.label(text="• Ratio > 1.0: UVs are stretched")
        info_column.label(text="• Ratio < 1.0: UVs are compressed") 
        info_column.label(text="• Ratio ≈ 1.0: Optimal mapping")
        info_column.label(text="Formula: UV Area ÷ 3D Area")
        
        layout.separator()
        
        # Main calculation button
        column = layout.column(align=True)
        column.scale_y = 1.3
        column.operator("uv.calculate_uv_3d_ratio", icon='SHADERFX')
        
        # Display results if available
        scene = context.scene
        if hasattr(scene, 'uv_ratio_result') and scene.uv_ratio_result:
            layout.separator()
            
            # Result box
            result_box = layout.box()
            result_column = result_box.column(align=True)
            result_column.label(text=scene.uv_ratio_result, icon='INFO')
            
            # Detailed information
            if hasattr(scene, 'uv_ratio_details') and scene.uv_ratio_details:
                details_lines = scene.uv_ratio_details.split('\n')
                for line in details_lines:
                    if ':' in line:
                        label_text, value_text = line.split(':', 1)
                        detail_row = result_column.row()
                        detail_row.label(text=f"{label_text}:")
                        detail_row.label(text=value_text.strip())
                    else:
                        result_column.label(text=line)
            
            # Scaling controls
            if (hasattr(scene, 'uv_ratio_value') and 
                scene.uv_ratio_value > 0 and 
                "Error" not in scene.uv_ratio_result):
                
                layout.separator()
                scaling_box = layout.box()
                scaling_box.label(text="UV Optimization", icon='MODIFIER')
                scaling_column = scaling_box.column(align=True)
                scaling_column.operator("uv.scale_uv_to_optimal", 
                                       text="Scale to Optimal Ratio",
                                       icon='FULLSCREEN_ENTER')


class UV_PT_RatioPanel(bpy.types.Panel, UVRatioPanel):
    """UV/3D Ratio panel for UV Editor"""
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "UV"
    bl_label = "UV/3D Area Ratio Tool"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        """Draw the panel"""
        self.draw_panel_content(context, self.layout)


class VIEW3D_PT_RatioPanel(bpy.types.Panel, UVRatioPanel):
    """UV/3D Ratio panel for 3D Viewport"""
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "UV"
    bl_label = "UV/3D Area Ratio Tool"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        """Only show panel when there's an active mesh object"""
        active_object = context.active_object
        return active_object and active_object.type == 'MESH'

    def draw(self, context):
        """Draw the panel"""
        self.draw_panel_content(context, self.layout)


# Registration
classes = (
    UV_OT_CalculateRatio,
    UV_OT_ScaleToOptimal,
    UV_PT_RatioPanel,
    VIEW3D_PT_RatioPanel,
)


def register():
    """Register addon classes and properties"""
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # Scene properties for storing results
    bpy.types.Scene.uv_ratio_result = bpy.props.StringProperty(
        name="UV/3D Ratio Result",
        description="UV Area ÷ 3D Area ratio result. Values >1 indicate stretching, <1 indicate compression",
        default=""
    )
    
    bpy.types.Scene.uv_ratio_details = bpy.props.StringProperty(
        name="UV/3D Ratio Details",
        description="Detailed information about the UV/3D area ratio calculation and interpretation",
        default=""
    )
    
    bpy.types.Scene.uv_ratio_value = bpy.props.FloatProperty(
        name="UV/3D Ratio Value",
        description="Numerical ratio value (UV Area ÷ 3D Area) for internal calculations and optimization",
        default=1.0,
        min=0.0
    )


def unregister():
    """Unregister addon classes and properties"""
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    # Remove scene properties
    del bpy.types.Scene.uv_ratio_result
    del bpy.types.Scene.uv_ratio_details
    del bpy.types.Scene.uv_ratio_value


if __name__ == "__main__":
    register()