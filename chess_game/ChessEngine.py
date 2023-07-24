"""
Stores information about current gamestate and is responsible for determining valid moves. Keeps move log
"""
import numpy as np

class GameState():
    def __init__(self):
        # 8x8 board, 2D numpy array, each element has 2 characters
        # first character denotes colour, second character denotes piece
        # " " denotes empty tile on chess board
        self.board = np.array([
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ])
        self.move_functions = {"P": self.get_pawn_moves, "R": self.get_rook_moves,
                               "N": self.get_knight_moves, "B": self.get_bishop_moves,
                               "K": self.get_king_moves, "Q": self.get_queen_moves}
        self.white_to_move = True
        self.move_log = []
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.enpassant_possible = ()
        self.current_castling_rights = CastlingRights(True, True, True, True)
        self.castling_rights_log = [CastlingRights(self.current_castling_rights.wks,
                                                   self.current_castling_rights.wqs,
                                                   self.current_castling_rights.bks,
                                                   self.current_castling_rights.bqs)]

    """
    takes move as a parameter and executes it (this will not work for castling, en passant, or pawn promotion)
    """

    def make_move(self, move, choice=None):
        self.board[move.start_row][move.start_col] = " "
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)  # log move so can view it later
        self.white_to_move = not self.white_to_move
        # update kings location
        if move.piece_moved == "wK":
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == "bK":
            self.black_king_location = (move.end_row, move.end_col)

        # pawn promotion
        if move.pawn_promotion and choice is not None: # true if pawn promotion and player has entered input
            self.board[move.end_row][move.end_col] = move.piece_moved[0] + choice

        if move.enpassant:
            self.board[move.end_row][move.end_col] = move.piece_moved
            self.board[move.start_row][move.end_col] = " " # capturing pawn

        # update our enpassant_possible field
        if move.piece_moved[1] == "P" and abs(move.start_row - move.end_row) == 2:
            self.enpassant_possible = ((move.start_row + move.end_row)//2, move.start_col)
        else:
            self.enpassant_possible = ()

        # castling move
        if move.is_castle:
            if move.end_col - move.start_col == 2: # king side
                self.board[move.end_row][move.end_col - 1] = self.board[move.end_row][move.end_col + 1]
                self.board[move.end_row][move.end_col + 1] = " "
            else: # queen side
                self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 2]
                self.board[move.end_row][move.end_col - 2] = " "


        # update castling rights
        self.update_castling_rights(move)
        self.castling_rights_log.append(CastlingRights(self.current_castling_rights.wks,
                                                       self.current_castling_rights.wqs,
                                                       self.current_castling_rights.bks,
                                                       self.current_castling_rights.bqs))

    """
    write function to undo last move
    """

    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            print("INDS", move.start_row, move.end_row)
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move
            # update kings position
            if move.piece_moved == "wK":
                self.white_king_location = (move.start_row, move.start_col)
            elif move.piece_moved == "bK":
                self.black_king_location = (move.start_row, move.start_col)

            # undo enpassant
            if move.enpassant and move.piece_captured != " ": # only if capture occurs
                print("YAYAYAYAYA EN PASSANT")
                print(move.piece_captured)
                print(move.piece_moved)
                print(move.start_row, move.start_col)
                print(move.end_row, move.end_col)
                self.board[move.end_row][move.end_col] = " " # reset landing square to blank
                self.board[move.start_row][move.end_col] = move.piece_captured
                self.enpassant_possible = (move.end_row, move.end_col)

            # undo two square pawn advance
            print("NEXT:", move.piece_moved, move.start_row, move.end_row)
            if move.piece_moved[1] == "P" and abs(move.start_row - move.end_row) == 2:
                self.enpassant_possible = ()

            #undo castling rights
            self.castling_rights_log.pop() # remove last castling rights
            new_rights = self.castling_rights_log[-1] # update current
            self.current_castling_rights = CastlingRights(new_rights.wks, new_rights.wqs,
                                                          new_rights.bks, new_rights.bqs)

            # undo castle move
            if move.is_castle:
                if move.end_col - move.start_col == 2: # king side
                    self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 1]
                    self.board[move.end_row][move.end_col - 1] = " "
                else: # queen side
                    self.board[move.end_row][move.end_col - 2] = self.board[move.end_row][move.end_col + 1]
                    self.board[move.end_row][move.end_col + 1] = " "

    def update_castling_rights(self, move):
        if move.piece_moved == "wK":
            self.current_castling_rights.wks = False
            self.current_castling_rights.wqs = False
        elif move.piece_moved[1] == "wR":
            if move.start_row == 7:
                if move.start_col == 0:
                    self.current_castling_rights.wqs = False
                elif move.start_col == 7:
                    self.current_castling_rights.wks = False
        elif move.piece_moved[0] == "bK":
            self.current_castling_rights.bks = False
            self.current_castling_rights.bqs = False
        elif move.piece_moved[1] == "bR":
            if move.start_row == 0:
                if move.start_col == 0:
                    self.current_castling_rights.bqs = False
                elif move.start_col == 7:
                    self.current_castling_rights.bks = False

    """
    get all moves considering checks
    """

    def get_valid_moves(self):
        temp_enpassant_possible = self.enpassant_possible # store copy
        temp_castling_rights = CastlingRights(self.current_castling_rights.wks,
                                              self.current_castling_rights.wqs,
                                              self.current_castling_rights.bks,
                                              self.current_castling_rights.bqs)
        # get all possible moves
        moves = self.get_possible_moves()
        if self.white_to_move:
            self.get_castle_moves(self.white_king_location[0], self.white_king_location[1], moves)
        else:
            self.get_castle_moves(self.black_king_location[0], self.black_king_location[1], moves)
        # make all possible moves, getting the set of possible next moves for each
        for i in range(len(moves) - 1, -1, -1):  # go through list backwards to remove indexing issue when removing items
            self.make_move(moves[i])
            self.white_to_move = not self.white_to_move  # switch turns for in_check function
            if self.in_check():
                moves.remove(moves[i])
            self.white_to_move = not self.white_to_move  # switch back again
            self.undo_move()
        # see if stalemate or checkmate
        if len(moves) == 0:
            if self.in_check():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False

        self.enpassant_possible = temp_enpassant_possible # reset variable
        self.current_castling_rights = temp_castling_rights # reset
        return moves

    """
    determine if current player is under attack
    """

    def in_check(self):
        if self.white_to_move:
            return self.square_under_attack(self.white_king_location[0], self.white_king_location[1])
        else:
            return self.square_under_attack(self.black_king_location[0], self.black_king_location[1])

    """
    determine if enemy can attack square (row, col)
    """

    def square_under_attack(self, row, col):
        self.white_to_move = not self.white_to_move  # perspective of opponent
        next_moves = self.get_possible_moves()  # get opponents moves
        self.white_to_move = not self.white_to_move  # switch turns back
        for move in next_moves:
            if move.end_row == row and move.end_col == col:
                return True
        return False

    """
    get all moves without considering checks
    """

    def get_possible_moves(self):
        moves = []
        for row in range(len(self.board)):  # number of rows
            for col in range(len(self.board[row])):  # number of columns in given row
                turn = self.board[row][col][0]  # 'w', 'b', or ' '
                if (turn == "w" and self.white_to_move) or (turn == "b" and not self.white_to_move):
                    piece = self.board[row][col][1]  # either P, R, N, B, Q, K, or " "
                    self.move_functions[piece](row, col, moves)  # calls appropriate function
        return moves

    """
    make functions to get moves for each piece
    """

    def get_pawn_moves(self, row, col, moves):
        if self.white_to_move:  # white pawn moves
            if self.board[row - 1][col] == " ":  # one square pawn advance
                moves.append(Move((row, col), (row - 1, col), self.board))
                if row == 6 and self.board[row - 2][col] == " ":  # two square pawn advance
                    moves.append(Move((row, col), (row - 2, col), self.board))
            if col >= 1:  # captures to left
                if self.board[row - 1][col - 1][0] == 'b':
                    moves.append(Move((row, col), (row - 1, col - 1), self.board))
                elif (row - 1, col - 1) == self.enpassant_possible:
                    moves.append(Move((row, col), (row - 1, col - 1), self.board, is_enpassant=True))
            if col <= 6:  # captures to right
                if self.board[row - 1][col + 1][0] == 'b':
                    moves.append(Move((row, col), (row - 1, col + 1), self.board))
                elif (row - 1, col + 1) == self.enpassant_possible:
                    moves.append(Move((row, col), (row - 1, col + 1), self.board, is_enpassant=True))
        elif row + 1 <= 7:  # black pieces (remove indexing issue)
            if self.board[row + 1][col] == " ":  # one square pawn advance for black
                moves.append(Move((row, col), (row + 1, col), self.board))
                if row == 1 and self.board[row + 2][col] == " ":  # two square pawn advance
                    moves.append(Move((row, col), (row + 2, col), self.board))
            if col >= 1:  # captures to left
                if self.board[row + 1][col - 1][0] == 'w':
                    moves.append(Move((row, col), (row + 1, col - 1), self.board))
                elif (row + 1, col - 1) == self.enpassant_possible:
                    moves.append(Move((row, col), (row + 1, col - 1), self.board, is_enpassant=True))
            if col <= 6:  # captures to right
                if self.board[row + 1][col + 1][0] == 'w':
                    moves.append(Move((row, col), (row + 1, col + 1), self.board))
                elif (row + 1, col + 1) == self.enpassant_possible:
                    moves.append(Move((row, col), (row + 1, col + 1), self.board, is_enpassant=True))

    def get_rook_moves(self, row, col, moves):
        directions = ((-1, 0), (1, 0), (0, -1), (0, 1))  # up, down, left, right
        for d in directions:
            for i in range(1, 8):
                current_row = row + d[0] * i
                current_col = col + d[1] * i
                if 0 <= current_row < 8 and 0 <= current_col < 8:
                    if self.board[current_row][current_col] == " ":  # empty tile
                        moves.append(Move((row, col), (current_row, current_col), self.board))
                    elif self.board[current_row][current_col][0] != self.board[row][col][0]:  # opposite colour
                        moves.append(Move((row, col), (current_row, current_col), self.board))
                        break
                    else:  # piece of same colour
                        break
                else:  # gone off edge of board
                    break

    def get_knight_moves(self, row, col, moves):
        directions = ((1, 1), (1, -1), (-1, -1), (-1, 1))  # splits knight moves into quadrants, (row, col)
        for d in directions:
            if (
                    (0 <= row + d[0] * 1 < 8 and 0 <= col + d[1] * 2 < 8) and
                    self.board[row + d[0] * 1][col + d[1] * 2][0] != self.board[row][col][0]
            ):  # if both coordinates are on board
                moves.append(Move((row, col), (row + d[0] * 1, col + d[1] * 2), self.board))
            if (
                    (0 <= row + d[0] * 2 < 8 and 0 <= col + d[1] * 1 < 8) and
                    self.board[row + d[0] * 2][col + d[1] * 1 ][0] != self.board[row][col][0]
            ):  # second possible move in quadrant
                moves.append(Move((row, col), (row + d[0] * 2, col + d[1] * 1), self.board))

    def get_bishop_moves(self, row, col, moves):
        directions = ((1, 1), (1, -1), (-1, -1), (-1, 1))  # direction (row, col)
        for d in directions:
            for i in range(1, 8):
                current_row = row + d[0] * i
                current_col = col + d[1] * i
                if 0 <= current_row < 8 and 0 <= current_col < 8:
                    if self.board[current_row][current_col] == " ":  # empty tile
                        moves.append(Move((row, col), (current_row, current_col), self.board))
                    elif self.board[current_row][current_col][0] != self.board[row][col][0]:  # opposite colour
                        moves.append(Move((row, col), (current_row, current_col), self.board))
                        break
                    else:  # piece of same colour
                        break
                else:  # gone off edge of board
                    break

    def get_king_moves(self, row, col, moves):
        directions = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))  # (row, col)
        for d in directions:
            current_row = row + d[0]
            current_col = col + d[1]
            if (
                    0 <= current_row < 8 and 0 <= current_col < 8 and
                    self.board[current_row][current_col][0] != self.board[row][col][0]
            ):
                moves.append(Move((row, col), (current_row, current_col), self.board))

    def get_castle_moves(self, row, col, moves):
        if self.square_under_attack(row, col):
            return
        if (self.white_to_move and self.current_castling_rights.wks) or (not self.white_to_move and self.current_castling_rights.bks):
            self.get_KS_castle_moves(row, col, moves)
        if (self.white_to_move and self.current_castling_rights.wqs) or (not self.white_to_move and self.current_castling_rights.bqs):
            self.get_QS_castle_moves(row, col, moves)

    def get_KS_castle_moves(self, row, col, moves):
        if self.board[row][col + 1] == " " and self.board[row][col + 2] == " ":
            if not self.square_under_attack(row, col+1) and not self.square_under_attack(row, col+2):
                moves.append(Move((row, col), (row, col+2), self.board, is_castle=True))

    def get_QS_castle_moves(self, row, col, moves):
        if self.board[row][col - 1] == " " and self.board[row][col - 2] == " " and self.board[row][col - 3] == " ":
            if not self.square_under_attack(row, col-1) and not self.square_under_attack(row, col-2):
                moves.append(Move((row, col), (row, col-2), self.board, is_castle=True))


    def get_queen_moves(self, row, col, moves):
        self.get_rook_moves(row, col, moves)
        self.get_bishop_moves(row, col, moves)

class CastlingRights():
    def __init__(self, wks, wqs, bks, bqs): # 'white king side', 'white queen side', ...
        self.wks = wks
        self.wqs = wqs
        self.bks = bks
        self.bqs = bqs

class Move():
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}

    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_sq, end_sq, board, is_enpassant=False, is_castle=False):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        # pawn promotion
        self.pawn_promotion = (self.piece_moved == "wP" and self.end_row == 0) or (self.piece_moved == "bP" and self.end_row == 7)
        # en passant
        self.enpassant = is_enpassant
        if self.enpassant:
            self.piece_captured = "wP" if self.piece_moved == "bP" else "bP"

        self.is_castle = is_castle

        self.moveID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col



    """
    overriding the equals method
    """

    def __eq__(self, other):
        if isinstance(other, Move):
            return other.moveID == self.moveID

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]
