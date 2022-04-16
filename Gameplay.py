import pygame as pg
from Gamedata import piece_names, piece_values, piece_amount, piece_moves_w, piece_moves_b, initial_positions_b, \
    initial_positions_w, pawn_capture_b, pawn_capture_w, square_size
from Gamefunctions import get_folder_file, makeimg
from Gameclasses import Piece


def realgame(scr):
    pieces = []
    for m in range(2):  # 0 is black, 1 is white
        if m == 0:
            positions = initial_positions_b
            piece_moves = piece_moves_b
            pawn = pawn_capture_b
        else:
            positions = initial_positions_w
            piece_moves = piece_moves_w
            pawn = pawn_capture_w
        for n in range(len(piece_names)):
            for q in range(piece_amount[n]):
                temp_name = piece_names[n]
                temp_value = piece_values[n]
                temp_move = piece_moves[n]
                temp_position = positions[n][q]
                temp_img, temp_rect = makeimg(get_folder_file("Images", temp_name + str(m) + ".png"), True, 0.5)
                pieces.append(Piece(temp_name, temp_img, temp_rect, temp_value, temp_move, m, temp_position, q, pawn))

    running = True
    clicked = False
    switch = False  # See when the mouse button changes from pressed to released
    switch2 = False  # See when the mouse button changes from released to pressed
    false_click = False  # If player clicks on something other than a piece
    mouse_piece = pieces[0]
    castling_black_left = True  # if the king or rook has not moved
    castling_black_right = True
    temp_castling_black_left = False  # if there are no pieces in between
    temp_castling_black_right = False
    castling_white_left = True  # if the king or rook has not moved
    castling_white_right = True
    temp_castling_white_left = False  # if there are no pieces in between
    temp_castling_white_right = False
    white_win = False    # use to see who won
    quit_game = False   # see if the game has ended by clicking the cross on the top right of the window

    current_player = 1  # white begins

    while running:
        pg.event.pump()
        scr.fill((100, 100, 100))

        # Mouse position (outputs are in (x, y))
        mouse_place = (pg.mouse.get_pos()[0] // square_size, pg.mouse.get_pos()[1] // square_size)  # square number
        mouse_coordinates = (pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
        false_click_detector = []
        if switch2:  # if click starts
            for piece in pieces:
                if mouse_place == piece.position:  # if the mouse is on a white piece
                    mouse_piece = piece
                    false_click_detector.append(1)
            if sum(false_click_detector) == 0:
                false_click = True
            else:
                false_click = False
        if false_click and switch:
            false_click = False

        # Draw the board
        for i in range(8):  # y position
            row = i % 2  # Even row = 0, odd row = 1
            for j in range(8):  # x position
                pg.draw.rect(scr, (150, 150, 150), [square_size * (2 * j + row), square_size * i, square_size, square_size])

        # Draw the pieces (first run in for loop is for square coloring, second for pieces; otherwise colors might overlap
        # the pieces)
        colored_squares = []
        other_piece = []  # so that the code does not crash because it doesn't know other_piece
        for q in range(2):
            for piece in pieces:
                # center is the center of the piece
                center = (int(square_size * (piece.position[0] + 0.5)),
                          int(square_size * (piece.position[1] + 0.5)))
                if q == 0:  # Draw the colored squares (equivalent to determining where the piece is allowed to go)
                    if (mouse_place == piece.position or clicked) and not false_click:
                        # either mouse hovers over piece or is dragging it
                        if not clicked:  # mouse is hovering
                            mouse_piece = piece
                        center = (int(square_size * (mouse_piece.position[0] + 0.5)),
                                  int(square_size * (mouse_piece.position[1] + 0.5)))

                        # Check castling opportunities
                        if mouse_piece.name == "King" and (castling_black_right or castling_black_left or
                                                           castling_white_right or castling_white_left):
                            if mouse_piece.color == 0:
                                temp_pos = []
                                for piece4 in pieces:  # check if there are any pieces between the king and rook
                                    temp_pos.append(piece4.position)
                                if (1, 0) in temp_pos or (2, 0) in temp_pos or (3, 0) in temp_pos:
                                    temp_castling_black_left = False
                                else:
                                    temp_castling_black_left = True
                                if (5, 0) in temp_pos or (6, 0) in temp_pos:
                                    temp_castling_black_right = False
                                else:
                                    temp_castling_black_right = True
                            else:
                                temp_pos = []
                                for piece4 in pieces:  # check if there are any pieces between the king and rook
                                    temp_pos.append(piece4.position)
                                if (1, 7) in temp_pos or (2, 7) in temp_pos or (3, 7) in temp_pos:
                                    temp_castling_white_left = False
                                else:
                                    temp_castling_white_left = True
                                if (5, 7) in temp_pos or (6, 7) in temp_pos:
                                    temp_castling_white_right = False
                                else:
                                    temp_castling_white_right = True

                        for line in mouse_piece.move:  # For the pawn, separate moves and captures
                            collision = False  # To see if another piece obstructs the line
                            other_piece_bool = False  # if the possible move of the current piece intersects a piece of the other color
                            for move in line:
                                if not collision and not other_piece_bool:  # Also use this if statement here to make the program faster
                                    pos = (int(center[0] + square_size * (move[0] - 0.5)),
                                           int(center[1] + square_size * (move[1] - 0.5)))
                                    for piece2 in pieces:
                                        if mouse_piece.position[0] + move[0] == piece2.position[0] \
                                                and mouse_piece.position[1] + move[1] == piece2.position[1]:
                                            if mouse_piece.color == piece2.color or mouse_piece.name == "Pawn":
                                                collision = True
                                            elif not other_piece_bool:  # if it's a different color and the line hasn't been intersected yet
                                                other_piece_bool = True
                                                other_piece.append(piece2)
                                    if not collision and mouse_piece.color == current_player:
                                        if not other_piece_bool:
                                            pg.draw.rect(scr, (200, 200, 150), [pos[0], pos[1], square_size, square_size])
                                        else:
                                            pg.draw.rect(scr, (200, 150, 150), [pos[0], pos[1], square_size, square_size])
                                        colored_squares.append((pos[0] // square_size, pos[1] // square_size))

                        if mouse_piece.name == "King" and mouse_piece.color == current_player:
                            if mouse_piece.color == 0:
                                if temp_castling_black_left and castling_black_left:
                                    pos = (int(square_size * 2), 0)
                                    pg.draw.rect(scr, (200, 200, 150), [pos[0], pos[1], square_size, square_size])
                                    colored_squares.append((pos[0] // square_size, pos[1] // square_size))
                                if temp_castling_black_right and castling_black_right:
                                    pos = (int(square_size * 6), 0)
                                    pg.draw.rect(scr, (200, 200, 150), [pos[0], pos[1], square_size, square_size])
                                    colored_squares.append((pos[0] // square_size, pos[1] // square_size))
                            if mouse_piece.color == 1:
                                if temp_castling_white_left and castling_white_left:
                                    pos = (int(square_size * 2), int(square_size * 7))
                                    pg.draw.rect(scr, (200, 200, 150), [pos[0], pos[1], square_size, square_size])
                                    colored_squares.append((pos[0] // square_size, pos[1] // square_size))
                                if temp_castling_white_right and castling_white_right:
                                    pos = (int(square_size * 6), int(square_size * 7))
                                    pg.draw.rect(scr, (200, 200, 150), [pos[0], pos[1], square_size, square_size])
                                    colored_squares.append((pos[0] // square_size, pos[1] // square_size))

                        if mouse_piece.name == "Pawn" and mouse_piece.color == current_player:
                            for piece3 in pieces:
                                for move2 in mouse_piece.pawn:
                                    pos2 = (int(center[0] + square_size * (move2[0] - 0.5)),
                                            int(center[1] + square_size * (move2[1] - 0.5)))
                                    if mouse_piece.position[0] + move2[0] == piece3.position[0] \
                                            and mouse_piece.position[1] + move2[1] == piece3.position[1]:
                                        if mouse_piece.color != piece3.color:
                                            other_piece.append(piece3)
                                            pg.draw.rect(scr, (200, 150, 150), [pos2[0], pos2[1], square_size, square_size])
                                            colored_squares.append((pos2[0] // square_size, pos2[1] // square_size))

                else:  # Draw the pieces
                    if mouse_piece == piece and clicked and not false_click \
                            and mouse_piece.color == current_player:  # piece is dragged
                        if switch and mouse_place in colored_squares:  # change stationary position to new one
                            # See if a king or rook is moved, if this is the case, castling is not possible anymore.
                            if piece.name == "King":
                                if piece.color == 0:
                                    if castling_black_left and temp_castling_black_left and mouse_place == (2, 0):
                                        for qq in range(len(pieces)):
                                            piece6 = pieces[qq]
                                            if piece6.color == 0 and piece6.name == "Rook" and piece6.position == (0, 0):
                                                pieces[qq].position = (3, 0)
                                    if castling_black_right and temp_castling_black_right and mouse_place == (6, 0):
                                        for ww in range(len(pieces)):
                                            piece7 = pieces[ww]
                                            if piece7.color == 0 and piece7.name == "Rook" and piece7.position == (7, 0):
                                                pieces[ww].position = (5, 0)
                                    castling_black_left = False
                                    castling_black_right = False
                                else:
                                    if castling_white_left and temp_castling_white_left and mouse_place == (2, 7):
                                        for ee in range(len(pieces)):
                                            piece8 = pieces[ee]
                                            if piece8.color == 1 and piece8.name == "Rook" and piece8.position == (0, 7):
                                                pieces[ee].position = (3, 7)
                                    if castling_white_right and temp_castling_white_right and mouse_place == (6, 7):
                                        for rr in range(len(pieces)):
                                            piece9 = pieces[rr]
                                            if piece9.color == 1 and piece9.name == "Rook" and piece9.position == (7, 7):
                                                pieces[rr].position = (5, 7)
                                    castling_white_left = False
                                    castling_white_right = False
                            if piece.name == "Rook":
                                if piece.color == 0:
                                    if piece.position == (0, 0):
                                        castling_black_left = False
                                    if piece.position == (7, 0):
                                        castling_black_right = False
                                else:
                                    if piece.position == (0, 7):
                                        castling_white_left = False
                                    if piece.position == (7, 7):
                                        castling_white_right = False

                            # remove other piece if applicable
                            other_piece_positions = []
                            for i in other_piece:
                                other_piece_positions.append(i.position)
                            if mouse_place in other_piece_positions:
                                for j in pieces:
                                    if mouse_place == j.position:
                                        # Check if the removed piece is a rook, this influences castling.
                                        if j.name == "Rook":
                                            if j.color == 0:
                                                if j.position == (0, 0):
                                                    castling_black_left = False
                                                if j.position == (7, 0):
                                                    castling_black_right = False
                                            else:
                                                if j.position == (0, 7):
                                                    castling_white_left = False
                                                if j.position == (7, 7):
                                                    castling_white_right = False
                                        elif j.name == "King":
                                            running = False
                                            if j.color == 0:
                                                white_win = True
                                            else:
                                                white_win = False
                                        pieces.remove(j)

                            # change position of current piece
                            center = (int(square_size * (mouse_place[0] + 0.5)),
                                      int(square_size * (mouse_place[1] + 0.5)))
                            piece.position = mouse_place
                            piece.rect.center = center
                            scr.blit(piece.img, piece.rect)

                            # Pawn can move two blocks the first move, only one block after that.
                            if piece.name == "Pawn":
                                if piece.color == 0:  # black
                                    piece.move = [[(0, 1)]]
                                    if piece.position[1] == 7:  # if the pawn has reached the other side
                                        piece.name = "Queen"
                                        piece.img, piece.rect = makeimg(get_folder_file("Images", "Queen" + str(piece.color)
                                                                                        + ".png"), True, 0.5)
                                        piece.value = piece_values[1]
                                        piece.move = piece_moves_b[1]
                                else:  # white
                                    piece.move = [[(0, -1)]]
                                    if piece.position[1] == 0:  # if the pawn has reached the other side
                                        piece.name = "Queen"
                                        piece.img, piece.rect = makeimg(get_folder_file("Images", "Queen" + str(piece.color)
                                                                                        + ".png"), True, 0.5)
                                        piece.value = piece_values[1]
                                        piece.move = piece_moves_w[1]

                            # Other player may now move.
                            if current_player == 0:
                                current_player = 1
                            else:
                                current_player = 0

                        else:  # return to original position
                            center = (int(square_size * (piece.position[0] + 0.5)),
                                      int(square_size * (piece.position[1] + 0.5)))
                            mouse_piece.rect.center = mouse_coordinates
                            scr.blit(mouse_piece.img, mouse_piece.rect)
                    else:  # piece is drawn in stationary position
                        piece.rect.center = center
                        scr.blit(piece.img, piece.rect)
        if pg.mouse.get_pressed(3)[0] == 1:
            clicked = True
        else:
            clicked = False
        pg.display.flip()
        switch = False
        switch2 = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                quit_game = True
            if event.type == pg.MOUSEBUTTONDOWN:
                switch2 = True
            if event.type == pg.MOUSEBUTTONUP:
                switch = True
    return white_win, quit_game


def aigame(scr):
    # Real player is white, AI is black.
    # Outline of AI is to copy the state of the game and in an 'alternate game' execute all moves to find the best one.
    pieces = []
    for m in range(2):  # 0 is black, 1 is white
        if m == 0:
            positions = initial_positions_b
            piece_moves = piece_moves_b
            pawn = pawn_capture_b
        else:
            positions = initial_positions_w
            piece_moves = piece_moves_w
            pawn = pawn_capture_w
        for n in range(len(piece_names)):
            for q in range(piece_amount[n]):
                temp_name = piece_names[n]
                temp_value = piece_values[n]
                temp_move = piece_moves[n]
                temp_position = positions[n][q]
                temp_img, temp_rect = makeimg(get_folder_file("Images", temp_name + str(m) + ".png"), True, 0.5)
                pieces.append(Piece(temp_name, temp_img, temp_rect, temp_value, temp_move, m, temp_position, q, pawn))

    running = True
    clicked = False
    switch = False  # See when the mouse button changes from pressed to released
    switch2 = False  # See when the mouse button changes from released to pressed
    false_click = False  # If player clicks on something other than a piece
    mouse_piece = pieces[0]
    castling_black_left = True  # if the king or rook has not moved
    castling_black_right = True
    temp_castling_black_left = False  # if there are no pieces in between
    temp_castling_black_right = False
    castling_white_left = True  # if the king or rook has not moved
    castling_white_right = True
    temp_castling_white_left = False  # if there are no pieces in between
    temp_castling_white_right = False
    white_win = False    # use to see who won
    quit_game = False   # see if the game has ended by clicking the cross on the top right of the window

    # During the AI's turn, store the game in a list / parallel game.
    parallel_game = []

    current_player = 1  # white begins

    while running:
        pg.event.pump()
        scr.fill((100, 100, 100))

        # Mouse position (outputs are in (x, y))
        mouse_place = (pg.mouse.get_pos()[0] // square_size, pg.mouse.get_pos()[1] // square_size)  # square number
        mouse_coordinates = (pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
        false_click_detector = []
        if switch2:  # if click starts
            for piece in pieces:
                if mouse_place == piece.position:  # if the mouse is on a white piece
                    mouse_piece = piece
                    false_click_detector.append(1)
            if sum(false_click_detector) == 0:
                false_click = True
            else:
                false_click = False
        if false_click and switch:
            false_click = False

        # Draw the board
        for i in range(8):  # y position
            row = i % 2  # Even row = 0, odd row = 1
            for j in range(8):  # x position
                pg.draw.rect(scr, (150, 150, 150), [square_size * (2 * j + row), square_size * i, square_size, square_size])

        # Draw the pieces (first run in for loop is for square coloring, second for pieces; otherwise colors might overlap
        # the pieces)
        colored_squares = []
        other_piece = []  # so that the code does not crash because it doesn't know other_piece
        for q in range(2):
            for piece in pieces:
                # center is the center of the piece
                center = (int(square_size * (piece.position[0] + 0.5)),
                          int(square_size * (piece.position[1] + 0.5)))
                if q == 0:  # Draw the colored squares (equivalent to determining where the piece is allowed to go)
                    if (mouse_place == piece.position or clicked) and not false_click:
                        # either mouse hovers over piece or is dragging it
                        if not clicked:  # mouse is hovering
                            mouse_piece = piece
                        center = (int(square_size * (mouse_piece.position[0] + 0.5)),
                                  int(square_size * (mouse_piece.position[1] + 0.5)))

                        # Check castling opportunities
                        if mouse_piece.name == "King" and (castling_black_right or castling_black_left or
                                                           castling_white_right or castling_white_left):
                            if mouse_piece.color == 0:
                                temp_pos = []
                                for piece4 in pieces:  # check if there are any pieces between the king and rook
                                    temp_pos.append(piece4.position)
                                if (1, 0) in temp_pos or (2, 0) in temp_pos or (3, 0) in temp_pos:
                                    temp_castling_black_left = False
                                else:
                                    temp_castling_black_left = True
                                if (5, 0) in temp_pos or (6, 0) in temp_pos:
                                    temp_castling_black_right = False
                                else:
                                    temp_castling_black_right = True
                            else:
                                temp_pos = []
                                for piece4 in pieces:  # check if there are any pieces between the king and rook
                                    temp_pos.append(piece4.position)
                                if (1, 7) in temp_pos or (2, 7) in temp_pos or (3, 7) in temp_pos:
                                    temp_castling_white_left = False
                                else:
                                    temp_castling_white_left = True
                                if (5, 7) in temp_pos or (6, 7) in temp_pos:
                                    temp_castling_white_right = False
                                else:
                                    temp_castling_white_right = True

                        for line in mouse_piece.move:  # For the pawn, separate moves and captures
                            collision = False  # To see if another piece obstructs the line
                            other_piece_bool = False  # if the possible move of the current piece intersects a piece of the other color
                            for move in line:
                                if not collision and not other_piece_bool:  # Also use this if statement here to make the program faster
                                    pos = (int(center[0] + square_size * (move[0] - 0.5)),
                                           int(center[1] + square_size * (move[1] - 0.5)))
                                    for piece2 in pieces:
                                        if mouse_piece.position[0] + move[0] == piece2.position[0] \
                                                and mouse_piece.position[1] + move[1] == piece2.position[1]:
                                            if mouse_piece.color == piece2.color or mouse_piece.name == "Pawn":
                                                collision = True
                                            elif not other_piece_bool:  # if it's a different color and the line hasn't been intersected yet
                                                other_piece_bool = True
                                                other_piece.append(piece2)
                                    if not collision and mouse_piece.color == 1 and current_player == 1:
                                        if not other_piece_bool:
                                            pg.draw.rect(scr, (200, 200, 150), [pos[0], pos[1], square_size, square_size])
                                        else:
                                            pg.draw.rect(scr, (200, 150, 150), [pos[0], pos[1], square_size, square_size])
                                        colored_squares.append((pos[0] // square_size, pos[1] // square_size))

                        if mouse_piece.name == "King" and mouse_piece.color == 1 and current_player == 1:
                            if mouse_piece.color == 0:
                                if temp_castling_black_left and castling_black_left:
                                    pos = (int(square_size * 2), 0)
                                    pg.draw.rect(scr, (200, 200, 150), [pos[0], pos[1], square_size, square_size])
                                    colored_squares.append((pos[0] // square_size, pos[1] // square_size))
                                if temp_castling_black_right and castling_black_right:
                                    pos = (int(square_size * 6), 0)
                                    pg.draw.rect(scr, (200, 200, 150), [pos[0], pos[1], square_size, square_size])
                                    colored_squares.append((pos[0] // square_size, pos[1] // square_size))
                            if mouse_piece.color == 1:
                                if temp_castling_white_left and castling_white_left:
                                    pos = (int(square_size * 2), int(square_size * 7))
                                    pg.draw.rect(scr, (200, 200, 150), [pos[0], pos[1], square_size, square_size])
                                    colored_squares.append((pos[0] // square_size, pos[1] // square_size))
                                if temp_castling_white_right and castling_white_right:
                                    pos = (int(square_size * 6), int(square_size * 7))
                                    pg.draw.rect(scr, (200, 200, 150), [pos[0], pos[1], square_size, square_size])
                                    colored_squares.append((pos[0] // square_size, pos[1] // square_size))

                        if mouse_piece.name == "Pawn" and mouse_piece.color == 1 and current_player == 1:
                            for piece3 in pieces:
                                for move2 in mouse_piece.pawn:
                                    pos2 = (int(center[0] + square_size * (move2[0] - 0.5)),
                                            int(center[1] + square_size * (move2[1] - 0.5)))
                                    if mouse_piece.position[0] + move2[0] == piece3.position[0] \
                                            and mouse_piece.position[1] + move2[1] == piece3.position[1]:
                                        if mouse_piece.color != piece3.color:
                                            other_piece.append(piece3)
                                            pg.draw.rect(scr, (200, 150, 150), [pos2[0], pos2[1], square_size, square_size])
                                            colored_squares.append((pos2[0] // square_size, pos2[1] // square_size))

                else:  # Draw the pieces
                    if mouse_piece == piece and clicked and not false_click \
                            and mouse_piece.color == 1 and current_player == 1:  # piece is dragged
                        if switch and mouse_place in colored_squares:  # change stationary position to new one
                            # See if a king or rook is moved, if this is the case, castling is not possible anymore.
                            if piece.name == "King":
                                if piece.color == 0:
                                    if castling_black_left and temp_castling_black_left and mouse_place == (2, 0):
                                        for qq in range(len(pieces)):
                                            piece6 = pieces[qq]
                                            if piece6.color == 0 and piece6.name == "Rook" and piece6.position == (0, 0):
                                                pieces[qq].position = (3, 0)
                                    if castling_black_right and temp_castling_black_right and mouse_place == (6, 0):
                                        for ww in range(len(pieces)):
                                            piece7 = pieces[ww]
                                            if piece7.color == 0 and piece7.name == "Rook" and piece7.position == (7, 0):
                                                pieces[ww].position = (5, 0)
                                    castling_black_left = False
                                    castling_black_right = False
                                else:
                                    if castling_white_left and temp_castling_white_left and mouse_place == (2, 7):
                                        for ee in range(len(pieces)):
                                            piece8 = pieces[ee]
                                            if piece8.color == 1 and piece8.name == "Rook" and piece8.position == (0, 7):
                                                pieces[ee].position = (3, 7)
                                    if castling_white_right and temp_castling_white_right and mouse_place == (6, 7):
                                        for rr in range(len(pieces)):
                                            piece9 = pieces[rr]
                                            if piece9.color == 1 and piece9.name == "Rook" and piece9.position == (7, 7):
                                                pieces[rr].position = (5, 7)
                                    castling_white_left = False
                                    castling_white_right = False
                            if piece.name == "Rook":
                                if piece.color == 0:
                                    if piece.position == (0, 0):
                                        castling_black_left = False
                                    if piece.position == (7, 0):
                                        castling_black_right = False
                                else:
                                    if piece.position == (0, 7):
                                        castling_white_left = False
                                    if piece.position == (7, 7):
                                        castling_white_right = False

                            # remove other piece if applicable
                            other_piece_positions = []
                            for i in other_piece:
                                other_piece_positions.append(i.position)
                            if mouse_place in other_piece_positions:
                                for j in pieces:
                                    if mouse_place == j.position:
                                        # Check if the removed piece is a rook, this influences castling.
                                        if j.name == "Rook":
                                            if j.color == 0:
                                                if j.position == (0, 0):
                                                    castling_black_left = False
                                                if j.position == (7, 0):
                                                    castling_black_right = False
                                            else:
                                                if j.position == (0, 7):
                                                    castling_white_left = False
                                                if j.position == (7, 7):
                                                    castling_white_right = False
                                        elif j.name == "King":
                                            running = False
                                            if j.color == 0:
                                                white_win = True
                                            else:
                                                white_win = False
                                        pieces.remove(j)

                            # change position of current piece
                            center = (int(square_size * (mouse_place[0] + 0.5)),
                                      int(square_size * (mouse_place[1] + 0.5)))
                            piece.position = mouse_place
                            piece.rect.center = center
                            scr.blit(piece.img, piece.rect)

                            # Pawn can move two blocks the first move, only one block after that.
                            if piece.name == "Pawn":
                                if piece.color == 0:  # black
                                    piece.move = [[(0, 1)]]
                                    if piece.position[1] == 7:  # if the pawn has reached the other side
                                        piece.name = "Queen"
                                        piece.img, piece.rect = makeimg(get_folder_file("Images", "Queen" + str(piece.color)
                                                                                        + ".png"), True, 0.5)
                                        piece.value = piece_values[1]
                                        piece.move = piece_moves_b[1]
                                else:  # white
                                    piece.move = [[(0, -1)]]
                                    if piece.position[1] == 0:  # if the pawn has reached the other side
                                        piece.name = "Queen"
                                        piece.img, piece.rect = makeimg(get_folder_file("Images", "Queen" + str(piece.color)
                                                                                        + ".png"), True, 0.5)
                                        piece.value = piece_values[1]
                                        piece.move = piece_moves_w[1]

                            # Other player may now move.
                            if current_player == 0:
                                current_player = 1
                            else:
                                current_player = 0

                        else:  # return to original position
                            center = (int(square_size * (piece.position[0] + 0.5)),
                                      int(square_size * (piece.position[1] + 0.5)))
                            mouse_piece.rect.center = mouse_coordinates
                            scr.blit(mouse_piece.img, mouse_piece.rect)
                    else:  # piece is drawn in stationary position
                        piece.rect.center = center
                        scr.blit(piece.img, piece.rect)
        if pg.mouse.get_pressed(3)[0] == 1:
            clicked = True
        else:
            clicked = False
        pg.display.flip()
        switch = False
        switch2 = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                quit_game = True
            if event.type == pg.MOUSEBUTTONDOWN:
                switch2 = True
            if event.type == pg.MOUSEBUTTONUP:
                switch = True
    return white_win, quit_game
