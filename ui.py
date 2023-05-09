########################################################################################################################
# Imports
########################################################################################################################


import bpy


########################################################################################################################
# Functions
########################################################################################################################


def blautorenamer_ui(self, context):
    if context.space_data.display_mode in ['VIEW_LAYER', 'SCENES']:
        settings = context.scene.blautorenamer.rename_objects
        row = self.layout.row(align=True)
        row.prop(settings, 'keyword', text='', icon='EVENT_B')
        row.prop(settings, 'side', text='')
        row.operator('blautorenamer.auto_rename_all', icon='BRUSH_DATA', text='')
        row.operator('blautorenamer.sort_collections', icon='OUTLINER', text='')


########################################################################################################################
# Registration
########################################################################################################################


def register():
    bpy.types.OUTLINER_HT_header.append(blautorenamer_ui)


def unregister():
    bpy.types.OUTLINER_HT_header.remove(blautorenamer_ui)
