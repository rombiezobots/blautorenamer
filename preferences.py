################################################################################
# Imports
################################################################################


import bpy


################################################################################
# Classes
################################################################################


class Acronyms(bpy.types.PropertyGroup):

    armature: bpy.props.StringProperty(
        name='Armatures',
        default='RIG'
    )
    camera: bpy.props.StringProperty(
        name='Cameras',
        default='CAM'
    )
    collection: bpy.props.StringProperty(
        name='Collections',
        default='GRP'
    )
    curve: bpy.props.StringProperty(
        name='Curves',
        default='CRV'
    )
    empty: bpy.props.StringProperty(
        name='Empties',
        default='LOC'
    )
    grease_pencil: bpy.props.StringProperty(
        name='Grease Pencil',
        default='GPL'
    )
    lattice: bpy.props.StringProperty(
        name='Lattices',
        default='LAT'
    )
    material: bpy.props.StringProperty(
        name='Materials',
        default='MAT'
    )
    mesh: bpy.props.StringProperty(
        name='Meshes',
        default='GEO'
    )
    text: bpy.props.StringProperty(
        name='Text',
        default='TXT'
    )
    volume: bpy.props.StringProperty(
        name='Volumes',
        default='VOL'
    )
    world: bpy.props.StringProperty(
        name='Worlds',
        default='SKY'
    )


class AutoRenamerAddonPreferences(bpy.types.AddonPreferences):

    bl_idname = __package__
    acronyms: bpy.props.PointerProperty(type=Acronyms)

    def draw(self, context):

        lay = self.layout
        lay.use_property_split = True
        box = lay.box()
        box.label(text='Data Type Acronyms:')
        col = box.column(align=True)
        for key in Acronyms.__annotations__.keys():
            col.prop(self.acronyms, key)


################################################################################
# Registration
################################################################################


register, unregister = bpy.utils.register_classes_factory([
    Acronyms,
    AutoRenamerAddonPreferences,
])
