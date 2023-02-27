import chess
import json


def update_game(input_json):
    input_fen = json.loads(input_json)['fen']

    game_data = {
        'legal_moves': None,
        'termination': None,
        'winner': None
    }
    board = chess.Board(input_fen)
    # print(board)

    result = board.outcome()
    if result:
        if result.termination.name == 'CHECKMATE':
            game_data['termination'] = 'checkmate'
            if result.winner:
                game_data['winner'] = 'white'
            else:
                game_data['winner'] = 'black'
        else:
            game_data['termination'] = 'draw'

    game_data['legal_moves'] = list(board.generate_legal_moves())

    json_data = json.dumps(game_data)
    return json_data
