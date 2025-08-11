# 🏰 UV3D Ratio Calculator - Nazarick Edition 🏰
## *A Tool Worthy of the Great Tomb of Nazarick*

[![Blender](https://img.shields.io/badge/Blender-4.5+-orange.svg)](https://www.blender.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Overlord](https://img.shields.io/badge/Overlord-Approved%20by%20Ainz-gold.svg)](https://overlord-anime.com/)

> *"Knowledge is power, and power is everything. Let this tool guide you to perfect UV mapping, as befits a creation worthy of Nazarick's greatness."*  
> — **Albedo, Guardian Overseer of the Great Tomb of Nazarick**

---

## 🌟 Introduction

Behold! By the supreme will of **Ainz Ooal Gown**, Overlord of the Great Tomb of Nazarick, this magnificent add-on has been forged to assist all subjects in achieving perfect UV mapping ratios. Created in the spirit of excellence that defines all works within Nazarick's domain, this tool calculates the precise ratio between UV space and 3D surface area - a critical aspect for texture accuracy that even the Floor Guardians would appreciate.

Inspired by the wisdom shared in **Alexandre Albisser's Sewing Toolbox**, where the importance of UV-to-3D ratios was illuminated, this add-on transforms complex manual calculations into effortless divine computation. No longer shall artists struggle with the mysteries of UV scaling - for this tool brings the precision of Nazarick's engineering to your workflow.

**HAIL AINZ OOAL GOWN! GLORY TO NAZARICK!** 🏰⚡

---

## ✨ Features

### 🎯 **Core Functionality**
- **Dual-Panel Interface**: Identical panels available in both UV Editor and 3D Viewport sidebars
- **Precise UV/3D Ratio Calculation**: Uses advanced triangulation algorithms to measure exact area ratios
- **Selection-Aware Calculations**: Works with selected faces, edges, or entire mesh (automatically detects scope)
- **Unified UI Experience**: Changes in one panel are instantly reflected in the other
- **Intelligent Interpretation**: Provides clear guidance on whether your UVs are perfect, stretched, or compressed
- **One-Click UV Scaling**: Automatically adjusts UV coordinates to achieve the perfect 1:1 ratio
- **Real-time Feedback**: Displays calculation time, face count, scope (selected vs all), and detailed area measurements
- **Non-destructive Workflow**: All operations can be undone with Blender's standard undo system

### 🛡️ **Technical Excellence**
- **Optimized Performance**: Efficient triangulation-based area calculations
- **Precise Mathematics**: Handles complex polygon geometries with accuracy
- **Memory Efficient**: Minimal memory footprint during calculations
- **Error Handling**: Graceful handling of edge cases and invalid geometry

### 👑 **User Experience**
- **Dual-Location Access**: Available in both UV Editor and 3D Viewport for maximum convenience
- **Nazarick-themed Interface**: Beautiful UI panels with consistent appearance across both locations
- **Clear Visual Feedback**: Color-coded results and intuitive icons
- **Selection Context Awareness**: Automatically detects and processes selected geometry or entire mesh
- **Comprehensive Results**: Detailed breakdown of calculations with scope indication (selected vs all faces)
- **Seamless Integration**: Works perfectly within Blender's native UV editing workflow
- **Synchronized Updates**: Changes made in one panel are instantly visible in the other

---

## 🚀 Installation

### **Requirements**
- **Blender 4.5.0** or newer
- **Operating System**: Windows, macOS, or Linux
- **Memory**: Minimal requirements (works with any system that runs Blender)

### **Installation Steps**

1. **Download the Add-on**
   ```
   Download: uv_total_ratio_compare_Version2.py
   ```

2. **Install in Blender**
   - Open Blender 4.5+
   - Go to `Edit` → `Preferences` → `Add-ons`
   - Click `Install...` button
   - Navigate to and select `uv_total_ratio_compare_Version2.py`
   - Click `Install Add-on`

3. **Enable the Add-on**
   - In the Add-ons preferences, search for "UV Total Ratio Compare"
   - Check the box next to "UV: UV Total Ratio Compare"
   - The add-on is now active!

4. **Verify Installation**
   - Switch to the **UV Editing** workspace OR stay in **Layout/Modeling** workspace
   - Select a mesh object and enter **Edit Mode**
   - Press `N` to open the sidebar
   - Look for the **"Nazarick UV Tools"** panel 🏰
   - The panel appears in BOTH the UV Editor and 3D Viewport sidebars!

---

## 📖 Usage Guide

### **Basic Workflow**

#### 1. **Prepare Your Model**
```
• Select your mesh object
• Enter Edit Mode (Tab)
• Ensure your object has UV coordinates
• Switch to UV Editing workspace
```

#### 2. **Access the Tool**
```
• Open the sidebar (N key) in either UV Editor OR 3D Viewport
• Find "Nazarick UV Tools" panel (available in both locations)
• Click "Calculate UV/3D Ratio"
• Results appear instantly in BOTH panels simultaneously
```

#### 3. **Interpret Results**
The tool provides several ratio interpretations:

| Ratio Range | Status | Meaning |
|-------------|--------|---------|
| 0.99 - 1.01 | ✅ **PERFECT** | 1:1 UV to 3D ratio (ideal) |
| 1.05 - 1.5 | ⚠️ **Slightly Large** | Minor texture stretching |
| > 1.5 | 🔴 **Much Larger** | Significant texture stretching |
| 0.5 - 0.95 | ⚠️ **Slightly Small** | Minor texture compression |
| < 0.5 | 🔴 **Much Smaller** | Significant texture compression |

#### 4. **Auto-Correction (Optional)**
```
• Click "Scale UVs to Match 3D" to automatically achieve 1:1 ratio
• The tool preserves UV layout while scaling proportionally
• Results update automatically after scaling
```

### **Advanced Usage**

#### **Understanding the Calculations**
- **3D Area**: Surface area of your mesh in 3D space
- **UV Area**: Area covered by UV coordinates in UV space
- **Ratio**: UV Area ÷ 3D Area
- **Scope**: Shows whether calculation used "selected faces" or "all faces"
- **Face Count**: Number of faces processed
- **Calculation Time**: Performance measurement

#### **Selection-Based Workflow**
1. **Whole Mesh**: No selection = calculates entire mesh
2. **Selected Faces**: Select specific faces = calculates only selected geometry
3. **Mixed Selection**: Works with any face selection combination
4. **Real-time Updates**: Both panels update simultaneously when you recalculate

#### **Best Practices**
1. **Clean Geometry**: Ensure manifold geometry for accurate calculations
2. **Proper UVs**: Verify UVs are unwrapped before measuring
3. **Consistent Scale**: Apply transforms before measuring for accurate results
4. **Iterative Workflow**: Measure → Adjust → Measure → Perfect

---

## 🛠️ Troubleshooting & FAQ

### **Common Issues**

#### **❌ "Object has no UV maps"**
**Solution**: 
- Enter Edit Mode
- Select all faces (A)
- Press `U` → `Unwrap` to create UV coordinates
- Try the calculation again

#### **❌ "Could not calculate area (3D area is zero)"**
**Solution**: 
- Check that your mesh has actual geometry
- Ensure you're not working with a plane with zero thickness
- Verify the mesh scale is reasonable (not microscopic)

#### **❌ "No active UV map found"**
**Solution**: 
- Go to Object Properties → UV Maps
- Ensure you have at least one UV map
- Make sure the UV map is set as active

#### **⚠️ Results seem incorrect**
**Solution**: 
- Apply all transforms (Ctrl+A → All Transforms)
- Check for non-manifold geometry (Select → Select All by Trait → Non-Manifold)
- Ensure consistent face normals (Mesh → Normals → Recalculate Outside)

### **Performance Tips**
- For very high-poly meshes, consider using the Decimate modifier for testing
- The tool is optimized but extremely dense meshes may take longer to process
- Results are cached until you run the calculation again

### **Compatibility**
- **Blender Versions**: Tested on 4.5.0, should work on newer versions
- **Mesh Types**: Works with any manifold mesh geometry
- **UV Types**: Compatible with all standard UV mapping methods

---

## 🏆 Credits & Acknowledgments

### **Supreme Leadership**
- **Ainz Ooal Gown** - *Supreme Being and Overlord of Nazarick*
- **Albedo** - *Guardian Overseer and Author Attribution*

### **Inspiration & Foundation**
- **Alexandre Albisser** - Creator of the Sewing Toolbox and inspiration for UV ratio importance
- **Sewing Toolbox Community** - For highlighting the critical nature of UV-to-3D ratios in professional workflows

### **Technical Development**
- **Nines Own Goal** - Primary developer and Nazarick loyalist
- **Blender Foundation** - For providing the magnificent Blender platform
- **Python Software Foundation** - For the powerful Python language that makes this magic possible

### **Special Recognition**
- **Floor Guardians of Nazarick** - For their unwavering dedication to perfection that inspired this tool's precision
- **Great Tomb of Nazarick** - For providing the supreme standards of excellence that guide all development
- **Overlord Community** - For appreciating the finest details that make great tools

---

## 📜 License

This add-on is released under the **MIT License**, ensuring it remains free and accessible to all subjects of the realm.

```
MIT License - Copyright (c) 2025 Nines Own Goal

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

[Full license text available in LICENSE file]
```

---

## 🌟 Final Words

*"In the pursuit of perfect UV mapping, let precision be your guide and excellence your standard. May this tool serve you well in your creative endeavors, bringing the methodical perfection of Nazarick to your artistic workflow."*

**For the glory of the Great Tomb of Nazarick!** 🏰

---

### 🔗 **Quick Links**
- [Blender Download](https://www.blender.org/download/) - Get the latest Blender
- [UV Mapping Basics](https://docs.blender.org/manual/en/latest/modeling/meshes/uv/unwrapping/index.html) - Blender UV Documentation
- [Alexandre Albisser's Work](https://www.youtube.com/c/AlexandreAlbisser) - Sewing Toolbox creator
- [Report Issues](../../issues) - Report bugs or request features

*Last Updated: January 2025 | Version 1.0.0 | Nazarick Edition*
