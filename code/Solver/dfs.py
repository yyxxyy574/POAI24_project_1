import time

def hash(game_map):
    map_list = [game_map.player[0], game_map.player[1]]
    if game_map.game_mode == "all":
        sorted_boxes = sorted(game_map.boxes[box] for box in game_map.boxes)
        map_list += [box_pos_xy for box_pos in sorted_boxes for box_pos_xy in box_pos]
    else:
        map_list += [box_pos_xy for box_id in game_map.boxes for box_pos_xy in game_map.boxes[box_id]]
    return ''.join(map(str, map_list))

def dfs_search(game_map):
    map_q = []
    map_q.append(game_map)
    visited_map = set()
    visited_map.add(hash(game_map))
    start_time = time.time()
    while len(map_q) != 0:
        prev_map = map_q.pop()
        if prev_map.is_success():
            return prev_map.move_sequence, time.time() - start_time
        for action in prev_map.valid_moves():
            next_map = prev_map.copy_map()
            next_map.move(action)
            if hash(next_map) not in visited_map:
                visited_map.add(hash(next_map))
                if not next_map.is_fail():
                    map_q.append(next_map)
    return None, None