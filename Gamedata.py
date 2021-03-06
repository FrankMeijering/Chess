# Size of the squares on the board
square_size = 80
res = (square_size*8, square_size*8)

piece_names = ["King", "Queen", "Rook", "Bishop", "Knight", "Pawn"]
piece_values = [99, 9, 5, 3, 3, 1]
piece_amount = [1, 1, 2, 2, 2, 8]
# Piece moves is (x, y). The sublists are for lines (to make them disappear when other pieces are in the way)
piece_moves_b = [[[(0, 1)], [(1, 1)], [(1, 0)], [(1, -1)], [(0, -1)], [(-1, -1)], [(-1, 0)], [(-1, 1)]],
                 [[(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)],
                  [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)],
                  [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)],
                  [(1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7)],
                  [(0, -1), (0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7)],
                  [(-1, -1), (-2, -2), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7)],
                  [(-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0)],
                  [(-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7)]],
                 [[(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)],
                  [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)],
                  [(0, -1), (0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7)],
                  [(-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0)]],
                 [[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)],
                  [(1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7)],
                  [(-1, -1), (-2, -2), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7)],
                  [(-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7)]],
                 [[(1, 2)], [(-1, 2)], [(1, -2)], [(-1, -2)], [(2, 1)], [(-2, 1)], [(2, -1)], [(-2, -1)]],
                 [[(0, 1), (0, 2)]]]
piece_moves_w = [[[(0, 1)], [(1, 1)], [(1, 0)], [(1, -1)], [(0, -1)], [(-1, -1)], [(-1, 0)], [(-1, 1)]],
                 [[(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)],
                  [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)],
                  [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)],
                  [(1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7)],
                  [(0, -1), (0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7)],
                  [(-1, -1), (-2, -2), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7)],
                  [(-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0)],
                  [(-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7)]],
                 [[(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)],
                  [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)],
                  [(0, -1), (0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7)],
                  [(-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0)]],
                 [[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)],
                  [(1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7)],
                  [(-1, -1), (-2, -2), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7)],
                  [(-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7)]],
                 [[(1, 2)], [(-1, 2)], [(1, -2)], [(-1, -2)], [(2, 1)], [(-2, 1)], [(2, -1)], [(-2, -1)]],
                 [[(0, -1), (0, -2)]]]
# Chess square numbering is (x, y) (seen from top left) starting at 0 and ending at 7
initial_positions_b = [[(4, 0)], [(3, 0)], [(0, 0), (7, 0)], [(2, 0), (5, 0)], [(1, 0), (6, 0)],
                       [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]]
initial_positions_w = [[(4, 7)], [(3, 7)], [(0, 7), (7, 7)], [(2, 7), (5, 7)], [(1, 7), (6, 7)],
                       [(0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]]

pawn_capture_b = [(-1, 1), (1, 1)]    # these also appear in non-pawn pieces, but are not used in that case.
pawn_capture_w = [(-1, -1), (1, -1)]
