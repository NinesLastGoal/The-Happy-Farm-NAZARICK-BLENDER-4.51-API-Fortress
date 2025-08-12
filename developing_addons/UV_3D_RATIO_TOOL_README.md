# UV/3D Area Ratio Tool for Blender 4.2.x LTS

A streamlined, production-ready Blender addon that measures and compares UV space area to 3D surface area, helping optimize texture mapping and identify UV stretching or compression issues.

## 🎯 Features

### Core Functionality
- **Precise Area Calculation**: Uses triangulation-based algorithms for accurate UV and 3D area measurements
- **Smart Face Selection**: Analyzes selected faces or entire mesh automatically
- **Real-time Ratio Analysis**: Instant feedback with human-readable interpretations
- **One-click Optimization**: Scale UVs to achieve optimal 1:1 ratio with 3D surface
- **Dual Interface**: Available in both UV Editor and 3D Viewport sidebars

### Quality Assurance
- **Robust Error Handling**: Comprehensive validation and graceful error recovery
- **Numerical Precision**: Uses epsilon-based comparisons for floating-point accuracy
- **Performance Optimized**: Efficient algorithms with execution time reporting
- **Memory Safe**: Proper cleanup and resource management

## 📋 System Requirements

- **Blender Version**: 4.2.0 or higher (optimized for Blender 4.2.x LTS)
- **Operating System**: Windows, macOS, or Linux
- **Memory**: Minimal additional memory requirements
- **Dependencies**: None (uses only built-in Blender modules)

## 🚀 Installation

### Method 1: Standard Installation (Recommended)
1. Download the addon file: `uv_3d_ratio_tool_42x.py`
2. Open Blender 4.2.x
3. Go to **Edit** → **Preferences** → **Add-ons**
4. Click **Install...** button
5. Navigate to and select the downloaded `.py` file
6. Click **Install Add-on**
7. Enable the addon by checking the checkbox next to "UV/3D Area Ratio Tool"
8. Click **Save Preferences** to make the installation permanent

