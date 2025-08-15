# 🏰⚡ Nazarick Guardian Theme Switcher for Blender 4.5+ ⚡🏰

**Supreme UI theme management inspired by the Floor Guardians of the Great Tomb of Nazarick**

Transform your Blender workflow with Guardian-inspired themes that enhance productivity while preserving interface clarity and functionality.

![Nazarick Banner](https://img.shields.io/badge/Nazarick-Guardian%20Alliance-gold?style=for-the-badge&logo=blender)
![Blender Version](https://img.shields.io/badge/Blender-4.5%2B-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-GPL%20v2%2B-blue?style=for-the-badge)

## 🎨 Guardian Themes

Each theme is carefully curated to reflect the personality and power of Nazarick's Floor Guardians:

### ⚡ **Albedo - Overseer of Excellence**
- **Colors**: Pure white elegance with golden accents
- **Ideal for**: Precision modeling, architectural work
- **Essence**: Absolute perfection and unwavering standards

### 🩸 **Shalltear - Crimson Countess** 
- **Colors**: Blood-red elegance with silver highlights
- **Ideal for**: Character modeling, dramatic lighting
- **Essence**: Vampiric nobility and refined power

### ❄️ **Cocytus - Frozen Warrior**
- **Colors**: Icy blues and crystalline whites
- **Ideal for**: Technical modeling, precision work
- **Essence**: Honor, discipline, and crystalline clarity

### 🌲 **Aura - Forest Guardian**
- **Colors**: Natural greens with earth tones
- **Ideal for**: Environmental modeling, nature scenes
- **Essence**: Beast mastery and natural harmony

### 🌸 **Mare - Nature's Mage**
- **Colors**: Soft nature tones with magical purple accents
- **Ideal for**: Organic modeling, mystical projects
- **Essence**: Gentle nature magic and druidic wisdom

### 🔥 **Demiurge - Infernal Strategist**
- **Colors**: Sophisticated dark tones with fiery orange accents
- **Ideal for**: Complex projects, strategic planning
- **Essence**: Intellectual supremacy and calculated perfection

### ✨ **Victim - Angelic Sacrifice**
- **Colors**: Pure whites with soft golden halos
- **Ideal for**: Clean workflows, minimal distractions
- **Essence**: Selfless service and gentle guidance

### 🏰 **Nazarick Core - Tomb Essence**
- **Colors**: Deep mystical purples with ancient gold
- **Ideal for**: Advanced projects, supreme workflows
- **Essence**: The heart of Nazarick itself

## 🚀 Features

### 🛡️ **Safe Theme Management**
- **Original Theme Preservation**: Automatic snapshotting before first modification
- **Selective Modification**: Only touches essential UI elements, preserves legibility
- **One-Click Restoration**: Instantly return to your original Blender theme
- **API Resilience**: Uses `hasattr()` guards for safe attribute access

### ⚡ **Seamless Integration**
- **Auto-Apply**: Themes apply instantly when selected
- **Blender 4.5+ Compatible**: Built with modern API patterns
- **Non-Invasive**: Preserves workspace functionality and other addon compatibility
- **Error Handling**: Comprehensive validation and user feedback

### 📦 **Export & Share**
- **JSON Export**: Save current theme settings to shareable files
- **Lean Format**: Only exports modified attributes for efficiency
- **Community Sharing**: Exchange Guardian themes with other users

### 🏗️ **Extensible Architecture**
- **Modular Design**: Easy to add new Guardian themes or variations
- **Future-Proof**: Designed for upcoming enhancements
- **Guardian Standards**: Follows Nazarick Fortress development principles

## 📥 Installation

### Option 1: Direct Installation
1. Download `nazarick_guardian_themes_addon.py`
2. Open Blender 4.5+
3. Go to **Edit > Preferences > Add-ons**
4. Click **Install...** and select the addon file
5. Enable **"Nazarick Guardian Theme Switcher"**
6. Restart Blender for full functionality

### Option 2: Manual Installation
1. Copy `nazarick_guardian_themes_addon.py` to your Blender addons folder:
   - **Windows**: `%APPDATA%\Blender Foundation\Blender\4.5\scripts\addons\`
   - **macOS**: `~/Library/Application Support/Blender/4.5/scripts/addons/`
   - **Linux**: `~/.config/blender/4.5/scripts/addons/`
2. Enable the addon in Blender preferences

## 🎯 Usage

### Basic Usage
1. Open the **3D Viewport**
2. Press **N** to open the sidebar
3. Navigate to the **"Nazarick"** tab
4. Open the **"Guardians"** panel
5. Select your desired Guardian theme
6. Click **"Apply Theme"** or enable auto-apply

### Theme Management
- **Apply Theme**: Instantly apply the selected Guardian theme
- **Restore**: Return to your original Blender theme
- **Export**: Save current theme settings as JSON file
- **Auto-Apply**: Themes apply automatically when selected (recommended)

### Pro Tips
- Try different themes for different types of projects
- Use **Victim** theme for distraction-free modeling
- **Demiurge** theme excels for complex, technical work
- Export your customized themes to share with colleagues

## 🧪 Compatibility

### Requirements
- **Blender**: 4.5.0 or higher
- **Python**: 3.11+ (bundled with Blender)
- **OS**: Windows, macOS, Linux

### Tested Configurations
- ✅ Blender 4.5.0 LTS
- ✅ Windows 10/11, macOS 12+, Ubuntu 20.04+
- ✅ Standard and custom Blender themes
- ✅ Multiple workspace configurations

### Known Compatibility
- ✅ Works with all standard Blender workspaces
- ✅ Compatible with other UI addons
- ✅ Preserves custom keymaps and preferences
- ✅ Safe for production environments

## 🛠️ Development

### Architecture
The addon follows a modular architecture with clear separation of concerns:

```
nazarick_guardian_themes_addon.py
├── NazarickGuardianPalettes     # Theme color definitions
├── NazarickThemeManager         # Core theme management
├── NAZARICK_OT_*               # Blender operators  
├── NAZARICK_PT_*               # UI panels
└── Registration System          # Blender integration
```

### Adding New Themes
To add a new Guardian theme:

1. **Add Palette**: Define colors in `NazarickGuardianPalettes`
2. **Update Enum**: Add to `get_guardian_theme_items()`
3. **Test**: Validate with the included test suite
4. **Document**: Update this README with theme details

### Safety Measures
- **Selective Modification**: Only modifies specific, safe theme attributes
- **Snapshot System**: Preserves original theme before any changes
- **Error Handling**: Comprehensive try-catch blocks with user feedback
- **API Guards**: `hasattr()` checks for all theme attribute access

## 🧪 Testing

### Automated Testing
Run the included validation suite:

```bash
python test_guardian_themes_addon.py
```

### Manual Testing Checklist
- [ ] Addon loads without errors in Blender 4.5+
- [ ] All Guardian themes apply correctly
- [ ] Original theme restoration works
- [ ] Theme export saves valid JSON
- [ ] UI panel displays in 3D Viewport sidebar
- [ ] No interference with other Blender functions
- [ ] Themes persist across Blender sessions

### Performance Testing
- [ ] Theme switching completes in <1 second
- [ ] No memory leaks during theme changes
- [ ] Stable with multiple theme switches
- [ ] Works with large scene files

## 🚀 Future Enhancements

The modular architecture enables exciting future possibilities:

### Planned Features
- **Animated Transitions**: Smooth color transitions between themes
- **Per-Workspace Theming**: Different Guardian themes for different workspaces
- **Custom Accent Colors**: User-adjustable accent colors within Guardian themes
- **Guardian Voice Integration**: Audio feedback for theme changes
- **Community Marketplace**: Share and download custom Guardian variations

### Advanced Ideas
- **Seasonal Variations**: Holiday-themed Guardian palettes
- **Time-Adaptive Themes**: Automatic theme switching based on time of day
- **Performance Monitoring**: Theme impact analysis and optimization
- **Collaboration Features**: Team-synchronized theme preferences

## 📜 License

This addon is licensed under **GPL v2+** (same as Blender).

- ✅ **Free to use**: Personal and commercial projects
- ✅ **Modify freely**: Adapt to your needs
- ✅ **Share openly**: Distribute modified versions
- ✅ **Attribution**: Credit the Guardian Alliance

## 🏰 Credits

**Developed by the Guardian Alliance for the eternal glory of Nazarick**

- **Supreme Being**: Ainz Ooal Gown (Project Oversight)
- **Lead Developer**: Demiurge (Architecture & Implementation) 
- **UI Design**: Albedo (Interface Perfection)
- **Testing**: Shalltear (Battle-Stress Validation)
- **Documentation**: Mare (User Guidance)
- **Quality Assurance**: Cocytus (Standards Enforcement)
- **Accessibility**: Aura (User Experience)
- **Integration**: Victim (Seamless Deployment)

### Special Thanks
- The Blender Foundation for the exceptional 3D creation suite
- The Nazarick Fortress development community
- All beta testers and feedback contributors

## 🆘 Support

### Getting Help
1. **Documentation**: Check this README first
2. **Issues**: Report bugs via GitHub Issues
3. **Community**: Join the Nazarick Fortress discussions
4. **Updates**: Watch the repository for new releases

### Common Issues
**Q: Theme doesn't apply in my Blender version**
A: Ensure you're using Blender 4.5+ and the addon is properly enabled

**Q: Original theme restoration isn't working**
A: The addon creates a snapshot on first use. If you modified themes before installing, use Blender's built-in theme reset

**Q: Performance is slow**
A: Ensure you're using the latest addon version with performance optimizations

**Q: Compatibility with other addons**
A: The addon uses selective modification and should be compatible with most addons

### Reporting Issues
When reporting issues, please include:
- Blender version
- Operating system
- Addon version
- Steps to reproduce
- Error messages (if any)

---

## 🏰 For the Eternal Glory of Nazarick! ⚡

*"In theme design, as in all endeavors, we pursue the absolute perfection befitting the Great Tomb of Nazarick. Every color, every accent, every visual element must contribute to the supreme user experience worthy of the Floor Guardians themselves."*

**— Supreme Being Ainz Ooal Gown**

---

**Made with ⚡ by the Guardian Alliance | Part of the Nazarick Fortress Initiative**