class Player:
    def __init__(self, color):
        self.color = color


class Piece:
    def __init__(self, name, img, rect, value, move, color, position, number, pawn):
        self.name = name
        self.img = img
        self.rect = rect
        self.value = value
        self.move = move
        self.color = color
        self.position = position
        self.number = number
        self.pawn = pawn
