################################################################################
# Imports
################################################################################


import bpy


################################################################################
# Classes
################################################################################


class RenameObjectsSettings(bpy.types.PropertyGroup):
    keyword: bpy.props.StringProperty(name='Keyword', default='keyword')
    side: bpy.props.EnumProperty(name='Side', items=[
        ('auto', 'Auto Side',
            'Automatically determine what side each object is on.'),
        ('C', 'Center',
            'Set the object\'s side to Center, regardless of its position.'),
        ('L', 'Left',
            'Set the object\'s side to Left, regardless of its position.'),
        ('R', 'Right',
            'Set the object\'s side to Right, regardless of its position.'),
    ])


class BlautorenamerSceneProperties(bpy.types.PropertyGroup):
    rename_objects: bpy.props.PointerProperty(
        type=RenameObjectsSettings)


################################################################################
# Registration
################################################################################


classes = [
    RenameObjectsSettings,
    BlautorenamerSceneProperties,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.blautorenamer = bpy.props.PointerProperty(
        type=BlautorenamerSceneProperties)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.blautorenamer
