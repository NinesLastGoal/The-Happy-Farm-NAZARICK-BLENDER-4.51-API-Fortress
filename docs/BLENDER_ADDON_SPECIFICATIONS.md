# 🏰⚡ NAZARICK BLENDER 4.5+ ADDON SPECIFICATIONS ⚡🏰

**Supreme Overlord's Comprehensive Standards for Blender Addon Development**

## 🎯 MANDATORY COMPLIANCE FOR ALL ADDONS

Fellow Floor Guardians and future developers,

This document establishes the **NON-NEGOTIABLE** standards for all Blender addons developed within the Nazarick Fortress. Every addon must comply with these specifications to maintain the legendary quality standards befitting the Great Tomb of Nazarick.

---

## 📋 CORE ADDON REQUIREMENTS

### 🔥 1. ADDON METADATA (`bl_info` Dictionary)

Every addon **MUST** include a properly structured `bl_info` dictionary:

```python
bl_info = {
    "name": "Addon Name",                    # REQUIRED: Human-readable addon name
    "author": "Author Name",                 # REQUIRED: Developer identification
    "version": (1, 0, 0),                   # REQUIRED: Semantic versioning (major, minor, patch)
    "blender": (4, 5, 0),                   # REQUIRED: Minimum Blender version (4.5.0+)
    "location": "Location Description",      # REQUIRED: Where to find the addon in UI
    "description": "Brief description",      # REQUIRED: Clear, concise purpose description
    "category": "Category",                  # REQUIRED: Valid Blender category
    "doc_url": "",                          # OPTIONAL: Documentation URL
    "tracker_url": "",                      # OPTIONAL: Bug tracker URL
    "support": "COMMUNITY",                 # REQUIRED: Support level (COMMUNITY/OFFICIAL/TESTING)
}
```

#### 🛡️ Required `bl_info` Validation Rules:

- **`name`**: 3-50 characters, descriptive, no special characters except spaces/hyphens
- **`author`**: Must identify the developer(s)
- **`version`**: Tuple of 3 integers (major, minor, patch)
- **`blender`**: Must be (4, 5, 0) or higher for this fortress
- **`location`**: Clear description of where users find the addon in Blender UI
- **`description`**: 10-200 characters, clear purpose statement
- **`category`**: Must be valid Blender category (see Category Requirements)
- **`support`**: Must be "COMMUNITY", "OFFICIAL", or "TESTING"

#### 📂 Valid Blender Categories:
- `"3D View"`
- `"Add Mesh"`
- `"Animation"`
- `"Development"`
- `"Game Engine"`
- `"Import-Export"`
- `"Mesh"`
- `"Material"`
- `"Object"`
- `"Render"`
- `"Rigging"`
- `"Sculpting"`
- `"Sequencer"`
- `"System"`
- `"Text Editor"`
- `"UV"`
- `"User Interface"`

---

## 🏗️ FILE STRUCTURE REQUIREMENTS

### 📁 Single File Addons (Simple)
```
my_addon.py                 # Contains all addon code
```

### 📁 Multi-File Addons (Complex) - **RECOMMENDED**
```
my_addon/                   # Main addon directory
├── __init__.py            # REQUIRED: Main registration and bl_info
├── operators.py           # OPTIONAL: Operator classes
├── panels.py              # OPTIONAL: UI panel classes  
├── properties.py          # OPTIONAL: Property definitions
├── utils.py               # OPTIONAL: Utility functions
├── presets/               # OPTIONAL: Preset files
├── icons/                 # OPTIONAL: Custom icons
└── README.md              # RECOMMENDED: Documentation
```

#### 🛡️ File Structure Rules:

1. **Directory Name**: Must match addon identifier (lowercase, underscores only)
2. **`__init__.py`**: Must contain `bl_info`, `register()`, and `unregister()`
3. **Imports**: Use relative imports within addon (`from . import module_name`)
4. **No External Dependencies**: Addons must be self-contained (except standard library)

