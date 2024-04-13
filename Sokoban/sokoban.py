from threading import Thread
import os
import pygame
import copy

from map import Map
from Solver.astar import *
from Solver.bfs import *
from Solver.dfs import *

# Load common icon
# Assets folder poistion, modify if you move the program
ASSETS_FOLDER = '.\Assets'
# Image for inco
icon = pygame.image.load(os.path.join(ASSETS_FOLDER, "icon.png"))

animPtr = 0

clock = pygame.time.Clock()

def StartMenu():
    """
    Set the start menu of sokoban
    """
    end = False
    pygame.init()
    # Set screen size, caption and icon
    screen = pygame.display.set_mode((416, 416))
    screen.fill((53, 73, 94))
    pygame.display.set_caption("Sokoban")
    pygame.display.set_icon(icon)
    
    while not end:
        # Set frame rate
        clock.tick(24)
        # Set the main interface
        screen.blit(pygame.transform.scale(icon, (80, 80)), (168, 10))
        font_title = pygame.font.SysFont('Cascadia mono', 64)
        font_choice = pygame.font.SysFont('Cascadia mono', 32)
        title = font_title.render('Sokoban', True, (0, 255, 125), (53, 73, 94))
        screen.blit(title, (120, 100))
        start_game = font_choice.render('Start Game', True, (40, 255, 40), (53, 73, 94))
        screen.blit(start_game, (150, 200))
        instructions = font_choice.render('Instructions', True, (40, 255, 40), (53, 73, 94))
        screen.blit(instructions, (148, 250))
        
        # React according to the user behavior
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                # If the user click the "Start Game" button
                if 150 <= mouse[0] <= 270 and 200 <= mouse[1] <= 232:
                    SelectModeMenu()
                    end = True
                # If the user click the "Instructions" button
                if 148 <= mouse[0] <= 272 and 250 <= mouse[1] <= 282:
                    InstructionsMenu()
                    end = True
                    
        pygame.display.update()
        
def InstructionsMenu():
    """
    Set the game instructions menu for sokoban
    """
    end = False
    pygame.init()
    # Set screen size, caption and icon
    screen = pygame.display.set_mode((416, 416))
    screen.fill((53, 73, 94))
    pygame.display.set_caption("Sokoban")
    pygame.display.set_icon(icon)
    
    while not end:
        # Set frame rate
        clock.tick(24)
        # Set the main interface
        screen.blit(pygame.transform.scale(icon, (80, 80)), (168, 10))
        font_title = pygame.font.SysFont('Cascadia mono', 64)
        font_choice = pygame.font.SysFont('Cascadia mono', 32)
        title = font_title.render('Sokoban', True, (0, 255, 125), (53, 73, 94))
        screen.blit(title, (120, 100))
        return_prev = font_choice.render('Return', True, (40, 255, 40), (53, 73, 94))
        screen.blit(return_prev, (170, 350))
        
        # React according to the user behavior
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                # If the user click the "Return" button
                if 170 <= mouse[0] <= 240 and 350 <= mouse[1] <= 382:
                    StartMenu()
                    end = True
                    
        pygame.display.update()
        
