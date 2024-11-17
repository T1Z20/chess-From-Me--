from flask import Flask, request, render_template, redirect, url_for, jsonify
import chess as ch
import chess.svg
import random
import INGDIY 
import os


app = Flask(__name__)


board = chess.Board()





@app.route('/')
def index():
    
    board_svg = chess.svg.board(board)
    return render_template('index.html', board_svg=board_svg)

@app.route('/legal_moves')
def get_legal_moves():
    legal_moves = []
    for move in board.legal_moves:
        move_uci = move.uci()
        from_square = chess.square_name(move.from_square)
        to_square = chess.square_name(move.to_square)
        move_san = board.san(move)
        legal_moves.append({
            'uci': move_uci,
            'san': move_san,
            'from': from_square,
            'to': to_square
        })
    return jsonify(legal_moves)


@app.route('/move', methods=['POST'])
def move():
    global board  # Aseguramos que estamos utilizando la variable global `board`
    
    # Obtener el movimiento del jugador desde el formulario
    move = request.form.get('move')
    promotion = request.form.get('promotion', 'q')  # Promoción por defecto: dama
    message = ""

    # Validar el movimiento del jugador
    while True:
        try:
            chess_move = create_chess_move(move, promotion)
            if chess_move and board.is_legal(chess_move):
                board.push(chess_move)
                game_status = check_game_status()
                if game_status:
                    message = game_status
                break  # Salir del bucle si el movimiento es válido
            else:
                message = 'Movimiento ilegal. Inténtalo de nuevo.'
                return render_template('index.html', board_svg=chess.svg.board(board), message='Movimiento ilegal. Inténtalo de nuevo.')
        except ValueError as e:
            message = str(e)
            return render_template('index.html', board_svg=chess.svg.board(board), message='Movimiento ilegal. Inténtalo de nuevo.')

    # Movimiento del bot
    try:
        best_move = INGDIY.MEJORmov(board, 4, ch.BLACK)
        if best_move and board.is_legal(best_move):
            board.push(best_move)
            game_status = check_game_status()
            if game_status:
                message = game_status
        else:
            message = 'Movimiento ilegal del bot (esto no debería ocurrir).'
    except ValueError as e:
        message = str(e)
    
    # tablero actualizado
    board_svg = chess.svg.board(board)
    return render_template('index.html', board_svg=board_svg, message=message)

    
 #Funcion que transforma el movimiento ingresado en un movimiento legal y agrega en caso de necesitarlo la promo 
def create_chess_move(move, promotion):
    
    if isinstance(move, chess.Move):
        return move
    chess_move = chess.Move.from_uci(move)
    if (board.piece_at(chess_move.from_square) and 
        board.piece_at(chess_move.from_square).piece_type == chess.PAWN and
        chess_move.to_square in chess.SquareSet(chess.BB_BACKRANKS)):
        promotion_map = {'q': chess.QUEEN, 'r': chess.ROOK, 'b': chess.BISHOP, 'n': chess.KNIGHT}
        if promotion in promotion_map:
            return chess.Move.from_uci(move + promotion)
        else:
            raise ValueError("Invalid promotion piece")
    
    return chess_move

def check_game_status():
    
    if board.is_checkmate():
        return '¡Jaque mate!'
    elif board.is_stalemate():
        return '¡Empate por ahogado!'
    elif board.is_insufficient_material():
        return '¡Empate por material insuficiente!'
    elif board.is_seventyfive_moves():
        return '¡Empate por 75 movimientos!'
    elif board.is_fivefold_repetition():
        return '¡Empate por repetición cinco veces!'
    elif board.is_variant_draw():
        return '¡Empate!'
    return None

@app.route('/reset', methods=['POST'])
def reset():
    
    global board
    board = chess.Board()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))