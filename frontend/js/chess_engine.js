function onDragStart (source, piece, position, orientation) {
  // do not pick up pieces if the game is over
  if (game.game_over) return false

  // only pick up pieces for the side to move
  console.log(color)
  if ((game.turn === 'w' && color === "black") ||
      (game.turn === 'b' && color === "white"))
    {return false}
  if ((game.turn === 'w' && piece.search(/^b/) !== -1) ||
      (game.turn === 'b' && piece.search(/^w/) !== -1)) {
    return false
  }
}

function onDrop (source, target) {
  // see if the move is legal
  var move = source + target // TODO add promotions

  if (!game.legal_moves.includes(move)){
      return 'snapback'
  }

  // if legal make and send data JSON
  const data = {
    client_id: client_id,
    champ_id: champ_id,
    timestamp: Date.now(),
    game_id: game_id,
    move: move
  };

  ws.send(JSON.stringify(data))
}