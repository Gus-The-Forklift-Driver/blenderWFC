import bpy
import sys
import random
from mathutils import *


class tileKey:
    __slots__ = ['name', 'Xplus', 'Xminus',
                 'Yplus', 'Yminus', 'Zplus', 'Zminus']

    def __init__(self, name):
        self.name = name
        self.Xplus = ()
        self.Xminus = ()
        self.Yplus = ()
        self.Yminus = ()
        self.Zplus = ()
        self.Zminus = ()


class waveFunction:
    def __init__(self, database: dict, size: tuple):
        self.database = database
        self.size = size

        self.tilesToUpdate = []

        self.tileList = []
        for keys in database:
            self.tileList.append(str(keys))

        self.cellGrid = []
        for x in range(self.size[0]):
            self.cellGrid.append([])
            for y in range(self.size[1]):
                self.cellGrid[x].append([])
                for z in range(self.size[2]):
                    self.cellGrid[x][y].append(self.tileList.copy())

        self.errors = 0

    def update_cell(self, source: tuple, target: tuple, direction: str):
        availableSource = self.cellGrid[source[0]][source[1]][source[2]]
        availableTarget = self.cellGrid[target[0]][target[1]][target[2]]
        # print(availableSource)
        # print(availableTarget)
        updated = False
        if availableSource == ['error']:
            return False
        if availableTarget == ['error']:
            return False

        possibleTilesList = []
        for targ in availableTarget:
            for possibleTile in self.database[targ][direction]:
                if possibleTile not in possibleTilesList:
                    possibleTilesList.append(possibleTile)

        #print(f'Compairing : {color.RED}{source}{color.END}')
        # print(availableSource)
        #print(f'With : {color.RED}{target}{color.END}')
        # print(possibleTilesList)

        for tileSource in list(availableSource):
            if tileSource not in possibleTilesList:
                #print(f'{color.RED}Removing {tileSource}{color.END}')
                availableSource.remove(tileSource)
                updated = True
        self.cellGrid[source[0]][source[1]][source[2]] = availableSource
        # if no cells can be put next to this one, an error is raised
        if availableSource == []:
            #print(f'{color.REV}{color.RED} EMPTY CELL{color.END}')
            self.cellGrid[source[0]][source[1]][source[2]] = ['error']
            self.errors += 1
        return updated

    def propagate(self):
        location = self.tilesToUpdate[0]
        self.tilesToUpdate.pop(0)

        x = location[0]
        y = location[1]
        z = location[2]

        # print('------------------------------')
        #print(f'{color.YELLOW}Propagating at {x},{y},{z} : {color.END}', end='')

        updated = False

        if len(self.cellGrid[x][y][z]) <= 1:
            #print(f'{color.GREEN}Skipping because entropy is 1 {color.END}')
            return
        else:

            if x != 0:
                if self.update_cell(location, (x-1, y, z), 'x+'):
                    updated = True
            if x != self.size[0] - 1:
                if self.update_cell(location, (x+1, y, z), 'x-'):
                    updated = True
            if y != 0:
                if self.update_cell(location, (x, y-1, z), 'y+'):
                    updated = True
            if y != self.size[1] - 1:
                if self.update_cell(location, (x, y+1, z), 'y-'):
                    updated = True
            if z != 0:
                if self.update_cell(location, (x, y, z-1), 'z+'):
                    updated = True
            if z != self.size[2] - 1:
                if self.update_cell(location, (x, y, z+1), 'z-'):
                    updated = True

            if updated:
                self.update_adjacent(location)
            # print('------------------------------')

    def update_adjacent(self, location: tuple):
        x = location[0]
        y = location[1]
        z = location[2]
        if x != 0:
            if (x-1, y, z) not in self.tilesToUpdate:
                self.tilesToUpdate.append((x-1, y, z))
        if x != self.size[0] - 1:
            if (x+1, y, z) not in self.tilesToUpdate:
                self.tilesToUpdate.append((x+1, y, z))
        if y != 0:
            if (x, y-1, z) not in self.tilesToUpdate:
                self.tilesToUpdate.append((x, y-1, z))
        if y != self.size[1] - 1:
            if (x, y+1, z) not in self.tilesToUpdate:
                self.tilesToUpdate.append((x, y+1, z))
        if z != 0:
            if (x, y, z-1) not in self.tilesToUpdate:
                self.tilesToUpdate.append((x, y, z-1))
        if z != self.size[2] - 1:
            if (x, y, z+1) not in self.tilesToUpdate:
                self.tilesToUpdate.append((x, y, z+1))

    def consolidate_entropy(self):
        maximum = len(self.tileList)
        max = maximum
        lowestsEntropy = []
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                for z in range(self.size[2]):
                    entropy = len(self.cellGrid[x][y][z])
                    if entropy == max:
                        lowestsEntropy.append((x, y, z))
                    elif entropy < max and not entropy == 1:
                        max = entropy
                        lowestEntropy = [(x, y, z)]
        if maximum == max:
            return False
        else:
            return random.choice(lowestEntropy)

    def set_cell(self, cell: tuple, tile: str = -1):
        #print(f'setting cell at {cell} with {tile}')
        if tile == -1:
            a = self.cellGrid[cell[0]][cell[1]][cell[2]]
            #print(f'piking within {a}')
            self.cellGrid[cell[0]][cell[1]][cell[2]] = [a.pop(
                random.randint(0, len(a)-1))]
        else:
            self.cellGrid[cell[0]][cell[1]][cell[2]] = [tile]
        return self.cellGrid[cell[0]][cell[1]][cell[2]]

    def display_status(self, steps: int):
        progress = 0.0
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                for z in range(self.size[2]):
                    tilesLeft = len(
                        self.cellGrid[x][y][z])
                    if tilesLeft == 1:
                        progress += 1.0

        progress = progress / (self.size[0]*self.size[1]*self.size[2])
        progress = f'{round(progress *100,2)}%'
        sys.stdout.write('\u001b[1A')
        sys.stdout.write('\u001b[1000D')
        sys.stdout.write('Progress  |Cells to update|Steps     |Errors\n')
        sys.stdout.write(
            f'{progress:<10}|{len(self.tilesToUpdate):<15}|{steps:<10}|{self.errors:<6}')
        sys.stdout.flush()

    def set_starting_state(self, left: str = -1, right: str = -1, front: str = -1, back: str = -1, top: str = -1, bottom: str = -1):

        if bottom != -1:
            for x in range(self.size[0]):
                for y in range(self.size[1]):
                    self.set_cell((x, y, 0), bottom)
        if top != -1:
            for x in range(self.size[0]):
                for y in range(self.size[1]):
                    self.set_cell((x, y, self.size[2]-1), top)
        if left != -1:
            for z in range(self.size[2]):
                for y in range(self.size[1]):
                    self.set_cell((0, y, z), left)
        if right != -1:
            for z in range(self.size[2]):
                for y in range(self.size[1]):
                    self.set_cell((self.size[0]-1, y, z), right)
        if front != -1:
            for z in range(self.size[2]):
                for x in range(self.size[0]):
                    self.set_cell((x, 0, z), front)
        if back != -1:
            for z in range(self.size[2]):
                for x in range(self.size[0]):
                    self.set_cell((x, self.size[0]-1, z), back)

        pass

    def set_start(self, coordinates: tuple = -1, tile: str = -1):
        if coordinates == -1:
            startX = random.randint(0, self.size[0]-1)
            startY = random.randint(0, self.size[1]-1)
            startZ = random.randint(0, self.size[2]-1)
        else:
            startX = coordinates[0]
            startY = coordinates[1]
            startZ = coordinates[2]

        if tile == -1:
            tile = self.tileList[random.randint(0, len(self.tileList)-1)]

        startingCell = self.set_cell((startX, startY, startZ), tile)
        self.update_adjacent((startX, startY, startZ))
        #print(f'{color.GREEN}Starting at {startX}.{startY}.{startZ} with tile : {str(startingCell)}{color.END}')
