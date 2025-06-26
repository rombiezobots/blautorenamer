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
    keep_existing_side: bpy.props.BoolProperty(
        name='Keep Existing Side', default=True, description='Keep existing side acronym, if any'
    )
    collections: bpy.props.BoolProperty(
        name='Collections', default=True, description='Sanitize collection names and copy them to their instances'
    )
    materials: bpy.props.BoolProperty(name='Materials', default=True, description='Sanitize material names')
    images: bpy.props.BoolProperty(name='Images', default=True, description='Rename images to their filename')
    worlds: bpy.props.BoolProperty(name='Worlds', default=True, description='Sanitize world names')

    def _determine_existing_side(self, name: str) -> str:
        valid_name = name.split('.')
        if len(valid_name) == 4:
            if valid_name[1] in ['C', 'L', 'R']:
                return valid_name[1]
        return None

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)

    def draw(self, context):
        lay = self.layout
        lay.use_property_split = True
        lay.prop(self, 'collections')
        lay.prop(self, 'objects_and_data')
        split = lay.split(factor=0.1)
        split.active = self.objects_and_data
        split.label(text='')
        split.prop(self, 'keep_existing_side')
        lay.prop(self, 'materials')
        lay.prop(self, 'images')
        lay.prop(self, 'worlds')

    def execute(self, context):

        if self.collections:
            collections = [c for c in bpy.data.collections if not common.is_linked(data=c)]

            for c in collections:
                new_name = common.get_clean_name(data=c)
                c.name = new_name

        if self.objects_and_data:
            objects = [ob for ob in bpy.data.objects if not common.is_linked(data=ob)]

            for ob in objects:
                # For collection instances, simply copy the collection's name to the object.
                if ob.instance_collection:
                    ob.name = ob.instance_collection.name

                # For all other objects, create a sanitized name. If the
                # object's data is accessible, rename it as well.
                else:
                    if self.keep_existing_side:
                        ob.name = common.get_clean_name(
                            data=ob, include_side=True, override_side=self._determine_existing_side(ob.name)
                        )
                    else:
                        ob.name = common.get_clean_name(data=ob, include_side=True)
                    if ob.data:
                        if not common.is_linked(data=ob.data):
                            ob.data.name = common.get_clean_name(data=ob.data)

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


########################################################################################################################
# Registration
########################################################################################################################


register, unregister = bpy.utils.register_classes_factory(
    [
        BLAUTORENAMER_OT_auto_rename_all,
    ]
)
