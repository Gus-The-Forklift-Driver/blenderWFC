import json
import bpy
import random
import sys
import os
import importlib
from mathutils import *


dir = os.path.dirname(bpy.data.filepath)
sys.path.append(dir)
import utils
import wavefunction

importlib.reload(wavefunction)
importlib.reload(utils)



dir = os.path.dirname(bpy.data.filepath)
sys.path.append(dir)
#sys.path.append(dir)
#importlib.reload(wavefunction)
#importlib.reload(utils)



# todo naming
# todo better status
# todo database stats and result stats

os.system('cls')
print(f'{utils.color.BOLD}{utils.color.REV}{utils.color.CYAN}***************************************')
print(f'{utils.color.BOLD}{utils.color.CYAN}*****************START*****************')
print(f'{utils.color.BOLD}{utils.color.CYAN}***************************************{utils.color.END}')

size = (5, 5, 5)
databaseFile = open(f'{dir}\database.json', 'r')

database = json.loads(databaseFile.read())

wave = wavefunction.waveFunction(database, size)

print(f'\n{utils.color.GREEN}{utils.color.BOLD}--CHOOSING STARTING TILE AND CELL--{utils.color.END}')

# choose a random starting cell
wave.set_starting_state(top='air')
wave.set_start(tile='Plande.008')

print(f'{utils.color.GREEN}{utils.color.BOLD}--COLLAPSING--{utils.color.END}{utils.color.REV}\n')

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
wave.display_status(step)
print(f'\n{utils.color.END}{utils.color.GREEN}{utils.color.BOLD}--CREATING GRID VISUALISATION--{utils.color.END}')
utils.preview_grid(size, wave.cellGrid)
print(f'\n{utils.color.GREEN}{utils.color.BOLD}--CLEANING UP--{utils.color.END}')
utils.cleanup(size)
print('\n')

print(f'{utils.color.BOLD}{utils.color.REV}{utils.color.CYAN}***************************************')
print(f'{utils.color.BOLD}{utils.color.CYAN}******************DONE*****************')
print(f'{utils.color.BOLD}{utils.color.CYAN}***************************************{utils.color.END}')
