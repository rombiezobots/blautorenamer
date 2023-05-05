########################################################################################################################
# Imports
########################################################################################################################


import bpy
import re
from mathutils import Vector


########################################################################################################################
# Functions
########################################################################################################################


def get_clean_name(
    data: bpy.types.ID,
    keyword: str = None,
    include_side: bool = False,
    override_side: str = None,
) -> str:
    '''This is the main sanitization function. The keyword, acronym, and optionally the object side are determined and
    combined as per the naming convention.'''

    # If the keyword was not provided, grab it from the existing name.
    if not keyword or keyword == '':
        keyword = ''.join([c for c in re.split('\W+', data.name)[0]])

    # Determine the acronym.
    acronym = get_data_info(data=data)['acronym']

    # If the object side is requested, include it in the name.
    if include_side:
        side = override_side if override_side else get_side(ob=data)
        return f'{keyword}.{side}.{acronym}.001'
    return f'{keyword}.{acronym}.001'


def get_data_info(data: bpy.types.ID):
    '''Get acronyms, bl_types and data_types for supported ID types.'''
    prefs = bpy.context.preferences.addons[__package__].preferences.acronyms
    types = [
        {'acronym': prefs.armature, 'bl_type': 'bpy.types.Armature', 'data_type': 'ARMATURE'},
        {'acronym': prefs.camera, 'bl_type': 'bpy.types.Camera', 'data_type': 'CAMERA'},
        {'acronym': prefs.curve, 'bl_type': 'bpy.types.Curve', 'data_type': 'CURVE'},
        {'acronym': prefs.empty, 'bl_type': 'NoneType', 'data_type': 'EMPTY'},
        {'acronym': prefs.text, 'bl_type': 'bpy.types.TextCurve', 'data_type': 'FONT'},
        {'acronym': prefs.grease_pencil, 'bl_type': 'bpy.types.GreasePencil', 'data_type': 'GPENCIL'},
        {'acronym': prefs.lattice, 'bl_type': 'bpy.types.Lattice', 'data_type': 'LATTICE'},
        {'acronym': prefs.material, 'bl_type': 'bpy.types.Material', 'data_type': 'MATERIAL'},
        {'acronym': prefs.mesh, 'bl_type': 'bpy_types.Mesh', 'data_type': 'MESH'},
        {'acronym': prefs.volume, 'bl_type': 'bpy.types.Volume', 'data_type': 'VOLUME'},
        {'acronym': prefs.world, 'bl_type': 'bpy.types.World', 'data_type': 'WORLD'},
    ]

    # If the data is an object, look for its datablock's type.
    if str(type(data)) == '<class \'bpy_types.Object\'>':
        return next((typ for typ in types if typ.get('data_type') == data.type), {'acronym': 'OBJ'})

    # Else, look for its datablock type based on the Python / C++ class name. If it can't be found, it's a Collection.
    return next(
        (typ for typ in types if f"<class '{typ['bl_type']}'>" == str(type(data))), {'acronym': prefs.collection}
    )


def get_side(ob: bpy.types.Object, treshold_factor: float = 1.1) -> str:
    '''Determine the side of an object based on whether or not it crosses the Y-axis.'''

    bbox_ws = [ob.matrix_world @ Vector(corner) for corner in ob.bound_box]
    xmin = abs(bbox_ws[0][0])
    xmax = abs(bbox_ws[4][0])

    if xmax > xmin * treshold_factor:
        return 'L'
    if xmax * treshold_factor < xmin:
        return 'R'
    return 'C'


def is_linked(data: bpy.types.ID) -> bool:
    return data.library or data.override_library
