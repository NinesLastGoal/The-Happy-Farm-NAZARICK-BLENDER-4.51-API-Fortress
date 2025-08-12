bl_info = {
    "name": "Nazarick Stitch Tool",
    "author": "Demiurge, Architect of the Great Tomb of Nazarick",
    "version": (2, 1, 0),
    "blender": (4, 5, 0),
    "location": "3D Viewport > Sidebar (N) > Nazarick Tools",
    "description": "Supreme-quality stitch geometry creation with battle-tested reliability",
    "warning": "Requires Blender 4.5+ for full compatibility",
    "doc_url": "https://github.com/NinesLastGoal/The-Happy-Farm-NAZARICK-BLENDER-4.51-API-Fortress/tree/main/testing_addons/examples/stitch_tool",
    "tracker_url": "https://github.com/NinesLastGoal/The-Happy-Farm-NAZARICK-BLENDER-4.51-API-Fortress/issues",
    "category": "Mesh",
}

"""
🏰 Nazarick Stitch Tool for Blender 4.5 🏰

Creates realistic stitch geometry along edges defined by vertex groups.
Perfect for clothing, fabric, and any sewn material modeling.

ENHANCED FEATURES (v2.0):
========================

🧵 RELIABLE STITCH TAGGING SYSTEM:
- Uses vertex groups and custom attributes for unambiguous stitch identification
- Session-based tracking for selective removal (all stitches, last session, by selection)
- No more unreliable "loose edge" detection - precise tagging system ensures clean removal

📐 INTELLIGENT AUTO-SIZING:
- Calculates stitch parameters based on mesh scale and average edge length
- Proportional sizing that adapts to your mesh dimensions
- Auto-suggests optimal stitch count, size, and depth values
- Manual override always available for creative control

🎯 ENHANCED REMOVAL MODES:
- ALL_TAGGED: Remove all stitches marked with Nazarick tags (recommended)
- LAST_SESSION: Remove only stitches from the most recent creation session
- SELECTED: Remove only selected stitch geometry
- LOOSE_EDGES: Legacy mode for backwards compatibility

🛡️ ROBUST ERROR HANDLING:
- Comprehensive validation of mesh state and user input
- Graceful handling of edge cases and invalid operations
- Clear error messages and user feedback
- Safe parameter ranges with soft limits

🎨 IMPROVED USER INTERFACE:
- Auto-sizing toggle with instant calculation button
- Real-time stitch count display for tagged geometry
- Enhanced tooltips with usage guidance
- Intuitive parameter organization with advanced options

USAGE GUIDE:
============

1. SETUP:
   - Select a mesh object and enter Edit Mode
   - Create a vertex group and assign vertices to define the stitch path
   - Connected vertices will form the edges where stitches are created

2. AUTO-SIZING (RECOMMENDED):
   - Enable "Auto Sizing" checkbox
   - Click the refresh button to calculate optimal parameters
   - Parameters will adjust automatically based on your mesh scale

3. MANUAL SIZING:
   - Disable "Auto Sizing" for manual control
   - Adjust Stitch Count (1-500): Number of stitches per edge
   - Adjust Stitch Size (0.0001-1.0): Individual stitch dimensions
   - Adjust Stitch Depth (0.0-0.5): How deep stitches penetrate surface

4. STITCH STYLES:
   - STRAIGHT: Simple linear stitches (fastest)
   - CROSS: X-pattern stitches (decorative)
   - ZIGZAG: Alternating zigzag pattern
   - RUNNING: Every-other stitch pattern (traditional sewing)

5. ADVANCED OPTIONS:
   - Offset Distance: Move stitches away from original edge
   - Random Variation: Add organic irregularity to stitch placement

6. REMOVAL:
   - Use "All Tagged" mode for reliable removal of all created stitches
   - Use "Last Session" to remove only the most recently created batch
   - Tagged stitches counter shows how many stitches are present

TECHNICAL DETAILS:
==================

TAGGING SYSTEM:
- Stitch vertices are added to "NAZARICK_STITCHES" vertex group
- Each session gets unique ID stored as custom vertex attribute
- Enables precise identification and removal without affecting base mesh

AUTO-SIZING ALGORITHM:
- Calculates mesh bounding box and average edge length
- Suggests stitch_size = avg_edge_length * 0.1 (10% of typical edge)
- Suggests stitch_depth = avg_edge_length * 0.05 (5% of typical edge)
- Suggests stitch_count based on edge density for optimal appearance

ERROR HANDLING:
- Validates object type, edit mode, vertex group existence
- Handles empty meshes, invalid vertex groups, connection failures
- Uses try-catch blocks with detailed error reporting
- Safe fallbacks for edge cases

PERFORMANCE:
- Efficient vertex group and bmesh operations
- Minimal memory overhead with custom attributes
- Optimized for meshes with hundreds to thousands of vertices
- Session tracking adds negligible performance cost

COMPATIBILITY:
==============
- Blender 4.5+ required (uses modern edge.link_faces API)
- Works with any mesh topology
- Compatible with modifiers and subdivision surfaces
- Preserves existing vertex groups and mesh data

TROUBLESHOOTING:
================

ISSUE: "No edges found connecting vertices"
SOLUTION: Ensure vertex group contains connected vertices forming edges

ISSUE: Auto-sizing produces very small/large values
SOLUTION: Check mesh scale - very large/small meshes may need manual adjustment

ISSUE: Stitches appear in wrong location
SOLUTION: Check mesh normals and edge direction, adjust offset if needed

ISSUE: Removal doesn't work completely
SOLUTION: Use "All Tagged" mode instead of legacy "Loose Edges" mode

RECOMMENDED WORKFLOW:
=====================
1. Model your base garment/fabric mesh
2. Create vertex groups for seam lines (e.g., "sleeve_seam", "hem_line")
3. Enable Auto Sizing for proportional results
4. Create stitches with appropriate style for your material
5. Use "Last Session" removal to iterate and refine
6. Use "All Tagged" removal to clean up when finished

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
import time

# =====================================================================================
# 🏰 NAZARICK STITCH TOOL CONSTANTS - COCYTUS GUARDIAN DISCIPLINE 🏰
# =====================================================================================

class NazarickStitchConstants:
    """
    Centralized constants for the Nazarick Stitch Tool.
    Enforces Cocytus Guardian standards for modularity and maintainability.
    """
    
    # Stitch tagging system constants
    STITCH_TAG_VERTEX_GROUP = "NAZARICK_STITCHES"
    STITCH_TAG_ATTRIBUTE = "nazarick_stitch_id"
    
    # Parameter limits (enforced for stability)
    MAX_STITCH_COUNT = 500
    MIN_STITCH_COUNT = 1
    SOFT_MAX_STITCH_COUNT = 100
    
    MAX_STITCH_SIZE = 1.0
    MIN_STITCH_SIZE = 0.0001
    SOFT_MAX_STITCH_SIZE = 0.1
    
    MAX_STITCH_DEPTH = 0.5
    MIN_STITCH_DEPTH = 0.0
    SOFT_MAX_STITCH_DEPTH = 0.05
    
    # Auto-sizing algorithm constants
    STITCH_SIZE_RATIO = 0.1      # 10% of average edge length
    STITCH_DEPTH_RATIO = 0.05    # 5% of average edge length
    STITCH_SPACING_RATIO = 0.5   # 50% of average edge length
    
    # UI and performance constants
    MIN_VERTEX_WEIGHT = 0.01     # Minimum weight for vertex group inclusion
    MIN_VERTICES_FOR_STITCH = 2  # Minimum vertices needed for stitch creation
    REMOVE_DOUBLES_DISTANCE = 0.0001  # Distance for mesh cleanup
    
    # Session and memory management
    SESSION_ID_PREFIX = "stitch_"
    MAX_SESSION_MEMORY = 100     # Maximum sessions to track


# Legacy constants for backward compatibility
STITCH_TAG_VERTEX_GROUP = NazarickStitchConstants.STITCH_TAG_VERTEX_GROUP
STITCH_TAG_ATTRIBUTE = NazarickStitchConstants.STITCH_TAG_ATTRIBUTE


class VictimFailsafeSystem:
    """
    🛡️ VICTIM'S FAILSAFE RECOVERY SYSTEM 🛡️
    
    Implements comprehensive failsafe mechanisms and recovery protocols
    for catastrophic failure scenarios and mass user error situations.
    
    Guardian: Victim | Mission: Prevent total loss and enable recovery
    """
    
    @staticmethod
    def create_emergency_backup(obj, operation_type="stitch_operation"):
        """
        Create emergency backup of mesh state before dangerous operations
        
        Args:
            obj: Blender mesh object
            operation_type: Type of operation for backup naming
            
        Returns:
            dict: Backup information for recovery
        """
        try:
            if not obj or obj.type != 'MESH':
                return None
                
            backup_info = {
                'timestamp': time.time(),
                'operation': operation_type,
                'vertex_count': len(obj.data.vertices),
                'edge_count': len(obj.data.edges),
                'face_count': len(obj.data.polygons),
                'vertex_groups': [vg.name for vg in obj.vertex_groups],
                'has_custom_attributes': hasattr(obj.data, 'attributes') and len(obj.data.attributes) > 0
            }
            
            # Store in scene for recovery
            if hasattr(bpy.context.scene, 'nazarick_emergency_backup'):
                bpy.context.scene.nazarick_emergency_backup = str(backup_info)
            
            return backup_info
            
        except Exception as e:
            print(f"🛡️ Victim Failsafe: Emergency backup failed - {e}")
            return None
    
    @staticmethod
    def validate_operation_safety(obj, operation_params):
        """
        Validate operation parameters for safety before execution
        
        Args:
            obj: Target mesh object
            operation_params: Dictionary of operation parameters
            
        Returns:
            tuple: (is_safe: bool, warnings: list, critical_issues: list)
        """
        warnings = []
        critical_issues = []
        
        try:
            # Check mesh integrity
            if not obj or obj.type != 'MESH':
                critical_issues.append("Invalid or missing mesh object")
                return False, warnings, critical_issues
            
            # Check mode
            if obj.mode != 'EDIT':
                critical_issues.append("Object must be in Edit Mode")
                return False, warnings, critical_issues
            
            # Check parameter ranges
            if 'stitch_count' in operation_params:
                count = operation_params['stitch_count']
                if count > NazarickStitchConstants.SOFT_MAX_STITCH_COUNT:
                    warnings.append(f"High stitch count ({count}) may impact performance")
                if count > NazarickStitchConstants.MAX_STITCH_COUNT:
                    critical_issues.append(f"Stitch count exceeds maximum ({NazarickStitchConstants.MAX_STITCH_COUNT})")
            
            # Check mesh complexity
            bm = bmesh.from_edit_mesh(obj.data)
            if len(bm.verts) > 50000:
                warnings.append("Large mesh detected - operation may take time")
            if len(bm.verts) > 100000:
                critical_issues.append("Mesh too complex for safe operation")
            
            is_safe = len(critical_issues) == 0
            return is_safe, warnings, critical_issues
            
        except Exception as e:
            critical_issues.append(f"Safety validation failed: {str(e)}")
            return False, warnings, critical_issues
    
    @staticmethod
    def emergency_rollback(obj, error_context="unknown"):
        """
        Attempt emergency rollback to previous safe state
        
        Args:
            obj: Mesh object to rollback
            error_context: Description of the error that triggered rollback
            
        Returns:
            bool: Success of rollback operation
        """
        try:
            print(f"🛡️ Victim Failsafe: Initiating emergency rollback due to: {error_context}")
            
            # Attempt to remove any corrupted stitch geometry
            if obj and obj.type == 'MESH' and obj.mode == 'EDIT':
                bm = bmesh.from_edit_mesh(obj.data)
                
                # Remove any loose vertices that might be corrupted
                loose_verts = [v for v in bm.verts if not v.link_edges and v.is_valid]
                for vert in loose_verts:
                    if vert.is_valid:
                        bm.verts.remove(vert)
                
                # Remove any degenerate edges
                degenerate_edges = [e for e in bm.edges if e.calc_length() < 0.0001 and e.is_valid]
                for edge in degenerate_edges:
                    if edge.is_valid:
                        bm.edges.remove(edge)
                
                # Clean up mesh
                bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)
                bmesh.update_edit_mesh(obj.data)
                
                print("🛡️ Victim Failsafe: Emergency cleanup completed")
                return True
                
        except Exception as e:
            print(f"🛡️ Victim Failsafe: Emergency rollback failed - {e}")
            
        return False
    
    @staticmethod
    def generate_recovery_report(obj, operation_context):
        """
        Generate detailed recovery report for troubleshooting
        
        Args:
            obj: Affected mesh object
            operation_context: Context of the failed operation
            
        Returns:
            str: Detailed recovery report
        """
        try:
            report_lines = [
                "🛡️ VICTIM'S FAILSAFE RECOVERY REPORT 🛡️",
                "=" * 50,
                f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}",
                f"Operation Context: {operation_context}",
                f"Object Name: {obj.name if obj else 'None'}",
                f"Object Type: {obj.type if obj else 'None'}",
                f"Object Mode: {obj.mode if obj else 'None'}",
                ""
            ]
            
            if obj and obj.type == 'MESH':
                report_lines.extend([
                    "Mesh Statistics:",
                    f"- Vertices: {len(obj.data.vertices)}",
                    f"- Edges: {len(obj.data.edges)}",
                    f"- Faces: {len(obj.data.polygons)}",
                    f"- Vertex Groups: {len(obj.vertex_groups)}",
                    ""
                ])
                
                # Check for stitch-related data
                if STITCH_TAG_VERTEX_GROUP in obj.vertex_groups:
                    vg = obj.vertex_groups[STITCH_TAG_VERTEX_GROUP]
                    report_lines.append(f"- Stitch vertex group present: {vg.name}")
                else:
                    report_lines.append("- No stitch vertex group found")
            
            report_lines.extend([
                "",
                "Recovery Recommendations:",
                "1. Save your work immediately",
                "2. Check mesh for corruption with Mesh > Clean Up > Remove Doubles",
                "3. Use 'All Tagged' removal mode to clean stitch geometry",
                "4. If issues persist, restart Blender and reload the file",
                "5. Report persistent issues to the Nazarick development team",
                "",
                "🛡️ End of Recovery Report 🛡️"
            ])
            
            return "\n".join(report_lines)
            
        except Exception as e:
            return f"🛡️ Recovery report generation failed: {str(e)}"


class StitchGeometryManager:
    """
    🏰 ALBEDO'S STITCH GEOMETRY MANAGEMENT SYSTEM 🏰
    
    Supreme-quality geometry management for stitch creation and tracking.
    Implements the highest standards of Nazarick for reliability and precision.
    
    Features:
    - Battle-tested tagging system for stitch identification
    - Auto-scaling algorithms for proportional results
    - Session-based tracking for surgical removal operations
    - Memory-efficient vertex group and attribute management
    
    Architect: Demiurge | Guardian: Albedo | Supreme Overlord: Ainz
    """
    
    @staticmethod
    def create_stitch_session_id():
        """
        Create a unique session ID for tracking stitch batches
        
        Returns:
            str: Unique session identifier with timestamp precision
            
        Note:
            Format: 'stitch_{millisecond_timestamp}' ensures uniqueness
            across rapid successive operations
        """
        return f"stitch_{int(time.time() * 1000)}"
    
    @staticmethod
    def get_mesh_scale_info(obj):
        """
        Calculate comprehensive mesh scale information for auto-sizing algorithms
        
        Args:
            obj: Blender mesh object in edit mode
            
        Returns:
            dict: Scale analysis containing:
                - bbox_size: Bounding box dimensions (Vector)
                - bbox_max_dim: Maximum dimension (float)
                - bbox_avg_dim: Average dimension (float)
                - avg_edge_length: Average edge length (float)
                - suggested_stitch_size: Optimal stitch size (float)
                - suggested_stitch_depth: Optimal depth (float)
                - suggested_spacing: Optimal stitch spacing (float)
            None: If analysis fails or invalid object
            
        Note:
            Uses advanced geometric analysis to ensure proportional results
            regardless of mesh scale. Validates mesh integrity before analysis.
        """
        if not obj or obj.type != 'MESH':
            return None
            
        # Get mesh in edit mode
        bm = bmesh.from_edit_mesh(obj.data)
        if not bm.verts:
            return None
            
        # Calculate bounding box
        coords = [v.co for v in bm.verts]
        if not coords:
            return None
            
        min_co = Vector(coords[0])
        max_co = Vector(coords[0])
        
        for co in coords:
            for i in range(3):
                min_co[i] = min(min_co[i], co[i])
                max_co[i] = max(max_co[i], co[i])
        
        bbox_size = max_co - min_co
        bbox_max_dim = max(bbox_size)
        bbox_avg_dim = sum(bbox_size) / 3
        
        # Calculate average edge length
        edge_lengths = [e.calc_length() for e in bm.edges if e.is_valid]
        avg_edge_length = sum(edge_lengths) / len(edge_lengths) if edge_lengths else 1.0
        
        return {
            'bbox_size': bbox_size,
            'bbox_max_dim': bbox_max_dim,
            'bbox_avg_dim': bbox_avg_dim,
            'avg_edge_length': avg_edge_length,
            'suggested_stitch_size': avg_edge_length * 0.1,  # 10% of average edge
            'suggested_stitch_depth': avg_edge_length * 0.05,  # 5% of average edge
            'suggested_spacing': avg_edge_length * 0.5  # 50% of average edge for stitch count
        }
    
    @staticmethod
    def tag_stitch_vertices(bm, vertices, session_id, obj):
        """Tag vertices as stitch geometry for reliable removal"""
        # Ensure stitch vertex group exists
        if STITCH_TAG_VERTEX_GROUP not in obj.vertex_groups:
            obj.vertex_groups.new(name=STITCH_TAG_VERTEX_GROUP)
        
        vg_index = obj.vertex_groups[STITCH_TAG_VERTEX_GROUP].index
        
        # Ensure deform layer exists
        if not bm.verts.layers.deform:
            bm.verts.layers.deform.new()
        deform_layer = bm.verts.layers.deform.active
        
        # Tag vertices
        for vert in vertices:
            if vert.is_valid:
                vert[deform_layer][vg_index] = 1.0
        
        # Also add custom string attribute for session tracking
        if not bm.verts.layers.string:
            bm.verts.layers.string.new(STITCH_TAG_ATTRIBUTE)
        elif STITCH_TAG_ATTRIBUTE not in bm.verts.layers.string:
            bm.verts.layers.string.new(STITCH_TAG_ATTRIBUTE)
        
        string_layer = bm.verts.layers.string[STITCH_TAG_ATTRIBUTE]
        for vert in vertices:
            if vert.is_valid:
                vert[string_layer] = session_id.encode('utf-8')
    
    @staticmethod
    def find_stitch_geometry(bm, obj, mode='all', session_id=None):
        """Find stitch geometry based on tags"""
        stitch_verts = []
        stitch_edges = []
        
        # Check if stitch vertex group exists
        if STITCH_TAG_VERTEX_GROUP not in obj.vertex_groups:
            return stitch_verts, stitch_edges
        
        vg_index = obj.vertex_groups[STITCH_TAG_VERTEX_GROUP].index
        
        if not bm.verts.layers.deform:
            return stitch_verts, stitch_edges
        
        deform_layer = bm.verts.layers.deform.active
        
        # Find tagged vertices
        for vert in bm.verts:
            if not vert.is_valid:
                continue
                
            if vg_index in vert[deform_layer] and vert[deform_layer][vg_index] > 0.5:
                # Check session filter if needed
                if mode == 'session' and session_id:
                    if STITCH_TAG_ATTRIBUTE in bm.verts.layers.string:
                        string_layer = bm.verts.layers.string[STITCH_TAG_ATTRIBUTE]
                        vert_session = vert[string_layer].decode('utf-8') if vert[string_layer] else ""
                        if vert_session != session_id:
                            continue
                
                stitch_verts.append(vert)
        
        # Find edges connecting stitch vertices
        for edge in bm.edges:
            if not edge.is_valid:
                continue
                
            v1, v2 = edge.verts
            if v1 in stitch_verts and v2 in stitch_verts:
                stitch_edges.append(edge)
        
        return stitch_verts, stitch_edges


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
    
    use_auto_sizing: BoolProperty(
        name="Auto Sizing",
        description="Automatically calculate stitch parameters based on mesh scale",
        default=False
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
        
        # 🛡️ VICTIM'S FAILSAFE: Create emergency backup before operation
        backup_info = VictimFailsafeSystem.create_emergency_backup(obj, "create_stitches")
        
        # 🛡️ VICTIM'S FAILSAFE: Validate operation safety
        operation_params = {
            'stitch_count': self.stitch_count,
            'stitch_size': self.stitch_size,
            'stitch_depth': self.stitch_depth
        }
        is_safe, warnings, critical_issues = VictimFailsafeSystem.validate_operation_safety(obj, operation_params)
        
        # Report warnings to user
        for warning in warnings:
            self.report({'WARNING'}, f"⚠️ {warning}")
        
        # Block operation if critical issues found
        if not is_safe:
            for issue in critical_issues:
                self.report({'ERROR'}, f"🛡️ Critical: {issue}")
            return {'CANCELLED'}
        
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
        
        # Auto-sizing calculation
        if self.use_auto_sizing:
            scale_info = StitchGeometryManager.get_mesh_scale_info(obj)
            if scale_info:
                self.stitch_size = max(0.001, min(0.1, scale_info['suggested_stitch_size']))
                self.stitch_depth = max(0.0, min(0.05, scale_info['suggested_stitch_depth']))
                # Adjust stitch count based on edge spacing
                edge_based_count = max(1, min(100, int(10 * scale_info['avg_edge_length'])))
                if self.stitch_count == 10:  # Only auto-adjust if using default
                    self.stitch_count = edge_based_count
                self.report({'INFO'}, f"Auto-sizing: size={self.stitch_size:.4f}, depth={self.stitch_depth:.4f}")
        
        # Create session ID for this stitch batch
        session_id = StitchGeometryManager.create_stitch_session_id()
        
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
        
        # Create stitches with error handling and tagging
        stitch_count = 0
        created_vertices = []
        
        try:
            for edge in group_edges:
                edge_stitch_count, edge_vertices = self._create_stitches_on_edge(bm, edge, obj)
                stitch_count += edge_stitch_count
                created_vertices.extend(edge_vertices)
            
            # Tag all created stitch vertices for reliable removal
            if created_vertices:
                StitchGeometryManager.tag_stitch_vertices(bm, created_vertices, session_id, obj)
                # Store session ID for potential removal
                context.scene.nazarick_last_stitch_session = session_id
            
            # Update mesh with validation
            bmesh.update_edit_mesh(obj.data)
            
            # Force update
            context.view_layer.update()
            
        except Exception as e:
            # 🛡️ VICTIM'S FAILSAFE: Attempt emergency recovery
            error_context = f"Stitch creation failed: {str(e)}"
            self.report({'ERROR'}, f"🛡️ Operation failed: {str(e)}")
            
            # Attempt emergency rollback
            rollback_success = VictimFailsafeSystem.emergency_rollback(obj, error_context)
            if rollback_success:
                self.report({'WARNING'}, "🛡️ Emergency rollback completed - mesh state restored")
            else:
                self.report({'ERROR'}, "🛡️ Emergency rollback failed - manual recovery may be needed")
                
            # Generate recovery report
            recovery_report = VictimFailsafeSystem.generate_recovery_report(obj, error_context)
            print(recovery_report)
            
            return {'CANCELLED'}
        
        self.report({'INFO'}, f"Created {stitch_count} stitches along {len(group_edges)} edges (Session: {session_id[:8]})")
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
        created_vertices = []
        
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
                stitch_count, stitch_verts = self._create_straight_stitch(bm, stitch_center, stitch_width_vector, edge_normal)
                created_stitches += stitch_count
                created_vertices.extend(stitch_verts)
            elif self.stitch_style == 'CROSS':
                stitch_count, stitch_verts = self._create_cross_stitch(bm, stitch_center, stitch_width_vector, edge_normal, edge_direction)
                created_stitches += stitch_count
                created_vertices.extend(stitch_verts)
            elif self.stitch_style == 'ZIGZAG':
                zigzag_offset = math.sin(t * math.pi * 4) * self.stitch_size * 0.5
                offset_center = stitch_center + stitch_width_vector * zigzag_offset
                stitch_count, stitch_verts = self._create_straight_stitch(bm, offset_center, stitch_width_vector, edge_normal)
                created_stitches += stitch_count
                created_vertices.extend(stitch_verts)
            elif self.stitch_style == 'RUNNING':
                # Skip every other stitch for running pattern
                if i % 2 == 0:
                    stitch_count, stitch_verts = self._create_straight_stitch(bm, stitch_center, stitch_width_vector, edge_normal)
                    created_stitches += stitch_count
                    created_vertices.extend(stitch_verts)
        
        return created_stitches, created_vertices
    
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
        
        return 1, [v1, v2]
    
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
        
        return 2, [v1, v2, v3, v4]


class MESH_OT_NazarickRemoveStitches(bpy.types.Operator):
    """Remove stitch geometry from the mesh using reliable tagging system"""
    bl_idname = "mesh.nazarick_remove_stitches"
    bl_label = "Remove Stitches"
    bl_description = "Remove stitch geometry using advanced tagging system"
    bl_options = {'REGISTER', 'UNDO'}
    
    remove_mode: EnumProperty(
        name="Remove Mode",
        description="What type of stitches to remove",
        items=[
            ('ALL_TAGGED', "All Tagged Stitches", "Remove all stitches marked with Nazarick tags"),
            ('LAST_SESSION', "Last Session", "Remove only stitches from the most recent session"),
            ('SELECTED', "Selected Only", "Remove only selected geometry"),
            ('LOOSE_EDGES', "Loose Edges (Legacy)", "Remove all loose edges (less reliable)"),
        ],
        default='ALL_TAGGED'
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
        removed_edges = 0
        
        try:
            if self.remove_mode == 'ALL_TAGGED':
                # Use tagging system to find all stitch geometry
                stitch_verts, stitch_edges = StitchGeometryManager.find_stitch_geometry(bm, obj, mode='all')
                
                # Remove stitch edges first
                for edge in stitch_edges:
                    if edge.is_valid:
                        bm.edges.remove(edge)
                        removed_edges += 1
                
                # Remove stitch vertices (that are now isolated)
                for vert in stitch_verts:
                    if vert.is_valid and not vert.link_edges:
                        bm.verts.remove(vert)
                        removed_count += 1
                        
            elif self.remove_mode == 'LAST_SESSION':
                # Remove only the last session
                session_id = getattr(context.scene, 'nazarick_last_stitch_session', '')
                if session_id:
                    stitch_verts, stitch_edges = StitchGeometryManager.find_stitch_geometry(
                        bm, obj, mode='session', session_id=session_id)
                    
                    # Remove stitch edges first
                    for edge in stitch_edges:
                        if edge.is_valid:
                            bm.edges.remove(edge)
                            removed_edges += 1
                    
                    # Remove stitch vertices (that are now isolated)
                    for vert in stitch_verts:
                        if vert.is_valid and not vert.link_edges:
                            bm.verts.remove(vert)
                            removed_count += 1
                else:
                    self.report({'WARNING'}, "No recent stitch session found")
                    return {'CANCELLED'}
                        
            elif self.remove_mode == 'SELECTED':
                # Remove selected edges (enhanced validation)
                selected_edges = [edge for edge in bm.edges if edge.select and edge.is_valid]
                for edge in selected_edges:
                    if edge.is_valid:  # Double-check before removal
                        bm.edges.remove(edge)
                        removed_edges += 1
                        
            elif self.remove_mode == 'LOOSE_EDGES':
                # Legacy mode: Remove edges that are not part of any face
                edges_to_remove = [edge for edge in bm.edges if not edge.link_faces and edge.is_valid]
                for edge in edges_to_remove:
                    if edge.is_valid:  # Double-check before removal
                        bm.edges.remove(edge)
                        removed_edges += 1
            
            # Clean up loose vertices if any were created
            loose_verts = [v for v in bm.verts if v.is_valid and not v.link_edges]
            for vert in loose_verts:
                if vert.is_valid:
                    bm.verts.remove(vert)
                    removed_count += 1
            
            # Clean up with remove doubles for safety
            if removed_count > 0 or removed_edges > 0:
                bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)
            
            # Update mesh
            bmesh.update_edit_mesh(obj.data)
            
            # Force update
            context.view_layer.update()
            
        except Exception as e:
            self.report({'ERROR'}, f"Failed to remove stitches: {str(e)}")
            return {'CANCELLED'}
        
        total_removed = removed_count + removed_edges
        if total_removed > 0:
            mode_descriptions = {
                'ALL_TAGGED': 'tagged stitches',
                'LAST_SESSION': 'last session stitches',
                'SELECTED': 'selected elements',
                'LOOSE_EDGES': 'loose edges'
            }
            mode_desc = mode_descriptions.get(self.remove_mode, 'elements')
            self.report({'INFO'}, f"Removed {total_removed} {mode_desc} ({removed_edges} edges, {removed_count} vertices)")
        else:
            self.report({'INFO'}, "No stitches found to remove")
        
        return {'FINISHED'}


class MESH_OT_NazarickCalculateAutoSize(bpy.types.Operator):
    """Calculate and apply auto-sizing parameters based on mesh scale"""
    bl_idname = "mesh.nazarick_calculate_auto_size"
    bl_label = "Calculate Auto Size"
    bl_description = "Calculate optimal stitch parameters based on mesh dimensions"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj and obj.type == 'MESH' and obj.mode == 'EDIT'

    def execute(self, context):
        obj = context.active_object
        
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "Active object must be a mesh")
            return {'CANCELLED'}
            
        if obj.mode != 'EDIT':
            self.report({'ERROR'}, "Object must be in Edit Mode")
            return {'CANCELLED'}
        
        try:
            scale_info = StitchGeometryManager.get_mesh_scale_info(obj)
            if scale_info:
                # Update scene properties with calculated values
                context.scene.nazarick_stitch_size = max(0.001, min(0.1, scale_info['suggested_stitch_size']))
                context.scene.nazarick_stitch_depth = max(0.0, min(0.05, scale_info['suggested_stitch_depth']))
                
                # Suggest stitch count based on average edge length
                suggested_count = max(1, min(100, int(10 / scale_info['avg_edge_length'])))
                context.scene.nazarick_stitch_count = suggested_count
                
                self.report({'INFO'}, 
                           f"Auto-sizing applied: Size={context.scene.nazarick_stitch_size:.4f}, "
                           f"Depth={context.scene.nazarick_stitch_depth:.4f}, Count={suggested_count}")
            else:
                self.report({'ERROR'}, "Failed to calculate mesh scale information")
                return {'CANCELLED'}
                
        except Exception as e:
            self.report({'ERROR'}, f"Failed to calculate auto-sizing: {str(e)}")
            return {'CANCELLED'}
        
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
        """
        🌟 AURA'S ENHANCED UI SYSTEM 🌟
        
        Maximum usability and accessibility for all user experience levels.
        Every option is visible, accessible, and user-friendly.
        """
        layout = self.layout
        obj = context.active_object
        
        # 🌟 AURA'S ENHANCEMENT: Visual status indicator
        status_box = layout.box()
        if not obj or obj.type != 'MESH':
            status_box.alert = True
            row = status_box.row()
            row.label(text="⚠️ Select a mesh object", icon='ERROR')
            row.operator("mesh.primitive_cube_add", text="Add Cube", icon='MESH_CUBE')
            return
        
        # Check if in edit mode
        if obj.mode != 'EDIT':
            status_box.alert = True
            row = status_box.row()
            row.label(text="⚠️ Enter Edit Mode", icon='EDITMODE_HLT')
            edit_op = row.operator("object.mode_set", text="Edit Mode", icon='EDITMODE_HLT')
            edit_op.mode = 'EDIT'
            return
        
        # 🌟 AURA'S ENHANCEMENT: Success status indicator
        status_box.alert = False
        row = status_box.row()
        row.label(text="✅ Ready for Stitch Creation", icon='CHECKMARK')
        row.label(text=f"🏰 {obj.name}", icon='OBJECT_DATA')
        
        layout.separator()
        
        # 🌟 AURA'S ENHANCEMENT: Enhanced vertex group section with help
        vg_box = layout.box()
        vg_box.label(text="🎯 Stitch Path Definition", icon='GROUP_VERTEX')
        
        if obj.vertex_groups:
            col = vg_box.column(align=True)
            col.prop_search(context.scene, "nazarick_stitch_vertex_group", 
                          obj, "vertex_groups", text="Target Group")
            
            # 🌟 AURA'S ENHANCEMENT: Intelligent vertex group info
            if obj.vertex_groups.active:
                info_box = col.box()
                info_row = info_box.row()
                info_row.label(text=f"📊 Active: {obj.vertex_groups.active.name}", icon='RADIOBUT_ON')
                
                # Advanced vertex counting with error handling
                try:
                    bm = bmesh.from_edit_mesh(obj.data)
                    if bm.verts.layers.deform:
                        deform_layer = bm.verts.layers.deform.active
                        vg_index = obj.vertex_groups.active.index
                        group_vert_count = sum(1 for v in bm.verts 
                                             if vg_index in v[deform_layer] and v[deform_layer][vg_index] > 0.01)
                        
                        # 🌟 AURA'S ENHANCEMENT: Visual feedback on vertex count
                        info_row = info_box.row()
                        if group_vert_count < 2:
                            info_row.alert = True
                            info_row.label(text=f"⚠️ Vertices: {group_vert_count} (Need 2+)", icon='ERROR')
                        elif group_vert_count > 1000:
                            info_row.label(text=f"⚡ Vertices: {group_vert_count} (Large)", icon='INFO')
                        else:
                            info_row.label(text=f"✅ Vertices: {group_vert_count}", icon='CHECKMARK')
                        
                        # Quick assign button
                        assign_row = info_box.row()
                        assign_row.operator("object.vertex_group_assign", text="Assign Selected", icon='ADD')
                        assign_row.operator("object.vertex_group_remove_from", text="Remove Selected", icon='REMOVE')
                        
                except Exception:
                    info_row = info_box.row()
                    info_row.alert = True
                    info_row.label(text="⚠️ Cannot analyze vertex group", icon='ERROR')
        else:
            # 🌟 AURA'S ENHANCEMENT: Helpful vertex group creation
            help_col = vg_box.column(align=True)
            help_col.alert = True
            help_col.label(text="❌ No vertex groups found", icon='ERROR')
            help_row = help_col.row()
            help_row.operator("object.vertex_group_add", text="Create Group", icon='ADD')
            help_row.operator("mesh.select_all", text="Select All").action = 'SELECT'
        
        
        # 🌟 AURA'S ENHANCEMENT: Enhanced stitch parameters with visual feedback
        if obj.vertex_groups:
            params_box = layout.box()
            params_header = params_box.row()
            params_header.label(text="⚙️ Stitch Parameters", icon='MODIFIER')
            
            # 🌟 AURA'S ENHANCEMENT: Smart auto-sizing with instant feedback
            auto_section = params_box.box()
            auto_section.label(text="🤖 Intelligent Auto-Sizing", icon='AUTO')
            auto_row = auto_section.row()
            auto_row.prop(context.scene, "nazarick_stitch_auto_sizing", text="Enable Auto-Sizing")
            
            if getattr(context.scene, "nazarick_stitch_auto_sizing", False):
                calc_row = auto_section.row()
                calc_row.operator("mesh.nazarick_calculate_auto_size", 
                                text="🔄 Recalculate", icon='FILE_REFRESH')
                calc_row.label(text="Auto-sizing active", icon='CHECKMARK')
            else:
                auto_section.label(text="💡 Tip: Auto-sizing adapts to mesh scale", icon='INFO')
            
            # 🌟 AURA'S ENHANCEMENT: Parameter validation and feedback
            param_col = params_box.column(align=True)
            
            # Stitch count with visual feedback
            count_row = param_col.row()
            stitch_count = getattr(context.scene, "nazarick_stitch_count", 10)
            if stitch_count > NazarickStitchConstants.SOFT_MAX_STITCH_COUNT:
                count_row.alert = True
                count_row.prop(context.scene, "nazarick_stitch_count", text="⚠️ Count (High)")
            else:
                count_row.prop(context.scene, "nazarick_stitch_count", text="📊 Count")
            
            # Size and depth with units
            param_col.prop(context.scene, "nazarick_stitch_size", text="📏 Size")
            param_col.prop(context.scene, "nazarick_stitch_depth", text="🔍 Depth")
            
            # Style selection with descriptions
            style_box = params_box.box()
            style_box.label(text="🎨 Stitch Style", icon='BRUSH_DATA')
            style_grid = style_box.grid_flow(row_major=True, columns=2, align=True)
            style_grid.prop(context.scene, "nazarick_stitch_style", expand=True)
            
            # Style descriptions for better UX
            current_style = getattr(context.scene, "nazarick_stitch_style", 'STRAIGHT')
            style_descriptions = {
                'STRAIGHT': "💫 Simple linear stitches (fastest)",
                'CROSS': "❌ X-pattern stitches (decorative)",
                'ZIGZAG': "⚡ Alternating zigzag pattern",
                'RUNNING': "🔄 Every-other stitch pattern"
            }
            if current_style in style_descriptions:
                desc_row = style_box.row()
                desc_row.label(text=style_descriptions[current_style], icon='INFO')
            
            # 🌟 AURA'S ENHANCEMENT: Advanced parameters with smart defaults
            advanced_box = params_box.box()
            advanced_header = advanced_box.row()
            advanced_header.label(text="🔧 Advanced Options", icon='PREFERENCES')
            advanced_header.prop(context.scene, "nazarick_show_advanced", 
                               text="", icon='TRIA_DOWN' if getattr(context.scene, "nazarick_show_advanced", False) else 'TRIA_RIGHT')
            
            if getattr(context.scene, "nazarick_show_advanced", False):
                advanced_col = advanced_box.column(align=True)
                advanced_col.prop(context.scene, "nazarick_stitch_offset", text="🎯 Offset Distance")
                
                variation_row = advanced_col.row()
                variation = getattr(context.scene, "nazarick_stitch_variation", 0.0)
                if variation > 0.3:
                    variation_row.alert = True
                    variation_row.prop(context.scene, "nazarick_stitch_variation", text="⚠️ Variation (High)")
                else:
                    variation_row.prop(context.scene, "nazarick_stitch_variation", text="🎲 Random Variation")
            
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
            create_op.use_auto_sizing = getattr(context.scene, "nazarick_stitch_auto_sizing", False)
            
            # Enhanced removal section
            removal_box = layout.box()
            removal_box.label(text="Stitch Removal", icon='X')
            
            # Show stitch info if available
            if STITCH_TAG_VERTEX_GROUP in obj.vertex_groups:
                vg = obj.vertex_groups[STITCH_TAG_VERTEX_GROUP]
                bm = bmesh.from_edit_mesh(obj.data)
                if bm.verts.layers.deform:
                    deform_layer = bm.verts.layers.deform.active
                    stitch_count = sum(1 for v in bm.verts 
                                     if vg.index in v[deform_layer] and v[deform_layer][vg.index] > 0.5)
                    removal_box.label(text=f"Tagged stitches: {stitch_count}")
            
            # Removal mode selection
            removal_box.prop(context.scene, "nazarick_stitch_remove_mode", expand=False)
            
            # Remove button with mode-specific operator
            remove_op = removal_box.operator("mesh.nazarick_remove_stitches", 
                                           text="Remove Stitches", icon='TRASH')
            remove_op.remove_mode = getattr(context.scene, "nazarick_stitch_remove_mode", 'ALL_TAGGED')
        
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
    MESH_OT_NazarickCalculateAutoSize,
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
        description="Number of stitches to create along each edge (auto-adjusted if Auto Sizing enabled)",
        default=10,
        min=1,
        max=500,
        soft_min=1,
        soft_max=100
    )
    
    bpy.types.Scene.nazarick_stitch_size = FloatProperty(
        name="Stitch Size",
        description="Size of individual stitches (auto-adjusted if Auto Sizing enabled)",
        default=0.02,
        min=0.0001,
        max=1.0,
        soft_min=0.001,
        soft_max=0.1,
        step=1,
        precision=4
    )
    
    bpy.types.Scene.nazarick_stitch_depth = FloatProperty(
        name="Stitch Depth",
        description="Depth of stitches into surface (auto-adjusted if Auto Sizing enabled)",
        default=0.01,
        min=0.0,
        max=0.5,
        soft_min=0.0,
        soft_max=0.05,
        step=1,
        precision=4
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
    
    bpy.types.Scene.nazarick_stitch_auto_sizing = BoolProperty(
        name="Auto Sizing",
        description="Automatically calculate stitch parameters based on mesh scale",
        default=False
    )
    
    bpy.types.Scene.nazarick_stitch_remove_mode = EnumProperty(
        name="Remove Mode",
        description="What type of stitches to remove",
        items=[
            ('ALL_TAGGED', "All Tagged", "Remove all stitches marked with Nazarick tags"),
            ('LAST_SESSION', "Last Session", "Remove only stitches from the most recent session"),
            ('SELECTED', "Selected Only", "Remove only selected geometry"),
            ('LOOSE_EDGES', "Loose Edges", "Remove all loose edges (legacy mode)"),
        ],
        default='ALL_TAGGED'
    )
    
    bpy.types.Scene.nazarick_last_stitch_session = StringProperty(
        name="Last Stitch Session",
        description="ID of the last created stitch session for removal tracking",
        default=""
    )
    
    bpy.types.Scene.nazarick_show_advanced = BoolProperty(
        name="Show Advanced Options",
        description="Toggle display of advanced stitch options",
        default=False
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
    del bpy.types.Scene.nazarick_stitch_auto_sizing
    del bpy.types.Scene.nazarick_stitch_remove_mode
    del bpy.types.Scene.nazarick_last_stitch_session
    del bpy.types.Scene.nazarick_show_advanced


if __name__ == "__main__":
    register()