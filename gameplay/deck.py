import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append('..')
from cards.utils import *
from random import shuffle
import numpy as np

class Deck():
    def __init__(self):
        self.cards = []

    def _add_card(self, card_name):
        self.cards.append(get_card(card_name))

    def _remove_top(self, ncards=1):
        for i in range(ncards):
            self.cards.pop(0)

    def _get_names(self):
        return [c.name for c in self.cards]
    
    def _remove_card(self, card_name):
        self.cards.pop([c.name for c in self.cards].index(card_name))

    def _topdeck_card(self, card_name):
        self.cards.insert(0, get_card(card_name))

    def _shuffle(self):
        shuffle(self.cards)

    def _empty(self):
        self.cards = []

    def _get_value(self):
        return sum([c.value for c in self.cards])

    def __str__(self):
        return f'{", ".join([c.name for c in self.cards])}'

    def __repr__(self):
        return f'{[c.name for c in self.cards]}'

    def _display(self, conn=None):
        print(f'{self.name}:')
        print_cards_in_row(self.cards, conn=conn)

    def _count_ncards(self):
        return len(self.cards)

    def _count_victory_points(self):
        points = self._count_garden_points()
        for c in self.cards:
            points += c.points   
        return points

    def _count_treasures(self):
        count = 0
        for c in self.cards:
            if c.type == 'Treasure':
                count += 1
        return count

    def _count_n_of_card(self, card_name):
        count = 0
        for c in self.cards:
            if c.name == card_name:
                count +=1
        return count

    def _count_garden_points(self):
        return self._count_n_of_card('Gardens') * (self._count_ncards() // 10) * 10

    def _has_action(self):
        for c in self.cards:
            if c.type == 'Action':
                return True
        return False

    def _has_treasure(self):
        for c in self.cards:
            if c.type == 'Treasure':
                return True
        return False

    def _has_victory_point(self):
        for c in self.cards:
            if c.type == 'Victory Point':
                return True
        return False

    def _count_victory_point_cards(self):
        types = np.array([])
        for c in self.cards:
            types = np.append(types, c.type)
        return len(np.where(types == 'Victory Point')[0])
        
class DrawPile(Deck):
    def __init__(self):
        super().__init__()
        self.name = 'Draw'
        
        for i in range(7):
            self.cards.append(Copper())
        for i in range(3):
            self.cards.append(Estate())


class Hand(Deck):
    def __init__(self):
        super().__init__()
        self.name = 'Hand'

class InPlay(Deck):
    def __init__(self):
        super().__init__()
        self.name = 'In Play'

    def _get_inplay(self):
        return [c.name for c in self.cards]

class DiscardPile(Deck):
    def __init__(self):
        super().__init__()
        self.name = 'Discard'

class LookAt(Deck):
    def __init__(self):
        super().__init__()
        self.name = 'Look At'

        
    
        
            