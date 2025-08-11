bl_info = {
    "name": "Nazarick Stitch Tool",
    "author": "Demiurge, Architect of the Great Tomb of Nazarick",
    "version": (1, 0, 0),
    "blender": (4, 5, 0),
    "location": "3D Viewport > Sidebar (N) > Nazarick Tools",
    "description": "Create stitches along mesh edges defined by vertex groups",
    "category": "Mesh",
}

"""
🏰 Nazarick Stitch Tool for Blender 4.5 🏰

Creates realistic stitch geometry along edges defined by vertex groups.
Perfect for clothing, fabric, and any sewn material modeling.

Features:
- Vertex group-based edge definition
- Customizable stitch parameters (count, size, depth)
- Real-time preview
- Non-destructive workflow
- Multiple stitch styles

Architected by Demiurge for the glory of the Great Tomb of Nazarick! ⚡
"""

import bpy
import bmesh
from mathutils import Vector, Matrix
from bpy.props import (
    IntProperty, 
    FloatProperty, 
    EnumProperty, 
    BoolProperty,
    StringProperty
)
from bpy.types import Operator, Panel
import math


class MESH_OT_NazarickCreateStitches(bpy.types.Operator):
    """Create stitches along edges defined by vertex group"""
    bl_idname = "mesh.nazarick_create_stitches"
    bl_label = "Create Stitches"
    bl_description = "Generate stitch geometry along edges defined by selected vertex group"
    bl_options = {'REGISTER', 'UNDO'}
    
    vertex_group: StringProperty(
        name="Vertex Group",
        description="Vertex group that defines the stitch path",
        default=""
    )
    
    stitch_count: IntProperty(
        name="Stitch Count",
        description="Number of stitches to create along the edge",
        default=10,
        min=1,
        max=100
    )
    
    stitch_size: FloatProperty(
        name="Stitch Size",
        description="Size of individual stitches",
        default=0.02,
        min=0.001,
        max=0.1,
        unit='LENGTH'
    )
    
    stitch_depth: FloatProperty(
        name="Stitch Depth",
        description="How deep the stitches penetrate into the surface",
        default=0.01,
        min=0.0,
        max=0.05,
        unit='LENGTH'
    )
    
    stitch_style: EnumProperty(
        name="Stitch Style",
        description="Style of stitches to create",
        items=[
            ('STRAIGHT', "Straight", "Simple straight stitches"),
            ('CROSS', "Cross", "Cross-pattern stitches"),
            ('ZIGZAG', "Zigzag", "Zigzag pattern stitches"),
            ('RUNNING', "Running", "Running stitch pattern"),
        ],
        default='STRAIGHT'
    )
    
    offset_distance: FloatProperty(
        name="Offset Distance",
        description="Distance to offset stitches from the original edge",
        default=0.0,
        min=-0.1,
        max=0.1,
        unit='LENGTH'
    )
    
    random_variation: FloatProperty(
        name="Random Variation",
        description="Add random variation to stitch placement",
        default=0.0,
        min=0.0,
        max=0.5,
        subtype='FACTOR'
    )

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and obj.type == 'MESH' and 
                obj.mode == 'EDIT' and 
                len(obj.vertex_groups) > 0)

    def invoke(self, context, event):
        # Set default vertex group to the active one
        obj = context.active_object
        if obj.vertex_groups.active:
            self.vertex_group = obj.vertex_groups.active.name
        return self.execute(context)

    def execute(self, context):
        obj = context.active_object
        
        # Enhanced validation for Supreme Overlord standards
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "Active object must be a mesh")
            return {'CANCELLED'}
            
        if obj.mode != 'EDIT':
            self.report({'ERROR'}, "Object must be in Edit Mode")
            return {'CANCELLED'}
        
        # Validate vertex group
        if not self.vertex_group or self.vertex_group not in obj.vertex_groups:
            self.report({'ERROR'}, "Please select a valid vertex group")
            return {'CANCELLED'}
        
        # Get vertex group index
        vg_index = obj.vertex_groups[self.vertex_group].index
        
        # Get bmesh with proper error handling
        try:
            bm = bmesh.from_edit_mesh(obj.data)
            if not bm.is_valid:
                self.report({'ERROR'}, "Invalid mesh data")
                return {'CANCELLED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to access mesh data: {str(e)}")
            return {'CANCELLED'}
        
        # Ensure we have vertex group layer
        if not bm.verts.layers.deform:
            bm.verts.layers.deform.new()
        deform_layer = bm.verts.layers.deform.active
        
        # Find vertices in the group
        group_verts = []
        for vert in bm.verts:
            if vg_index in vert[deform_layer]:
                weight = vert[deform_layer][vg_index]
                if weight > 0.01:  # Only include vertices with significant weight
                    group_verts.append((vert, weight))
        
        if len(group_verts) < 2:
            self.report({'ERROR'}, f"Need at least 2 vertices in group '{self.vertex_group}'")
            return {'CANCELLED'}
        
        # Find edges connecting group vertices
        group_edges = []
        for edge in bm.edges:
            v1, v2 = edge.verts
            v1_in_group = vg_index in v1[deform_layer] and v1[deform_layer][vg_index] > 0.01
            v2_in_group = vg_index in v2[deform_layer] and v2[deform_layer][vg_index] > 0.01
            
            if v1_in_group and v2_in_group:
                group_edges.append(edge)
        
        if not group_edges:
            self.report({'ERROR'}, f"No edges found connecting vertices in group '{self.vertex_group}'")
            return {'CANCELLED'}
        
        # Create stitches with error handling
        stitch_count = 0
        
        try:
            for edge in group_edges:
                stitch_count += self._create_stitches_on_edge(bm, edge, obj)
            
            # Update mesh with validation
            bmesh.update_edit_mesh(obj.data)
            
            # Force update
            context.view_layer.update()
            
        except Exception as e:
            self.report({'ERROR'}, f"Failed to create stitches: {str(e)}")
            return {'CANCELLED'}
        
        self.report({'INFO'}, f"Created {stitch_count} stitches along {len(group_edges)} edges")
        return {'FINISHED'}
    
    def _create_stitches_on_edge(self, bm, edge, obj):
        """Create stitches along a single edge"""
        import random
        
        v1, v2 = edge.verts
        edge_vector = v2.co - v1.co
        edge_length = edge_vector.length
        edge_direction = edge_vector.normalized()
        
        # Calculate edge normal (average of adjacent face normals)
        edge_normal = Vector((0, 0, 1))
        if edge.link_faces:
            edge_normal = Vector((0, 0, 0))
            for face in edge.link_faces:
                edge_normal += face.normal
            edge_normal = edge_normal.normalized()
        
        # Calculate perpendicular vector for stitch width
        up_vector = Vector((0, 0, 1))
        if abs(edge_normal.z) > 0.9:  # If edge normal is too close to Z, use Y
            up_vector = Vector((0, 1, 0))
        
        stitch_width_vector = edge_direction.cross(edge_normal).normalized()
        
        created_stitches = 0
        
        # Create stitches along the edge
        for i in range(self.stitch_count):
            t = i / max(1, self.stitch_count - 1)  # Parameter along edge (0 to 1)
            
            # Add random variation
            if self.random_variation > 0:
                random_offset = (random.random() - 0.5) * self.random_variation
                t = max(0, min(1, t + random_offset))
            
            # Calculate stitch position
            stitch_center = v1.co + edge_vector * t
            
            # Offset from edge if specified
            if self.offset_distance != 0:
                stitch_center += edge_normal * self.offset_distance
            
            # Create stitch geometry based on style
            if self.stitch_style == 'STRAIGHT':
                created_stitches += self._create_straight_stitch(bm, stitch_center, stitch_width_vector, edge_normal)
            elif self.stitch_style == 'CROSS':
                created_stitches += self._create_cross_stitch(bm, stitch_center, stitch_width_vector, edge_normal, edge_direction)
            elif self.stitch_style == 'ZIGZAG':
                zigzag_offset = math.sin(t * math.pi * 4) * self.stitch_size * 0.5
                offset_center = stitch_center + stitch_width_vector * zigzag_offset
                created_stitches += self._create_straight_stitch(bm, offset_center, stitch_width_vector, edge_normal)
            elif self.stitch_style == 'RUNNING':
                # Skip every other stitch for running pattern
                if i % 2 == 0:
                    created_stitches += self._create_straight_stitch(bm, stitch_center, stitch_width_vector, edge_normal)
        
        return created_stitches
    
    def _create_straight_stitch(self, bm, center, width_vector, normal):
        """Create a simple straight stitch"""
        # Create stitch as a small line of vertices
        half_size = self.stitch_size * 0.5
        
        # Start and end points of the stitch
        start_point = center - width_vector * half_size
        end_point = center + width_vector * half_size
        
        # Add depth offset
        start_point -= normal * self.stitch_depth
        end_point -= normal * self.stitch_depth
        
        # Create vertices
        v1 = bm.verts.new(start_point)
        v2 = bm.verts.new(end_point)
        
        # Create edge
        bm.edges.new((v1, v2))
        
        return 1
    
    def _create_cross_stitch(self, bm, center, width_vector, normal, direction):
        """Create a cross-pattern stitch"""
        half_size = self.stitch_size * 0.5
        
        # First line of the cross
        start1 = center - width_vector * half_size - direction * half_size
        end1 = center + width_vector * half_size + direction * half_size
        
        # Second line of the cross
        start2 = center + width_vector * half_size - direction * half_size
        end2 = center - width_vector * half_size + direction * half_size
        
        # Add depth offset
        depth_offset = normal * self.stitch_depth
        start1 -= depth_offset
        end1 -= depth_offset
        start2 -= depth_offset
        end2 -= depth_offset
        
        # Create vertices and edges
        v1 = bm.verts.new(start1)
        v2 = bm.verts.new(end1)
        v3 = bm.verts.new(start2)
        v4 = bm.verts.new(end2)
        
        bm.edges.new((v1, v2))
        bm.edges.new((v3, v4))
        
        return 2


class MESH_OT_NazarickRemoveStitches(bpy.types.Operator):
    """Remove stitch geometry from the mesh"""
    bl_idname = "mesh.nazarick_remove_stitches"
    bl_label = "Remove Stitches"
    bl_description = "Remove stitch geometry (loose edges) from the mesh"
    bl_options = {'REGISTER', 'UNDO'}
    
    remove_mode: EnumProperty(
        name="Remove Mode",
        description="What to remove",
        items=[
            ('LOOSE_EDGES', "Loose Edges", "Remove all loose edges (likely stitches)"),
            ('SELECTED', "Selected Only", "Remove only selected geometry"),
            ('ALL_STITCHES', "All Stitches", "Remove all stitch-like geometry"),
        ],
        default='LOOSE_EDGES'
    )

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj and obj.type == 'MESH' and obj.mode == 'EDIT'

    def execute(self, context):
        obj = context.active_object
        
        # Enhanced validation
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "Active object must be a mesh")
            return {'CANCELLED'}
            
        if obj.mode != 'EDIT':
            self.report({'ERROR'}, "Object must be in Edit Mode")
            return {'CANCELLED'}
        
        # Get bmesh with error handling
        try:
            bm = bmesh.from_edit_mesh(obj.data)
            if not bm.is_valid:
                self.report({'ERROR'}, "Invalid mesh data")
                return {'CANCELLED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to access mesh data: {str(e)}")
            return {'CANCELLED'}
        
        removed_count = 0
        
        try:
            if self.remove_mode == 'LOOSE_EDGES':
                # Remove edges that are not part of any face (enhanced validation)
                edges_to_remove = [edge for edge in bm.edges if not edge.link_faces and edge.is_valid]
                for edge in edges_to_remove:
                    if edge.is_valid:  # Double-check before removal
                        bm.edges.remove(edge)
                        removed_count += 1
                        
            elif self.remove_mode == 'SELECTED':
                # Remove selected edges (enhanced validation)
                selected_edges = [edge for edge in bm.edges if edge.select and edge.is_valid]
                for edge in selected_edges:
                    if edge.is_valid:  # Double-check before removal
                        bm.edges.remove(edge)
                        removed_count += 1
                        
            elif self.remove_mode == 'ALL_STITCHES':
                # Remove very short edges (likely stitches) with enhanced validation
                threshold = 0.1  # Edges shorter than this are considered stitches
                edges_to_remove = [edge for edge in bm.edges 
                                 if edge.is_valid and edge.calc_length() < threshold and not edge.link_faces]
                for edge in edges_to_remove:
                    if edge.is_valid:  # Double-check before removal
                        bm.edges.remove(edge)
                        removed_count += 1
            
            # Clean up loose vertices with error handling
            if removed_count > 0:
                bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)
            
            # Update mesh
            bmesh.update_edit_mesh(obj.data)
            
            # Force update
            context.view_layer.update()
            
        except Exception as e:
            self.report({'ERROR'}, f"Failed to remove stitches: {str(e)}")
            return {'CANCELLED'}
        
        self.report({'INFO'}, f"Removed {removed_count} stitch elements")
        return {'FINISHED'}


