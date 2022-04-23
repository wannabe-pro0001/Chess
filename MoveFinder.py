import random

pieceVal = {'K' : 0, 'Q' : 9, 'R': 6, 'B' : 3, 'N': 3, 'p' : 1}
CHECKMATE = 1000
STALEMATE = 0

def FindRandomMove(validMove):
    return random.choice(validMove)

def FindBestMove():
    return 

#evaluation 
'''
pieceVal = {'K' : 0, 'Q' : 9, 'R': 6, 'B' : 3, 'N': 3, 'p' : 1}
score += pieceVal[piece] * ([piece - piece']) #piece' stand for black other is white
        + 0.5(M - M')
        +

'''