import pygame as pg
from Gameplay import realgame, aigame
from Gamedata import res
from Main_menu import mainmenu
from Endscreen import endscreen


# Bonus rules to include: en passant, king sacrifice not allowed, stalemate
pg.init()
scr = pg.display.set_mode(res)
pg.font.init()
font = pg.font.SysFont("microsofthimalaya", 200, False, False)  # alternatively: microsoftyibaiti

running = True
real_game = True  # If not real_game: AI game.
while running:
    running, real, ai = mainmenu(scr, font)

    if real:
        white_win, quit_game = realgame(scr)
        if not quit_game:
            endscreen(scr, white_win)
    if ai:
        white_win, quit_game = aigame(scr)
        if not quit_game:
            endscreen(scr, white_win)

    pg.display.flip()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

pg.quit()
