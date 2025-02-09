from player import Player
from supply import Supply
from cards import *

s = Supply(2, ['Cellar', 'Chapel', 'Harbinger', 'Merchant', 'Market', 'Moneylender', 'Festival', 'Remodel', 'Vassal', 'Library', 'Sentry'])
p = Player('George')
for i in range(1000):
    p.take_turn(s)
