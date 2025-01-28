from player import Player
from supply import Supply
from cards import *

s = Supply(2, ['Cellar', 'Chapel', 'Harbinger', 'Merchant', 'Vassal', 'Village', 'Workshop'])
p = Player('George')
for i in range(10):
    p.take_turn(s)