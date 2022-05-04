import random
import numpy

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3

class Heuristics:
    pieceScore = {'K' : 200, 'Q' : 9, 'R': 5, 'B' : 3.2, 'N': 3, 'p' : 1}

    PAWN_TABLE = numpy.array([
            [100, 100, 100, 100, 100,  100,  100,  100],
            [ 50,  50,  50,  50,  50, 50, 50, 50],
            [ 10,  10,  20,  40,  40, 20, 10, 10],
            [  5,   5,  10,  35,  35, 10,  5,  5],
            [  0,   0,   0,  30,  30,  0,  0,  0],
            [  5,  -5, -10,   0,   0,-10, -5,  5],
            [  5,  10,  10, -30, -30, 10, 10,  5],
            [  0,   0,   0,   0,   0,  0,  0,  0]
        ])

    KNIGHT_TABLE = numpy.array([
            [-50, -40, -30, -30, -30, -30, -40, -50],
            [-40, -20,   0,   5,   5,   0, -20, -40],
            [-30,   5,  10,  15,  15,  10,   5, -30],
            [-30,   0,  15,  20,  20,  15,   0, -30],
            [-30,   0,  15,  20,  20,  15,   0, -30],
            [-30,   5,  10,  15,  15,  10,   5, -30],
            [-40, -20,   0,   0,   0,   0, -20, -40],
            [-50, -40, -30, -30, -30, -30, -40, -50]
        ])

    BISHOP_TABLE = numpy.array([
            [-20, -10, -10, -10, -10, -10, -10, -20],
            [-10,   5,   0,   0,   0,   0,   5, -10],
            [-10,  10,  10,  10,  10,  10,  10, -10],
            [-10,   0,  10,  10,  10,  10,   0, -10],
            [-10,   5,   5,  10,  10,   5,   5, -10],
            [-10,   0,   5,  10,  10,   5,   0, -10],
            [-10,   0,   0,   0,   0,   0,   0, -10],
            [-20, -10, -10, -10, -10, -10, -10, -20]
        ])

    ROOK_TABLE = numpy.array([
            [ 0,  0,  0,  5,  5,  0,  0,  0],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [ 5, 10, 10, 10, 10, 10, 10,  5],
            [ 0,  0,  0,  0,  0,  0,  0,  0]
        ])

    QUEEN_TABLE = numpy.array([
            [-20, -10, -10, -5, -5, -10, -10, -20],
            [-10,   0,   5,  0,  0,   0,   0, -10],
            [-10,   5,   5,  5,  5,   5,   0, -10],
            [  0,   0,   5,  5,  5,   5,   0,  -5],
            [ -5,   0,   5,  5,  5,   5,   0,  -5],
            [-10,   0,   5,  5,  5,   5,   0, -10],
            [-10,   0,   0,  0,  0,   0,   0, -10],
            [-20, -10, -10, -5, -5, -10, -10, -20]
        ])

    @staticmethod
    def evaluate(board):
        ''' evaluation
        score += pieceVal[piece] * ([piece - piece']) #piece' stand for black other is white
            + 0.5(M - M') m stand for number of move
            +
        '''
        material = Heuristics.get_material_score(board)

        pawns = Heuristics.get_piece_position_score(board, 'p', Heuristics.PAWN_TABLE)
        knights = Heuristics.get_piece_position_score(board, 'N', Heuristics.KNIGHT_TABLE)
        bishops = Heuristics.get_piece_position_score(board, 'B', Heuristics.BISHOP_TABLE)
        rooks = Heuristics.get_piece_position_score(board, 'R', Heuristics.ROOK_TABLE)
        queens = Heuristics.get_piece_position_score(board, 'Q', Heuristics.QUEEN_TABLE)

        return material + pawns + knights + bishops + rooks + queens
    
    @staticmethod
    def get_piece_position_score(board, piece_type, table):
        white = 0
        black = 0
        for row in range(len(board)):
            for col in range(len(board[row])):
                piece = board[row][col]
                if (piece != "--"):
                    if (piece[1] == piece_type):
                        if (piece[0] == 'w'):
                            white += table[row][col] * .01
                        else:
                            black += table[7-row][col] * .01
        return white - black

    @staticmethod
    def get_material_score(board):
        white = 0
        black = 0
        for row in range(len(board)):
            for col in range(len(board[row])):
                piece = board[row][col]
                if (piece != "--"): 
                    if (piece[0] == 'w'):
                        white += Heuristics.pieceScore[piece[1]]
                    else:
                        black += Heuristics.pieceScore[piece[1]]

        return white - black
    
    '''
    A positive score is good for white, a negative score is good for black.
    '''
    def scoreBoard(self, gs):
        if gs.checkMate:
            if gs.whiteToMove:
                return -CHECKMATE #black wins
            else:
                return CHECKMATE #white wins
        elif gs.staleMate:
            return self.STALEMATE
        
        score = 0
        for row in gs.board:
            for square in row:
                if square[0] == 'w':
                    score += self.pieceScore[square[1]]
                elif square[0] == 'b':
                    score -= self.pieceScore[square[1]] 
        return score    

    '''
    Score the board based on material.
    '''
    def scoreMaterial(self, board):
        score = 0
        for row in board:
            for square in row:
                if square[0] == 'w':
                    score += self.pieceScore[square[1]]
                elif square[0] == 'b':
                    score -= self.pieceScore[square[1]] 
        return score   

