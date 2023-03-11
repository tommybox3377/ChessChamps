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

    legal_moves = [str(x) for x in list(board.generate_legal_moves())]
    game_data['legal_moves'] = legal_moves

    if board.turn:
        game_data["turn"] = "w"
    else:
        game_data["turn"] = "b"

    json_data = json.dumps(game_data)
    return json_data

incoming_json = {
    "game_id": "abc",
    "moves": ["a3b8"],
    "next_to_move": 0,
    "fen":"rnbqkb1r/pppp1p1p/5n2/4p1p1/8/5NP1/PPPPPPBP/RNBQK2R w KQkq - 0 1"
}

h = update_game(json.dumps(incoming_json))
resp_json = {
    "game_id": "abc",
    "legal_moves": ["a3bg", "g6h7"],
    "next_to_move": 1
}

## in the database
init_dict = {
    "player1_id": "abc",
    "player2_id": "abd",
    "player1_champ": 0,
    "player2_champ": 0,
    "moves": ["a3bg", "g6h7", "a3b7"],
    "board_id": 0,
    "termination": "draw",
}

game = {
    "game_over": False,
    "turn": "w",
    "legal_moves":[],
}
