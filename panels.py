################################################################################
# Imports
################################################################################


import bpy


################################################################################
# Classes
################################################################################


class VIEW3D_PT_blautorenamer(bpy.types.Panel):

    bl_category = 'Item'
    bl_idname = 'VIEW3D_PT_blautorenamer'
    bl_label = 'Auto Renamer'
    bl_region_type = 'UI'
    bl_space_type = 'VIEW_3D'

    def draw(self, context):
        settings = context.scene.blautorenamer.rename_objects
        lay = self.layout
        col = lay.column(align=True)
        split = col.split(align=True, factor=0.6)
        split.prop(settings, 'keyword', text='')
        split.prop(settings, 'side', text='')
        col.operator('blautorenamer.rename_objects', icon='EVENT_S')
        lay.operator('blautorenamer.sanitize_existing', icon='BRUSH_DATA')


################################################################################
# Registration
################################################################################


register, unregister = bpy.utils.register_classes_factory([
    VIEW3D_PT_blautorenamer,
])
