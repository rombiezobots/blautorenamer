################################################################################
# Imports
################################################################################


if 'bpy' in locals():
    import importlib
    properties = importlib.reload(properties)
    operators = importlib.reload(operators)
    panels = importlib.reload(panels)
else:
    from . import properties
    from . import operators
    from . import panels


################################################################################
# Add-on information
################################################################################


bl_info = {
    'name': 'blautorenamer',
    'description': 'Auto-renaming tools.',
    'author': 'Sam Van Hulle',
    'version': (0, 0, 1),
    'blender': (3, 4, 0),
    'location': 'View3D > UI',
    'category': 'Tools'
}


################################################################################
# Registration
################################################################################


modules = [
    properties,
    operators,
    panels,
]


def register():
    for module in modules:
        module.register()


def unregister():
    for module in reversed(modules):
        module.unregister()


if __name__ == '__main__':
    register()
