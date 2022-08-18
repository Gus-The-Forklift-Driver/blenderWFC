import bpy
from mathutils import *
import json
import os


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


class databaseMaker:
    def __init__(self):
        self.dir = os.path.dirname(bpy.data.filepath)

        # print(f'{color.BOLD}{color.CYAN}***************************************{color.END}')

        # obj = bpy.data.objects["Cube"]  # particular object by name

    def save_database_to_file(self, database, name='database.json'):
        databaseFile = open(f'{self.dir}/{name}', 'w')
        databaseFile.write(str(json.dumps(database)))
        databaseFile.close()
        print(f'saved file to : {self.dir}/{name}')

    def create_database(self, threshold=0.001):
        database = {}
        for object in bpy.context.selected_objects:
            if object.type == 'MESH':
                database[object.name] = {}
                database[object.name]['x+'] = []
                database[object.name]['x-'] = []
                database[object.name]['y+'] = []
                database[object.name]['y-'] = []
                database[object.name]['z+'] = []
                database[object.name]['z-'] = []
                for target in bpy.context.selected_objects:
                    if target.type == 'MESH':
                        #print(f'Source : {object.name} | Destination : {target.name}')
                        if is_mesh_compatible(object, target, 'x+', threshold):
                            #print(f'{color.BOLD}{color.GREEN}{object.name} compatible on the X+ with {target.name}{color.END}')
                            database[object.name]['x+'].append(target.name)
                        if is_mesh_compatible(object, target, 'x-', threshold):
                            database[object.name]['x-'].append(target.name)
                        if is_mesh_compatible(object, target, 'y+', threshold):
                            database[object.name]['y+'].append(target.name)
                        if is_mesh_compatible(object, target, 'y-', threshold):
                            database[object.name]['y-'].append(target.name)
                        if is_mesh_compatible(object, target, 'z+', threshold):
                            database[object.name]['z+'].append(target.name)
                        if is_mesh_compatible(object, target, 'z-', threshold):
                            database[object.name]['z-'].append(target.name)
        return database

    def sortDatabaseKeys(self, database):
        sortedKeys = sorted(database)
        sortedDatabase = {}
        for key in sortedKeys:
            sortedDatabase[key] = database[key]
        return sortedDatabase
