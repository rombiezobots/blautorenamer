########################################################################################################################
# Imports
########################################################################################################################


if 'common' in locals():
    import importlib

    common = importlib.reload(common)
else:
    from . import common
    from pathlib import Path
    import bpy


########################################################################################################################
# Functions
########################################################################################################################


########################################################################################################################
# Classes
########################################################################################################################


class BLAUTORENAMER_OT_auto_rename_all(bpy.types.Operator):
    '''Apply naming conventions to existing names'''

    bl_idname = 'blautorenamer.auto_rename_all'
    bl_label = 'Auto Rename All...'
    bl_options = {'REGISTER', 'UNDO'}

    objects_and_data: bpy.props.BoolProperty(
        name='Objects and Data',
        default=True,
        description='Sanitize object data names, taking the keyword from their owners',
    )
    # TODO: keep existing side if any
    collections: bpy.props.BoolProperty(
        name='Collections', default=True, description='Sanitize collection names and copy them to their instances'
    )
    materials: bpy.props.BoolProperty(name='Materials', default=True, description='Sanitize material names')
    images: bpy.props.BoolProperty(name='Images', default=True, description='Rename images to their filename')
    worlds: bpy.props.BoolProperty(name='Worlds', default=True, description='Sanitize world names')

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)

    def execute(self, context):
        if self.objects_and_data:
            objects = [ob for ob in bpy.data.objects if not common.is_linked(data=ob)]

            for ob in objects:
                # For collection instances, rename their instancing collection
                # first, then copy its name to the object.
                if ob.instance_collection:
                    ob.instance_collection.name = common.get_clean_name(data=ob.instance_collection)
                    ob.name = common.get_clean_name(data=ob.instance_collection)

                # For all other objects, simply create a sanitized name. If the
                # object's data is accessible, rename it as well.
                else:
                    ob.name = common.get_clean_name(data=ob, include_side=True)
                    if ob.data:
                        if not common.is_linked(data=ob.data):
                            ob.data.name = common.get_clean_name(data=ob.data)

        if self.collections:
            collections = [c for c in bpy.data.collections if not common.is_linked(data=c)]

            for c in collections:
                c.name = common.get_clean_name(data=c)

        if self.materials:
            materials = [m for m in bpy.data.materials if not common.is_linked(data=m)]

            for m in materials:
                m.name = common.get_clean_name(data=m)

        if self.images:
            images = [i for i in bpy.data.images if not common.is_linked(data=i) and not i.name == 'Render Result']

            for i in images:
                abs_path = i.filepath
                if i.filepath.startswith('//'):
                    abs_path = bpy.path.abspath(i.filepath, library=i.library)
                i.name = Path(abs_path).stem

        if self.worlds:
            worlds = [w for w in bpy.data.worlds if not common.is_linked(data=w)]

            for w in worlds:
                w.name = common.get_clean_name(data=w)

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


########################################################################################################################
# Registration
########################################################################################################################


register, unregister = bpy.utils.register_classes_factory(
    [
        BLAUTORENAMER_OT_auto_rename_all,
        BLAUTORENAMER_OT_sort_collections,
    ]
)