def SelectModeMenu():
    """
    Set the mode selection menu for sokoban
    """
    end = False
    pygame.init()
    # Set screen size, caption and icon
    screen = pygame.display.set_mode((416, 416))
    screen.fill((53, 73, 94))
    pygame.display.set_caption("Sokoban")
    pygame.display.set_icon(icon)
    
    while not end:
        # Set frame rate
        clock.tick(24)
        # Set the main interface
        screen.blit(pygame.transform.scale(icon, (80, 80)), (168, 10))
        font_title = pygame.font.SysFont('Cascadia mono', 64)
        font_choice = pygame.font.SysFont('Cascadia mono', 32)
        title = font_title.render('Sokoban', True, (0, 255, 125), (53, 73, 94))
        screen.blit(title, (120, 100))
        all = font_choice.render('All Is OK', True, (40, 255, 40), (53, 73, 94))
        screen.blit(all, (165, 200))
        one = font_choice.render('One To One', True, (40, 255, 40), (53, 73, 94))
        screen.blit(one, (148, 250))
        return_prev = font_choice.render('Return', True, (40, 255, 40), (53, 73, 94))
        screen.blit(return_prev, (170, 350))
        
        # React according to the user behavior
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                # If the user click the "All Is OK" button
                if 165 <= mouse[0] <= 260 and 200 <= mouse[1] <= 232:
                    SelectMapMenu(game_mode="all")
                    end = True
                # If the user click the "One To One" button
                if 148 <= mouse[0] <= 272 and 250 <= mouse[1] <= 282:
                    SelectMapMenu(game_mode="one")
                    end = True
                # If the user click the "Return" button
                if 170 <= mouse[0] <= 240 and 350 <= mouse[1] <= 382:
                    StartMenu()
                    end = True
                    
        pygame.display.update()
        
        
def SelectMapMenu(game_mode):
    """
    Set the map mode selection menu for sokoban
    """
    end = False
    pygame.init()
    # Set screen size, caption and icon
    screen = pygame.display.set_mode((416, 416))
    screen.fill((53, 73, 94))
    pygame.display.set_caption("Sokoban")
    pygame.display.set_icon(icon)
    
    while not end:
        # Set frame rate
        clock.tick(24)
        # Set the main interface
        screen.blit(pygame.transform.scale(icon, (80, 80)), (168, 10))
        font_title = pygame.font.SysFont('Cascadia mono', 64)
        font_choice = pygame.font.SysFont('Cascadia mono', 32)
        title = font_title.render('Sokoban', True, (0, 255, 125), (53, 73, 94))
        screen.blit(title, (120, 100))
        demo = font_choice.render('Demo', True, (40, 255, 40), (53, 73, 94))
        screen.blit(demo, (180, 200))
        library = font_choice.render('Library', True, (40, 255, 40), (53, 73, 94))
        screen.blit(library, (175, 250))
        random = font_choice.render('Random', True, (40, 255, 40), (53, 73, 94))
        screen.blit(random, (168, 300))
        return_prev = font_choice.render('Return', True, (40, 255, 40), (53, 73, 94))
        screen.blit(return_prev, (170, 350))
        
        # React according to the user behavior
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                # If the user click the "Demo" button
                if 180 <= mouse[0] <= 240 and 200 <= mouse[1] <= 232:
                    GamePlayMenu(game_mode=game_mode, map_mode="demo")
                    end = True
                # If the user click the "Library" button
                if 175 <= mouse[0] <= 255 and 250 <= mouse[1] <= 282:
                    GamePlayMenu(game_mode=game_mode, map_mode="library")
                    end = True
                # If the user click the "Random" button
                if 168 <= mouse[0] <= 243 and 300 <= mouse[1] <= 332:
                    GamePlayMenu(game_mode=game_mode, map_mode="random")
                    end = True
                # If the user click the "Return" button
                if 170 <= mouse[0] <= 240 and 350 <= mouse[1] <= 382:
                    SelectModeMenu()
                    end = True
                    
        pygame.display.update()
        
