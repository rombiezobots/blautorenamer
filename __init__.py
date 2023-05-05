########################################################################################################################
# Imports
########################################################################################################################


if 'properties' in locals():
    import importlib

    preferences = importlib.reload(preferences)
    properties = importlib.reload(properties)
    operators = importlib.reload(operators)
    ui = importlib.reload(ui)
else:
    from . import preferences
    from . import properties
    from . import operators
    from . import ui


########################################################################################################################
# Add-on information
########################################################################################################################


bl_info = {
    'name': 'blautorenamer',
    'description': 'Auto-renaming tools.',
    'author': 'Sam Van Hulle',
    'version': (0, 0, 1),
    'blender': (3, 4, 0),
    'location': 'View3D > UI',
    'category': 'Tools',
}


########################################################################################################################
# Registration
########################################################################################################################


modules = [
    preferences,
    properties,
    operators,
    ui,
]


def register():
    for module in modules:
        module.register()


def unregister():
    for module in reversed(modules):
        module.unregister()


if __name__ == '__main__':
    register()
