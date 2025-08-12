# UV/3D Ratio Analysis Tool

A sleek and efficient Blender 4.5+ addon that provides minimal 3D surface area to UV area ratio analysis for selected objects with optional Geometry Nodes integration.

## Features

- ✅ **Efficient Calculation**: Calculate 3D surface area to UV area ratio for active mesh objects
- ✅ **Minimal UI**: Clean, simple UI panel in 3D View > Sidebar (N-panel)
- ✅ **Geometry Nodes Integration**: Optional toggle to write results to custom attributes
- ✅ **Smart Toggle**: When disabled, GeoNode attribute updates are skipped to reduce overhead
- ✅ **Blender 4.5+ Compatible**: Uses modern Blender API patterns
- ✅ **Proper Structure**: Organized in proper Blender addon directory structure
- ✅ **Well Documented**: Clear code comments for maintainability

## Installation

1. Download or clone this repository
2. Copy the `uv_3d_ratio_tool` folder to your Blender addons directory:
   - **Windows**: `%APPDATA%\Blender Foundation\Blender\4.5\scripts\addons\`
   - **macOS**: `~/Library/Application Support/Blender/4.5/scripts/addons/`
   - **Linux**: `~/.config/blender/4.5/scripts/addons/`
3. Open Blender and go to Edit > Preferences > Add-ons
4. Search for "UV/3D Ratio Analysis Tool" and enable it

## Usage

1. **Select a Mesh Object**: Make sure you have a mesh object selected
2. **Enter Edit Mode**: Switch to Edit Mode (Tab key)
3. **Open the Panel**: In the 3D Viewport, press 'N' to open the sidebar
4. **Find the Tool**: Look for the "UV/3D Ratio" panel in the sidebar
5. **Calculate Ratio**: Click "Calculate UV/3D Ratio" button
6. **Optional GeoNode Integration**: Enable the toggle to write results to custom attributes

## UI Panel Features

### Main Controls
- **Calculate UV/3D Ratio Button**: Performs the analysis calculation
- **Geometry Nodes Integration Toggle**: Enable/disable custom attribute writing

### Results Display
- **UV/3D Ratio Value**: Shows the calculated ratio (e.g., 1.2345)
- **Status Interpretation**: Describes the ratio (Optimal, Stretched, Compressed, etc.)
- **Detailed Values**: Shows 3D surface area and UV area values

### Geometry Nodes Integration
When the toggle is enabled:
- Creates a custom attribute named "UV_3D_Ratio"
- Attribute type: Float (per face)
- Accessible in Geometry Nodes for procedural workflows
- When disabled: No attribute updates for better performance

## Ratio Interpretation

- **0.95 - 1.05**: Optimal (1:1 ratio) - Perfect UV mapping
- **> 1.5**: UV Stretched - UVs are much larger than needed
- **< 0.5**: UV Compressed - UVs are much smaller than needed
- **1.05 - 1.5**: Slightly Stretched - Minor stretching detected
- **0.5 - 0.95**: Slightly Compressed - Minor compression detected

## Technical Details

### Requirements
- Blender 4.5+
- Mesh object with UV mapping
- Edit Mode for calculations

### Performance
- Efficient triangulation-based area calculations
- Optional GeoNode attribute updates to minimize overhead
- Validates input data to prevent errors

### API Usage
The addon uses modern Blender 4.5+ API patterns:
- `bmesh.from_edit_mesh()` for mesh data access
- `bpy.types.Operator` and `bpy.types.Panel` for UI
- `mesh_data.attributes.new()` for custom attributes
- Proper registration/unregistration system

## Development

### File Structure
```
uv_3d_ratio_tool/
├── __init__.py          # Main addon file
└── README.md           # This documentation
```

### Key Functions
- `calculate_3d_surface_area()`: Calculates 3D mesh surface area
- `calculate_uv_area()`: Calculates UV mapping area
- `UV3D_OT_CalculateRatio`: Main operator for calculations
- `UV3D_PT_RatioPanel`: UI panel for 3D viewport

### Testing
The addon includes comprehensive test validation:
```bash
python3 tests/test_uv3d_ratio_tool.py
```

## License

This addon follows the same license as Blender (GPL v2 or later).

## Credits

Developed for Blender 4.5+ API compatibility with focus on efficiency and minimalism.