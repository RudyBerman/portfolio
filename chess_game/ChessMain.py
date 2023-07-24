"""
Main driver file. Responsible for handling user input and displaying current gamestate
"""

import pygame as p

from Chess.chess import ChessEngine

WIDTH = HEIGHT = 512 # power of 2 so useful
DIMENSION = 8 # dimensions of chess board are 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 # for animations later on
IMAGES = {}

"""
Initialise global dictionary of images. This will only be called once in the main
"""

def load_images():
    pieces = ["wP", "wR", "wN", "wB", "wK", "wQ", "bP", "bR", "bN", "bB", "bK", "bQ"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # can now access image using this dictionary

"""
Main driver to handle user input and update board
"""

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    valid_moves = gs.get_valid_moves()
    move_made = False
    animate = False

    load_images() # do this once, before while loop
    running = True
    sq_selected = () # no square is initially selected, tuple: (row, col)
    player_clicks = [] # list of 2 tuples: [(6, 4), (4, 4)]

    while running:
        # if gs.checkmate:
        #     print("CHECKMATE")
        # elif gs.stalemate:
        #     print("STALEMATE")
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.KEYDOWN: # for undoing moves
                if e.key == p.K_z:
                    print(gs.move_log[-1].piece_moved, gs.move_log[-1].piece_captured)
                    gs.undo_move()
                    move_made = True
                    animate = False
                    # print(gs.white_to_move)
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # (x, y) location of mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sq_selected == (row, col): # if clicked on already selected square
                    sq_selected = ()
                    player_clicks = []
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected) # append for both first and second clicks

                if len(player_clicks) == 2: # for making moves
                    move = ChessEngine.Move(player_clicks[0], player_clicks[1], gs.board)
                    # print("CASLTE" if move.is_castle else "")
                    for i in range(len(valid_moves)):
                        if move == valid_moves[i]:
                            if valid_moves[i].pawn_promotion:
                                choice = input("Please choose a piece to promote to (Q, R, B, N): ")
                                gs.make_move(valid_moves[i], choice=choice)
                            else:
                                gs.make_move(valid_moves[i])
                            move_made = True
                            animate = True
                            sq_selected = () # reset user clicks
                            player_clicks = []
                            break
                    if not move_made:
                        player_clicks = [sq_selected]

            if move_made: # if game state has changed, get new set of valid moves
                if animate:
                    animate_move(gs.move_log[-1], screen, gs.board, clock)
                valid_moves = gs.get_valid_moves()
                move_made = False
                animate = False

        draw_game_state(screen, gs, valid_moves, sq_selected)
        clock.tick(MAX_FPS)
        p.display.flip()

"""
highlight potential moves and display results
"""
def highlight_squares(screen, gs, valid_moves, sq_selected):
    if sq_selected != ():
        row, col = sq_selected
        if gs.board[row][col][0] == ("w" if gs.white_to_move else "b"):
            # highlight selected squares
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) # transparency
            s.fill(p.Color("blue"))
            screen.blit(s, (col*SQ_SIZE, row*SQ_SIZE))
            s.fill(p.Color("yellow"))
            for move in valid_moves:
                if move.start_row == row and move.start_col == col:
                    screen.blit(s, (move.end_col*SQ_SIZE, move.end_row*SQ_SIZE))


"""
Responsible for all graphics in current gamestate
"""
def draw_game_state(screen, gs, valid_moves, sq_selected):
    draw_board(screen)
    highlight_squares(screen, gs, valid_moves, sq_selected)
    draw_piece(screen, gs.board)

def draw_board(screen):
    global colours
    colours = [p.Color("white"), p.Color("gray")]
    for x in range(DIMENSION):
        for y in range(DIMENSION):
            c = colours[((x + y) % 2) ]
            p.draw.rect(screen, c, (y*SQ_SIZE, x*SQ_SIZE, SQ_SIZE, SQ_SIZE))

    # draw indexing for ranks
    for i in range(DIMENSION):
        rank_colour = "white" if (i % 2 != 0) else "gray"
        font = p.font.SysFont(None, 20) # set font
        rank_img = font.render(str(8 - i), True, rank_colour) # render image from text
        screen.blit(rank_img, (2, i * SQ_SIZE)) # add ranks
        file_colour = "white" if (i % 2 == 0) else "gray"
        file_img = font.render(chr(i + 97), True, file_colour) # use ASCII to get characters
        screen.blit(file_img, ((i + 1) * SQ_SIZE - 8, 500)) # add files

"""
animating a move
"""
def animate_move(move, screen, board, clock):
    pass
    # global colours
    # dR = move.end_row - move.start_row
    # dC = move.end_col - move.start_col
    # frames_per_square = 10
    # frame_count = (abs(dR) + abs(dC)) * frames_per_square
    # for frame in range(frame_count + 1):
    #     r, c = (move.start_row + dR*(frame/frame_count), move.start_col + dC*(frame/frame_count))
    #     draw_board(screen)
    #     draw_piece(screen, board)
    #     # erase piece moved from its ending square
    #     colour = colours[((move.end_row + move.end_col) % 2)]
    #     end_square = p.Rect(move.end_col*SQ_SIZE, move.end_row*SQ_SIZE, SQ_SIZE, SQ_SIZE)
    #     p.draw.rect(screen, colour, end_square)
    #     # drawn captured piece back
    #     if move.piece_captured != " ":
    #         screen.blit(IMAGES[move.piece_captured], end_square)
    #     # draw moving piece
    #     screen.blit(IMAGES[move.piece_moved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    #     # print("PIECE MOVED:", move.piece_moved)
    #     p.display.flip()
    #     clock.tick(1000)


def draw_piece(screen, board):
    for x in range(DIMENSION):
        for y in range(DIMENSION):
            piece = board[x][y]
            if piece != " ":
                if x == 6:
                    print(piece, y)
                screen.blit(IMAGES[piece], p.Rect(y*SQ_SIZE, x*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == '__main__':
    main()
