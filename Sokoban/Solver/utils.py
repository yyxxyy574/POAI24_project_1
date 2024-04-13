def is_in(current_map, map_q):
    for map in map_q:
        if (current_map.player == map.player) and (current_map.map_matrix == map.map_matrix):
            return True
    return False