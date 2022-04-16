import pygame as pg
from Gamedata import res


def endscreen(scr, white_win):
    running = True
    while running:
        pg.event.pump()
        scr.fill((0, 0, 0))

        if white_win:
            txt = "White wins!"
        else:
            txt = "Black wins!"

        font = pg.font.SysFont("microsofthimalaya", 100, False, False)  # alternatively: microsoftyibaiti
        txt1 = font.render(txt, False, (255, 255, 255))
        txtrect1 = txt1.get_rect()
        txtrect1.center = (int(res[0] / 2), int(res[1] / 2))
        scr.blit(txt1, txtrect1)

        mouse_position = pg.mouse.get_pos()
        if res[0] * 7/20 < mouse_position[0] < res[0] * 13/20 and res[1] * 11/20 < mouse_position[1] < res[1] * 13/20:
            size = 50
            color = (255, 255, 255)
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    running = False

        else:
            size = 40
            color = (150, 150, 150)
        font = pg.font.SysFont("microsofthimalaya", size, False, False)  # alternatively: microsoftyibaiti
        txt2 = font.render("Main menu", False, color)
        txtrect2 = txt2.get_rect()
        txtrect2.center = (int(res[0] / 2), int(res[1] * 6 / 10))
        scr.blit(txt2, txtrect2)

        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