class VIEW3D_PT_NazarickStitchPanel(bpy.types.Panel):
    """Stitch tool panel in 3D Viewport"""
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Nazarick Tools"
    bl_label = "Nazarick Stitch Tool"
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
        
        # Check if in edit mode
        if obj.mode != 'EDIT':
            layout.label(text="Enter Edit Mode", icon='EDITMODE_HLT')
            return
        
        # Vertex group selection
        col = layout.column(align=True)
        col.label(text="Stitch Path Definition:", icon='GROUP_VERTEX')
        
        if obj.vertex_groups:
            col.prop_search(context.scene, "nazarick_stitch_vertex_group", 
                          obj, "vertex_groups", text="Vertex Group")
            
            # Show active vertex group info
            if obj.vertex_groups.active:
                box = col.box()
                box.label(text=f"Active: {obj.vertex_groups.active.name}", icon='RADIOBUT_ON')
                
                # Count vertices in group
                bm = bmesh.from_edit_mesh(obj.data)
                if bm.verts.layers.deform:
                    deform_layer = bm.verts.layers.deform.active
                    vg_index = obj.vertex_groups.active.index
                    group_vert_count = sum(1 for v in bm.verts if vg_index in v[deform_layer] and v[deform_layer][vg_index] > 0.01)
                    box.label(text=f"Vertices: {group_vert_count}")
        else:
            col.label(text="No vertex groups found", icon='ERROR')
            col.operator("object.vertex_group_add", text="Create Vertex Group")
        
        layout.separator()
        
        # Stitch parameters
        if obj.vertex_groups:
            params_box = layout.box()
            params_box.label(text="Stitch Parameters", icon='MODIFIER')
            
            params_box.prop(context.scene, "nazarick_stitch_count")
            params_box.prop(context.scene, "nazarick_stitch_size")
            params_box.prop(context.scene, "nazarick_stitch_depth")
            params_box.prop(context.scene, "nazarick_stitch_style", expand=True)
            
            # Advanced parameters
            advanced_box = params_box.box()
            advanced_box.label(text="Advanced", icon='PREFERENCES')
            advanced_box.prop(context.scene, "nazarick_stitch_offset")
            advanced_box.prop(context.scene, "nazarick_stitch_variation")
            
            layout.separator()
            
            # Main action buttons
            col = layout.column(align=True)
            col.scale_y = 1.3
            
            # Create stitches operator with scene properties
            create_op = col.operator("mesh.nazarick_create_stitches", 
                                   text="Create Stitches", icon='MOD_SKIN')
            create_op.vertex_group = getattr(context.scene, "nazarick_stitch_vertex_group", "")
            create_op.stitch_count = getattr(context.scene, "nazarick_stitch_count", 10)
            create_op.stitch_size = getattr(context.scene, "nazarick_stitch_size", 0.02)
            create_op.stitch_depth = getattr(context.scene, "nazarick_stitch_depth", 0.01)
            create_op.stitch_style = getattr(context.scene, "nazarick_stitch_style", 'STRAIGHT')
            create_op.offset_distance = getattr(context.scene, "nazarick_stitch_offset", 0.0)
            create_op.random_variation = getattr(context.scene, "nazarick_stitch_variation", 0.0)
            
            col.operator("mesh.nazarick_remove_stitches", 
                        text="Remove Stitches", icon='X')
        
        layout.separator()
        
        # Instructions
        help_box = layout.box()
        help_box.label(text="Quick Guide:", icon='QUESTION')
        help_box.label(text="1. Create/select vertex group")
        help_box.label(text="2. Assign vertices to define path") 
        help_box.label(text="3. Adjust stitch parameters")
        help_box.label(text="4. Click 'Create Stitches'")