def GamePlayMenu(game_mode, map_mode):
    """
    Set the game playing menu for sokoban
    """
    # Load sound effects for different kinds of actions
    push = pygame.mixer.Sound(os.path.join(ASSETS_FOLDER, "push.wav"))
    footstep = pygame.mixer.Sound(os.path.join(ASSETS_FOLDER, "footstep.wav"))
    metal = pygame.mixer.Sound(os.path.join(ASSETS_FOLDER, "metal.wav"))
    
    end = False
    buffer = 0
    search_time = None
    pygame.init()
    pygame.mixer.init()
    # Set screen size, caption and icon
    screen = pygame.display.set_mode((416, 416))
    pygame.display.set_caption("Sokoban")
    pygame.display.set_icon(icon)
    # Set map and search button
    initial_game_map = Map(game_mode=game_mode, map_mode=map_mode)
    current_game_map = copy.deepcopy(initial_game_map)
    
    while not end:
        # Set frame rate
        clock.tick(24)
        
        # React according to the user behavior
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                    if event.key == pygame.K_UP:
                        action = (0, -1)
                    elif event.key == pygame.K_DOWN:
                        action = (0, 1)
                    elif event.key == pygame.K_LEFT:
                        action = (-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        action = (1, 0)
                    if current_game_map.is_vaild_move(action):
                        if current_game_map.map_matrix[current_game_map.player[1] + action[1]][current_game_map.player[0] + action[0]] == 0:
                            pygame.mixer.Sound.play(footstep)
                            pygame.mixer.music.stop()
                        elif current_game_map.map_matrix[current_game_map.player[1] + action[1]][current_game_map.player[0] + action[0]] == 2:
                            pygame.mixer.Sound.play(metal)
                            pygame.mixer.music.stop()
                        elif current_game_map.map_matrix[current_game_map.player[1] + action[1]][current_game_map.player[0] + action[0]] in (3, 4):
                            pygame.mixer.Sound.play(push)
                            pygame.mixer.music.stop()
                        current_game_map.move(action)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                # If the user click the "bfs" button
                if 45.5 <= mouse[0] <= 123.5 and 360 <= mouse[1] <= 393:
                    bfs_game_map = copy.deepcopy(initial_game_map)
                    solution, search_time = bfs_search(bfs_game_map)
                # If the user click the "astar" button
                if 169 <= mouse[0] <= 247 and 360 <= mouse[1] <= 393:
                    astar_game_map = copy.deepcopy(initial_game_map)
                    solution, search_time = astar_search(astar_game_map)
                # If the user click the "dfs" button
                if 292.5 <= mouse[0] <= 370.5 and 360 <= mouse[1] <= 393:
                    dfs_game_map = copy.deepcopy(initial_game_map)
                    solution, search_time = dfs_search(dfs_game_map)
                if solution:
                    current_game_map = copy.deepcopy(initial_game_map)
                    t = Thread(target=auto_move, args=(screen, current_game_map, solution))
                    t.start()
                    t.join()
                else:
                    FailMenu()
                    end = True
            if current_game_map.is_success():
                SuccessMenu(len(current_game_map.move_sequence), search_time)
                end = True
            if current_game_map.is_fail():
                FailMenu()
                end = True
                
        screen.fill((53, 73, 94))
        buffer += 1
        if not (buffer % 4):
            animPtr += 1
        draw_map(screen, current_game_map)
        pygame.display.update()
        
def SuccessMenu(step, time=None):
    """
    Set the success menu for sokoban
    """
    # Load image for success
    # Image for solve
    solve = pygame.image.load(os.path.join(ASSETS_FOLDER, "solve.png"))
    
    end = False
    pygame.init()
    # Set screen size, caption and icon
    screen = pygame.display.set_mode((416, 416))
    screen.fill((53, 73, 94))
    pygame.display.set_caption("Sokoban")
    pygame.display.set_icon(icon)
    
    while not end:
        # Set frame rate
        clock.tick(24)
        # Set the main interface
        screen.blit(pygame.transform.scale(solve, (80, 80)), (168, 10))
        font_choice = pygame.font.SysFont('Cascadia mono', 32)
        step = font_choice.render(f'{step} step', True, (40, 255, 40), (53, 73, 94))
        screen.blit(step, (160, 200))
        if time:
            time = font_choice.render(f'{time} s', True, (40, 255, 40), (53, 73, 94))
            screen.blit(time, (160, 200))
        play_again = font_choice.render('Play Again', True, (40, 255, 40), (53, 73, 94))
        screen.blit(play_again, (160, 350))
        
        # React according to the user behavior
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                # If the user click the "Play Again" button
                if 160 <= mouse[0] <= 250 and 350 <= mouse[1] <= 382:
                    StartMenu()
                    end = True
                    
        pygame.display.update()

def FailMenu():
    """
    Set the fail menu for sokoban
    """
    # Load image for fail
    fail = pygame.image.load(os.path.join(ASSETS_FOLDER, "fail.png"))
    
    end = False
    pygame.init()
    # Set screen size, caption and icon
    screen = pygame.display.set_mode((416, 416))
    screen.fill((53, 73, 94))
    pygame.display.set_caption("Sokoban")
    pygame.display.set_icon(icon)
    
    while not end:
        # Set frame rate
        clock.tick(24)
        # Set the main interface
        screen.blit(pygame.transform.scale(fail, (80, 80)), (168, 10))
        font_title = pygame.font.SysFont('Cascadia mono', 64)
        font_choice = pygame.font.SysFont('Cascadia mono', 32)
        title = font_title.render('Failed!', True, (0, 255, 125), (53, 73, 94))
        screen.blit(title, (120, 100))
        play_again = font_choice.render('Play Again', True, (40, 255, 40), (53, 73, 94))
        screen.blit(play_again, (165, 200))
        quit = font_choice.render('Quit', True, (40, 255, 40), (53, 73, 94))
        screen.blit(quit, (148, 250))
        
        # React according to the user behavior
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                # If the user click the "Play Again" button
                if 165 <= mouse[0] <= 260 and 200 <= mouse[1] <= 232:
                    StartMenu()
                    end = True
                # If the user click the "Quit" button
                if 148 <= mouse[0] <= 272 and 250 <= mouse[1] <= 282:
                    end = True
                    
        pygame.display.update()
        
def draw_map(screen, game_map):
    """
    Set the game map
    """
    # load images
    # Image for botton
    aStarBtn = pygame.image.load(os.path.join(ASSETS_FOLDER, "aStarBtn.png"))
    bfsBtn = pygame.image.load(os.path.join(ASSETS_FOLDER, "bfsBtn.png"))
    dfsBtn = pygame.image.load(os.path.join(ASSETS_FOLDER, "dfsBtn.png"))
    # Image for two kinds of boxes and holes
    crate = pygame.image.load(os.path.join(ASSETS_FOLDER, "crate.png"))
    treasure = pygame.image.load(os.path.join(ASSETS_FOLDER, "treasure.png"))
    coin = (pygame.image.load(os.path.join(ASSETS_FOLDER, "c1.png")), pygame.image.load(os.path.join(ASSETS_FOLDER, "c2.png")), pygame.image.load(os.path.join(ASSETS_FOLDER, "c3.png")), pygame.image.load(os.path.join(ASSETS_FOLDER, "c4.png")), pygame.image.load(os.path.join(ASSETS_FOLDER, "c5.png")), pygame.image.load(os.path.join(ASSETS_FOLDER, "c6.png")), pygame.image.load(os.path.join(ASSETS_FOLDER, "c7.png")), pygame.image.load(os.path.join(ASSETS_FOLDER, "c8.png")))
    # Image for different kinds of walls
    wb = pygame.image.load(os.path.join(ASSETS_FOLDER, "wb.png"))
    wl = pygame.image.load(os.path.join(ASSETS_FOLDER, "wl.png"))
    wr = pygame.image.load(os.path.join(ASSETS_FOLDER, "wr.png"))
    wt = pygame.image.load(os.path.join(ASSETS_FOLDER, "wt.png"))
    wb = pygame.image.load(os.path.join(ASSETS_FOLDER, "wb.png"))
    wlt = pygame.image.load(os.path.join(ASSETS_FOLDER, "wlt.png"))
    wlb = pygame.image.load(os.path.join(ASSETS_FOLDER, "wlb.png"))
    wrt = pygame.image.load(os.path.join(ASSETS_FOLDER, "wrt.png"))
    wrb = pygame.image.load(os.path.join(ASSETS_FOLDER, "wrb.png"))
    wtb = pygame.image.load(os.path.join(ASSETS_FOLDER, "wtb.png"))
    wlr = pygame.image.load(os.path.join(ASSETS_FOLDER, "wlr.png"))
    w3l = pygame.image.load(os.path.join(ASSETS_FOLDER, "w3l.png"))
    w3r = pygame.image.load(os.path.join(ASSETS_FOLDER, "w3r.png"))
    w3t = pygame.image.load(os.path.join(ASSETS_FOLDER, "w3t.png"))
    w3b = pygame.image.load(os.path.join(ASSETS_FOLDER, "w3b.png"))
    w4 = pygame.image.load(os.path.join(ASSETS_FOLDER, "w4.png"))
    # Image for different kinds of grounds
    tl = (pygame.image.load(os.path.join(ASSETS_FOLDER, "tl1.png")),pygame.image.load(os.path.join(ASSETS_FOLDER, "tl2.png")))
    td = (pygame.image.load(os.path.join(ASSETS_FOLDER, "td1.png")),pygame.image.load(os.path.join(ASSETS_FOLDER, "td2.png")))
    tls =(pygame.image.load(os.path.join(ASSETS_FOLDER, "tls1.png")),pygame.image.load(os.path.join(ASSETS_FOLDER, "tls2.png")))
    tds = (pygame.image.load(os.path.join(ASSETS_FOLDER, "tds1.png")),pygame.image.load(os.path.join(ASSETS_FOLDER, "tds2.png")))
    # Image for different kinds of characters
    charS = pygame.image.load(os.path.join(ASSETS_FOLDER, "charS.png"))
    char = (pygame.image.load(os.path.join(ASSETS_FOLDER, "char1.png")), pygame.image.load(os.path.join(ASSETS_FOLDER, "char2.png")))
    
    x = (416 - 32 * game_map.size[1]) // 2
    y = (416 - 32 * game_map.size[0]) // 2
    for i in range(game_map.size[0]):
        for j in range(game_map.size[1]):
            if game_map.map_matrix[i][j] == 0:
                # Open place
                if (i + j) % 2 == 0:
                    if game_map.map_matrix[i - 1][j] == 1:
                        screen.blit(tds[(i * j) % 2], (x, y))
                    else:
                        screen.blit(td[(i * j) % 2], (x, y))
                else:
                    if game_map.map_matrix[i - 1][j] == 1:
                        screen.blit(tls[(i * j) % 2 - 1], (x, y))
                    else:
                        screen.blit(tl[(i * j) % 2], (x, y))
                if (game_map.player[1] == i - 1) and (game_map.player[0] == j):
                    screen.blit(charS, (x, y))
            elif game_map.map_matrix[i][j] == 1:
                # Wall
                wall_type = get_wall_faces(game_map.map_matrix, (j, i))
                if len(wall_type) == 1:
                    if (i + j) % 2 == 0:
                        screen.bilt(td[(i * j) % 2], (x, y))
                    else:
                        screen.bilt(tl[(i * j) % 2], (x, y))
                    if (1, 0) in wall_type:
                        screen.blit(wl, (x, y))
                    elif (-1, 0) in wall_type:
                        screen.blit(wr, (x, y))
                    elif (0, 1) in wall_type:
                        screen.blit(wt, (x, y))
                    elif (0, -1) in wall_type:
                        screen.blit(wb, (x, y))
                elif len(wall_type) == 2:
                    if (i + j) % 2 == 0:
                        screen.bilt(td[(i * j) % 2], (x, y))
                    else:
                        screen.bilt(tl[(i * j) % 2], (x, y))
                    if (1, 0) in wall_type:
                        if (0, 1) in wall_type:
                            screen.blit(wlt, (x, y))
                        elif (0, -1) in wall_type:
                            screen.blit(wlb, (x, y))
                        else:
                            screen.blit(wtb, (x, y))
                    elif (-1, 0) in wall_type:
                        if (0, 1) in wall_type:
                            screen.blit(wrt, (x, y))
                        elif (-1, 0) in wall_type:
                            screen.blit(wrb, (x, y))
                    else:
                        screen.blit(wlr, (x, y))
                elif len(wall_type) == 3:
                    if (i + j) % 2 == 0:
                        screen.bilt(td[(i * j) % 2], (x, y))
                    else:
                        screen.bilt(tl[(i * j) % 2], (x, y))
                    if (1, 0) not in wall_type:
                        screen.blit(w3r, (x, y))
                    elif (-1, 0) not in wall_type:
                        screen.blit(w3l, (x, y))
                    elif (0, 1) not in wall_type:
                        screen.blit(w3b, (x, y))
                    elif (0, -1) not in wall_type:
                        screen.blit(w3t, (x, y))
                elif len(wall_type) == 4:
                    if (i + j) % 2 == 0:
                        screen.bilt(td[(i * j) % 2], (x, y))
                    else:
                        screen.bilt(tl[(i * j) % 2], (x, y))
                    screen.blit(w4, (x, y))
            elif game_map.map_matrix[i][j] == 2:
                if (i + j) % 2 == 0:
                    if game_map.map_matrix[i - 1][j] == 1:
                        screen.blit(tds[(i * j) % 2], (x, y))
                    else:
                        screen.blit(td[(i * j) % 2], (x, y))
                else:
                    if game_map.map_matrix[i - 1][j] == 1:
                        screen.blit(tls[(i * j) % 2], (x, y))
                    else:
                        screen.blit(tl[(i * j) % 2], (x, y))
                if (game_map.player[1] == i - 1) and (game_map.player[0] == j):
                    screen.blit(charS, (x, y))
                screen.blit(coin[animPtr % 8], (x, y))
            elif game_map.map_matrix[i][j] == 3:
                if (i + j) % 2 == 0:
                    if game_map.map_matrix[i - 1][j] == 1:
                        screen.blit(tds[(i * j) % 2], (x, y))
                    else:
                        screen.blit(td[(i * j) % 2], (x, y)) 
                else:
                    if game_map.map_matrix[i - 1][j] == 1:
                        screen.blit(tls[(i * j) % 2], (x, y))
                    else:
                        screen.blit(tl[(i * j) % 2], (x, y))
                screen.blit(crate, (x, y))
            elif game_map.map_matrix[i][j] == 4:
                if (i + j) % 2 == 0:
                    if game_map.map_matrix[i - 1][j] == 1:
                        screen.blit(tds[(i * j) % 2], (x, y))
                    else:
                        screen.blit(td[(i * j) % 2], (x, y)) 
                else:
                    if game_map.map_matrix[i - 1][j] == 1:
                        screen.blit(tls[(i * j) % 2], (x, y))
                    else:
                        screen.blit(tl[(i * j) % 2], (x, y))
                screen.blit(treasure, (x, y))
            if (game_map.player[1] == i) and (game_map.player[0] == j):
                screen.blit(char[animPtr % 2], (x, y))
            x += 32
        y += 32
        
    screen.blit(bfsBtn, (45.5, 360))
    screen.blit(aStarBtn, (169, 360))
    screen.blit(dfsBtn, (292.5, 360))

def get_wall_faces(map_matrix, wall_pos):
    faces = []
    if (wall_pos[0] > 0) and (map_matrix[wall_pos[1]][wall_pos[0] - 1] != 1):
        faces.append((-1, 0))
    if (wall_pos[0] < len(map_matrix[0]) - 1) and (map_matrix[wall_pos[1]][wall_pos[0] + 1] != 1):
        faces.append((1, 0))
    if (wall_pos[1] > 0) and (map_matrix[wall_pos[1] - 1][wall_pos[0]] != 1):
        faces.append((0, -1))
    if (wall_pos[1] < len(map_matrix) - 1) and (map_matrix[wall_pos[1] + 1][wall_pos[0]] != 1):
        faces.append((0, 1))
    return faces

def auto_move(screen, game_map, moves):
    global animPtr
    for action in moves:
        pygame.time.wait(100)
        game_map.move(action)
        screen.fill((53, 73, 94))
        animPtr += 1
        draw_map(screen, game_map)
        pygame.display.update()
        
if __name__ == '__main__':
    StartMenu()