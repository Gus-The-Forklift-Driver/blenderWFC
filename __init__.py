# create dataset
# edit dataset

# WFC:
# create empty grid
# fill it according to the parameters given (with veights as well)
# choose starting location

# collapse
# update the neighboring cells that need to be updated
# repeat

import bpy
import sys
import os
import json
from . import database
from . import wavefunction
from . import utils

# if "bpy" in locals():
#     import importlib
#     importlib.reload(database)
# else:
#     from . import database


bl_info = {
    "name": "BlenderWFC",
    "author": "Smonking_Sheep",
    "description": "",
    "blender": (2, 80, 0),
    "version": (0, 0, 1),
    "location": "",
    "warning": "",
    "category": "Generic"
}


class helloWorld(bpy.types.Operator):
    """Prints hello world into the console"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.hello_world"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Print Hello World"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):
        print('hello world')
        return {'FINISHED'}


class ObjectMoveX(bpy.types.Operator):
    """My Object Moving Script"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.move_x"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Move X by One"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    # execute() is called when running the operator.
    def execute(self, context):

        # The original script
        scene = context.scene
        for obj in scene.objects:
            obj.location.x += 1.0

        return {'FINISHED'}


class CreateAndSaveDatabase(bpy.types.Operator):
    """Create and save the WFC in a json file"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "wfc.create_database"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Create database"         # Display name in the interface.
    bl_options = {'REGISTER'}

    # execute() is called when running the operator.
    def execute(self, context):
        d = database.databaseMaker()
        d.save_database_to_file(d.create_database())
        return {'FINISHED'}


class runWaveFunction(bpy.types.Operator):
    """runs and displays the wave function"""
    bl_idname = "wfc.run"
    bl_label = "run the wavefunction"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # read the database
        dir = os.path.dirname(bpy.data.filepath)
        databaseFile = open(f'{dir}/database.json', 'r')
        print(f'opening : {dir}/database.json \n\n')
        database = json.loads(databaseFile.read())

        size = (5, 5, 5)
        # create the wfc object
        wave = wavefunction.waveFunction(database, size)
        # initiate it at random location and tile
        wave.set_start()

        step = 0
        while True:
            if len(wave.tilesToUpdate) == 0:
                coord = wave.consolidate_entropy()
                if coord == False:
                    break
                else:
                    wave.set_cell(coord)
                    wave.update_adjacent(coord)
            else:
                wave.propagate()
            # print(tilesToUpdate)
            step += 1
            if step % 50 == 0:
                wave.display_status(step)
                pass
        print('\n**** CREATING GRID VIZ ****')
        # print(wave.cellGrid)
        utils.preview_grid(size, wave.cellGrid)

        return {'FINISHED'}


class cleanMeshes(bpy.types.Operator):
    """round the vertices of every selected meshes"""
    bl_idname = "wfc.clean_meshes"
    bl_label = "clean meshes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        utils.clean_meshes()
        return {'FINISHED'}


def register():

    bpy.utils.register_class(helloWorld)
    bpy.utils.register_class(ObjectMoveX)
    bpy.utils.register_class(CreateAndSaveDatabase)
    bpy.utils.register_class(runWaveFunction)
    bpy.utils.register_class(cleanMeshes)


def unregister():
    bpy.utils.unregister_class(helloWorld)
    bpy.utils.unregister_class(ObjectMoveX)
    bpy.utils.unregister_class(CreateAndSaveDatabase)
    bpy.utils.unregister_class(runWaveFunction)
    bpy.utils.unregister_class(cleanMeshes)