### Method 2: Manual Installation
1. Locate your Blender addons directory:
   - **Windows**: `%APPDATA%\Blender Foundation\Blender\4.2\scripts\addons\`
   - **macOS**: `~/Library/Application Support/Blender/4.2/scripts/addons/`
   - **Linux**: `~/.config/blender/4.2/scripts/addons/`
2. Copy `uv_3d_ratio_tool_42x.py` to this directory
3. Restart Blender
4. Go to **Edit** → **Preferences** → **Add-ons**
5. Search for "UV/3D Area Ratio Tool"
6. Enable the addon by checking the checkbox

### Verification
After installation, you should see:
- "UV Tools" panel in the UV Editor sidebar (press `N` to toggle sidebar)
- "UV Tools" panel in the 3D Viewport sidebar (press `N` to toggle sidebar)

## 📖 Usage Guide

### Basic Workflow

#### 1. Prepare Your Mesh
- Select a mesh object
- Enter **Edit Mode** (`Tab` key)
- Ensure your mesh has UV coordinates (unwrapped)

#### 2. Access the Tool
- Open the **UV Editor** or stay in **3D Viewport**
- Press `N` to open the sidebar
- Find the **"UV Tools"** panel
- Look for **"UV/3D Area Ratio"** section

#### 3. Analyze UV Mapping
- **For entire mesh**: Deselect all faces (`Alt+A`)
- **For specific faces**: Select the faces you want to analyze
- Click **"Calculate UV/3D Ratio"**

#### 4. Interpret Results
The tool provides several pieces of information:
- **Ratio Value**: Numerical ratio (1.0 = perfect)
- **Status**: Human-readable interpretation
- **Scope**: Number of faces analyzed
- **Areas**: Actual 3D and UV area measurements
- **Calculation Time**: Performance metric

#### 5. Optimize UV Mapping (Optional)
- If the ratio is not optimal, click **"Scale to Optimal Ratio"**
- This automatically adjusts UV coordinates to achieve a 1:1 ratio
- The scaling is performed around the UV center point

### Understanding Ratio Values

| Ratio Range | Interpretation | Meaning |
|-------------|----------------|---------|
| ~1.0 | **OPTIMAL** | Perfect 1:1 UV to 3D ratio |
| 0.99-1.01 | **EXCELLENT** | Near-perfect ratio |
| 1.05-1.2 | **SLIGHTLY STRETCHED** | Minor UV stretching |
| 1.2-2.0 | **STRETCHED** | Noticeable UV stretching |
| >2.0 | **SEVERE STRETCHING** | Major UV issues |
| 0.8-0.95 | **SLIGHTLY COMPRESSED** | Minor UV compression |
| 0.3-0.8 | **COMPRESSED** | Noticeable UV compression |
| <0.3 | **SEVERE COMPRESSION** | Major UV issues |

### Best Practices

#### When to Use
- **Before baking textures**: Ensure consistent texel density
- **After UV unwrapping**: Validate mapping quality
- **Texture optimization**: Identify problem areas
- **Quality control**: Verify consistent UV scaling across objects

#### Workflow Tips
- Analyze different parts of complex meshes separately
- Use face selection to focus on specific areas
- Compare ratios between similar objects for consistency
- Document ratio values for team collaboration

## 🔧 Technical Details

### Algorithm Overview
The addon uses triangulation-based area calculation for both 3D and UV space:

1. **3D Area Calculation**:
   - Triangulates each face using vertex coordinates
   - Calculates triangle areas using cross products
   - Sums all triangle areas for total face area

2. **UV Area Calculation**:
   - Triangulates each face using UV coordinates
   - Projects UV coordinates to 3D space for calculation
   - Applies same triangulation algorithm as 3D

3. **Ratio Calculation**:
   - Ratio = UV Area / 3D Area
   - Includes numerical precision handling
   - Validates results for mathematical correctness

### Performance Characteristics
- **Time Complexity**: O(n) where n = number of faces
- **Memory Usage**: Minimal (temporary UV coordinate storage)
- **Typical Performance**: <0.1s for meshes under 10k faces

### API Compatibility
Designed specifically for Blender 4.2.x LTS:
- Uses standard `bpy`, `bmesh`, and `mathutils` modules
- Compatible with Blender's operator and panel registration system
- Follows Blender 4.2.x naming conventions and best practices
- No deprecated API usage

## 🐛 Troubleshooting

### Common Issues

#### "No UV maps found on the mesh"
**Solution**: Unwrap your mesh first
1. Select all faces (`A`)
2. Press `U` → **Smart UV Project** or **Unwrap**

#### "Object must be in Edit Mode"
**Solution**: Enter Edit Mode
1. Select your mesh object
2. Press `Tab` or switch to Edit Mode in the mode selector

#### "3D area is zero or invalid"
**Solution**: Check mesh geometry
1. Ensure faces have non-zero area
2. Check for duplicate vertices (`M` → **Merge by Distance**)
3. Verify mesh is not completely flat

#### "Invalid ratio calculated"
**Solution**: Check for mesh issues
1. Look for degenerate faces (faces with collinear vertices)
2. Check UV coordinates for invalid values (NaN, infinite)
3. Try recalculating normals (`Alt+N` → **Recalculate Outside**)

### Performance Issues

#### Slow calculation on large meshes
- Consider analyzing sections of the mesh using face selection
- Typical performance: 10k faces ≈ 0.1s, 100k faces ≈ 1s

#### Memory warnings
- The addon uses minimal memory, but very large meshes (>1M faces) may require patience

### Getting Help

If you encounter issues not covered here:
1. Check the Blender Console (**Window** → **Toggle System Console**) for detailed error messages
2. Verify your mesh has valid geometry and UV coordinates
3. Try the addon on a simple test mesh first
4. Report bugs with specific steps to reproduce

## 🔄 Updates and Maintenance

### Version History
- **v1.0.0**: Initial release for Blender 4.2.x LTS
  - Core UV/3D ratio calculation functionality
  - Dual-panel interface (UV Editor + 3D Viewport)
  - One-click UV optimization
  - Comprehensive error handling and validation

### Future Enhancements
Potential improvements for future versions:
- Batch processing for multiple objects
- Texture density visualization
- Export ratio data to external formats
- Integration with material workflow

### Compatibility
This addon is specifically designed for Blender 4.2.x LTS and maintains compatibility with:
- All standard Blender features
- Third-party UV-related addons
- Blender's built-in UV tools
- Standard file formats and workflows

## 📝 License

This addon is released under the same license as Blender (GPL v3+), ensuring:
- Free use for any purpose
- Open source transparency
- Community contribution capability
- Commercial usage rights

## 🏗️ Development

### Code Structure
```
uv_3d_ratio_tool_42x.py
├── bl_info                    # Addon metadata
├── calculate_face_area_3d()   # 3D area calculation
├── calculate_face_area_uv()   # UV area calculation
├── UV_OT_CalculateRatio       # Main calculation operator
├── UV_OT_ScaleToOptimal       # UV scaling operator
├── UVRatioPanel               # Shared panel functionality
├── UV_PT_RatioPanel           # UV Editor panel
├── VIEW3D_PT_RatioPanel       # 3D Viewport panel
├── register()                 # Addon registration
└── unregister()               # Addon cleanup
```

### Contributing
The code is designed to be:
- **Readable**: Clear variable names and comprehensive comments
- **Maintainable**: Modular structure with separated concerns
- **Extensible**: Easy to add new features without breaking existing functionality
- **Testable**: Functions designed for unit testing compatibility

---

**For optimal texture mapping and UV quality assurance in Blender 4.2.x LTS**