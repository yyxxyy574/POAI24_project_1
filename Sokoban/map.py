import numpy as np
import copy
import json
import random
import itertools

from Solver.astar import astar_test

class Map:
    def __init__(self, game_mode="all", map_mode=None):
        self.game_mode = game_mode
        self.move_sequence = []
        self.size = (0, 0)
        self.walls = set()
        self.holes = dict()
        self.boxes = dict()
        self.player = (0, 0)
        self.map_matrix = None
        
        # Get map information given game mode and map mode
        if map_mode == "demo":
            size, walls, holes, boxes, player = read_json('.\Maps\map_0.json')
            self.build_from_map_info(size, walls, holes, boxes, player)
        elif map_mode == "library":
            id = random.randint(0, 2)
            size, walls, holes, boxes, player = read_json(f'.\Maps\map_{id}.json')
            self.build_from_map_info(size, walls, holes, boxes, player)
        elif map_mode == "random_slow":
            self.random_build_slow()
        elif map_mode == "random_fast":
            self.random_build_fast()
            
    def print_map(self):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                print(self.map_matrix[i][j], end=' ')
            print()
        print(self.player)           
                
    def build_from_map_info(self, size=(0, 0), walls=set(), holes=dict(), boxes=dict(), player=(0, 0)):
        """
        Build map according to map information
        """
        # Basic information
        self.size = size
        self.walls = walls
        self.holes = holes
        self.boxes = boxes
        self.player = player
        # Set map matrix
        self.map_matrix = np.zeros([self.size[0], self.size[1]])
        for wall in self.walls:
            self.map_matrix[wall[1]][wall[0]] = 1
        for hole in self.holes:
            hole_pos = holes[hole]
            self.map_matrix[hole_pos[1]][hole_pos[0]] = 2
        for box in self.boxes:
            box_pos = boxes[box]
            if self.map_matrix[box_pos[1]][box_pos[0]] == 0:
                self.map_matrix[box_pos[1]][box_pos[0]] = 3
            else:
                self.map_matrix[box_pos[1]][box_pos[0]] = 4 
                
    def is_valid_move(self, action):
        new_player = (self.player[0] + action[0], self.player[1] + action[1])
        if self.map_matrix[new_player[1]][new_player[0]] in (3, 4):
            new_box_pos = (self.player[0] + 2 * action[0], self.player[1] + 2 * action[1])
            return self.map_matrix[new_box_pos[1]][new_box_pos[0]] in (0, 2)
        else:
            return self.map_matrix[new_player[1]][new_player[0]] in (0, 2)
        
    def valid_moves(self):
        available_moves = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        valid_moves = []
        for action in available_moves:
            if self.is_valid_move(action):
                valid_moves.append(action)
        return valid_moves
    
    def move(self, action):
        if not self.is_valid_move(action):
            return False
        self.move_sequence.append(action)
        self.player = (self.player[0] + action[0], self.player[1] + action[1])
        if self.map_matrix[self.player[1]][self.player[0]] in (3, 4):
            box_id = None
            for box in self.boxes:
                if self.boxes[box] == self.player:
                    box_id = box
                    break
            if self.map_matrix[self.player[1]][self.player[0]] == 3:
                self.map_matrix[self.player[1]][self.player[0]] = 0
            else:
                self.map_matrix[self.player[1]][self.player[0]] = 2
            new_box_pos = (self.player[0] + action[0], self.player[1] + action[1])
            if self.map_matrix[new_box_pos[1]][new_box_pos[0]] == 0:
                self.map_matrix[new_box_pos[1]][new_box_pos[0]] = 3
                self.boxes[box_id] = new_box_pos
            else:
                if self.game_mode == "all":
                    self.map_matrix[new_box_pos[1]][new_box_pos[0]] = 4
                    self.boxes[box_id] = new_box_pos
                else:
                    hole_id = None
                    for hole in self.holes:
                        if self.holes[hole] == new_box_pos:
                            hole_id = hole
                            break
                    if box_id == hole_id:
                        self.boxes.pop(box_id)
                    else:
                        self.map_matrix[new_box_pos[1]][new_box_pos[0]] = 4
                        self.boxes[box_id] = new_box_pos
                        
    def cost(self):
        cost = 0
        if self.game_mode == "all":
            sorted_holes_x = sorted(self.holes[hole][0] for hole in self.holes)
            sorted_holes_y = sorted(self.holes[hole][1] for hole in self.holes)
            sorted_boxes_x = sorted(self.boxes[box][0] for box in self.boxes)
            sorted_boxes_y = sorted(self.boxes[box][1] for box in self.boxes)
            for i in range(len(self.boxes)):
                cost += np.abs(sorted_holes_x[i] - sorted_boxes_x[i]) + np.abs(sorted_holes_y[i] - sorted_boxes_y[i])
        else:
            for box in self.boxes:
                cost += np.abs(self.holes[box][0] - self.boxes[box][0]) + np.abs(self.holes[box][1] - self.boxes[box][1])
        return cost
          
    def is_success(self):
        """
        Judge if is success
        """
        empty_boxes = np.where(self.map_matrix == 3)
        if len(empty_boxes[0]) == 0:
            return True
        else:
            return False 
    
    def is_fail(self):
        """
        Judge if is fail
        """
        # 0 for box and 1 for wall
        # 1
        failures_1 = [
            # 1_1
            {(0, -1): 1, (-1, 0): 1},
            # 1_2
            {(1, 0): 1, (0, -1): 1},
            # 1_3
            {(0, 1): 1, (-1, 0): 1},
            # 1_4
            {(1, 0): 1, (0, 1): 1},
        ]
        # 2
        failures_2 = [
            # 2_1
            {(1, 0): 1, (0, 1): 0, (1, 1): 1},
            {(0, -1): 0, (1, -1): 1, (1, 0): 1},
            # 2_2
            {(0, -1): 1, (1, -1): 1, (1, 0): 0},
            {(-1, -1): 1, (0, -1): 1, (-1, 0): 0},
            # 2_3
            {(-1, 0): 1, (-1, 1): 1, (0, 1): 0},
            {(-1, -1): 1, (0, -1): 0, (-1, 0): 1},
            # 2_4
            {(1, 0): 0, (0, 1): 1, (1, 1): 1},
            {(-1, 0): 0, (-1, 1): 1, (0, 1): 1},
        ]
        # 3
        failures_3 = [
            # 3_1_1
            {(-1, 0): 1, (-1, 1): 0, (0, 1): 0},
            {(0, -1): 1, (1, -1): 0, (1, 0): 0},
            {(-1, -1): 1, (0, -1): 0, (-1, 0): 0},
            # 3_1_2
            {(1, 0): 1, (0, 1): 0, (1, 1): 0},
            {(0, -1): 0, (1, -1): 1, (1, 0): 0},
            {(-1, -1): 0, (0, -1): 1, (-1, 0): 0},
            # 3_1_3
            {(1, 0): 0, (0, 1): 1, (1, 1): 0},
            {(-1, 0): 0, (-1, 1): 1, (0, 1): 0},
            {(-1, -1): 0, (0, -1): 0, (-1, 0): 1},
            # 3_1_4
            {(1, 0): 0, (0, 1): 0, (1, 1): 1},
            {(-1, 0): 0, (-1, 1): 0, (0, 1): 1},
            {(0, -1): 0, (1, -1): 0, (1, 0): 1},
            # 3_2_1
            {(1, 0): 1, (-1, 1): 1, (0, 1): 0, (0, 2): 0, (1, 2): 1},
            {(0, -1): 0, (1, -1): 1, (-1, 0): 1, (0, 1): 0, (1, 1): 1},
            {(0, -2): 0, (1, -2): 1, (-1, -1): 1, (0, -1): 0, (1, 0): 1},
            # 3_2_2
            {(-1, 0): 1, (0, 1): 0, (1, 1): 1, (-1, 2): 1, (0, 2): 0},
            {(-1, -1): 1, (0, -1): 0, (1, 0): 1, (-1, 1): 1, (0, 1): 0},
            {(-1, 2): 1, (0, 2): 0, (1, 0): 1, (-1, 1): 1, (0, 1): 0},
            # 3_2_3
            {(0, -1): 1, (2, -1): 1, (1, 0): 0, (2, 0): 0, (1, 1): 1},
            {(-1, -1): 1, (1, -1): 1, (-1, 0): 0, (1, 0): 0, (0, 1): 1},
            {(-2, -1): 1, (0, -1): 1, (-2, 0): 0, (-1, 0): 0, (-1 , 1): 1},
            # 3_2_3
            {(0, 1): 1, (2, 1): 1, (1, 0): 0, (2, 0): 0, (1, -1): 1},
            {(-1, 1): 1, (1, 1): 1, (-1, 0): 0, (1, 0): 0, (0, -1): 1},
            {(-2, 1): 1, (0, 1): 1, (-2, 0): 0, (-1, 0): 0, (-1 , -1): 1},
        ]
        # 4
        failures_4 = [
            {(1, 0): 0, (0, 1): 0, (1, 1): 0},
            {(-1, 0): 0, (-1, 1): 0, (0, 1): 0},
            {(1, 0): 0, (1, -1): 0, (0, -1): 0},
            {(0, -1): 0, (-1, -1): 0, (-1, 0): 0},
        ]
        
        empty_boxes = np.where(self.map_matrix == 3)
        failures = []
        if len(empty_boxes) > 0:
            failures += failures_1
        if len(empty_boxes) > 1:
            failures += failures_2
        if len(empty_boxes) > 2:
            failures += failures_3
        if len(empty_boxes) > 3:
            failures += failures_4
        for i in range(len(empty_boxes[0])):
            empty_box_pos = (empty_boxes[1][i], empty_boxes[0][i])
            is_fail = False
            for failure in failures:
                is_same = True
                for surround in failure:
                    if failure[surround] == 0:
                        if self.map_matrix[empty_box_pos[1] + surround[1]][empty_box_pos[0] + surround[0]] not in (3, 4):
                            is_same = False
                            break
                    else:
                        if self.map_matrix[empty_box_pos[1] + surround[1]][empty_box_pos[0] + surround[0]] != 1:
                            is_same = False
                            break
                if is_same:
                    # If it is the same as one of the fail situations, then fail
                    is_fail = True
                    break
            if is_fail:
                return True
        return False
    
    def random_initialize(self):
        """
        Initialize a map randomly
        """
        # Random size
        self.size = (random.randint(8, 12), random.randint(8, 12))
        # Random number of boxes
        box_num = random.randint(1, 4)
        
        # Initial a map
        self.map_matrix = np.zeros(self.size)
        # Surrounded by walls
        self.map_matrix[0, :] = 1
        self.walls.add(wall for wall in list(itertools.product(list(range(0, self.size[1])), [0])))
        self.map_matrix[:, 0] = 1
        self.walls.add(wall for wall in list(itertools.product([0], list(range(0, self.size[0])))))
        self.map_matrix[-1, :] = 1
        self.walls.add(wall for wall in list(itertools.product(list(range(0, self.size[1])), [self.size[0] - 1])))
        self.map_matrix[:, -1] = 1
        self.walls.add(wall for wall in list(itertools.product([self.size[1] - 1], list(range(0, self.size[0])))))
        # Random walls
        not_occupied = list(itertools.product(list(range(1, self.size[1] - 1)), list(range(1, self.size[0] - 1))))
        for wall in random.sample(not_occupied, (self.size[0] + self.size[1]) // 2):
            self.map_matrix[wall[1]][wall[0]] = 1
            self.walls.add(wall)
        not_occupied = list(set(not_occupied) - self.walls)
        # Random holes
        for i in range(box_num):
            while True:
                hole = random.choice(not_occupied)
                
                if not is_surrounded(self.map_matrix, hole):
                    # If not surrounded by walls
                    self.map_matrix[hole[1]][hole[0]] = 2
                    self.holes[chr(65 + i)] = hole
                    not_occupied -= {hole}
                    break
        # Random boxes
        for i in range(box_num):
            while True:
                box = random.choice(not_occupied)
                
                if not is_surrounded(self.map_matrix, box):
                    # If not surrounded by walls
                    if (self.game_mode == "one") and (self.holes[chr(65 + i)] == box):
                        # If in "one" mode the box is just at the position of the correspondent hole
                        continue
                    if self.map_matrix[box[1]][box[0]] == 2:
                        # If there is a hole
                        self.map_matrix[box[1]][box[0]] = 4
                    else:
                        # If there isn't a hole
                        self.map_matrix[box[1]][box[0]] = 3
                    
                    if self.is_fail():
                        # If this map is dead, then recover
                        if self.map_matrix[box[1]][box[0]] == 4:
                            self.map_matrix[box[1]][box[0]] = 2
                        else:
                            self.map_matrix[box[1]][box[0]] = 0
                    else:
                        # If this map is OK, then go on
                        self.boxes[chr(65 + i)] = box
                        not_occupied -= {box}
                        break
        not_occupied = list(set(not_occupied) - set(self.boxes.values()))
        # Random player position
        while True:
            self.player = random.choice(not_occupied)
            
            if not is_surrounded(self.map_matrix, self.player):
                break
    
    def random_build_fast(self, time_limit=30, step_limit=100):
        """
        Build a map randomly
        """
        # Initialize an easy map
        while True:
            self.random_initialize()
            result = astar_test(self.copy_map(), 10, 150)
            if not result in range(3):
                break
            
        # Add walls randomly to make the map more difficult
        traceback = 0
        while True:
            open_places = np.where(self.map_matrix == 0)
            if len(open_places[0]) == 0:
                break
            
            while True:
                id = random.randint(0, len(open_places[0]) - 1)
                if (open_places[1][id] != self.player[0]) or (open_places[0][id] != self.player[1]):
                    self.map_matrix[open_places[0][id]][open_places[1][id]] = 1
                    if not(self.is_fail()):
                        break
                    self.map_matrix[open_places[0][id]][open_places[1][id]] = 0
            result = astar_test(self.copy_map(), time_limit, step_limit)
            if result == 0:
                # If no solution, return to previous map
                traceback += 1
                self.map_matrix[open_places[0][id]][open_places[1][id]] = 0
                if traceback > 3:
                    break
            elif result == 1:
                # If it is beyond time, add this wall
                self.walls.add((open_places[0][id], open_places[1][id]))
                break
            elif result == 2:
                # If it is beyond step, keep current map
                self.walls.add((open_places[0][id], open_places[1][id]))
                continue
            
    def random_build_slow(self, time_limit=30, step_limit=100):
        """
        Build a map randomly
        """
        # Initialize an easy map
        while True:
            self.random_initialize()
            result = astar_test(self.copy_map(), 20, 200)
            if not result in range(3):
                break
        
        # Add walls randomly to make the map more difficult
        traceback = 0
        while True:
            open_places = np.where(self.map_matrix == 0)
            if len(open_places[0]) == 0:
                break
            
            while True:
                id = random.randint(0, len(open_places[0]) - 1)
                if (open_places[1][id] != self.player[0]) or (open_places[0][id] != self.player[1]):
                    self.map_matrix[open_places[0][id]][open_places[1][id]] = 1
                    if not(self.is_fail()):
                        break
                    self.map_matrix[open_places[0][id]][open_places[1][id]] = 0
            result = astar_test(self.copy_map(), time_limit, step_limit)
            if result == 0:
                # If no solution, return to previous map
                traceback += 1
                self.map_matrix[open_places[0][id]][open_places[1][id]] = 0
                if traceback > 3:
                    break
            elif result == 1:
                # If it is beyond time, add this wall
                self.walls.add((open_places[0][id], open_places[1][id]))
                break
            elif result == 2:
                # If it is beyond step, keep current map
                self.walls.add((open_places[0][id], open_places[1][id]))
                continue

    def copy_map(self):
        copied_map = Map(game_mode=self.game_mode)
        copied_map.size = copy.deepcopy(self.size)
        for wall in self.walls:
            copied_map.walls.add(wall)
        copied_map.holes = copy.deepcopy(self.holes)
        copied_map.boxes = copy.deepcopy(self.boxes)
        copied_map.player = copy.deepcopy(self.player)
        copied_map.map_matrix = copy.deepcopy(self.map_matrix)
        copied_map.move_sequence = copy.deepcopy(self.move_sequence)
        return copied_map
         
def read_json(path):
    """
    Read map information from a json file
    """
    walls = set()
    holes = dict()
    boxes = dict()
    with open(path, 'r') as f:
        map_info = json.load(f)
        size = (map_info["size"][0], map_info["size"][1])
        walls_info = map_info["walls"]
        for wall_pos in walls_info:
            walls.add((wall_pos[1], wall_pos[0]))
        holes_info = map_info["holes"]
        for hole_id in holes_info:
            holes[hole_id] = (holes_info[hole_id][1], holes_info[hole_id][0])
        boxes_info = map_info["boxes"]
        for box_id in boxes_info:
            boxes[box_id] = (boxes_info[box_id][1], boxes_info[box_id][0])
        player = (map_info["player"][1], map_info["player"][0])
    return size, walls, holes, boxes, player

def is_valid_pos(map_matrix, pos):
    row = len(map_matrix)
    col = len(map_matrix[0])
    return (0 <= pos[0] < col) and (0 <= pos[1] < row)

def is_surrounded(map_matrix, pos):
    # Up, left, down and right
    surrounds = [(0, -1), (-1, 0), (0, 1), (1, 0)]
    
    surrounded = True
    for surround in surrounds:
        if is_valid_pos(map_matrix, (pos[0] + surround[0], pos[1] + surround[1])):
            if map_matrix[pos[1] + surround[1]][pos[0] + surround[0]] in (0, 2):
                surrounded = False
    return surrounded