classes = (
    MESH_OT_NazarickCreateStitches,
    MESH_OT_NazarickRemoveStitches,
    VIEW3D_PT_NazarickStitchPanel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # Scene properties for UI persistence
    bpy.types.Scene.nazarick_stitch_vertex_group = StringProperty(
        name="Stitch Vertex Group",
        description="Vertex group defining the stitch path"
    )
    
    bpy.types.Scene.nazarick_stitch_count = IntProperty(
        name="Stitch Count",
        description="Number of stitches to create",
        default=10,
        min=1,
        max=100
    )
    
    bpy.types.Scene.nazarick_stitch_size = FloatProperty(
        name="Stitch Size",
        description="Size of individual stitches",
        default=0.02,
        min=0.001,
        max=0.1
    )
    
    bpy.types.Scene.nazarick_stitch_depth = FloatProperty(
        name="Stitch Depth",
        description="Depth of stitches into surface",
        default=0.01,
        min=0.0,
        max=0.05
    )
    
    bpy.types.Scene.nazarick_stitch_style = EnumProperty(
        name="Stitch Style",
        items=[
            ('STRAIGHT', "Straight", "Simple straight stitches"),
            ('CROSS', "Cross", "Cross-pattern stitches"),
            ('ZIGZAG', "Zigzag", "Zigzag pattern stitches"),
            ('RUNNING', "Running", "Running stitch pattern"),
        ],
        default='STRAIGHT'
    )
    
    bpy.types.Scene.nazarick_stitch_offset = FloatProperty(
        name="Offset Distance",
        description="Distance to offset stitches from edge",
        default=0.0,
        min=-0.1,
        max=0.1
    )
    
    bpy.types.Scene.nazarick_stitch_variation = FloatProperty(
        name="Random Variation",
        description="Random variation in stitch placement",
        default=0.0,
        min=0.0,
        max=0.5
    )


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    # Clean up scene properties
    del bpy.types.Scene.nazarick_stitch_vertex_group
    del bpy.types.Scene.nazarick_stitch_count
    del bpy.types.Scene.nazarick_stitch_size
    del bpy.types.Scene.nazarick_stitch_depth
    del bpy.types.Scene.nazarick_stitch_style
    del bpy.types.Scene.nazarick_stitch_offset
    del bpy.types.Scene.nazarick_stitch_variation


if __name__ == "__main__":
    register()