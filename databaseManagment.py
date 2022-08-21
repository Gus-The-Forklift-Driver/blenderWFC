from operator import truediv
import bpy
import json
import os
from . import utils

# Db is short for database


currentEditedTile = 0


def enableDbManagment():
    print('enabling database managment')
    # read the database
    dir = os.path.dirname(bpy.data.filepath)
    databaseFile = open(f'{dir}/database.json', 'r')
    print(f'opening : {dir}/database.json \n\n')
    global database
    database = json.loads(databaseFile.read())
    # hide every objects
    for object in bpy.context.scene.objects:
        if object.wfc_object.tile_type == 'DBTILE':
            pass
        else:
            object.hide_viewport = True


def disableDbManagment():
    print('disabling database managment')
    global currentEditedTile
    currentEditedTile = 0
    for object in bpy.context.scene.objects:
        object.hide_viewport = False


def displayTile(tileToDisplay: str = '', tileIndex: int = None):
    global currentEditedTile
    if tileIndex != None:
        currentEditedTile += tileIndex
        if currentEditedTile > len(list(database))-1 or currentEditedTile < 0:
            currentEditedTile -= tileIndex
        tileToDisplay = list(database)[currentEditedTile]
    utils.duplicate_object((0, 0, 0), tileToDisplay, tile_type='TILEPREV')
    offset = 1
    for x in database[tileToDisplay]['x+']:
        utils.duplicate_object((offset*2, 0, 0), x, tile_type='TILEPREV')
        offset = offset + 1
    offset = 1
    for x in database[tileToDisplay]['x-']:
        utils.duplicate_object((offset*-2, 0, 0), x, tile_type='TILEPREV')
        offset = offset + 1

    offset = 1
    for y in database[tileToDisplay]['y+']:
        utils.duplicate_object((0, offset*2, 0), y, tile_type='TILEPREV')
        offset = offset + 1
    offset = 1
    for y in database[tileToDisplay]['y-']:
        utils.duplicate_object((0, offset*-2, 0), y, tile_type='TILEPREV')
        offset = offset + 1

    offset = 1
    for z in database[tileToDisplay]['z+']:
        utils.duplicate_object((0, 0, offset*2), z, tile_type='TILEPREV')
        offset = offset + 1
    offset = 1
    for z in database[tileToDisplay]['z-']:
        utils.duplicate_object((0, 0, offset*-2), z, tile_type='TILEPREV')
        offset = offset + 1
    return tileToDisplay


def removeCurrentlyDisplayedTile():
    for object in bpy.context.scene.objects:
        if object.wfc_object.tile_type == 'TILEPREV':
            bpy.data.objects.remove(object, do_unlink=True)


def neighbouringTile():
    tiles = []
    # get the db managment objects
    for object in bpy.context.scene.objects:
        if object.wfc_object.tile_type == 'TILEPREV':
            tiles.append(object)
    print(tiles)
    # check their coordinates and add them to the proper key

    return


def updateDb(self):
    pass
