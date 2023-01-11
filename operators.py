################################################################################
# Imports
################################################################################


import bpy


################################################################################
# Classes
################################################################################


class BLAUTORENAMER_OT_rename_objects(bpy.types.Operator):
    '''Rename the selected objects'''

    bl_idname = 'blautorenamer.rename_objects'
    bl_label = 'Rename Selected Objects'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        return {'FINISHED'}


class BLAUTORENAMER_OT_sanitize_existing(bpy.types.Operator):
    '''Rename the selected collections'''

    bl_idname = 'blautorenamer.sanitize_existing'
    bl_label = 'Sanitize Existing Names'
    bl_options = {'REGISTER', 'UNDO'}

    object_data: bpy.props.BoolProperty(name='Object Data',
                                        default=False,
                                        description='Sanitize object data names, taking the keyword from their owners')
    collections: bpy.props.BoolProperty(name='Collections',
                                        default=True,
                                        description='Sanitize collection names')
    materials: bpy.props.BoolProperty(name='Materials',
                                      default=True,
                                      description='Sanitize material names')
    images: bpy.props.BoolProperty(name='Images',
                                   default=True,
                                   description='Rename images to their filename')
    worlds: bpy.props.BoolProperty(name='Worlds',
                                   default=True,
                                   description='Sanitize world names')

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)

    def execute(self, context):
        return {'FINISHED'}


class BLAUTORENAMER_OT_sort_collections(bpy.types.Operator):
    '''Sort collections alphabetically'''

    bl_idname = 'blautorenamer.sort_collections'
    bl_label = 'Sort Collections'
    bl_options = {'UNDO'}

    def execute(self, context):
        return {'FINISHED'}


################################################################################
# Registration
################################################################################


register, unregister = bpy.utils.register_classes_factory([
    BLAUTORENAMER_OT_rename_objects,
    BLAUTORENAMER_OT_sanitize_existing,
    BLAUTORENAMER_OT_sort_collections,
])
