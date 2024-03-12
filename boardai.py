import pieces
from move import Move

class Boardai:

    WIDTH = 8
    HEIGHT = 8

    def __init__(self, chesspieces, white_king_moved, black_king_moved):
        self.chesspieces = chesspieces
        self.white_king_moved = white_king_moved
        self.black_king_moved = black_king_moved

    @classmethod
    def clone(cls, chessboardai):
        chesspieces = [[0 for x in range(Boardai.WIDTH)] for y in range(Boardai.HEIGHT)]
        for x in range(Boardai.WIDTH):
            for y in range(Boardai.HEIGHT):
                piece = chessboardai.chesspieces[x][y]
                if (piece != 0):
                    chesspieces[x][y] = piece.clone()
        return cls(chesspieces, chessboardai.white_king_moved, chessboardai.black_king_moved)

    @classmethod
    def new(cls):
        chess_pieces = [[0 for x in range(Boardai.WIDTH)] for y in range(Boardai.HEIGHT)]
        # Create pawns.
        for x in range(Boardai.WIDTH):
            chess_pieces[x][Boardai.HEIGHT-2] = pieces.Pawn(x, Boardai.HEIGHT-2, pieces.Piece.WHITE, id="WhitePawn_"+str(x))
            chess_pieces[x][1] = pieces.Pawn(x, 1, pieces.Piece.BLACK, id="BlackPawn_"+str(x))

        # Create rooks.
        chess_pieces[0][Boardai.HEIGHT-1] = pieces.Rook(0, Boardai.HEIGHT-1, pieces.Piece.WHITE, id="WhiteRook_0")
        chess_pieces[Boardai.WIDTH-1][Boardai.HEIGHT-1] = pieces.Rook(Boardai.WIDTH-1, Boardai.HEIGHT-1, pieces.Piece.WHITE, id="WhiteRook_1")
        chess_pieces[0][0] = pieces.Rook(0, 0, pieces.Piece.BLACK, id="BlackRook_0")
        chess_pieces[Boardai.WIDTH-1][0] = pieces.Rook(Boardai.WIDTH-1, 0, pieces.Piece.BLACK, id="BlackRook_1")

        # Create Knights.
        chess_pieces[1][Boardai.HEIGHT-1] = pieces.Knight(1, Boardai.HEIGHT-1, pieces.Piece.WHITE, id="WhiteKnight_0")
        chess_pieces[Boardai.WIDTH-2][Boardai.HEIGHT-1] = pieces.Knight(Boardai.WIDTH-2, Boardai.HEIGHT-1, pieces.Piece.WHITE, id="WhiteKnight_1")
        chess_pieces[1][0] = pieces.Knight(1, 0, pieces.Piece.BLACK, id="BlackKnight_0")
        chess_pieces[Boardai.WIDTH-2][0] = pieces.Knight(Boardai.WIDTH-2, 0, pieces.Piece.BLACK, id="BlackKnight_1")
        
        # Create Bishops.
        chess_pieces[2][Boardai.HEIGHT-1] = pieces.Bishop(2, Boardai.HEIGHT-1, pieces.Piece.WHITE, id="WhiteBishop_0")
        chess_pieces[Boardai.WIDTH-3][Boardai.HEIGHT-1] = pieces.Bishop(Boardai.WIDTH-3, Boardai.HEIGHT-1, pieces.Piece.WHITE, id="WhiteBishop_1")
        chess_pieces[2][0] = pieces.Bishop(2, 0, pieces.Piece.BLACK, id="BlackBishop_0")
        chess_pieces[Boardai.WIDTH-3][0] = pieces.Bishop(Boardai.WIDTH-3, 0, pieces.Piece.BLACK, id="BlackBishop_1")

        # Create King & Queen.
        chess_pieces[4][Boardai.HEIGHT-1] = pieces.King(4, Boardai.HEIGHT-1, pieces.Piece.WHITE, id="WhiteKing")
        chess_pieces[3][Boardai.HEIGHT-1] = pieces.Queen(3, Boardai.HEIGHT-1, pieces.Piece.WHITE, id="WhiteQueen")
        chess_pieces[4][0] = pieces.King(4, 0, pieces.Piece.BLACK, id="BlackKing")
        chess_pieces[3][0] = pieces.Queen(3, 0, pieces.Piece.BLACK, id="BlackQueen")

        return cls(chess_pieces, False, False)

    def get_possible_moves(self, color):
        moves = []
        for x in range(Boardai.WIDTH):
            for y in range(Boardai.HEIGHT):
                piece = self.chesspieces[x][y]
                if (piece != 0):
                    if (piece.color == color):
                        moves += piece.get_possible_moves(self)

        return moves

    def perform_move(self, move):
        piece = self.chesspieces[move.xfrom][move.yfrom]
        self.move_piece(piece, move.xto, move.yto)

        # If a pawn reaches the end, upgrade it to a queen.
        if (piece.piece_type == pieces.Pawn.PIECE_TYPE):
            if (piece.y == 0 or piece.y == Boardai.HEIGHT-1):
                self.chesspieces[piece.x][piece.y] = pieces.Queen(piece.x, piece.y, piece.color)

        if (piece.piece_type == pieces.King.PIECE_TYPE):
            # Mark the king as having moved.
            if (piece.color == pieces.Piece.WHITE):
                self.white_king_moved = True
            else:
                self.black_king_moved = True
            
            # Check if king-side castling
            if (move.xto - move.xfrom == 2):
                rook = self.chesspieces[piece.x+1][piece.y]
                self.move_piece(rook, piece.x-1, piece.y)
            # Check if queen-side castling
            if (move.xto - move.xfrom == -2):
                rook = self.chesspieces[piece.x-2][piece.y]
                self.move_piece(rook, piece.x+1, piece.y)
    
    def move_piece(self, piece, xto, yto):
        self.chesspieces[piece.x][piece.y] = 0
        piece.x = xto
        piece.y = yto

        self.chesspieces[xto][yto] = piece


    # Returns if the given color is checked.
    def is_check(self, color):
        other_color = pieces.Piece.WHITE
        if (color == pieces.Piece.WHITE):
            other_color = pieces.Piece.BLACK

        for move in self.get_possible_moves(other_color):
            copy = Boardai.clone(self)
            copy.perform_move(move)

            king_found = False
            for x in range(Boardai.WIDTH):
                for y in range(Boardai.HEIGHT):
                    piece = copy.chesspieces[x][y]
                    if (piece != 0):
                        if (piece.color == color and piece.piece_type == pieces.King.PIECE_TYPE):
                            king_found = True

            if (not king_found):
                return True

        return False

    # Returns piece at given position or 0 if: No piece or out of bounds.
    def get_piece(self, x, y):
        if (not self.in_bounds(x, y)):
            return 0

        return self.chesspieces[x][y]

    def in_bounds(self, x, y):
        return (x >= 0 and y >= 0 and x < Boardai.WIDTH and y < Boardai.HEIGHT)

    def to_string(self):
        string =  "    A  B  C  D  E  F  G  H\n"
        string += "    -----------------------\n"
        for y in range(Boardai.HEIGHT):
            string += str(8 - y) + " | "
            for x in range(Boardai.WIDTH):
                piece = self.chesspieces[x][y]
                if (piece != 0):
                    string += piece.to_string()
                else:
                    string += ".. "
            string += "\n"
        return string + "\n"
