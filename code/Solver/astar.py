import time
from queue import PriorityQueue

class PriorityMap():
    def __init__(self, priority, map):
        self.priority = priority
        self.map = map
    def __lt__(self, other):
        return self.priority < other.priority

def hash(game_map):
    map_list = [game_map.player[0], game_map.player[1]]
    if game_map.game_mode == "all":
        sorted_boxes = sorted(game_map.boxes[box] for box in game_map.boxes)
        map_list += [box_pos_xy for box_pos in sorted_boxes for box_pos_xy in box_pos]
    else:
        map_list += [box_pos_xy for box_id in game_map.boxes for box_pos_xy in game_map.boxes[box_id]]
    return ''.join(map(str, map_list))

def astar_search(game_map):
    map_q = PriorityQueue()
    map_q.put(PriorityMap(0, game_map))
    visited_map = set()
    visited_map.add(hash(game_map))
    start_time = time.time()
    while not map_q.empty():
        prev_map = map_q.get().map
        if prev_map.is_success():
            return prev_map.move_sequence, time.time() - start_time
        for action in prev_map.valid_moves():
            next_map = prev_map.copy_map()
            next_map.move(action)
            if hash(next_map) not in visited_map:
                visited_map.add(hash(next_map))
                if not next_map.is_fail():
                    map_q.put(PriorityMap(len(next_map.move_sequence) + next_map.cost(), next_map))
    return None, None

def astar_test(game_map, time_limit, step_limit):
    map_q = PriorityQueue()
    map_q.put(PriorityMap(0, game_map))
    visited_map = set()
    visited_map.add(hash(game_map))
    start_time = time.time()
    while not map_q.empty():
        if time.time() > start_time + time_limit:
            return 1
        prev_map = map_q.get().map
        if len(prev_map.move_sequence) > step_limit:
            return 2
        if prev_map.is_success():
            return prev_map.move_sequence
        for action in prev_map.valid_moves():
            next_map = prev_map.copy_map()
            next_map.move(action)
            if hash(next_map) not in visited_map:
                visited_map.add(hash(next_map))
                if not next_map.is_fail():
                    map_q.put(PriorityMap(len(next_map.move_sequence) + next_map.cost(), next_map))
    return 0