import bpy
from mathutils import *
import json
import os
from utils import color, is_mesh_compatible

dir = os.path.dirname(bpy.data.filepath)
class databaseMaker:
    def __init__(self):
        pass

        print(f'{color.BOLD}{color.CYAN}***************************************{color.END}')

        #obj = bpy.data.objects["Cube"]  # particular object by name
    
    def save_database_to_file(self,database,name='database.json'):
        databaseFile = open(f'{dir}\{name}','w')
        databaseFile.write(str(json.dumps(database)))
        databaseFile.close()
    
    def create_database(self,threshold=0.001):
        database = {}
        for object in C.selected_objects:
            if object.type == 'MESH':
                database[object.name] = {}
                database[object.name]['x+'] = []
                database[object.name]['x-'] = []
                database[object.name]['y+'] = []
                database[object.name]['y-'] = []
                database[object.name]['z+'] = []
                database[object.name]['z-'] = []
                for target in C.selected_objects:
                    if target.type == 'MESH':
                        #print(f'Source : {object.name} | Destination : {target.name}')
                        if is_mesh_compatible(object,target,'x+',threshold):
                            #print(f'{color.BOLD}{color.GREEN}{object.name} compatible on the X+ with {target.name}{color.END}')
                            database[object.name]['x+'].append(target.name)
                        if is_mesh_compatible(object,target,'x-',threshold):
                            database[object.name]['x-'].append(target.name)
                        if is_mesh_compatible(object,target,'y+',threshold):
                            database[object.name]['y+'].append(target.name)
                        if is_mesh_compatible(object,target,'y-',threshold):
                            database[object.name]['y-'].append(target.name)
                        if is_mesh_compatible(object,target,'z+',threshold):
                            database[object.name]['z+'].append(target.name)
                        if is_mesh_compatible(object,target,'z-',threshold):
                            database[object.name]['z-'].append(target.name)
        return database

        