################################################################################
# Imports
################################################################################


import bpy
import re
from mathutils import Vector
from pathlib import Path


################################################################################
# Functions
################################################################################


def get_acronym(data_type: str) -> str:

    preferences = bpy.context.preferences.addons[__package__].preferences

    acronyms = {
        'ARMATURE': preferences.acronyms.armature,
        'CAMERA': preferences.acronyms.camera,
        'COLLECTION': preferences.acronyms.collection,
        'CURVE': preferences.acronyms.curve,
        'EMPTY': preferences.acronyms.empty,
        'GPENCIL': preferences.acronyms.grease_pencil,
        'LATTICE': preferences.acronyms.lattice,
        'MATERIAL': preferences.acronyms.material,
        'MESH': preferences.acronyms.mesh,
        'FONT': preferences.acronyms.text,
        'VOLUME': preferences.acronyms.volume,
        'WORLD': preferences.acronyms.world
    }
    return acronyms.get(data_type, 'OBJ')


def get_side(ob: bpy.types.Object, treshold_factor: float = 1.1) -> str:
    '''Determine the side of an object based on whether or not it crosses the
    Y-axis.'''

    bbox_ws = [ob.matrix_world @ Vector(corner) for corner in ob.bound_box]
    xmin = abs(bbox_ws[0][0])
    xmax = abs(bbox_ws[4][0])

    if xmax > xmin * treshold_factor:
        return 'L'
    if xmax * treshold_factor < xmin:
        return 'R'
    return 'C'


def get_clean_name(data: bpy.types.ID,
                   data_type: str = None,
                   keyword: str = None,
                   include_side: bool = False,
                   override_side: str = None) -> str:
    '''This is the main sanitization function. The keyword, acronym, and
    optionally the object side are determined and combined as per the naming
    convention.'''

    # If the keyword was not provided, grab it from the existing name.
    if not keyword or keyword == '':
        keyword = ''.join([c for c in re.split('\W+', data.name)[0]])

    # Determine the acronym per the object type.
    if not data_type:
        data_type = data.type
    acronym = get_acronym(data_type=data_type)

    # If the object side is requested, include it in the name.
    if include_side:
        side = override_side if override_side else get_side(ob=data)
        return f'{keyword}.{side}.{acronym}.001'
    return f'{keyword}.{acronym}.001'


def is_linked(data: bpy.types.ID) -> bool:
    '''Return whether or not the datablock is linked into the current Blender
    file'''

    return data.library or data.override_library


################################################################################
# Classes
################################################################################


class BLAUTORENAMER_OT_rename_objects(bpy.types.Operator):
    '''Rename the selected objects'''

    bl_idname = 'blautorenamer.rename_objects'
    bl_label = 'Rename Selected Objects'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        settings = context.scene.blautorenamer.rename_objects
        objects = [ob for ob in context.selected_objects
                   if not is_linked(data=ob)]

        for ob in objects:

            # For collection instances, rename their instancing collection
            # first, then copy its name to the object.
            if ob.instance_collection:
                ob.instance_collection.name = get_clean_name(
                    data=ob.instance_collection,
                    keyword=settings.keyword
                )
                ob.name = ob.instance_collection.name

            # For all other objects, simply create a sanitized name. If the
            # object's data is accessible, rename it as well.
            else:
                override_side = None if settings.side == 'auto' else settings.side
                ob.name = get_clean_name(
                    data=ob,
                    keyword=settings.keyword,
                    include_side=True,
                    override_side=override_side
                )
                if ob.data:
                    if not is_linked(data=ob.data):
                        ob.data.name = get_clean_name(
                            data=ob.data,
                            data_type=ob.type,
                            keyword=settings.keyword
                        )

        return {'FINISHED'}


class BLAUTORENAMER_OT_auto_rename_all(bpy.types.Operator):
    '''Apply naming conventions to existing names'''

    bl_idname = 'blautorenamer.auto_rename_all'
    bl_label = 'Auto Rename All...'
    bl_options = {'REGISTER', 'UNDO'}

    objects_and_data: bpy.props.BoolProperty(
        name='Objects and Data',
        default=True,
        description='Sanitize object data names, taking the keyword from their owners'
    )
    collections: bpy.props.BoolProperty(
        name='Collections',
        default=True,
        description='Sanitize collection names and copy them to their instances'
    )
    materials: bpy.props.BoolProperty(
        name='Materials',
        default=True,
        description='Sanitize material names'
    )
    images: bpy.props.BoolProperty(
        name='Images',
        default=True,
        description='Rename images to their filename'
    )
    worlds: bpy.props.BoolProperty(
        name='Worlds',
        default=True,
        description='Sanitize world names'
    )

    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self, width=300)

    def execute(self, context):

        if self.objects_and_data:

            objects = [ob for ob in bpy.data.objects
                       if not is_linked(data=ob)]

            for ob in objects:

                # For collection instances, rename their instancing collection
                # first, then copy its name to the object.
                if ob.instance_collection:
                    ob.instance_collection.name = get_clean_name(
                        data=ob.instance_collection,
                        data_type='COLLECTION'
                    )
                    ob.name = get_clean_name(
                        data=ob.instance_collection,
                        data_type='COLLECTION'
                    )

                # For all other objects, simply create a sanitized name. If the
                # object's data is accessible, rename it as well.
                else:
                    ob.name = get_clean_name(
                        data=ob,
                        include_side=True
                    )
                    if ob.data:
                        if not is_linked(data=ob.data):
                            ob.data.name = get_clean_name(
                                data=ob.data,
                                data_type=ob.type
                            )

        if self.collections:

            collections = [c for c in bpy.data.collections
                           if not is_linked(data=c)]

            for c in collections:
                c.name = get_clean_name(
                    data=c,
                    data_type='COLLECTION'
                )

        if self.materials:

            materials = [m for m in bpy.data.materials
                         if not is_linked(data=m)]

            for m in materials:
                m.name = get_clean_name(
                    data=m,
                    data_type='MATERIAL'
                )

        if self.images:

            images = [i for i in bpy.data.images
                      if not is_linked(data=i)
                      and not i.name == 'Render Result']

            for i in images:
                abs_path = i.filepath
                if i.filepath.startswith('//'):
                    abs_path = bpy.path.abspath(i.filepath, library=i.library)
                i.name = Path(abs_path).stem

        if self.worlds:

            worlds = [w for w in bpy.data.worlds
                      if not is_linked(data=w)]

            for w in worlds:
                w.name = get_clean_name(
                    data=w,
                    data_type='WORLD'
                )

        return {'FINISHED'}


class BLAUTORENAMER_OT_sort_collections(bpy.types.Operator):
    '''Sort collections alphabetically'''

    bl_idname = 'blautorenamer.sort_collections'
    bl_label = 'Sort Collections'
    bl_options = {'UNDO'}

    def execute(self, context):

        def sort_collection(collection):
            '''Recursive function that unlinks and relinks every sub
            collection, then proceeds to repeat itself on that collection.'''

            if not collection.children:
                return

            children = sorted(collection.children, key=lambda c: c.name)
            for child in children:
                collection.children.unlink(child)
                collection.children.link(child)
                sort_collection(child)

        sort_collection(context.scene.collection)

        return {'FINISHED'}


################################################################################
# Registration
################################################################################


register, unregister = bpy.utils.register_classes_factory([
    BLAUTORENAMER_OT_rename_objects,
    BLAUTORENAMER_OT_auto_rename_all,
    BLAUTORENAMER_OT_sort_collections,
])
