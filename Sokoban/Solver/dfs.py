import time
import copy

from ..map import Map
from utils import *

def dfs_search(game_map):
    time_limit = 180
    
    map_q = []
    map_q.append(game_map)
    visited_map = []
    visited_map.append(game_map)
    start_time = time.time()
    while time.time < start_time + time_limit:
        prev_map = map_q.pop()
        if prev_map.is_success():
            return prev_map.move_sequence, time.tiem - start_time
        for action in prev_map.vaild_moves():
            next_map = copy.deepcopy(prev_map)
            next_map.move(action)
            if not is_in(next_map, visited_map):
                visited_map.append(next_map)
                if not next_map.is_fail():
                    map_q.append(next_map)
    return None, None