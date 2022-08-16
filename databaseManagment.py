from operator import truediv
import bpy
import json
import os
from . import utils

# Db is short for database


currentEditedTile = ''


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
        object.hide_viewport = True


def disableDbManagment():
    print('disabling database managment')
    for object in bpy.context.scene.objects:
        object.hide_viewport = False


def displayTile(tileToDisplay: str = 'Cube.027'):
    database
    utils.preview_object((0, 0, 0), tileToDisplay)
    offset = 1
    for x in database[tileToDisplay]['x+']:
        utils.preview_object((offset*2, 0, 0), x)
        offset = offset + 1
    offset = 1
    for x in database[tileToDisplay]['x-']:
        utils.preview_object((offset*-2, 0, 0), x)
        offset = offset + 1

    offset = 1
    for y in database[tileToDisplay]['y+']:
        utils.preview_object((0, offset*2, 0), y)
        offset = offset + 1
    offset = 1
    for y in database[tileToDisplay]['y-']:
        utils.preview_object((0, offset*-2, 0), y)
        offset = offset + 1

    offset = 1
    for z in database[tileToDisplay]['z+']:
        utils.preview_object((0, 0, offset*2), z)
        offset = offset + 1
    offset = 1
    for z in database[tileToDisplay]['z-']:
        utils.preview_object((0, 0, offset*-2), z)
        offset = offset + 1


def updateTile(tileToUpdate: str):
    pass


def updateDb(self):
    pass
