import numpy as np
from copy import deepcopy
import json
import random
import itertools

from Solver.astar import *

class Map:
    def __init__(self, game_mode="all", map_mode=None, map_matrix=None, player_pos=(0, 0)):
        # Get map information given game mode and map mode
        if map_mode == "demo":
            map_matrix, player_pos = Map.read_json('.\Maps\map_0.json')
        if map_mode == "library":
            id = random.randint(0, 3)
            map_matrix, player_pos = Map.read_json(f'.\Maps\map_{id}.json')
        if map_mode == "random":
            map_matrix, player_pos = Map.random_build(game_mode=game_mode)
        # Build map according to map information
        self.map_matrix = map_matrix
        self.row = len(map_matrix)
        self.col = len(map_matrix[0])
        self.palyer_x = player_pos[0]
        self.palyer_y = player_pos[1]
        self.game_mode = game_mode
        self.timeline = []
        
    def is_dead(self):
        if self.mode == "all":
            empty_boxes = np.where(self.map_matrix in range(2, 6))
        else:
            
    
    def is_success(self):
        empty_boxes = np.where(self.map_matrix in range(2, 6))
        if len(empty_boxes[0]) == 0:
            return True
        else:
            return False
         
def read_json(path):
    """
    Read map information from a json file
    """
    with open(path, 'r') as f:
        map_info = json.load(f)
        map_matrix = map_info["matrix"]
        player_pos = map_info["player_pos"]
    return map_matrix, player_pos

def is_surrounded(map_matrix, pos):
    # Up, down, left and right
    surrounds = [(0, 1), (0, -1), (-1, 0), (1, 0)]
    
    row = len(map_matrix)
    col = len(map_matrix[0])
    surrounded = True
    for surround in surrounds:
        if (0 <= pos[0] + surround[0] < col) and (0 <= pos[1] + surround[1] < row):
            if (map_matrix[pos[0] + surround[0]][pos[1] + surround[1]] == 0) or (map_matrix[pos[0] + surround[0]][pos[1] + surround[1]] in range(10, 14)):
                surrounded = False
    return surrounded

def random_initialize():
    """
    Initialize a map randomly
    """
    # Random size
    size = random.randint(8, 12)
    # Random number of boxes
    box_num = random.randint(1, 4)
    
    # Initial a map
    map_matrix = np.zeros((size, size))
    # Surrounded by walls
    map_matrix[0, :] = 1
    map_matrix[:, 0] = 1
    map_matrix[-1, :] = 1
    map_matrix[:, -1] = 1
    # Random walls
    no_walls = list(itertools.product(list(range(1, size - 1)), list(range(1, size - 1))))
    for wall in random.sample(no_walls, size):
        map_matrix[wall[0]][wall[1]] = 1
    # Random holes
    for i in range(box_num):
        while True:
            hole = random.choice(no_walls)
            
            if (map_matrix[hole[0]][hole[1]] != 1) and (not is_surrounded(map_matrix, hole)):
                # If not surrounded by walls
                map_matrix[box[0]][box[1]] = 10 + i
                break
    # Random boxes
    for i in range(box_num):
        while True:
            box = random.choice(no_walls)
            
            # If there is a wall, continue
            if map_matrix[box[0]][box[1]] == 1:
                continue
            
            original_value = map_matrix[box[0]][box[1]]
            if map_matrix[box[0]][box[1]] in range(65, 65 + box_num):
                # If there is a hole
                map_matrix[box[0]][box[1]] = 6 + i
            else:
                # If there isn't a hole
                map_matrix[box[0]][box[1]] = 2 + i
                
            if Map(map_matrix=map_matrix).is_dead():
                # If this map is dead, then recover
                map_matrix[box[0]][box[1]] = original_value
            else:
                # If this map is OK, then go on
                break
    # Random player position
    while True:
        player_pos = random.choice(no_walls)
        
        if (map_matrix[hole[0]][hole[1]] != 1)  and (map_matrix[hole[0]][hole[1]] not in range(2, 10)) and (not is_surrounded(map_matrix, player_pos)):
            break
        
    return map_matrix, player_pos
        
def random_build(game_mode="all", timelimit=20, steplimit=100):
    """
    Build a map randomly
    """
    # Initialize an easy map
    while True:
        map_matrix, player_pos = random_initialize()
        map = Map(game_mode=game_mode, map_matrix=map_matrix, player_pos=player_pos)
        result = astar_test(map, timelimit, steplimit)
        if not result in range(3):
            break
      
    # Add walls randomly to make the map more difficult
    traceback = 0
    while True:
        available_walls = np.where(map_matrix == 0)
        if len(available_walls[0]) == 0:
            break
        
        while True:
            id = random.randint(0, len(available_walls[0]) - 1)
            if (available_walls[0][id] != player_pos[0]) and (available_walls[1][id] != player_pos[1]):
                break
        new_map_matrix = deepcopy(map_matrix)
        new_map_matrix[available_walls[0][id]][available_walls[1][id]] = 1
        
        map = Map(game_mode=game_mode, map_matrix=new_map_matrix, player_pos=player_pos)
        result = astart_test(map, timelimit, steplimit)
        if result == 0:
            # If no solution, return to previous map
            traceback += 1
            if traceback > 3:
                break
        elif result == 1:
            # If it is beyond time, add this wall
            continue
        elif result == 2:
            # If it is beyond step, keep current map
            break
        else:
            map_matrix[available_walls[0][id]][available_walls[1][id]] = 1
            
    return map_matrix, player_pos