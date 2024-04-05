import asyncio
import json

from parsers import ChessLocationParser
from websocket import Websocket
from Stockfish import Stockfish

stockfish = Stockfish()
stockfish.init()
parser = ChessLocationParser()

prev_result = []


def onClientMessage(msg_string):
    global prev_result
    data = json.loads(msg_string)
    if data["type"] == "HTML":
        result = parser.processPiecesLocation(data["data"])
        if len(result) > len(prev_result):
            print("[RESULT]", result)
            next_move = stockfish.getNextMove(result)
            print(next_move)
            prev_result = result.copy()
    elif data["type"] == "COMMAND":
        if data["data"] == "reset":
            prev_result.clear()
            parser.prev_black_pos.clear()
            parser.prev_white_pos.clear()
            parser.moves_made.clear()


socket = Websocket(onClientMessage)
asyncio.run(socket.startServer())


def playLocal():
    moves_list = []
    while True:
        player_move = input("enter your move: ")
        opponent_move = input("enter opponent move")
        if player_move:
            moves_list.append(player_move)
        if opponent_move:
            moves_list.append(opponent_move)

        stockfish.getNextMove(moves_list)
