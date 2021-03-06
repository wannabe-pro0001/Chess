"""This is the main file. This file handling user input and displaying the current game state object"""

from ctypes.wintypes import HICON
from sympy import true
import ChessEngine, MoveFinder, SmartMoveFinder
import pygame as p
import button

BOARD_WIDTH = BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WITDH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
BUTTON_PANEL_HEIGHT = 125
BUTTON_PANEL_WIDTH = BOARD_WIDTH + MOVE_LOG_PANEL_WITDH
BUTTON_PANEL_LOCATION_Y = BOARD_HEIGHT + BUTTON_PANEL_HEIGHT / 2
DIMENSION = 8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
new_button = None
next_button = None
back_button = None
exit_button = None

def label(x, y, infomation):
    #draw text with location(x, y)
    font = p.font.Font('freesansbold.ttf', 20)
    text = font.render(infomation, True, p.Color("blue"), None)
    textRect = text.get_rect()
    textRect.center = (x,y)
    return text, textRect

def resize(image, scale):
    '''resize sacle of image'''
    x = image.get_width()
    y = image.get_height()
    image = p.transform.scale(image, (x*scale, y*scale))
    return image

""" Initialize a global dictionaty images. And this is called only one"""
def LoadImages():
    #load piece image
    pieces = ['wR', 'wN', 'wB', 'wQ', 'wK', 'wp', 'bR', 'bN', 'bB', 'bQ', 'bK', 'bp']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + '.png'), (SQ_SIZE, SQ_SIZE))

def Load_button(screen, button_panel_location_x :int, button_panel_location_y :int, button_panel_width :int, button_panel_height :int):
        button_rect = p.Rect(button_panel_location_x, button_panel_location_y, button_panel_width, button_panel_height)
        p.draw.rect(screen, (0, 0, 0), button_rect)

        #load button images
        new_img = p.image.load('Form\\nutnew1.png').convert_alpha()
        back_img= p.image.load('Form\\nutback1.png').convert_alpha()
        exit_img = p.image.load('Form\\nutexit1.png').convert_alpha()
        next_img = p.image.load('Form\\nutnext1.png').convert_alpha()

        new_img = resize(new_img, 0.3)
        back_img = resize(back_img, 0.3)
        exit_img = resize(exit_img, 0.3)
        next_img = resize(next_img, 0.3)

        #create button instances
        new_button = button.Button(70, BOARD_HEIGHT+25, new_img, 0.8)
        back_button = button.Button(260, BOARD_HEIGHT+25, back_img, 0.8)
        exit_button = button.Button(450, BOARD_HEIGHT+25, exit_img, 0.8)
        next_button = button.Button(640, BOARD_HEIGHT+25, next_img, 0.8)

        #create labels
        new_text, new_rect = label(95, BOARD_HEIGHT+95, 'New')
        back_text, back_rect = label(285, BOARD_HEIGHT+95, 'Back')
        exit_text, exit_rect = label(475, BOARD_HEIGHT+95, 'Exit')
        next_text, next_rect = label(665, BOARD_HEIGHT+95, 'Next')

        screen.blit(new_text, new_rect)
        screen.blit(back_text, back_rect)
        screen.blit(exit_text, exit_rect)
        screen.blit(next_text, next_rect)

        return new_button, back_button, exit_button, next_button

"""The main driver for our code. This will handle user input and updating graphics"""
def main():
    p.init()
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WITDH, BOARD_HEIGHT + BUTTON_PANEL_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    LoadImages()
    new_button, back_button, exit_button, next_button = Load_button(screen, 0, BOARD_HEIGHT, BUTTON_PANEL_WIDTH, BUTTON_PANEL_HEIGHT)
    moveLogFont = p.font.SysFont("Arial", 15, False, False)
    running = True
    gs = ChessEngine.GameStart()
    validMove = gs.GetValidMove()
    moveMade = False #flag when move is made
    animate = False # flag when to animate move
    sqSelected = () #none of square is selected, keep tracking of the last click of the user(tuple (row, col))
    playerClicks = [] #keep tracking of player clicks (two tuple [(6, 4), (4, 4)])
    gameOver = False
    PlayerOne = True #If human is playing white then this will be true/ If an AI is playing this will be false
    PlayerTwo = False  #same as above but for black
    while running:
        for e in p.event.get():
            humanTurn = (gs.whiteToMove and PlayerOne) or (not gs.whiteToMove and PlayerTwo)
            if e.type == p.QUIT:
                running = False
            elif not gameOver and humanTurn:
                if e.type == p.MOUSEBUTTONDOWN:
                    location = p.mouse.get_pos() #(x, y) location of mouse
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sqSelected == (row, col) or col >= 8 or row >= 8: #if square is already choose
                        sqSelected = () #deselect it
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board) 
                        #print(move.GetChessNotation()) #use for debug
                        for i in range(len(validMove)):
                            if move == validMove[i]:
                                gs.makeMove(validMove[i])   #this move is not the same as validMove[i] so if we use move we can get some trouble with espassant or castlling move
                                moveMade = True
                                animate = True
                                sqSelected = () #reset user click
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
            #key handler
            if e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    moveMade, animate = Undo_game(gs, gameOver, PlayerOne, PlayerTwo)
                if e.key == p.K_r:
                    gameOver, humanTurn, gs, validMove, sqSelected, playerClicks, moveMade, animate = Reset_game()

            #button handler
            if new_button.draw(screen):
                gameOver, humanTurn, gs, validMove, sqSelected, playerClicks, moveMade, animate = Reset_game()
            if back_button.draw(screen):
                moveMade, animate = Undo_game(gs, gameOver, PlayerOne, PlayerTwo)
            if exit_button.draw(screen):
                running = False
            if next_button.draw(screen):
                print('next')

            #Ai finder move
            if not gameOver and not humanTurn:
                #move = SmartMoveFinder.findBestMove(gs, validMove)
                move = MoveFinder.AI.findBestMove(gs, validMove)
                if move is None:
                    #move = SmartMoveFinder.findRandomMove(validMove)
                    move = MoveFinder.AI.findRandomMove(validMove)
                gs.makeMove(move)
                moveMade = True
                animate = True

            if moveMade:
                if animate:
                    AnimateMove(gs.moveLog[-1], screen, gs.board, clock)
                validMove = gs.GetValidMove()
                moveMade = False
                animate = False

        drawGameState(screen, gs, validMove, sqSelected, moveLogFont)

        if gs.checkMate or gs.staleMate:
            gameOver = True
            DrawText(screen, "Stalemate" if gs.staleMate else 'Black win by checkmate' if gs.whiteToMove else 'White win by checkmate')
           
        clock.tick(MAX_FPS)
        p.display.flip()

