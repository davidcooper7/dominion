import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from local_player import LocalPlayer
from local_game import LocalGame
from server import Server
import numpy as np
9
if __name__ == "__main__":
    # Set number of players
    n_players = input('How many players will be playing? ')
    
    # Set up server
    PORT = 3666
    server = Server(PORT, n_connections=int(n_players))

    # Set players
    clients = server.get_clients()
    players = []
    for (name, conn) in clients:
        players.append(LocalPlayer(name, conn))
    
    game = LocalGame(server, players)
    game.play()
    game.close()