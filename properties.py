# Imports
########################################################################################################################


if 'common' in locals():
    import importlib

    common = importlib.reload(common)
else:
    from . import common
    import bpy
    import re


########################################################################################################################
# Functions
########################################################################################################################


def rename_outliner_selection(self, context):

    settings = context.scene.blautorenamer.outliner
    prefs = context.preferences.addons[__package__].preferences.acronyms

    # NEW TAKE. DETERMINE KEYWORD OR LIST OF KEYWORDS.
    sequence_tokens = re.findall(pattern=r'\[{1}(?P<start>\d*|\w{1})\]{1}', string=settings.keyword)

    # Get all selected ids in the Outliner.
    ids = common.get_selected_outliner_ids()
    rename_map = common.get_rename_map(ids=ids, sequence_tokens=sequence_tokens)

    for new_name, id in rename_map.items():
        id.name = new_name

    # Determine if we're renaming using a list sequence.
    # If the keyword has one or more sequence tokens, use the list of sequential numbers or letters.
    # Else, just get one clean name for the selection.

    for index, id in enumerate(ids):

        if common.get_data_info(data=id).get('acronym') == prefs.collection:
            # If the id is a Collection, simply rename it.
            id.name = common.get_clean_name(data=id, keyword=settings.keyword)
            # TODO: rename all objects that instance this collection

        else:
            # For collection instances, rename their instanced collection first, then copy its name to the object.
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


class OutlinerSettings(bpy.types.PropertyGroup):
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
    outliner: bpy.props.PointerProperty(type=OutlinerSettings)


########################################################################################################################
# Registration
########################################################################################################################


classes = [
    OutlinerSettings,
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
