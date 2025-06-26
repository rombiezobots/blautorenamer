########################################################################################################################
# Imports
########################################################################################################################


import bpy


########################################################################################################################
# Functions
########################################################################################################################


def draw_main_menu(self, context):
    lay = self.layout
    lay.menu(TOPBAR_MT_blautorenamer.bl_idname)


########################################################################################################################
# Classes
########################################################################################################################


class TOPBAR_MT_blautorenamer(bpy.types.Menu):
    bl_label = 'blautorenamer'
    bl_idname = 'TOPBAR_MT_blautorenamer'

    def draw(self, context):
        lay = self.layout
        lay.operator('blautorenamer.auto_rename_all', icon='BRUSH_DATA')


########################################################################################################################
# Registration
########################################################################################################################


def register():
    bpy.utils.register_class(TOPBAR_MT_blautorenamer)
    bpy.types.TOPBAR_MT_editor_menus.append(draw_main_menu)


def unregister():
    bpy.types.TOPBAR_MT_editor_menus.remove(draw_main_menu)
    bpy.utils.unregister_class(TOPBAR_MT_blautorenamer)
