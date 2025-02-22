import os, sys, inspect, random
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append('..')
from gameplay.supply import Supply
from gameplay.game import Game
from server import Server
import numpy as np


class LocalGame(Game):
    def __init__(self, server, players, packs=['basegame']):
        super().__init__(players, packs)
        self.server = server

    def close(self):
        self.server.close()

    def play(self):
        while not self._eval_winning_criterion():
            for player in self.players:
                player._send_to_all(f"\n***************It is {player.name}'s turn***************\n")
                player.take_turn(self.supply)
                if self._eval_winning_criterion():
                    break
            if self._eval_winning_criterion():
                break

        self._eval_win()

    def _eval_win(self):
        most_points = 0
        wining_players = []
        for player in self.players:
            points = player._finish()
            player._send_to_all(f'> {player} finishes with {points} victory points!')
            if points > most_points:
                most_points = points
                wining_players = [player.name]
            elif points == most_points:
                wining_players.append(player.name)

        self.players[0]._send_to_all(f'> Players {wining_players} win with {most_points}!!!')
        


    