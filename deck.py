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

    def _display(self):
        print(f'{self.name}:')
        print_cards_in_row(self.cards)

    def _get_ncards(self):
        return len(self.cards)

    def _count_victory_points(self):
        points = 0
        for c in self.cards:
            points += c.points   
        return points


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
            print(c.type)
            types = np.append(types, c.type)
        print('!!!types', types)
        return len(np.where(types == 'Victory Point')[0])


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

        
    
        
            