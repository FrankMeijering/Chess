import pygame as pg
from Gamedata import res
from Gamefunctions import makeimg


def mainmenu(scr, font):
    img1, rect1 = makeimg("Row1.png", True, 0.8)
    img2, rect2 = makeimg("Row2.png", True, 0.75)
    img3, rect3 = makeimg("Row3.png", True, 0.55)
    img4, rect4 = makeimg("Row4.png", True, 0.5)

    txt1 = font.render("CHESS", False, (255, 255, 255))
    txtrect1 = txt1.get_rect()
    txtrect1.center = (int(res[0] / 2), int(res[1] / 4))

    running = True
    real = False
    ai = False
    while running and not real and not ai:
        pg.event.pump()
        scr.fill((0, 50, 0))
        for line in range(int(res[1] * 3 / 10)):
            pg.draw.rect(scr, (min(int(50 + line/1.5), 255), min(int(30 + line/1.5), 255),
                               min(int(10 + line/1.5), 255)), [0, int(res[1] * 7.3 / 10) + line, res[0], 1])

        mouseposition = pg.mouse.get_pos()
        rect1.center = (int(res[0] / 2 + (mouseposition[0] - res[0] / 2) / 6.5), int(res[1] * 15 / 20))
        rect2.center = (int(res[0] / 2 + (mouseposition[0] - res[0] / 2) / 9), int(res[1] * 14 / 20))
        rect3.center = (int(res[0] / 2 + (mouseposition[0] - res[0] / 2) / 25), int(res[1] * 12 / 20))
        rect4.center = (int(res[0] / 2 + (mouseposition[0] - res[0] / 2) / 60), int(res[1] * 11.5 / 20))

        scr.blit(img4, rect4)
        scr.blit(img3, rect3)
        scr.blit(img2, rect2)
        scr.blit(img1, rect1)

        # Mouse processing
        if res[0] / 5 < mouseposition[0] < res[0] * 4 / 5 and res[1] / 10 < mouseposition[1] < res[1] * 3 / 10:
            if res[1] / 10 < mouseposition[1] < res[1] * 2 / 10:
                font = pg.font.SysFont("microsofthimalaya", 50, False, False)  # alternatively: microsoftyibaiti
                txt2 = font.render("Play against real opponent", False, (255, 255, 255))
                txtrect2 = txt2.get_rect()
                txtrect2.center = (int(res[0] / 2), int(res[1] * 3.5 / 20))

                font = pg.font.SysFont("microsofthimalaya", 40, False, False)  # alternatively: microsoftyibaiti
                txt3 = font.render("Play against AI", False, (150, 150, 150))
                txtrect3 = txt3.get_rect()
                txtrect3.center = (int(res[0] / 2), int(res[1] * 5 / 20))

                for event in pg.event.get():
                    if event.type == pg.MOUSEBUTTONDOWN:
                        real = True

            else:
                font = pg.font.SysFont("microsofthimalaya", 40, False, False)  # alternatively: microsoftyibaiti
                txt2 = font.render("Play against real opponent", False, (150, 150, 150))
                txtrect2 = txt2.get_rect()
                txtrect2.center = (int(res[0] / 2), int(res[1] * 3.5 / 20))

                font = pg.font.SysFont("microsofthimalaya", 50, False, False)  # alternatively: microsoftyibaiti
                txt3 = font.render("Play against AI", False, (255, 255, 255))
                txtrect3 = txt3.get_rect()
                txtrect3.center = (int(res[0] / 2), int(res[1] * 5 / 20))

                for event in pg.event.get():
                    if event.type == pg.MOUSEBUTTONDOWN:
                        ai = True

            scr.blit(txt2, txtrect2)
            scr.blit(txt3, txtrect3)
        else:
            scr.blit(txt1, txtrect1)

        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
    if running:
        return True, real, ai
    else:
        return False, real, ai
