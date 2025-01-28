from cards import *
from random import shuffle

class Deck():
    def __init__(self):
        self.cards = []

    def _add_card(self, card_name):
        self.cards.append(get_card(card_name))

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
        return f'{[c.name for c in self.cards]}'

    def __repr__(self):
        return f'{[c.name for c in self.cards]}'

    def _display(self):
        print(f'{self.name}:')
        print_cards_in_row(self.cards)


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

        
    
        
            