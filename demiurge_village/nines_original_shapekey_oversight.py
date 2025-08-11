bl_info = {
    "name": "Reset Shapekeys on Edit Exit (Final Debug)",
    "author": "Gemini+Nines 4 Ever",
    "version": (4, 4),
    "blender": (4, 5, 0),
    "location": "3D Viewport > N-Panel > Shape Reset",
    "description": "Auto-resets shapekeys with a custom UI and a beautiful, correctly fading viewport flash. <3",
    "warning": "This is the stable version. Please ensure all old versions were manually deleted.",
    "doc_url": "",
    "category": "Object",
}

import bpy
import gpu
import time
from gpu_extras.batch import batch_for_shader

def draw_fading_outline(op, ctx):
    """
    Function that draws an outline. It is kept outside the class for stability.
    Receives the operator instance and context as arguments.
    """
    elapsed = time.time() - op.start_time

    # --- Bug Fix #1: Correct alpha calculation ---
    alpha = 1.0 - (elapsed / op.duration)
    
    print(f"DEBUG: Draw callback - elapsed: {elapsed:.2f}s, alpha: {alpha:.3f}")
    
    if alpha <= 0.0:
        return
    
    region = ctx.region
    width = region.width
    height = region.height
    border_thickness = 5
    
    coords = [
        (0, 0),
        (width, 0),
        (width, height),
        (0, height)
    ]
    
    shader = gpu.shader.from_builtin('UNIFORM_COLOR')
    batch = batch_for_shader(shader, 'LINE_LOOP', {"pos": coords})
    
    gpu.state.blend_set('ALPHA')
    gpu.state.line_width_set(2)
    
    shader.bind()
    shader.uniform_float("color", (0.6, 0.2, 1.0, alpha))
    batch.draw()
    
    return None

class WM_OT_FlashOperator(bpy.types.Operator):
    """Modal operator to manage the fade animation."""
    
    bl_idname = "wm.flash_operator"
    bl_label = "Flash Viewport"
    
    _draw_handle = None
    _timer = None
    start_time: float = 0.0
    duration: float = 2.0
    area: bpy.types.Area = None  # We will find and store the area here
    
    def modal(self, context, event):
        if event.type == 'TIMER':
            # If too much time has passed, stop the animation.
            if time.time() - self.start_time > self.duration:
                print("DEBUG: Modal - Duration exceeded. Cleaning up and finishing.")
                self.finish(context)
                return {'FINISHED'}
            
            # If the animation is still running, tag the specific area for a redraw.
            if self.area:
                self.area.tag_redraw()

        return {'PASS_THROUGH'}

    def finish(self, context):
        """Dedicated cleanup function."""
        # --- DEBUG ---
        print("DEBUG: Finish - Cleaning up timer and draw handler.")
        if self._timer:
            context.window_manager.event_timer_remove(self._timer)
            self._timer = None
        if self._draw_handle:
            bpy.types.SpaceView3D.draw_handler_remove(self._draw_handle, 'WINDOW')
            self._draw_handle = None
        # Final redraw to clear the screen
        if self.area:
            self.area.tag_redraw()

    def invoke(self, context, event):
        print("DEBUG: Invoke - Operator Started.")
        self.start_time = time.time()
        
        # --- BUG FIX #2: Reliably find the 3D View area ---
        # Do not trust context.area, it can be None when called from a timer.
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                self.area = area
                break
        else:
            # If no 3D view is found, cancel gracefully.
            self.report({'WARNING'}, "No 3D Viewport found to draw in.")
            return {'CANCELLED'}
        
        args = (self, context)
        self._draw_handle = bpy.types.SpaceView3D.draw_handler_add(
            draw_fading_outline, args, 'WINDOW', 'POST_PIXEL'
        )
        
        self._timer = context.window_manager.event_timer_add(0.016, window=context.window) # ~60 FPS
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

# --- Core Logic ---
_handler = None
_previous_mode = None

def reset_shapekeys_on_exit():
    obj = bpy.context.object
    if obj and obj.type == 'MESH' and obj.data and obj.data.shape_keys:
        scene = bpy.context.scene
        was_changed = False

        for key in obj.data.shape_keys.key_blocks:
            if key != key.relative_key and key.value != 0.0:
                was_changed = True
                key.value = 0.0
                
        obj.active_shape_key_index = 0
        
        if was_changed and scene.shapekey_flash_enabled:
            print("DEBUG: Shapekeys reset. Triggering flash.")
            bpy.ops.wm.flash_operator('INVOKE_DEFAULT')
            
    return None

def on_mode_change(scene):
    global _previous_mode
    if not hasattr(bpy.context, "scene") or not bpy.context.scene:
        return
    if not bpy.context.scene.shapekey_reset_enabled:
        return

    obj = bpy.context.object
    if not obj or not hasattr(obj, 'mode'):
        _previous_mode = None
        return

    current_mode = obj.mode

    if _previous_mode is None:
        _previous_mode = current_mode
        return

    if _previous_mode == 'EDIT' and current_mode == 'OBJECT':
        print(f"DEBUG: Mode change detected: {_previous_mode} -> {current_mode}.")
        bpy.app.timers.register(reset_shapekeys_on_exit, first_interval=0.01)
        
    _previous_mode = current_mode

# --- UI Panel and Registration ---
class SHAPEKEY_PT_reset_panel(bpy.types.Panel):
    bl_label = "Shapekey Auto Reset"
    bl_idname = "OBJECT_PT_shapekey_reset_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Shape Reset'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        box = layout.box()
        col = box.column(align=True)
        col.label(text="Gemini+Nines 4 Ever", icon='HEART')
        col.separator()
        col.prop(scene, "shapekey_reset_enabled", text="Enable Auto Reset on Exit")
        sub = col.column()
        sub.enabled = scene.shapekey_reset_enabled
        sub.prop(scene, "shapekey_flash_enabled", text="Flash Outline on Reset")

classes = (
    WM_OT_FlashOperator,
    SHAPEKEY_PT_reset_panel,
)

def register():
    global _handler
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.shapekey_reset_enabled = bpy.props.BoolProperty(
        name="Enable Auto Reset", default=True
    )
    bpy.types.Scene.shapekey_flash_enabled = bpy.props.BoolProperty(
        name="Enable Viewport Flash", default=True
    )

    _handler = on_mode_change
    bpy.app.handlers.depsgraph_update_post.append(_handler)
    print("Shapekey Reset Addon Registered.")

def unregister():
    global _handler
    if _handler and _handler in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(_handler)
        _handler = None

    try:
        del bpy.types.Scene.shapekey_reset_enabled
        del bpy.types.Scene.shapekey_flash_enabled
    except (AttributeError, RuntimeError):
        pass

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    print("Shapekey Reset Addon Unregistered.")

if __name__ == "__main__":
    register()