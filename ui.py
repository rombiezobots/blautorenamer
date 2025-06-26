########################################################################################################################
# Imports
########################################################################################################################


import bpy


########################################################################################################################
# Functions
########################################################################################################################


def blautorenamer_ui(self, context):
    if context.space_data.display_mode in ['VIEW_LAYER', 'SCENES']:
        settings = context.scene.blautorenamer.outliner
        row = self.layout.row(align=True)
        row.prop(settings, 'keyword', text='', icon='EVENT_B')
        row.prop(settings, 'side', text='')


########################################################################################################################
# Registration
########################################################################################################################


def register():
    bpy.types.OUTLINER_HT_header.append(blautorenamer_ui)


def unregister():
    bpy.types.OUTLINER_HT_header.remove(blautorenamer_ui)