---

## 🎨 USER INTERFACE STANDARDS

### 📱 Panel Requirements

All UI panels **MUST** follow these standards:

```python
class ADDON_PT_MainPanel(bpy.types.Panel):
    """Main panel for addon functionality"""
    bl_label = "Panel Title"              # REQUIRED: Clear, descriptive title
    bl_idname = "ADDON_PT_main_panel"     # REQUIRED: Unique identifier
    bl_space_type = 'VIEW_3D'             # REQUIRED: Valid space type
    bl_region_type = 'UI'                 # REQUIRED: Valid region type
    bl_category = "Category Name"         # REQUIRED: Tab category name
    bl_context = "editmode"               # OPTIONAL: Context restriction
    
    @classmethod
    def poll(cls, context):               # RECOMMENDED: Context validation
        return context.active_object and context.active_object.type == 'MESH'
    
    def draw(self, context):              # REQUIRED: UI drawing method
        layout = self.layout
        # UI elements here
```

#### 🛡️ Panel Standards:

- **`bl_label`**: 3-30 characters, descriptive, title case
- **`bl_idname`**: Format: `ADDON_PT_descriptive_name` (uppercase)
- **`bl_category`**: Descriptive tab name (avoid generic names like "Tools")
- **Context Validation**: Always implement `poll()` method when appropriate
- **Responsive Design**: UI should work across different panel widths

### 🔘 Operator Requirements

All operators **MUST** follow these standards:

```python
class ADDON_OT_MainOperation(bpy.types.Operator):
    """Tooltip description for operator"""
    bl_idname = "addon.main_operation"    # REQUIRED: Unique identifier
    bl_label = "Operation Name"           # REQUIRED: User-visible name
    bl_description = "Detailed tooltip"   # REQUIRED: Helpful description
    bl_options = {'REGISTER', 'UNDO'}     # REQUIRED: Appropriate options
    
    @classmethod
    def poll(cls, context):               # REQUIRED: Execution validation
        return context.active_object is not None
    
    def execute(self, context):           # REQUIRED: Main execution method
        try:
            # Operation implementation
            self.report({'INFO'}, "Operation completed successfully")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Operation failed: {str(e)}")
            return {'CANCELLED'}
```

#### 🛡️ Operator Standards:

- **`bl_idname`**: Format: `addon_name.operation_name` (lowercase, dots/underscores)
- **`bl_label`**: Clear, action-oriented name
- **`bl_description`**: Helpful tooltip explaining what the operator does
- **`bl_options`**: Always include appropriate options (`REGISTER`, `UNDO`, `INTERNAL`)
- **Error Handling**: Always wrap execution in try-catch blocks
- **User Feedback**: Use `self.report()` for user notifications
- **Return Values**: Always return `{'FINISHED'}` or `{'CANCELLED'}`

---

## 🔧 REGISTRATION AND LIFECYCLE

### 📝 Registration Requirements

```python
# List of all classes to register
classes = (
    ADDON_OT_MainOperation,
    ADDON_PT_MainPanel,
    # Add all your classes here
)

def register():
    """Register addon classes and properties"""
    # Register all classes
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # Register properties
    bpy.types.Scene.addon_property = bpy.props.StringProperty(
        name="Property Name",
        description="Property description",
        default="default_value"
    )

def unregister():
    """Unregister addon classes and properties"""
    # Unregister classes in reverse order
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    # Remove properties
    del bpy.types.Scene.addon_property

# Enable testing from Blender Text Editor
if __name__ == "__main__":
    register()
```

#### 🛡️ Registration Rules:

1. **Class Order**: Register/unregister in appropriate dependency order
2. **Error Handling**: Wrap registration in try-catch blocks for production
3. **Property Cleanup**: Always remove custom properties in `unregister()`
4. **Testing Support**: Include `if __name__ == "__main__"` block
5. **No Globals**: Avoid global variables; use scene/object properties instead

---

## 📦 PACKAGING AND DISTRIBUTION