def DrawHightLightSquare(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            #hight light selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) #transperancy value -> 0 transparent; 255 opaque
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            s.fill(p.Color('yellow')) #color of square that piece can move to
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    # circle = p.draw.circle(s, p.Color('green'), (move.endCol * SQ_SIZE + SQ_SIZE/2, move.endRow * SQ_SIZE - SQ_SIZE/2), SQ_SIZE/2, 3)
                    # s.blit(circle)
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE)) 

def drawGameState(screen, gs, validMoves, sqSelected, moveLogFont):
    DrawBoard(screen)   #draw square on the board
    #can draw hight light suare or move suggestion(later)
    DrawHightLightSquare(screen, gs, validMoves, sqSelected)
    DrawPieces(screen, gs.board) # draw pieces on top of those square
    DrawMoveLog(screen, gs, moveLogFont)

def DrawBoard(screen):
    """Draw the square on the board"""
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(SQ_SIZE*c, SQ_SIZE*r, SQ_SIZE, SQ_SIZE))

def DrawPieces(screen, board):
    """Draw the pieces on the board in the current gamestate.board"""
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(SQ_SIZE*c, SQ_SIZE*r, SQ_SIZE, SQ_SIZE))

def DrawText(screen, text):
    font = p.font.SysFont('Helvitca', 32, True, False)
    textObject = font.render(text, 0, p.Color('Blue'))
    textLocation = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH/2 - textObject.get_width()/2, BOARD_HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)

def DrawMoveLog(screen, gs, font):
    '''drawing text of move tracking all player or computer move'''
    moveLogRect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WITDH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, (100,100,100), moveLogRect)
    moveLog = gs.moveLog
    moveTexts = []
    for i in range(0, len(moveLog), 2):
        moveString = str(i//2 + 1) + "." + str(moveLog[i]) + " "
        if i+1 < len(moveLog):
            moveString += str(moveLog[i+1])
        moveTexts.append(moveString)

    # draw text 1. e4 2. Nc3 3. e5 4. Nxe5
    padding = 5;
    lineSpacing = 2
    movesPerRow = 3
    text_Y = padding
    for i in range(0, len(moveTexts), movesPerRow):
        text = ""
        for j in range(movesPerRow):
            if (i + j) < len(moveTexts):
                text += moveTexts[i+j] + " "*lineSpacing
        textObject = font.render(text, True, p.Color('White'))
        textLocation = moveLogRect.move(padding, text_Y)
        screen.blit(textObject, textLocation)
        text_Y += textObject.get_height() + lineSpacing

def Undo_game(gs, gameOver :bool, PlayerOne :bool, PlayerTwo :bool):
    '''Undo the move if next move is bot undo once more time'''
    if not gameOver:
        gs.undoMove()
    if not (gs.whiteToMove and PlayerOne) or (not gs.whiteToMove and PlayerTwo):
        gs.undoMove()
    return True, False #return moveMade and animate

def Reset_game():
    '''reset the game'''
    gameOver = False
    humanTurn = True
    gs = ChessEngine.GameStart()
    validMove = gs.GetValidMove()
    sqSelected = ()
    playerClicks = []
    moveMade = False
    animate = False
    return gameOver, humanTurn, gs, validMove, sqSelected, playerClicks, moveMade, animate

def Exit_game():
    pass

def blit_alpha(target, source, location, opacity):
    ''' Fade out captured piece
    Source: https://nerdparadise.com/programming/pygameblitopacity 
    '''
    x = location[0]
    y = location[1]
    temp = p.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)        
    target.blit(temp, location)

def AnimateMove(move, screen, board, clock):
    '''Draw animate move'''
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framePerSquare = 3 #frames to move one square
    frameCount = (abs(dR) + abs(dC))*framePerSquare
    for frame in range(frameCount+1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        alpha = 255 - int(255 * frame/frameCount)
        DrawBoard(screen)
        DrawPieces(screen, board)
        #erease the piece from ending square
        alpha = 255 - 255*(frame/frameCount)
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        #draw capture piece onto rectangle
        if move.pieceCaptured != '--':
            if move.isEnpassant:
                enPassantRow = move.endRow + 1 if move.pieceCaptured[0] == 'b' else move.endRow - 1
                endSquare.top = enPassantRow * SQ_SIZE;
            blit_alpha(screen, IMAGES[move.pieceCaptured], endSquare, alpha)
            #screen.blit(IMAGES[move.pieceCaptured], endSquare)
        #draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()