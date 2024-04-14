import time

def is_in(current_map, map_q):
    for map in map_q:
        if (current_map.player == map.player) and ((current_map.map_matrix == map.map_matrix).all()):
            return True
    return False

def dfs_search(game_map):
    time_limit = 180
    
    map_q = []
    map_q.append(game_map)
    visited_map = []
    visited_map.append(game_map)
    start_time = time.time()
    while len(map_q) != 0:
        prev_map = map_q.pop()
        if prev_map.is_success():
            return prev_map.move_sequence, time.time() - start_time
        for action in prev_map.valid_moves():
            next_map = prev_map.copy_map()
            next_map.move(action)
            if not is_in(next_map, visited_map):
                visited_map.append(next_map)
                if not next_map.is_fail():
                    map_q.append(next_map)
    return None, None