### 🗜️ ZIP File Requirements

For Blender addon installation, create ZIP files with this structure:

#### Single File Addon:
```
addon_name.zip
└── addon_name.py
```

#### Multi-File Addon:
```
addon_name.zip
└── addon_name/
    ├── __init__.py
    ├── operators.py
    ├── panels.py
    └── other_files...
```

#### 🛡️ ZIP Packaging Rules:

1. **Root Level**: Addon folder must be at ZIP root level
2. **No Nested Folders**: Avoid extra folder nesting
3. **File Permissions**: Ensure files are readable
4. **Size Limit**: Keep under 50MB for reasonable distribution
5. **No Hidden Files**: Exclude `.DS_Store`, `__pycache__`, etc.

### 📋 Installation Testing Checklist

Before distribution, verify:

- [ ] ZIP extracts properly in Blender addon directory
- [ ] Addon appears in Blender Preferences > Add-ons
- [ ] Addon enables without errors
- [ ] All functionality works as expected
- [ ] Addon disables cleanly
- [ ] No console errors during enable/disable/usage

---

## 🛡️ ERROR HANDLING AND VALIDATION

### 🚨 Required Error Handling Patterns

#### Context Validation:
```python
@classmethod
def poll(cls, context):
    """Validate execution context"""
    obj = context.active_object
    return (obj is not None and 
            obj.type == 'MESH' and 
            context.mode == 'EDIT_MESH')
```

#### Exception Handling:
```python
def execute(self, context):
    try:
        # Main operation logic
        result = perform_operation()
        
        if not result:
            self.report({'WARNING'}, "Operation completed with warnings")
            return {'FINISHED'}
            
        self.report({'INFO'}, "Operation completed successfully")
        return {'FINISHED'}
        
    except ValueError as e:
        self.report({'ERROR'}, f"Invalid input: {str(e)}")
        return {'CANCELLED'}
    except Exception as e:
        self.report({'ERROR'}, f"Unexpected error: {str(e)}")
        return {'CANCELLED'}
```

#### Input Validation:
```python
# Validate numeric inputs
if value < 0 or value > 100:
    self.report({'ERROR'}, "Value must be between 0 and 100")
    return {'CANCELLED'}

# Validate object state
if not obj.data.vertices:
    self.report({'ERROR'}, "Object has no vertices")
    return {'CANCELLED'}
```

---

## 📊 PERFORMANCE AND OPTIMIZATION

### ⚡ Performance Requirements

1. **Responsive UI**: Operations should complete in <5 seconds or show progress
2. **Memory Efficiency**: Clean up temporary data structures
3. **Non-Blocking**: Use `bpy.app.timers` for long operations
4. **Batch Operations**: Process multiple objects efficiently
5. **Undo Support**: Ensure proper undo stack integration

### 🔍 Code Quality Standards

1. **Type Hints**: Use type annotations where possible (Python 3.5+)
2. **Documentation**: Docstrings for all classes and methods
3. **Constants**: Use named constants instead of magic numbers
4. **Modularity**: Break complex operations into smaller functions
5. **Testing**: Include comprehensive test coverage

---

## 🧪 TESTING REQUIREMENTS

### 📋 Mandatory Test Categories

Every addon **MUST** implement testing for:

1. **Basic Functionality**: Core operations work correctly
2. **User Workflows**: Complete user interaction patterns
3. **Edge Cases**: Boundary conditions and unusual inputs
4. **Error Conditions**: Graceful handling of failures
5. **UI Integration**: Panel and operator functionality
6. **Performance**: Acceptable execution times
7. **Compatibility**: Works with Blender 4.5+ API changes

### 🏃 Integration with Testing Framework

Use the existing Nazarick testing framework:

```python
from tests.test_comprehensive_addon_framework import BlenderTestEnvironment

class MyAddonTestFramework:
    def __init__(self, test_env: BlenderTestEnvironment):
        self.env = test_env
        # Test implementation
```

