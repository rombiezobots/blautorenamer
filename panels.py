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
        pass


class VIEW3D_PT_rename_selected_objects(bpy.types.Panel):

    bl_idname = 'VIEW3D_PT_rename_selected_objects'
    bl_label = 'Rename Selected Objects'
    bl_parent_id = 'VIEW3D_PT_blautorenamer'
    bl_region_type = 'UI'
    bl_space_type = 'VIEW_3D'

    def draw(self, context):
        settings = context.scene.blautorenamer.rename_objects
        lay = self.layout
        col = lay.column(align=True)
        split = col.split(align=True, factor=0.6)
        split.prop(settings, 'keyword', text='')
        split.prop(settings, 'side', text='')
        row = col.row(align=True)
        row.scale_y = 1.5
        row.operator('blautorenamer.rename_objects', icon='EVENT_S')


class VIEW3D_PT_utilities(bpy.types.Panel):

    bl_idname = 'VIEW3D_PT_utilities'
    bl_label = 'Utilities'
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = 'VIEW3D_PT_blautorenamer'
    bl_region_type = 'UI'
    bl_space_type = 'VIEW_3D'

    def draw(self, context):
        lay = self.layout
        lay.operator('blautorenamer.auto_rename_all', icon='BRUSH_DATA')
        lay.operator('blautorenamer.sort_collections', icon='OUTLINER')


################################################################################
# Registration
################################################################################


register, unregister = bpy.utils.register_classes_factory([
    VIEW3D_PT_blautorenamer,
    VIEW3D_PT_rename_selected_objects,
    VIEW3D_PT_utilities,
])
