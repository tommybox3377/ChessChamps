import json
import uuid
from typing import Dict
import chess

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

app = FastAPI()


async def send_personal_message(message: str, websocket: WebSocket):
    await websocket.send_text(message)


class ConnectionManager:
    def __init__(self):
        self.active_connection_dict: Dict[WebSocket] = dict()
        self.queue = None
        self.games = dict()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connection_dict[websocket["path_params"]["client_id"]] = websocket

    def disconnect(self, websocket: WebSocket):
        del self.active_connection_dict[websocket["path_params"]["client_id"]]

    async def make_match(self, data, websocket: WebSocket):
        # If no one is waiting, put user in queue, else join the person in the queue
        if not self.queue:
            self.queue = (data["client_id"], data["champ_id"])
            resp_data = {
                "game_id": "In Queue"
            }
            await websocket.send_json(resp_data)
        else:
            # Create a game_id and game JSON
            game_id = str(uuid.uuid4()).replace("-", "")

            self.games[game_id] = {
                "player1_id": self.queue[0],
                "player2_id": websocket["path_params"]["client_id"],
                "which_white": "player1",
                "player1_champ": self.queue[1],
                "player2_champ": data["champ_id"],
                "moves": [],
                "board_id": 0,
                "termination": "None",
            }
            print(len(self.games), self.games[game_id])

            # create data to send to users and send to first user
            board = chess.Board()
            resp_data = {
                "game_id": str(game_id),
                "game_fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR",
                "game_over": False,
                "turn": "w",
                "legal_moves": [str(x) for x in list(board.generate_legal_moves())],
                "color": "white"
            }

            await websocket.send_json(resp_data)

            # Change the color to the second player, send them the data, and empty queue
            resp_data["color"] = "black"

            await self.active_connection_dict[self.queue[0]].send_json(resp_data)

            self.queue = None

    async def make_move(self, data):
        game_data = self.games[data["game_id"]]
        player1 = game_data["player1_id"]
        player2 = game_data["player2_id"]
        players = (player1, player2)

        move = data["move"]

        print(move)

        game_data["moves"].append(move)

        board = chess.Board()
        for move in game_data["moves"]:
            board.push_san(move)
        current_fen = board.board_fen()

        legal_moves = [str(x) for x in list(board.generate_legal_moves())]
        game_data['legal_moves'] = legal_moves

        if board.turn:
            game_data["turn"] = "w"
        else:
            game_data["turn"] = "b"

        game_data["game_over"] = False

        self.games[data["game_id"]] = game_data

        resp_data = {
            "player": data["client_id"],
            "move": move,
            "game_id": data["game_id"],
            "game_fen": current_fen,
            "turn": game_data["turn"],
            "game_over": game_data["game_over"],
            "legal_moves": game_data["legal_moves"],
            "color": False
        }

        for player in players:
            connection = self.active_connection_dict[player]
            await connection.send_json(resp_data)


manager = ConnectionManager()


# This is the endpoint of the websocket
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket):
    # upon joining the manger keeps all the connection in a dict with the client_id as a key
    await manager.connect(websocket)

    try:
        while True:

            # When a message is sent to the server it is all processed here
            data = await websocket.receive_text()
            data = json.loads(data)

            if "game_id" not in data:  # This is for if the sender is still not in a game
                await manager.make_match(data, websocket)
            else:  # this is used to receive, process and send out moves
                await manager.make_move(data)

    except WebSocketDisconnect:
        manager.disconnect(websocket)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8808)