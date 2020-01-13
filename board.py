class Board():
    def __init__(self, score=None, move=None, board=None):
        self.score = score
        self.move = move
        self.board = board

        self.previous = None

    def __repr__(self):
        return str(self.move)