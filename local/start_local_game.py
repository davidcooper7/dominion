import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append('..')
from gameplay.player import Player
from gameplay.game import Game
from server import Server
import numpy as np
9
if __name__ == "__main__":
    # Set number of players
    n_players = input('How many players will be playing? ')
    
    # Set up server
    PORT = 3668
    server = Server(PORT, n_connections=int(n_players))

    # Set players
    clients = server.get_clients()
    players = []
    for (name, conn) in clients:
        players.append(Player(name, conn))
    
    game = Game(server=server, players=players)
    game.play()
    game.close()