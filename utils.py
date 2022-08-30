import bpy
import sys
from mathutils import *
import os
import json


class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    REV = '\u001b[7m'
    END = '\033[0m'


def progress_bar(progress: int, max: int, step: int):
    if progress % step == 0:
        progress = progress / max * 100
        width = int((progress + 1) / 4)
        bar = "[" + "#" * width + " " * (25 - width) + "]"
        progress = f'{round(progress,2)}%'

        sys.stdout.write('\u001b[1000D')
        sys.stdout.write(f'{bar}{progress}')
        sys.stdout.flush()


def create_text_object(name, coordinates, text):
    font_curve = bpy.data.curves.new(type="FONT", name="Font Curve")
    font_curve.body = text
    font_obj = bpy.data.objects.new(name=name, object_data=font_curve)
    bpy.context.scene.collection.objects.link(font_obj)
    bpy.data.objects[name].location = coordinates


def preview_grid(size: tuple, cellGrid: list):
    done = 0
    print('\n')
    for x in range(size[0]):
        for y in range(size[1]):
            for z in range(size[2]):
                availableTiles = cellGrid[x][y][z]
                if len(availableTiles) == 1:
                    if availableTiles[0] == 'error':
                        pass
                    else:
                        try:
                            duplicate_object(
                                (x*2, y*2, z*2), availableTiles[0], 'wfc_')
                        except:
                            print(
                                f'failed to add tile : {availableTiles[0]} at {x}.{y}.{z}')
                else:
                    pass
                    #create_text_object(f'{x}.{y}.{z}.text', (x*2, y*2, z*2), str(len(availableTiles)))
                done += 1
                progress_bar(done, size[0]*size[1]*size[2], 20)


def duplicate_object(location: tuple, objectName, prefix='prev_', tile_type=''):
    # get the object to duplicate
    obj = bpy.data.objects[objectName]
    # make a copy of it
    duplicate = obj.copy()
    # link it to a collection

    # change location
    duplicate.location = location
    # change name
    duplicate.name = f'{prefix}{objectName}'
    # display it (only useful in db managment mode)
    duplicate.hide_viewport = False
    duplicate.wfc_object.tile_type = tile_type
    if tile_type == 'TILEPREV':
        duplicate.wfc_object.tile_name = objectName
    # link it to a collection
    bpy.context.scene.collection.objects.link(duplicate)


def preview_single_key(database: dict, key):
    duplicate_object((0, 0, 0), key)
    offset = 1
    for x in database[key]['x+']:
        duplicate_object((offset*2, 0, 0), x)
        offset = offset + 1
    offset = 1
    for x in database[key]['x-']:
        duplicate_object((offset*-2, 0, 0), x)
        offset = offset + 1

    offset = 1
    for y in database[key]['y+']:
        duplicate_object((0, offset*2, 0), y)
        offset = offset + 1
    offset = 1
    for y in database[key]['y-']:
        duplicate_object((0, offset*-2, 0), y)
        offset = offset + 1

    offset = 1
    for z in database[key]['z+']:
        duplicate_object((0, 0, offset*2), z)
        offset = offset + 1
    offset = 1
    for z in database[key]['z-']:
        duplicate_object((0, 0, offset*-2), z)
        offset = offset + 1


def render_step(step, size, cellGrid):
    dir = os.path.dirname(bpy.data.filepath)
    preview_grid(size, cellGrid)
    bpy.context.scene.render.filepath = f'{dir}/img_{step}.png'
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.ops.render.render(write_still=True)
    for x in range(size[0]):
        for y in range(size[1]):
            for z in range(size[2]):
                try:
                    bpy.data.objects.remove(
                        bpy.data.objects[f'{x}.{y}.{z}.mesh'], do_unlink=True)
                except:
                    pass


def clean_meshes(decimalLenght: int = 2):
    if bpy.context.selected_objects == []:
        objects = bpy.context.scene.objects
    else:
        objects = bpy.context.selected_objects

    for object in objects:
        if object.type == 'MESH':
            for verts in object.data.vertices:
                verts.co.x = round(verts.co.x, decimalLenght)
                verts.co.y = round(verts.co.y, decimalLenght)
                verts.co.z = round(verts.co.z, decimalLenght)


def load_database():
    return


def save_database(database, name='database.json'):
    dir = os.path.dirname(bpy.data.filepath)
    databaseFile = open(f'{dir}/{name}', 'w')
    databaseFile.write(str(json.dumps(database)))
    databaseFile.close()
    print(f'saved file to : {dir}/{name}')
