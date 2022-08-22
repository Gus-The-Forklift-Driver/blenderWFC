#  _____               _   _               _____ _
# |   __|_____ ___ ___| |_|_|___ ___      |   __| |_ ___ ___ ___
# |__   |     | . |   | '_| |   | . |     |__   |   | -_| -_| . |
# |_____|_|_|_|___|_|_|_,_|_|_|_|_  |_____|_____|_|_|___|___|  _|
#                               |___|_____|                 |_|
# ██╗    ██╗███████╗ ██████╗
# ██║    ██║██╔════╝██╔════╝
# ██║ █╗ ██║█████╗  ██║
# ██║███╗██║██╔══╝  ██║
# ╚███╔███╔╝██║     ╚██████╗
#  ╚══╝╚══╝ ╚═╝      ╚═════╝


# create dataset
# edit dataset

# WFC:
# create empty grid
# fill it according to the parameters given (with weights as well)
# choose starting location

# collapse
# update the neighboring cells that need to be updated
# repeat


import json
import os
from pickle import TRUE

import bpy

from . import database, databaseManagment, utils, wavefunction

# TODO create rotated variations of a single tile

bl_info = {
    "name": "BlenderWFC",
    "author": "Smonking_Sheep",
    "description": "",
    "blender": (3, 2, 1),
    "version": (0, 0, 3),
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
        layout.prop(scene.wfc, 'size')
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

        if context.scene.wfc.DbManagment == True:
            layout.operator('wfc.enable_disable_dbm',
                            text='disable database Managment')
        else:
            layout.operator('wfc.enable_disable_dbm',
                            text='enable database Managment')
        if context.scene.wfc.DbManagment == True:
            if context.scene.wfc.current_edited_tile != '':
                layout.label(text=context.scene.wfc.current_edited_tile)
            row = layout.row(align=True)
            row.operator('wfc.display_previous_tile', text='<< previous tile')
            row.operator('wfc.display_next_tile', text='next tile >>')
            layout.operator('wfc.update_tile', text='Update tile')


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
        layout.prop(scene.wfc, 'tools_decimalLenght')
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
        db = d.create_database()
        db = d.sortDatabaseKeys(db)
        d.save_database_to_file(db)
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
        size = context.scene.wfc.size

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


class enableDisableDbM(bpy.types.Operator):
    bl_idname = "wfc.enable_disable_dbm"
    bl_label = "enables or disables the db managment"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.scene.wfc.DbManagment == True:
            databaseManagment.removeCurrentlyDisplayedTile()
            databaseManagment.disableDbManagment()
            context.scene.wfc.DbManagment = False
            context.scene.wfc.current_edited_tile = ''
        else:
            databaseManagment.enableDbManagment()
            context.scene.wfc.current_edited_tile = databaseManagment.displayTile(
                tileIndex=0)
            context.scene.wfc.DbManagment = True
        return {'FINISHED'}


class displayNextTile(bpy.types.Operator):
    bl_idname = "wfc.display_next_tile"
    bl_label = 'changes the current displayed tile in db managment'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # remove the displayed tile
        # TODO check if they were created from the db managment
        databaseManagment.removeCurrentlyDisplayedTile()
        context.scene.wfc.current_edited_tile = databaseManagment.displayTile(
            tileIndex=1)
        return {'FINISHED'}


class displayPreviousTile(bpy.types.Operator):
    bl_idname = "wfc.display_previous_tile"
    bl_label = 'changes the current displayed tile in db managment'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # remove the displayed tile
        # TODO check if they were created from the db managment
        databaseManagment.removeCurrentlyDisplayedTile()
        context.scene.wfc.current_edited_tile = databaseManagment.displayTile(
            tileIndex=-1)
        return {'FINISHED'}


class updateTile(bpy.types.Operator):
    bl_idname = "wfc.update_tile"
    bl_label = 'update the object available tiles with the ones present'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        updatedTileValues = databaseManagment.neighbouringTile()
        databaseManagment.updateDb(updatedTileValues)
        return {'FINISHED'}


class cleanMeshes(bpy.types.Operator):
    """round the vertices of every selected meshes"""
    bl_idname = "wfc.clean_meshes"
    bl_label = "clean meshes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        utils.clean_meshes(context.scene.wfc.tools_decimalLenght)
        return {'FINISHED'}

# TODO move all propreties into this class


class wfcPropertiesGroup(bpy.types.PropertyGroup):
    #testint = bpy.props.IntProperty(name="testint",description="",default=1,min=1,)
    current_edited_tile: bpy.props.StringProperty(name='current_edited_tile')
    tools_decimalLenght: bpy.props.IntProperty(
        name='decimal lenght', min=0, max=10, soft_min=1, soft_max=4)
    size: bpy.props.IntVectorProperty(
        name='size', default=(5, 5, 5), min=1, soft_max=20)
    DbManagment: bpy.props.BoolProperty(name='DbManagment', default=False)


class wfcObjectPropertiesGroup(bpy.types.PropertyGroup):
    tile_type: bpy.props.StringProperty(name='tile_type')
    tile_name: bpy.props.StringProperty(name='tile_name')


CLASSES = [
    # property group
    wfcPropertiesGroup,
    wfcObjectPropertiesGroup,
    # operators
    CreateAndSaveDatabase,
    runWaveFunction,
    cleanMeshes,
    enableDisableDbM,
    displayNextTile,
    displayPreviousTile,
    updateTile,
    # panels
    CreateWfcDatabasePanel,
    runWfcPanel,
    databaseManagmentPanel,
    ToolsPanel,

]


def register():
    print(f'**** Registring {len(CLASSES)} class')
    for c in CLASSES:
        bpy.utils.register_class(c)
    print('**** Done')

    # register the property group
    bpy.types.Scene.wfc = bpy.props.PointerProperty(type=wfcPropertiesGroup)
    bpy.types.Object.wfc_object = bpy.props.PointerProperty(
        type=wfcObjectPropertiesGroup)


def unregister():
    print(f'**** Unregistring {len(CLASSES)} class')
    for c in CLASSES:
        bpy.utils.unregister_class(c)
    print('**** Done')

    # delete the proterty group
    del bpy.types.Scene.wfc
    del bpy.types.Object.wfc_object
