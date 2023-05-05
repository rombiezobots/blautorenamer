# Imports
########################################################################################################################


if 'common' in locals():
    import importlib

    common = importlib.reload(common)
else:
    from . import common
    import bpy


########################################################################################################################
# Functions
########################################################################################################################


def rename_outliner_selection(self, context):
    settings = context.scene.blautorenamer.rename_objects
    prefs = bpy.context.preferences.addons[__package__].preferences.acronyms

    # Get all selected ids in the Outliner.
    ids = [id for id in context.selected_ids if not common.is_linked(data=id)]

    for id in ids:
        if common.get_data_info(data=id).get('acronym') == prefs.collection:
            # If the id is a Collection, simply rename it.
            id.name = common.get_clean_name(data=id, keyword=settings.keyword)
            # TODO: rename all objects that instance this collection

        else:
            # For collection instances, rename their instancing collection first, then copy its name to the object.
            if id.instance_collection:
                id.instance_collection.name = common.get_clean_name(
                    data=id.instance_collection, keyword=settings.keyword
                )
                id.name = id.instance_collection.name

            # For all other objects, simply create a sanitized name. If the object's data is accessible, rename it
            # as well.
            else:
                override_side = None if settings.side == 'auto' else settings.side
                id.name = common.get_clean_name(
                    data=id, keyword=settings.keyword, include_side=True, override_side=override_side
                )
                if id.data and not common.is_linked(data=id.data):
                    id.data.name = common.get_clean_name(data=id.data, keyword=settings.keyword)


########################################################################################################################
# Classes
########################################################################################################################


class RenameObjectsSettings(bpy.types.PropertyGroup):
    keyword: bpy.props.StringProperty(name='Keyword', default='keyword', update=rename_outliner_selection)
    side: bpy.props.EnumProperty(
        name='Side',
        items=[
            ('auto', 'A', 'Automatically determine what side each object is on'),
            ('C', 'C', 'Set the object\'s side to Center, regardless of its position'),
            ('L', 'L', 'Set the object\'s side to Left, regardless of its position'),
            ('R', 'R', 'Set the object\'s side to Right, regardless of its position'),
        ],
    )


class BlautorenamerSceneProperties(bpy.types.PropertyGroup):
    rename_objects: bpy.props.PointerProperty(type=RenameObjectsSettings)


########################################################################################################################
# Registration
########################################################################################################################


classes = [
    RenameObjectsSettings,
    BlautorenamerSceneProperties,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.blautorenamer = bpy.props.PointerProperty(type=BlautorenamerSceneProperties)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.blautorenamer
