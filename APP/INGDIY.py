import chess as ch
import random as rd



#   Funcion incesesaria pero sirve para luego leer el codigo a la hora de usarlo 
#   y devuelve el mejor movimiento analizado 

def MEJORmov(board, profundidad, color):
    return ING(board, None, 1, profundidad, color)



#   Evalua el valor del tablero para el jugador (color) sumando el valor de las piexas
#   Comprueba si hay mate y siendo asi lo asigna como el valor mas alto (negativo segun el color)
#   La apertura sire para favorecer a los jugadores con mas movimientos 



def Eval_FUN(board, color):
    points = 0
    
    for i in range(64):
        # Suma los valores para cada casilla 
        points += Valores(board, ch.SQUARES[i], color)
    
    points += MATE(board, color) + Apertura(board, color) + 0.001 * rd.random()
    return points


# Si hay posibilidad de  mate hace que el valor sea alto para que siempre se lo tenga en cuenta 

def MATE(board, color):
    if board.legal_moves.count() == 0:
        if board.turn == color:
            return -999
        else:
            return 999
    return 0

# busca que en los primeros movimientos se aplien las jugadas lo mas posible

def Apertura(board, color):
    if board.fullmove_number < 10:
        if board.turn == color:
            return 1/30 * board.legal_moves.count()
        else:
            return -1/30 * board.legal_moves.count()
    return 0


# Encargada de devolver lo valores (ES LO MISMO QUE USAR UN DICCIONARIO)
# En caso de ser la jugada que resta invierte el valor (MINMAX)

def Valores(board, square, color):
    Piezas = {
        ch.PAWN: 1,
        ch.ROOK: 5.1,
        ch.BISHOP: 3.33,
        ch.KNIGHT: 3.2,
        ch.QUEEN: 8.8
    }
    
    piece_type = board.piece_type_at(square)
    if piece_type is None:
        return 0
        
    Valor_piezas = Piezas.get(piece_type, 0)
    
    if board.color_at(square) != color:
        return -Valor_piezas
    return Valor_piezas


    
def is_under_attack_by_pawn(board, square, attacking_color):
    attacking_pawns = board.pieces(ch.PAWN, attacking_color)
    for pawn_square in attacking_pawns:
        if square in board.attacks(pawn_square):
            return True
    return False


def ordenar_movimientos(board, movimientos, color):
    # Diccionario para almacenar los puntajes de los movimientos
    puntajes_movimientos = []

    for movimiento in movimientos:
        score = 0
        move_piece_type = board.piece_type_at(movimiento.from_square)
        capture_piece_type = board.piece_type_at(movimiento.to_square)

        # Calcular puntaje por captura
        if capture_piece_type is not None:
            score += Valores(board, movimiento.to_square, color) - Valores(board, movimiento.from_square, color) * 10

        # Penalizar si es un movimiento de peón a una casilla controlada por un peón oponente
        if move_piece_type == ch.PAWN:
            if is_under_attack_by_pawn(board, movimiento.to_square, ch.COLORS[color]):
                score -= 350  # Penalización

        # Añadir un bono por promoción
        if movimiento.promotion is not None:
            if movimiento.promotion == ch.QUEEN:
                score += 900
            elif movimiento.promotion == ch.ROOK:
                score += 500
            elif movimiento.promotion == ch.BISHOP:
                score += 330
            elif movimiento.promotion == ch.KNIGHT:
                score += 320

        # Guardar el movimiento y su puntaje
        puntajes_movimientos.append((movimiento, score))

    # Ordenar los movimientos por puntaje (de mayor a menor)
    puntajes_movimientos.sort(key=lambda x: x[1], reverse=True)

    # Devolver solo los movimientos ordenados
    return [movimiento for movimiento, score in puntajes_movimientos]
    #Esta funcion existe debido a que al llegar al final del arbol no tenia en cuenta que en la siguiente jugada todo podia darse vuelta siempre que no haya una captura 
    #Primero se evalua la posicion actual
    #si la evaluacion es lo suficiente mente buena se devuelve beta indicando que no hay que explorar mas 
    #en caso contrario 
    #Se actualiza alpha con el valor maximo entre el y evaluacion 
    #luego se hace lo mismo que en ING (se genera una lista de mov y se ordena)


