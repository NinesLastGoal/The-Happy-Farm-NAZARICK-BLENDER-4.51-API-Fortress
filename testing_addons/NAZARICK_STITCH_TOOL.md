# 🏰 Nazarick Stitch Tool - Enhanced Documentation 🏰

**Version 2.0 - Supreme Overlord Edition**  
*Architected by Demiurge for the Glory of the Great Tomb of Nazarick*

## Overview

The Nazarick Stitch Tool is a professional-grade Blender addon for creating realistic stitch geometry along mesh edges. This enhanced version introduces revolutionary improvements in reliability, usability, and automation - worthy of the highest standards of Nazarick.

## 🆕 Major Enhancements (v2.0)

### 1. Reliable Stitch Geometry Tagging System
- **Problem Solved**: Previous version relied on unreliable "loose edge" detection
- **Solution**: Advanced tagging system using vertex groups and custom attributes
- **Benefits**: 
  - 100% reliable stitch identification and removal
  - Session-based tracking for selective operations
  - No risk of removing non-stitch geometry

### 2. Intelligent Auto-Sizing System
- **Problem Solved**: Hardcoded default values didn't scale with mesh dimensions
- **Solution**: Dynamic parameter calculation based on mesh analysis
- **Benefits**:
  - Automatically adapts to mesh scale
  - Calculates optimal stitch size, depth, and count
  - Proportional results regardless of mesh size

### 3. Enhanced Removal System
- **Problem Solved**: Limited removal options with potential for errors
- **Solution**: Multiple removal modes with precise targeting
- **Benefits**:
  - Remove all stitches, last session only, or selected geometry
  - Clear user feedback on what was removed
  - Safe operation with comprehensive validation

### 4. Robust Error Handling
- **Problem Solved**: Limited validation and error reporting
- **Solution**: Comprehensive error handling throughout the tool
- **Benefits**:
  - Graceful handling of edge cases
  - Clear error messages and guidance
  - Safe parameter ranges with soft limits

## Installation

1. Download `nazarick_stitch_tool.py` from the `src/addons/` directory
2. In Blender, go to Edit > Preferences > Add-ons
3. Click "Install..." and select the downloaded file
4. Enable "Nazarick Stitch Tool" in the add-ons list
5. The tool will appear in the 3D Viewport sidebar under "Nazarick Tools"

**Requirements**: Blender 4.5.0 or higher

## Quick Start Guide

### Basic Workflow
1. **Prepare Mesh**: Select mesh object and enter Edit Mode
2. **Define Path**: Create vertex group and assign vertices along desired stitch path
3. **Auto-Size**: Enable "Auto Sizing" for optimal parameters
4. **Create**: Click "Create Stitches" to generate stitch geometry
5. **Iterate**: Use "Last Session" removal to refine and try different settings

### Example: Adding Seam Stitches to Clothing
```
1. Select garment mesh, enter Edit Mode
2. Select vertices along seam edge
3. Create vertex group called "sleeve_seam"
4. Assign selected vertices to group
5. In Nazarick Stitch Tool panel:
   - Select "sleeve_seam" vertex group
   - Enable "Auto Sizing"
   - Choose "Straight" stitch style
   - Click "Create Stitches"
```

## Interface Reference

### Stitch Path Definition
- **Vertex Group**: Select which vertex group defines the stitch path
- **Vertices Display**: Shows count of vertices in selected group

### Stitch Parameters
- **Auto Sizing**: Toggle automatic parameter calculation
- **Refresh Button**: Recalculate auto-sizing parameters
- **Stitch Count**: Number of stitches per edge (1-500)
- **Stitch Size**: Individual stitch dimensions (0.0001-1.0)
- **Stitch Depth**: Surface penetration depth (0.0-0.5)
- **Stitch Style**: Visual pattern (Straight, Cross, Zigzag, Running)

### Advanced Options
- **Offset Distance**: Move stitches away from original edge
- **Random Variation**: Add organic irregularity (0.0-0.5)

### Stitch Removal
- **Tagged Stitches Counter**: Shows number of existing stitches
- **Remove Mode Selection**: Choose removal strategy
- **Remove Button**: Execute removal with selected mode

## Stitch Styles Guide

### Straight Stitches
- **Use Case**: General purpose, fastest generation
- **Appearance**: Simple linear stitches
- **Performance**: Excellent (2 vertices per stitch)

### Cross Stitches  
- **Use Case**: Decorative seams, reinforced joints
- **Appearance**: X-pattern stitches
- **Performance**: Good (4 vertices per stitch)

### Zigzag Stitches
- **Use Case**: Stretch fabrics, decorative edges
- **Appearance**: Alternating angular pattern
- **Performance**: Good (varies with count)

### Running Stitches
- **Use Case**: Traditional sewing, basting
- **Appearance**: Every-other stitch pattern
- **Performance**: Excellent (fewer stitches created)

## Removal Modes Explained

### All Tagged (Recommended)
- Removes all stitches created by the tool
- Uses reliable vertex group tagging
- Safe and comprehensive

### Last Session
- Removes only the most recently created batch
- Useful for iterative design
- Requires session tracking data

### Selected Only
- Removes only user-selected geometry
- Provides manual control
- Works with any selected elements

