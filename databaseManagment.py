from operator import truediv
import bpy
import sys

# Db is short for database


currentEditedTile = ''


def enableDbManagment():
    print('enabling database managment')
    for object in bpy.context.scene.objects:
        object.hide_viewport = True


def disableDbManagment():
    print('disabling database managment')
    for object in bpy.context.scene.objects:
        object.hide_viewport = False


def displayTile(tileToDisplay: str):
    pass


def updateTile(tileToUpdate: str):
    pass


def updateDb(self):
    pass
