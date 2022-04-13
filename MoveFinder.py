import random

pieceVal = {'K' : 0, 'Q' : 9, 'R': 6, 'B' : 3, 'N': 3, 'p' : 1}
CHECKMATE = 1000
STALEMATE = 0

def FindRandomMove(validMove):
    return random.choice(validMove)

def FindBestMove():
    return 