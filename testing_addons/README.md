# 🧪 Testing Addons Directory

## ⚠️ ISOLATION POLICY - STRICTLY ENFORCED ⚠️

This directory contains addons used **ONLY for testing purposes** by the Fortress testing infrastructure.

### **CRITICAL ISOLATION RULES:**

1. **NO FORTRESS CORE REFERENCES**: Addons in this directory MUST NOT reference or import anything from the Fortress core (`/src/`)

2. **NO DEVELOPING ADDONS REFERENCES**: Addons here MUST NOT reference or import anything from `/developing_addons/`

3. **NO CROSS-ADDON REFERENCES**: Each addon in this directory MUST be self-contained and not reference other testing addons

4. **TESTING USE ONLY**: These addons exist solely to provide test subjects for the Fortress testing infrastructure

5. **GENERIC RESULTS ONLY**: All test results from these addons are sanitized before being used to improve the Fortress core

### **PERMITTED OPERATIONS:**
- ✅ Self-contained addon functionality
- ✅ Standard Blender API usage
- ✅ Internal addon logic and utilities
- ✅ Being tested by the Fortress infrastructure

### **FORBIDDEN OPERATIONS:**
- ❌ Importing from `/src/` (Fortress core)
- ❌ Importing from `/developing_addons/`
- ❌ Cross-referencing other testing addons
- ❌ Exposing addon-specific details to Fortress core

## 🛡️ PURPOSE

This directory serves as a **sanitized testing environment** where addons provide generic functionality for validating the Fortress testing infrastructure without contaminating the addon-neutral core.

**For the glory of Nazarick's architectural purity! 🏰**