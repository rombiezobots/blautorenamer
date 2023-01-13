# blautorenamer

An auto renamer for Blender, available under Item in the Viewport's side panel.

## Rename Selected Objects
This is your standard generic object renamer. It takes an optional **keyword**, with a fallback to each object's current name. You can also let the tool decide what **side** the object is on, or override it with Left, Right or Center. The side tokens, as well as the **object type acronym**, are yours to customize in the **add-on preferences**.

The new name is copied to the object's data. To support shared object data, the **side** token is left out here.

## Utilities

### Auto Rename All...
As the name suggests, this automates things. **Auto Rename All...** lets you select what types of datablocks (across the entire .blend file) need renaming, and applies the naming conventions to their **current names**.

### Sort Collections Alphabetically
Since collections are left out of alphabetical sorting in the Outliner, this button allows you to do exactly that.
