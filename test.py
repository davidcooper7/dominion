from player import Player
from supply import Supply
from cards import *
from game import Game

p1 = Player('David')
p2 = Player('Joseph')

game = Game(players=[p1, p2])
game.play()