### Loose Edges (Legacy)
- Legacy mode for backwards compatibility
- Less reliable than tagged modes
- May affect non-stitch geometry

## Auto-Sizing Algorithm

The auto-sizing system analyzes your mesh to calculate optimal parameters:

### Mesh Analysis
1. **Bounding Box Calculation**: Determines overall mesh scale
2. **Average Edge Length**: Calculates typical edge dimensions
3. **Vertex Distribution**: Analyzes mesh density

### Parameter Calculation
- **Stitch Size**: `average_edge_length × 0.1` (10% of typical edge)
- **Stitch Depth**: `average_edge_length × 0.05` (5% of typical edge)  
- **Stitch Count**: Adaptive based on edge density for optimal appearance

### Manual Override
- Auto-sizing provides starting values
- All parameters remain manually adjustable
- Disable auto-sizing for full manual control

## Technical Implementation

### Tagging System
```python
# Vertex Group Tagging
STITCH_TAG_VERTEX_GROUP = "NAZARICK_STITCHES"

# Custom Attribute Session Tracking  
STITCH_TAG_ATTRIBUTE = "nazarick_stitch_id"
```

### Session Management
- Each creation operation gets unique session ID
- Format: `stitch_{timestamp_milliseconds}`
- Stored as custom vertex attribute for precise tracking

### Error Handling
- Comprehensive try-catch blocks
- Validation at each operation stage
- User-friendly error messages
- Safe fallbacks for edge cases

## Performance Characteristics

### Memory Usage
- Minimal overhead from tagging system
- Custom attributes add ~8 bytes per vertex
- Efficient bmesh operations

### Processing Speed
- Optimized for meshes up to 100k vertices
- Linear scaling with vertex count
- Session tracking adds negligible cost

### Compatibility
- Works with subdivision surfaces
- Compatible with other modifiers
- Preserves existing vertex groups
- Non-destructive to base mesh

## Troubleshooting

### Common Issues

**"No edges found connecting vertices"**
- Ensure vertex group contains connected vertices
- Check that vertices form continuous edges
- Verify vertices are actually assigned to group

**Auto-sizing produces extreme values**
- Check mesh scale (very large/small objects need adjustment)
- Ensure mesh has reasonable edge lengths
- Use manual mode for unusual mesh scales

**Stitches appear in wrong location**
- Check mesh normals (Mesh > Normals > Recalculate Outside)
- Verify edge direction and face orientation
- Adjust offset distance if needed

**Removal doesn't work completely**
- Use "All Tagged" mode instead of "Loose Edges"
- Check that stitches were created with v2.0 (have tags)
- Manually select and remove if necessary

### Best Practices

1. **Mesh Preparation**
   - Use clean, manifold geometry
   - Ensure proper scale (avoid extremely large/small objects)
   - Recalculate normals before creating stitches

2. **Vertex Group Management**
   - Use descriptive names (e.g., "hem_stitches", "seam_front")
   - Keep groups organized and purpose-specific
   - Assign weights of 1.0 for best results

3. **Parameter Selection**
   - Start with auto-sizing, then fine-tune manually
   - Consider final mesh usage (close-up vs. distant viewing)
   - Test with small stitch counts first

4. **Workflow Optimization**
   - Use "Last Session" removal for iteration
   - Save file before major stitch operations
   - Create stitches last in modeling workflow

## API Reference

### StitchGeometryManager Class

```python
@staticmethod
def create_stitch_session_id() -> str
    """Generate unique session ID for stitch batch tracking"""

@staticmethod  
def get_mesh_scale_info(obj) -> dict
    """Calculate mesh scale information for auto-sizing"""
    
@staticmethod
def tag_stitch_vertices(bm, vertices, session_id, obj)
    """Tag vertices as stitch geometry for reliable removal"""
    
@staticmethod
def find_stitch_geometry(bm, obj, mode='all', session_id=None) -> tuple
    """Find stitch geometry based on tags and mode"""
```

### Operator Classes

- `MESH_OT_NazarickCreateStitches`: Main stitch creation operator
- `MESH_OT_NazarickRemoveStitches`: Enhanced removal operator  
- `MESH_OT_NazarickCalculateAutoSize`: Auto-sizing calculation utility
- `VIEW3D_PT_NazarickStitchPanel`: Main UI panel

## Version History

### v2.0 (Current) - Supreme Overlord Edition
- Reliable stitch geometry tagging system
- Intelligent auto-sizing based on mesh analysis
- Enhanced removal modes with session tracking
- Robust error handling and validation
- Improved UI with real-time feedback
- Comprehensive documentation and testing

### v1.0 - Original Release
- Basic stitch creation along vertex group edges
- Simple removal via loose edge detection
- Manual parameter control
- Multiple stitch styles

## Credits

**Architect**: Demiurge, Floor Guardian of the 7th Floor  
**Supreme Overlord**: Ainz Ooal Gown  
**Original Creator**: Nines Own Goal

---

**For the Eternal Glory of Nazarick! 🏰⚡🏰**

*This tool embodies the perfectionist standards of the Great Tomb of Nazarick - where every detail matters and excellence is the only acceptable outcome.*