class AI:
    INFINITE = CHECKMATE

    def findRandomMove(validMove):
        return random.choice(validMove)

    '''
    Helper method to make first recursive call
    '''
    @staticmethod
    def findBestMove(gs, validMoves):
        global nextMove, counter
        nextMove = None
        random.shuffle(validMoves)
        counter = 0 
        AI.findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -AI.INFINITE, AI.INFINITE, 1 if gs.whiteToMove else -1)
        #print(counter)
        return nextMove

    @staticmethod
    def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
        global nextMove, counter
        counter += 1
        if depth == 0:
            return turnMultiplier * Heuristics.evaluate(gs.board)
        
        # move ordering - implement later 
        maxScore = -AI.INFINITE if turnMultiplier else AI.INFINITE
        for move in validMoves:
            gs.makeMove(move)
            validMove = gs.GetValidMove()
            score = -AI.findMoveNegaMaxAlphaBeta(gs, validMove, depth - 1, -beta, -alpha, -turnMultiplier)
            if score > maxScore:
                maxScore = score 
                if depth == DEPTH:
                    print(str(move) + " " + str(maxScore))
                    nextMove = move
            gs.undoMove()
            if maxScore > alpha: #pruning happens
                alpha = maxScore
            if alpha >= beta:
                break
        return maxScore

        #from geek code minimax algorithm
        # if turnMultiplier == 1:
        #     maxScore = -AI.INFINITE
        #     for move in validMoves:
        #         gs.makeMove(move)
        #         validMove = gs.GetValidMove()
        #         score = AI.findMoveNegaMaxAlphaBeta(gs, validMove, depth - 1, alpha, beta, -turnMultiplier)
        #         maxScore = max(maxScore, score)
        #         alpha = max(maxScore, alpha)
        #         gs.undoMove()
        #         if beta <= alpha:
        #             break
        #     return maxScore
        # else:
        #     maxScore = AI.INFINITE
        #     for move in validMoves:
        #         gs.makeMove(move)
        #         validMove = gs.GetValidMove()
        #         score = AI.findMoveNegaMaxAlphaBeta(gs, validMove, depth - 1, alpha, beta, turnMultiplier)
        #         maxScore = min(maxScore, score)
        #         beta = min(maxScore, beta)
        #         gs.undoMove()
        #         if beta <= alpha:
        #             break
        # return maxScore