# 🔬 Developing Addons Directory

## ⚠️ COMPLETE ISOLATION POLICY - STRICTLY ENFORCED ⚠️

This directory contains addons under **active development** that are completely isolated from all other components.

### **ABSOLUTE ISOLATION RULES:**

1. **NO FORTRESS CORE REFERENCES**: Addons in this directory MUST NOT reference, import, or interact with anything from the Fortress core (`/src/`)

2. **NO TESTING ADDONS REFERENCES**: Addons here MUST NOT reference, import, or interact with anything from `/testing_addons/`

3. **NO CROSS-ADDON REFERENCES**: Each addon in this directory MUST be completely self-contained and not reference other developing addons

4. **SELF-CONTAINED DEVELOPMENT**: All code, documentation, and logic must be entirely within the individual addon scope

5. **NO CONTAMINATION**: Nothing from this directory may contaminate the Fortress core or testing infrastructure

### **PERMITTED OPERATIONS:**
- ✅ Self-contained addon development
- ✅ Standard Blender API usage only
- ✅ Internal addon documentation
- ✅ Addon-specific utilities and helpers
- ✅ Independent testing within the addon scope

### **FORBIDDEN OPERATIONS:**
- ❌ Importing from `/src/` (Fortress core)
- ❌ Importing from `/testing_addons/`
- ❌ Cross-referencing other developing addons
- ❌ Being referenced by the Fortress core
- ❌ Being referenced by testing infrastructure
- ❌ Sharing any code or logic outside the addon

## 🛡️ PURPOSE

This directory serves as a **completely isolated development environment** where addons can be developed without any interaction or contamination with the Fortress testing infrastructure or other addons.

### **DEVELOPMENT WORKFLOW:**
1. Develop addon in complete isolation here
2. When ready for testing, addon may be **copied** (not moved) to `/testing_addons/` for validation
3. Fortress core only sees sanitized, generic results - never the actual addon code or names

**For the glory of Nazarick's pure isolation! 🏰**