def buscar_capturas(board , alpha , beta , color):
    evaluacion = Eval_FUN(board , color)

    if evaluacion >= beta:
            return beta
    alpha = max(alpha, evaluacion)

    capture_moves = list(board.legal_moves)  # Filter captures here
    capture_moves = ordenar_movimientos(board, capture_moves, color)

    # Ahora se empieza el clasico bucle recursivo para buscar el mejor camino siguiendo con la implementacion de Poda 

    for move in capture_moves:
        board.push(move)
        value = -buscar_capturas(board, -beta, -alpha, color)
        board.pop()

        if value >= beta:
            return beta
        alpha = max(alpha, value)
    
    #Una vez se exploro todo se devuelve alpha que es la mejor jugada dentro de ese conjunto 
    
    return alpha



#Usamos MINMAX y poda alfa-beta de menera recursiva hasta el maximo(cantidad de profundiad)
#En caso de que sea movimiento de la "IA" los valores buscaran el MAXIMO (mejor ataque movimiento posible) 
# En caso de ser el movimiento del jugador se buscara el MINIMO (Mejor movimiento a recibir ) y lo restara al max 
# luego de hacer esto encontrara cual es la rama mas prometedora aunque el jugador haga el mejor movimiento posible 
        # Alpha (α): Representa el mejor valor (el valor más alto) que el jugador maximizador (generalmente el motor de ajedrez) puede garantizar en ese punto de la búsqueda.
        # El valor inicial de alpha es -∞ y se actualiza a medida que encontramos mejores opciones para el jugador maximizador.

        #Beta (β): Representa el mejor valor (el valor más bajo) que el jugador minimizador (generalmente el oponente) puede garantizar en ese punto de la búsqueda. 
        # El valor inicial de beta es +∞ y se actualiza conforme encontramos peores opciones para el jugador minimizador.


def ING(board, candidate, profundidad_actual, profundidad, color, alpha=float("-inf"), beta=float("inf")):
    # Si se alcanza la profundidad o no hay movimientos legales, da el  el valor de evaluación 
    if profundidad_actual == profundidad or board.legal_moves.count() == 0:
        return Eval_FUN(board, color)
    
    #  se generan todos los movimientos legales disponibles 
    lista_mov = list(board.legal_moves)
    lista_mov_ordenada = ordenar_movimientos(board, lista_mov, color)
    
     # Como se explica arriba 
     
     # float("-inf") es similar al valor alpha (para el maximizador).
     
     # float("inf") es similar al valor beta (para el minimizador).

    nuevo_movimiento = float("-inf") if profundidad_actual % 2 != 0 else float("inf") 
    mejor_movimiento = None  #  guardar el mejor movimiento en el primer nivel
    
    
    # Aqui es la parte recursiva y lo que diriamos la exploracion del arbol donde la funcion evalua todas las jugas por capa 
    for movimiento_actual in lista_mov_ordenada:
        board.push(movimiento_actual)
        
        # Obtener valor (explorando repercusiones)
        # dependiendo si esta max o min  ek valor de nuevo movimiento se actualiza debido a la recursividad 
        value = ING(board, nuevo_movimiento, profundidad_actual + 1, profundidad, color, alpha=float("-inf"), beta=float("inf")) 
        
        
        
        # Algoritmo minimax básico
        if profundidad_actual % 2 != 0:  # Maximizador
            if value > nuevo_movimiento:
                nuevo_movimiento = value
                if profundidad_actual == 1:
                    mejor_movimiento = movimiento_actual
            alpha = max(alpha, nuevo_movimiento)
        else:  # Minimizer
            if value < nuevo_movimiento:
                nuevo_movimiento = value
            beta = min(beta, nuevo_movimiento)
        
        # Alpha-beta pruning
        if beta <= alpha:
            board.pop()
            break
        
        # Deshacer último movimiento
        board.pop()
    
    # Retornar resultado
    if profundidad_actual > 1:
        return nuevo_movimiento
    else:
        return mejor_movimiento
    
    
    
    
    




