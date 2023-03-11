// NOTE: this example uses the chess.js library:
// https://github.com/jhlywa/chess.js

// var board = null
// var game = "{\"legal_moves\": [\"f3g5\", \"f3e5\", \"f3h4\", \"f3d4\", \"f3g1\", \"g2h3\", \"g2f1\", \"h1g1\", \"h1f1\", \"e1f1\", \"b1c3\", \"b1a3\", \"e1g1\", \"g3g4\", \"h2h3\", \"e2e3\", \"d2d3\", \"c2c3\", \"b2b3\", \"a2a3\", \"h2h4\", \"e2e4\", \"d2d4\", \"c2c4\", \"b2b4\", \"a2a4\"], \"termination\": null, \"winner\": null, \"turn\": \"w\"}"
// // var game = new Chess()
// game = JSON.parse(game)
var $status = $('#status')
var $fen = $('#fen')
var $pgn = $('#pgn')

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

    const data = {
      client_id: client_id,
      champ_id: champ_id,
      timestamp: Date.now(),
      game_id: game_id,
      move: move
    };

  ws.send(JSON.stringify(data))

  // illegal move
  // if (move === null) return 'snapback'

  // updateStatus()
}

// update the board position after the piece snap
// for castling, en passant, pawn promotion
function onSnapEnd () {
  // TODO this should be done on ws resp
  // board.position(game.fen())
}

// function updateStatus () {
//   var status = ''

  // var moveColor = 'White'
  // if (game.turn() === 'b') {
  //   moveColor = 'Black'
  // }

  // checkmate?
  // if (game.in_checkmate()) {
  //   status = 'Game over, ' + moveColor + ' is in checkmate.'
  // }

  // draw?
  // else if (game.in_draw()) {
  //   status = 'Game over, drawn position'
  // }

  // game still on
  // else {
  //   status = moveColor + ' to move'

    // check?
  //   if (game.in_check()) {
  //     status += ', ' + moveColor + ' is in check'
  //   }
  // }

  // $status.html(status)
  // $fen.html(game.fen())
  // $pgn.html(game.pgn())
// }