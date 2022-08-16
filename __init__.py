# create dataset
# edit dataset

# WFC:
# create empty grid
# fill it according to the parameters given (with weights as well)
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
from . import databaseManagment
from . import utils

# TODO create rotated variations of a single tile

bl_info = {
    "name": "BlenderWFC",
    "author": "Smonking_Sheep",
    "description": "",
    "blender": (2, 80, 0),
    "version": (0, 0, 2),
    "location": "",
    "warning": "",
    "category": "Generic"
}


class helloWorld(bpy.types.Operator):
    bl_idname = "object.hello_world"
    bl_label = "Print Hello World"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        return {'FINISHED'}

# creates the interface for the wfc


class runWfcPanel(bpy.types.Panel):
    # usefull guide to make blender panels :
    # https://medium.com/geekculture/creating-a-custom-panel-with-blenders-python-api-b9602d890663
    """create a panel"""
    bl_label = "run wfc"
    bl_idname = "VIEW3D_PT_runWfc"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Wavefunction"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.prop(scene, 'wfc_size')
        layout.operator('wfc.run', text='Run wave function')


class CreateWfcDatabasePanel(bpy.types.Panel):
    """create a panel"""
    bl_label = "Create database"
    bl_idname = "VIEW3D_PT_createDatabase"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Wavefunction"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.operator('wfc.create_database', text='Create database')


class databaseManagmentPanel(bpy.types.Panel):
    """create a panel"""
    bl_label = "Database Managment"
    bl_idname = "VIEW3D_PT_wfcDatabaseManagment"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Wavefunction"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.operator('wfc.enable_disable_dbm', text='enable / disable')
        layout.operator('wfc.display_tile', text='display single tile')


class ToolsPanel(bpy.types.Panel):
    """create a panel"""
    bl_label = "Tools"
    bl_idname = "VIEW3D_PT_wfcTools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Wavefunction"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.label(text='Round mesh vertex coordinates : ')
        layout.prop(scene, 'wfc_tools_decimalLenght')
        layout.operator('wfc.clean_meshes', text='Clean meshes')


# creates the database from the selected meshes and saves it into a file


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
    # TODO : save the file within the blender file
# TODO : option to use objects in a collection as tiles for the database
# TODO : option to load and save the database to external file


class runWaveFunction(bpy.types.Operator):
    """runs and displays the wave function"""
    bl_idname = "wfc.run"
    bl_label = "run the wavefunction"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # read the parameters
        size = context.scene.wfc_size

        # read the database
        dir = os.path.dirname(bpy.data.filepath)
        databaseFile = open(f'{dir}/database.json', 'r')
        print(f'opening : {dir}/database.json \n\n')
        database = json.loads(databaseFile.read())
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


class displayTile(bpy.types.Operator):
    bl_idname = "wfc.display_tile"
    bl_label = "dislplay the matching tiles for a tile"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        databaseManagment.displayTile()
        return {'FINISHED'}


class enableDisableDbM(bpy.types.Operator):
    bl_idname = "wfc.enable_disable_dbm"
    bl_label = "enables or disables the db managment"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        is_DbManagmentEnabled = context.scene.wfc_DbManagment
        if is_DbManagmentEnabled:
            databaseManagment.disableDbManagment()
            context.scene.wfc_DbManagment = False
        else:
            databaseManagment.enableDbManagment()
            context.scene.wfc_DbManagment = True
        return {'FINISHED'}


class cleanMeshes(bpy.types.Operator):
    """round the vertices of every selected meshes"""
    bl_idname = "wfc.clean_meshes"
    bl_label = "clean meshes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        utils.clean_meshes(context.scene.wfc_tools_decimalLenght)
        return {'FINISHED'}


CLASSES = [
    # operators
    CreateAndSaveDatabase,
    runWaveFunction,
    cleanMeshes,
    enableDisableDbM,
    displayTile,
    # panels
    CreateWfcDatabasePanel,
    runWfcPanel,
    databaseManagmentPanel,
    ToolsPanel,
]

PROPS = [
    #('prefix', bpy.props.StringProperty(name='Prefix', default='Pref')),
    # wfc settings
    ('wfc_size', bpy.props.IntVectorProperty(
        name='size', default=(5, 5, 5), min=1, soft_max=20)),

    # wfc db managment
    ('wfc_DbManagment', bpy.props.BoolProperty(name='DbManagment', default=False)),

    # wfc tools
    ('wfc_tools_decimalLenght', bpy.props.IntProperty(
        name='decimal lenght', min=0, max=10, soft_min=1, soft_max=4)),
]


def register():
    print(f'**** Registring {len(CLASSES)} class')

    for c in CLASSES:
        bpy.utils.register_class(c)
    print('**** Done')

    for (prop_name, prop_value) in PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)


def unregister():
    print(f'**** Unregistring {len(CLASSES)} class')
    for c in CLASSES:
        bpy.utils.unregister_class(c)
    print('**** Done')

    for (prop_name, _) in PROPS:
        delattr(bpy.types.Scene, prop_name)
