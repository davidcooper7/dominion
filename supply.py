import pandas as pd
pd.set_option('display.width', 100)
pd.set_option('display.max_colwidth', 50)
from IPython.display import display
from cards import *

class Supply():
    def __init__(self, n_players, kindom_card_names):
        
        starting_values = [
            ['c', 's', 'g', 'crs', 'e', 'd', 'p'],
            [60-n_players, 40, 30, self._get_n_curses(n_players), self._get_n_victory_points(n_players), \
             self._get_n_victory_points(n_players), self._get_n_victory_points(n_players)],
            [0, 3, 6, 0, 2, 5, 8],
        ]
        
        self.supply = pd.DataFrame(starting_values, columns=['Copper', 'Silver', 'Gold', 'Curse', 'Estate', 'Duchy', 'Province'], index=['Shorthand', 'Qty', 'Cost'])    

        for name in kindom_card_names:
            card = get_card(name)
            self.supply[card.name] = [card.shorthand, card.starting_qty, card.cost]
        self._display()


    def _get_n_curses(self, n_players):
        if n_players == 2:
            return 10
        elif n_players == 3:
            return 20
        else:
            return 30

    def _get_n_victory_points(self, n_players):
        if n_players == 2:
            return 8
        else:
            return 12

    def _display(self):
        display(self.supply)

    def _get_card_names(self):
        return self.supply.columns.to_list()

    def _check_qty(self, card_name):
        return self.supply[card_name]['Qty']

    def _get_card_cost(self, card_name):
        return self.supply[card_name]['Cost']

    def _reduce_qty(self, card_name):
        self.supply.loc['Qty', card_name] =  self.supply[card_name]['Qty'] - 1