import random, sys
sys.path.append('../')
from gameplay.player import Player
from cards.utils import *
import numpy as np

class DominionBot(Player):
    
    """""""""""""""""""""""""""""""""
                INIT BOT
    """""""""""""""""""""""""""""""""
    
    def __init__(self, name='Dummy'):
        super().__init__(name=name)

    """""""""""""""""""""""""""""""""
           COMMUNICATION METHODS
    """""""""""""""""""""""""""""""""

    def _send_recv(self, send_msg):
        print(send_msg)
        return read_input(self._respond(send_msg), self)

    """""""""""""""""""""""""""""""""
            RESPONSE METHODS
    """""""""""""""""""""""""""""""""

    def _respond(self, prompt):
        if prompt == f'{self.name} have {self.turn.value} to spend on {self.turn.buys} buys. What would {self.name} like to buy? (card name or N/n)':
            return self._pick_card_in_supply(max_cost=self.turn.value)
        elif prompt == '\n'.join([f'{self.name} has {self.inplay._get_inplay()} in-play with:',
                                                            f'\t{self.turn.actions} actions remaining', 
                                                            f'\t{self.turn.buys} buys remaining',
                                                            f'\t{self.turn.value} value in-play', 
                                                            f'What action would {self.name} like to play? (card name or N/n)']):
            return self._pick_card_from_hand(type='Action')
        else:
            raise Exception()

    def _pick_card_in_supply(self, max_cost=np.inf, force=False):
        supply_cards = np.array(self.supply._get_card_names())
        costs = np.array([self.supply._get_card_cost(card) for card in supply_cards])
        choice_inds = np.where(costs <= max_cost)[0]
        choices = supply_cards[choice_inds]
        if not force:
            choices = np.append(choices, 'n')
        return random.choice(choices)

    def _pick_card_from_hand(self, type='Any', force=False):
        cards_in_hand = np.array(self.hand._get_names())
        if type != 'Any':
            types = np.array([get_card(card).type for card in cards_in_hand])
            choice_inds = np.where(types == type)[0]
            choices = cards_in_hand[choice_inds]
        else:
            choices = cards_in_hand.copy()
        if not force:
            choices = np.append(choices, 'n')
        return random.choice(choices)

        
            
        
    
        
    