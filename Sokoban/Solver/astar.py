import time
import copy
from queue import PriorityQueue

from ..map import Map
from utils import *

def astar_search(game_map):
    time_limit = 180
    
    map_q = PriorityQueue()
    map_q.put((game_map.cost(), id(game_map), game_map))
    visited_map = []
    visited_map.append(game_map)
    start_time = time.time()
    while time.time < start_time + time_limit:
        prev_map = map_q.get()[2]
        if prev_map.is_success():
            return prev_map.move_sequence, time.tiem - start_time
        for action in prev_map.vaild_moves():
            next_map = copy.deepcopy(prev_map)
            next_map.move(action)
            if not is_in(next_map, visited_map):
                visited_map.append(next_map)
                if not next_map.is_fail():
                    map_q.put((next_map.cost(), id(next_map), next_map))
    return None, None

def astar_test(game_map, time_limit, step_limit):
    map_q = PriorityQueue()
    map_q.put((game_map.cost(), id(game_map), game_map))
    visited_map = []
    visited_map.append(game_map)
    start_time = time.time()
    search_step = 0
    while not map_q.empty():
        if time.time() > start_time + time_limit:
            return 1
        if search_step > step_limit:
            return 2
        prev_map = map_q.get()[2]
        if prev_map.is_success():
            return prev_map.move_sequence
        for action in prev_map.vaild_moves():
            next_map = copy.deepcopy(prev_map)
            next_map.move(action)
            if not is_in(next_map, visited_map):
                visited_map.append(next_map)
                if not next_map.is_fail():
                    map_q.put((next_map.cost(), id(next_map), next_map))
    return 0