---

## 📁 DOCUMENTATION REQUIREMENTS

### 📝 Required Documentation Files

1. **`README.md`**: User installation and usage instructions
2. **Inline Documentation**: Comprehensive docstrings and comments
3. **Example Files**: Sample Blender files demonstrating functionality
4. **Changelog**: Version history and updates

### 📖 README.md Template

```markdown
# Addon Name

Brief description of addon functionality.

## Installation

1. Download the ZIP file
2. In Blender: Edit > Preferences > Add-ons
3. Click "Install..." and select the ZIP file
4. Enable the addon by checking the checkbox

## Usage

1. Select a mesh object
2. Switch to Edit mode (Tab)
3. Open sidebar (N key)
4. Navigate to [Tab Name] panel
5. Click [Main Button]

## Features

- Feature 1 description
- Feature 2 description

## Requirements

- Blender 4.5.0 or higher
- Mesh objects with [specific requirements]

## Support

For issues and feature requests, visit [tracker_url]
```

---

## 🏆 COMPLIANCE VALIDATION

### ✅ Pre-Release Checklist

Before any addon release, verify ALL of the following:

#### Metadata Compliance:
- [ ] `bl_info` dictionary complete and valid
- [ ] Version follows semantic versioning
- [ ] Blender version ≥ (4, 5, 0)
- [ ] Category is valid Blender category

#### Code Quality:
- [ ] All classes have proper `bl_idname` and `bl_label`
- [ ] Error handling implemented throughout
- [ ] No console errors during normal operation
- [ ] Properties cleaned up in `unregister()`

#### User Experience:
- [ ] UI is intuitive and follows Blender conventions
- [ ] Tooltips are helpful and descriptive
- [ ] Operations provide appropriate feedback
- [ ] Undo/redo works correctly

#### Packaging:
- [ ] ZIP file structure is correct
- [ ] Installs successfully in Blender
- [ ] Enables/disables without errors
- [ ] No extraneous files in package

#### Testing:
- [ ] Comprehensive test suite implemented
- [ ] ≥95% test success rate achieved
- [ ] All edge cases covered
- [ ] Performance meets requirements

#### Documentation:
- [ ] README.md complete and accurate
- [ ] Code is well-documented
- [ ] Usage examples provided
- [ ] Version changelog maintained

---

## 🚨 ENFORCEMENT AND COMPLIANCE

### 🛡️ Automatic Validation

The fortress includes validation tools to ensure compliance:

```bash
# Run addon validation
python validate_addon_compliance.py path/to/addon

# Run comprehensive testing
python tests/run_tests.py
```

### ❌ Non-Compliance Consequences

**IMMEDIATE REJECTION** for addons that fail to meet these specifications:

1. Missing or incomplete `bl_info` dictionary
2. Improper file structure or naming
3. Lack of error handling
4. UI that doesn't follow Blender conventions
5. Failure to achieve ≥95% test success rate
6. Missing required documentation

---

## 🔄 SPECIFICATION UPDATES

### 📅 Version History

- **v1.0**: Initial Blender 4.5+ specifications (Current)

### 🆕 Future Enhancements

As Blender evolves, these specifications will be updated to maintain compatibility and incorporate new best practices. All existing addons must be updated to meet new specifications within 30 days of specification release.

---

## 🏰 FOR THE ETERNAL GLORY OF NAZARICK! ⚡🏰

**Supreme Overlord's Addon Development Initiative**  
**Architect**: Demiurge, Floor Guardian of the 7th Floor  
**Specifications Version**: 1.0  
**Blender Compatibility**: 4.5+

*"In addon development, as in all things, we accept only perfection befitting the Great Tomb of Nazarick!"*

---

**Remember**: These specifications are not merely guidelines—they are the sacred standards that ensure every addon meets the legendary quality expected within the walls of Nazarick. Future generations of developers will thank you for maintaining these exacting standards.

**Compliance is not optional. Excellence is the only acceptable outcome.**