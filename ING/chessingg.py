import chess as ch
import random as rd

def get_best_move(board, max_depth, color):
    return engine(board, None, 1, max_depth, color)

def eval_position(board, color):
    points = 0
    # Suma los valores materiales
    for i in range(64):
        points += square_res_points(board, ch.SQUARES[i], color)
    
    points += mate_opportunity(board, color) + opening_bonus(board, color) + 0.001 * rd.random()
    return points

def mate_opportunity(board, color):
    if board.legal_moves.count() == 0:
        if board.turn == color:
            return -999
        else:
            return 999
    return 0

def opening_bonus(board, color):
    if board.fullmove_number < 10:
        if board.turn == color:
            return 1/30 * board.legal_moves.count()
        else:
            return -1/30 * board.legal_moves.count()
    return 0

def square_res_points(board, square, color):
    piece_values = {
        ch.PAWN: 1,
        ch.ROOK: 5.1,
        ch.BISHOP: 3.33,
        ch.KNIGHT: 3.2,
        ch.QUEEN: 8.8
    }
    
    piece_type = board.piece_type_at(square)
    if piece_type is None:
        return 0
        
    piece_value = piece_values.get(piece_type, 0)
    
    if board.color_at(square) != color:
        return -piece_value
    return piece_value

def engine(board, candidate, depth, max_depth, color):
    # Caso base: profundidad máxima alcanzada o no hay movimientos posibles
    if depth == max_depth or board.legal_moves.count() == 0:
        return eval_position(board, color)
    
    # Obtener lista de movimientos legales
    move_list = list(board.legal_moves)
    
    # Inicializar nuevo candidato
    new_candidate = float("-inf") if depth % 2 != 0 else float("inf")
    best_move = None  # Para guardar el mejor movimiento en el primer nivel
    
    # Analizar tablero después de movimientos más profundos
    for current_move in move_list:
        # Jugar movimiento
        board.push(current_move)
        
        # Obtener valor del movimiento (explorando repercusiones)
        value = engine(board, new_candidate, depth + 1, max_depth, color)
        
        # Algoritmo minimax básico
        if value > new_candidate and depth % 2 != 0:  # Maximizando (turno del motor)
            if depth == 1:
                best_move = current_move
            new_candidate = value
        elif value < new_candidate and depth % 2 == 0:  # Minimizando (turno del jugador)
            new_candidate = value
            
        # Poda alfa-beta
        if (candidate is not None and 
            ((value < candidate and depth % 2 == 0) or  # Poda en nodo MIN
             (value > candidate and depth % 2 != 0))):  # Poda en nodo MAX
            board.pop()
            break
        
        # Deshacer último movimiento
        board.pop()
    
    # Retornar resultado
    if depth > 1:
        return new_candidate
    else:
        return best_move

