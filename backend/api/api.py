



@app.websocket("/ws/{join_game}")
async def join_game(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            data = json.loads(data)
            if not data["game_id"]:
                await manager.make_match(data, websocket)
            else:
                await manager.make_move(data)

    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.websocket("/ws/move")
async def websocket_endpoint(websocket: WebSocket):
    try:
        while True:
            data = await websocket.receive_text()
            data = json.loads(data)
            if not data["game_id"]:
                await manager.make_match(data, websocket)
            else:
                await manager.make_move(data)

    except WebSocketDisconnect:
        manager.disconnect(websocket)