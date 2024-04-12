from threading import Thread
import os
import pygame
import copy

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
    # load images and sound effects
    # Image for botton
    aStarBtn = pygame.image.load(os.path.join(ASSETS_FOLDER, "aStarBtn.png"))
    bfsBtn = pygame.image.load(os.path.join(ASSETS_FOLDER, "bfsBtn.png"))
    dfsBtn = pygame.image.load(os.path.join(ASSETS_FOLDER, "dfsBtn.png"))
    # Sound effects for different kinds of actions
    push = pygame.mixer.Sound(os.path.join(ASSETS_FOLDER, "push.wav"))
    footstep = pygame.mixer.Sound(os.path.join(ASSETS_FOLDER, "footstep.wav"))
    metal = pygame.mixer.Sound(os.path.join(ASSETS_FOLDER, "metal.wav"))
    
    end = False
    pygame.init()
    # Set screen size, caption and icon
    screen = pygame.display.set_mode((416, 416))
    screen.fill((53, 73, 94))
    pygame.display.set_caption("Sokoban")
    pygame.display.set_icon(icon)
    # Set map and search button
    DrawMap(game_mode=game_mode, map_mode=map_mode)
    screen.blit(bfsBtn, (45.5, 360))
    screen.blit(aStarBtn, (169, 360))
    screen.blit(dfsBtn, (292.5, 360))
    
    while not end:
        # Set frame rate
        clock.tick(24)
        
def SuccessMenu(step):
    """
    Set the success menu for sokoban
    """
    # Load image for success
    # Image for solve
    solve = pygame.image.load(os.path.join(ASSETS_FOLDER, "solve.png"))
    # Image for play again
    again = pygame.image.load(os.path.join(ASSETS_FOLDER, "again.png"))

def FailMenu():
    """
    Set the fail menu for sokoban
    """
    # Load image for fail
    fail = pygame.image.load(os.path.join(ASSETS_FOLDER, "fail.png"))
        
def DrawMap(game_mode, map_mode):
    """
    Set the game map
    """
    # load images and sound effects
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
        
if __name__ == '__main__':
    StartMenu()