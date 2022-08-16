import bpy
import math
import sys
from mathutils import *
import os


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

# Calculate if two points are overlapping within a given threshold.


def is_overlapping(point1: Vector, point2: Vector, direction: str, threshold=0.001) -> bool:
    point1 = point1.copy()
    point2 = point2.copy()

    if direction == 'x':
        point1.x = 0
        point2.x = 0
    elif direction == 'y':
        point1.y = 0
        point2.y = 0
    elif direction == 'z':
        point1.z = 0
        point2.z = 0
    distance = (point1 - point2).length
    if distance <= threshold:
        # print(f'{point1.x},{point1.y},{point1.z} overlapping with {point2.x},{point2.y},{point2.z}')
        return True
    else:
        return False

# check if the vertices of an object can be connected to another object


def is_mesh_compatible(object1: object, object2: object, direction: str, threshold=0.001) -> bool:
    object1Vertices = []
    object2Vertices = []

    if direction == 'x+':
        for verts in object1.data.vertices:
            if verts.co.x == 1:
                object1Vertices.append(verts.co)
        for verts in object2.data.vertices:
            if verts.co.x == -1:
                object2Vertices.append(verts.co)
        if len(object1Vertices) != len(object2Vertices):
            return False
        elif len(object1Vertices) == 0 and len(object2Vertices) == 0:
            return True

        overlappingVerts = 0
        for source in object1Vertices:
            for target in object2Vertices:
                if is_overlapping(source, target, 'x'):
                    overlappingVerts += 1
        if overlappingVerts == len(object1Vertices) == len(object2Vertices):
            return True
        else:
            return False
    elif direction == 'x-':
        for verts in object1.data.vertices:
            if verts.co.x == -1:
                object1Vertices.append(verts.co)
        for verts in object2.data.vertices:
            if verts.co.x == 1:
                object2Vertices.append(verts.co)
        if len(object1Vertices) != len(object2Vertices):
            return False
        elif len(object1Vertices) == 0 and len(object2Vertices) == 0:
            return True

        overlappingVerts = 0
        for source in object1Vertices:
            for target in object2Vertices:
                if is_overlapping(source, target, 'x'):
                    overlappingVerts += 1
        if overlappingVerts == len(object1Vertices) == len(object2Vertices):
            return True
        else:
            return False
    elif direction == 'y+':
        for verts in object1.data.vertices:
            if verts.co.y == 1:
                object1Vertices.append(verts.co)
        for verts in object2.data.vertices:
            if verts.co.y == -1:
                object2Vertices.append(verts.co)
        if len(object1Vertices) != len(object2Vertices):
            return False
        elif len(object1Vertices) == 0 and len(object2Vertices) == 0:
            return True

        overlappingVerts = 0
        for source in object1Vertices:
            for target in object2Vertices:
                if is_overlapping(source, target, 'y'):
                    overlappingVerts += 1
        if overlappingVerts == len(object1Vertices) == len(object2Vertices):
            return True
        else:
            return False
    elif direction == 'y-':
        for verts in object1.data.vertices:
            if verts.co.y == -1:
                object1Vertices.append(verts.co)
        for verts in object2.data.vertices:
            if verts.co.y == 1:
                object2Vertices.append(verts.co)
        if len(object1Vertices) != len(object2Vertices):
            return False
        elif len(object1Vertices) == 0 and len(object2Vertices) == 0:
            return True

        overlappingVerts = 0
        for source in object1Vertices:
            for target in object2Vertices:
                if is_overlapping(source, target, 'y'):
                    overlappingVerts += 1
        if overlappingVerts == len(object1Vertices) == len(object2Vertices):
            return True
        else:
            return False

    elif direction == 'z+':
        for verts in object1.data.vertices:
            if verts.co.z == 1:
                object1Vertices.append(verts.co)
        for verts in object2.data.vertices:
            if verts.co.z == -1:
                object2Vertices.append(verts.co)
        if len(object1Vertices) != len(object2Vertices):
            return False
        elif len(object1Vertices) == 0 and len(object2Vertices) == 0:
            return True

        overlappingVerts = 0
        for source in object1Vertices:
            for target in object2Vertices:
                if is_overlapping(source, target, 'z'):
                    overlappingVerts += 1
        if overlappingVerts == len(object1Vertices) == len(object2Vertices):
            return True
        else:
            return False
    elif direction == 'z-':
        for verts in object1.data.vertices:
            if verts.co.z == -1:
                object1Vertices.append(verts.co)
        for verts in object2.data.vertices:
            if verts.co.z == 1:
                object2Vertices.append(verts.co)
        if len(object1Vertices) != len(object2Vertices):
            return False
        elif len(object1Vertices) == 0 and len(object2Vertices) == 0:
            return True

        overlappingVerts = 0
        for source in object1Vertices:
            for target in object2Vertices:
                if is_overlapping(source, target, 'z'):
                    overlappingVerts += 1
        if overlappingVerts == len(object1Vertices) == len(object2Vertices):
            return True
        else:
            return False

    else:
        print("An error occurred during mesh compatibility checking")
        return False


