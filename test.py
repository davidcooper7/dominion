from player import Player
from supply import Supply
from cards import *

s = Supply(2, ['Cellar', 'Chapel', 'Harbinger', 'Merchant', 'Vassal', 'Moneylender', 'Festival', 'Remodel', 'Smithy', 'Laboratory', 'Library'])
p = Player('George')
for i in range(1000):
    p.take_turn(s)
