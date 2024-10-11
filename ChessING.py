import chess as ch
import random as rd

class Engine:
    def __init__(self, board, maxDepth, color):
        self.board = board
        self.color = color
        self.maxDepth = maxDepth
    
    def getBestMove(self):
        return self.engine(None, 1, float("-inf"), float("inf"))

    def evalFunct(self):
        compt = 0
        # Sums up the material values
        for i in range(64):
            compt += self.squareResPoints(ch.SQUARES[i])
        compt += self.mateOpportunity() + self.openning() + 0.001 * rd.random()
        return compt

    def mateOpportunity(self):
        if self.board.legal_moves.count() == 0:
            if self.board.turn == self.color:
                return -999
            else:
                return 999
        else:
            return 0

    # to make the engine develop in the first moves
    def openning(self):
        if self.board.fullmove_number < 10:
            if self.board.turn == self.color:
                return 1 / 30 * self.board.legal_moves.count()
            else:
                return -1 / 30 * self.board.legal_moves.count()
        else:
            return 0

    # Takes a square as input and 
    # returns the corresponding Hans Berliner's
    # system value of its resident
    def squareResPoints(self, square):
        pieceValue = 0
        if self.board.piece_type_at(square) == ch.PAWN:
            pieceValue = 1
        elif self.board.piece_type_at(square) == ch.ROOK:
            pieceValue = 5.1
        elif self.board.piece_type_at(square) == ch.BISHOP:
            pieceValue = 3.33
        elif self.board.piece_type_at(square) == ch.KNIGHT:
            pieceValue = 3.2
        elif self.board.piece_type_at(square) == ch.QUEEN:
            pieceValue = 8.8

        if self.board.color_at(square) != self.color:
            return -pieceValue
        else:
            return pieceValue

    def engine(self, candidate, depth, alpha, beta):
        if depth == self.maxDepth or self.board.legal_moves.count() == 0:
            return self.evalFunct()
        
        moveListe = list(self.board.legal_moves)
        newCandidate = None

        if depth % 2 != 0:
            newCandidate = float("-inf")
        else:
            newCandidate = float("inf")
        
        for i in moveListe:
            self.board.push(i)

            if self.board.is_capture(i):
                value = self.search_all_captures(alpha, beta)
            else:
                value = self.engine(newCandidate, depth + 1, alpha, beta)
            
            if value > newCandidate and depth % 2 != 0:
                if depth == 1:
                    move = i
                newCandidate = value
                alpha = max(alpha, newCandidate)
            
            elif value < newCandidate and depth % 2 == 0:
                newCandidate = value
                beta = min(beta, newCandidate)
            
            if candidate is not None and value < candidate and depth % 2 == 0:
                self.board.pop()
                break
            elif candidate is not None and value > candidate and depth % 2 != 0:
                self.board.pop()
                break

            self.board.pop()
        
        if depth > 1:
            return newCandidate
        else:
            return move
            
        def search_all_captures(alpha, beta):
        
            evaluation = self.evalFunct()
        
            if evaluation >= beta:
                return beta
            
            alpha = max(alpha, evaluation)
            
            
            capture_moves = [move for move in list(self.board.legal_moves) if self.board.is_capture(move)]
            
            
            capture_moves.sort(key=lambda move: self.board.piece_type_at(move.to_square), reverse=True)

           
            for move in capture_moves:
                # Make the move
                self.board.push(move)
                
                
                evaluation = -self.search_all_captures(-beta, -alpha)
                
                
                self.board.pop()
                
                if evaluation >= beta:
                    return beta
                
                alpha = max(alpha, evaluation)
            
            return alpha