def create_text_object(name, coordinates, text):
    font_curve = bpy.data.curves.new(type="FONT", name="Font Curve")
    font_curve.body = text
    font_obj = bpy.data.objects.new(name=name, object_data=font_curve)
    bpy.context.scene.collection.objects.link(font_obj)
    bpy.data.objects[name].location = coordinates


def cleanup(size):
    done = 0
    for x in range(size[0]):
        for y in range(size[1]):
            for z in range(size[2]):
                try:
                    bpy.data.objects[f'{x}.{y}.{z}.mesh'].select_set(True)
                except KeyError:
                    pass
                done += 1
                progress_bar(done, size[0]*size[1]*size[2], 5)

    objs = bpy.context.selected_objects
    coll_target = bpy.context.scene.collection.children.get("Grid")
    # If target found and object list not empty
    if coll_target and objs:

        # Loop through all objects
        for ob in objs:
            # Loop through all collections the obj is linked to
            for coll in ob.users_collection:
                # Unlink the object
                coll.objects.unlink(ob)

            # Link each object to the target collection
            coll_target.objects.link(ob)
        # bpy.data.collections["grid"].objects.link(bpy.data.objects[f'{x}.{y}.{z}.mesh'])


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
                            bpy.ops.object.add_named(name=availableTiles[0])
                        except:
                            print(
                                f'failed to add tile : {availableTiles[0]} at {x}.{y}.{z}')
                        else:
                            bpy.context.active_object.name = f'{x}.{y}.{z}.mesh'
                            bpy.data.objects[f'{x}.{y}.{z}.mesh'].location = (
                                x*2, y*2, z*2)
                else:
                    pass
                    #create_text_object(f'{x}.{y}.{z}.text', (x*2, y*2, z*2), str(len(availableTiles)))
                done += 1
                progress_bar(done, size[0]*size[1]*size[2], 20)


def preview_object(location: tuple, objectName):
    # get the object to duplicate
    obj = bpy.data.objects[objectName]
    # make a copy of it
    duplicate = obj.copy()
    # link it to a collection
    bpy.context.scene.collection.objects.link(duplicate)
    # change location
    duplicate.location = location
    # change name
    duplicate.name = f'prev_{location[0]}.{location[1]}.{location[2]}.{objectName}'


def preview_single_key(database: dict, key):
    preview_object((0, 0, 0), key)
    offset = 1
    for x in database[key]['x+']:
        preview_object((offset*2, 0, 0), x)
        offset = offset + 1
    offset = 1
    for x in database[key]['x-']:
        preview_object((offset*-2, 0, 0), x)
        offset = offset + 1

    offset = 1
    for y in database[key]['y+']:
        preview_object((0, offset*2, 0), y)
        offset = offset + 1
    offset = 1
    for y in database[key]['y-']:
        preview_object((0, offset*-2, 0), y)
        offset = offset + 1

    offset = 1
    for z in database[key]['z+']:
        preview_object((0, 0, offset*2), z)
        offset = offset + 1
    offset = 1
    for z in database[key]['z-']:
        preview_object((0, 0, offset*-2), z)
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
