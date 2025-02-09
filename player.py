from copy import deepcopy
from turn import Turn
from deck import *
import numpy as np

class Player():
    
    """""""""""""""""""""""""""""""""
              INIT PLAYER
    """""""""""""""""""""""""""""""""
    
    def __init__(self, name: str):
        self.name = name
        self._init_deck()

    def _init_deck(self):
        self.deck = Deck()
        self.draw = DrawPile()
        self.hand = Hand()
        self.inplay = InPlay()
        self.discard = DiscardPile()
        self.draw._shuffle()


    """""""""""""""""""""""""""""""""
               TURN ACTIONS
    """""""""""""""""""""""""""""""""
    
    def take_turn(self, supply):
        self.supply = supply
        self._draw(5)
        self.turn = Turn()
        self._play_actions()
        self._buy_cards()
        self._cleanup()

    def _play_actions(self):
        if self.hand._has_action():
            while self.turn.actions > 0 and self.hand._has_action():
                self.hand._display()
                choice = convert_shorthand(input('\n'.join([f'{self.name} has {self.inplay._get_inplay()} in-play with:',
                                                            f'\t{self.turn.actions} actions remaining', 
                                                            f'\t{self.turn.buys} buys remaining',
                                                            f'\t{self.turn.value} value in-play', 
                                                            f'What action would {self.name} like to play? (card name or N/n)'])))
                if choice not in ['n', 'N']:
                    if self._check_card_in_hand(choice) and self._check_card_is_action(choice):
                        card = get_card(choice)
                        self._put_inplay(choice)
                        card._play(self)
                        self.turn.actions -= 1
                else:
                    break   
        else:
            print('No Action Cards.')

    def _buy_cards(self):
        self.turn.value += self.hand._get_value()
        self.turn.value += self.inplay._get_value()
        self.supply._display()

        choice = None
        while self.turn.buys > 0:
            self.hand._display()
            choice = convert_shorthand(input(f'You have {self.turn.value} to spend on {self.turn.buys} buys. What would you like to buy? (card name or N/n)'))
            if choice not in ['n', 'N']:
                if self._check_card_buy(choice):
                    self._gain(choice)
                    self.turn.value -= self.supply._get_card_cost(choice)
                    self.turn.buys -= 1
            else:
                break

    def _cleanup(self):
        card_names = [c.name for c in self.hand.cards]
        for name in card_names:
            self._discard(name)
        self._remove_cards_from_play()

    """""""""""""""""""""""""""""""""
              USER CARD MOVEMENT
    """""""""""""""""""""""""""""""""
    def _user_discard(self, force=False):
        if self.hand._get_ncards() == 0:
            return False
        if force:
            choice = convert_shorthand(input('Which card would you like to discard? (card name)'))
        else:
            choice = convert_shorthand(input('Would you like to discard a card? (card name or n/N)'))
            if choice in ['n', 'N']:
                return False
        if self._check_card_in_hand(choice):
            self._discard(choice)
            self.hand._display()
            return True
        else:
            return self._user_discard(force=force)

    def _user_trash(self, force=False, return_cost=False):
        if force:
            choice = convert_shorthand(input('Which card would you like to trash? (card name)'))
        else:
            choice = convert_shorthand(input('Would you like to trash a card? (card name or n/N)'))
            if choice in ['n', 'N']:
                return False
        if self._check_card_in_hand(choice):
            self._trash(choice)
            self.hand._display()
            if return_cost:
                return get_card(choice).cost
            else:
                return True
        else:
            return self._user_trash(force=force)

    def _user_gain(self, force=False, max_cost=0):
        self.supply._display()
        if force:
            choice = convert_shorthand(input(f'Which card would you like to gain for up to {max_cost}? (card name)'))
        else:
            choice = convert_shorthand(input(f'Would you like to gain a card for up to {max_cost}? (card name)'))
            if choice in ['n', 'N']:
                return False
        if self._check_card_gain(choice, max_cost=max_cost):
            self._gain(choice)
        else:
            return self._user_gain(force=force, max_cost=max_cost)
            
    """""""""""""""""""""""""""""""""
          INTERNAL CARD MOVEMENT
    """""""""""""""""""""""""""""""""
    def _draw(self, ncards=1):
        if len(self.draw.cards) >= ncards:
            for i in range(ncards):
                self.hand.cards.append(self.draw.cards[0])
                print(f'> {self.name} draws a {self.draw.cards[0].name}')
                self.draw.cards.pop(0)
        else:
            self._discard_to_draw()
            self._draw(ncards)
    
    def _gain(self, card_name):
        print(f'> {self.name} gains a {card_name}')
        self.supply._reduce_qty(card_name)
        self.discard._add_card(card_name)
    
    def _discard(self, card_name):
        if card_name == 'Merchant' and self._check_card_in_hand('Silver'):
            self.turn.value -= 1
        
        self.hand._remove_card(card_name)
        self.discard._add_card(card_name)
        print(f'> {self.name} discards a {card_name}.')

    def _discard_to_draw(self):
        self.discard._shuffle()
        print(f'> {self.name} shuffles')
        for card in self.discard.cards:
            self.draw._add_card(card.name)
        self.discard._empty()

    def _put_inplay(self, card_name):
        print(f'> {self.name} plays a {card_name}')
        self.inplay._add_card(card_name)
        self.hand._remove_card(card_name)

    def _remove_cards_from_play(self):
        for card in self.inplay.cards:
            self.discard._add_card(card.name)
        self.inplay._empty()

    def _trash(self, card_name):
        print(f'> {self.name} trashes a {card_name}')
        self.hand._remove_card(card_name)

    def _lookat_draw_top(self, ncards=1):
        self.lookat = LookAt()
        if self.draw._get_ncards() >= ncards:
            for i in range(ncards):
                self.lookat._add_card(self.draw.cards[0].name)
                self.draw._remove_top()
        else:
            self._discard_to_draw()
            self._lookat_draw_top(ncards=ncards)

        print(f'> {self.name} looks at {self.lookat}')

    def _lookat_to_hand(self, card_name):
        self.lookat._remove_card(card_name)
        self.hand._add_card(card_name)
        print(f'> {self.name} draws a {card_name}')


    def _lookat_to_discard(self, card_name):
        self.lookat._remove_card(card_name)
        self.discard._add_card(card_name)
        print(f'> {self.name} discards a {card_name}')

    def _lookat_to_trash(self, card_name):
        self.lookat._remove_card(card_name)
        print(f'> {self.name} trashes a {card_name}')

    def _lookat_to_topdeck(self, card_name):
        self.lookat._remove_card(card_name)
        self.draw._topdeck_card(card_name)
        print(f'> {self.name} topdecks a {card_name}')

    def _lookat_to_inplay(self, card_name):
        self.lookat._remove_card(card_name)
        print(f'> {self.name} plays a {card_name}')
        self.inplay._add_card(card_name)
        
    """""""""""""""""""""""""""""""""
                 CHECKS
    """""""""""""""""""""""""""""""""


    def _check_card_gain(self, card_name, max_cost=np.inf):
        if card_name in self.supply._get_card_names():
            if self.supply._check_qty(card_name) > 0:
                if get_card(card_name).cost <= max_cost:
                    return True
                else:
                    print(f'Cannot gain {card_name} with maximum cost {max_cost}')
                    return False
            else:
                print(f'Cannot gain {card_name} with Qty 0.')
                return False
        else:
            print(f'{card_name} does not exist in the supply.')
            self.supply._display()
            return False
            
    
    def _check_card_buy(self, card_name):
        if self._check_card_gain(card_name):
            if self.supply._get_card_cost(card_name) <= self.turn.value:
                return True
            else:
                print(f'Cannot buy {card_name} with cost {self.supply._get_card_cost(card_name)} with value {self.turn.value}.')
                return False


    def _check_card_in_hand(self, card_name):
        if card_name in self.hand._get_names():
            return True
        else:
            print(f'{card_name} not in hand.')
            return False

    def _check_card_is_action(self, card_name):
        card = get_card(card_name)
        if card.type == 'Action':
            return True
        else:
            print(f'{card.name} is not an Action')
            return False

    def _check_card_is_treasure(self, card_name):
        card = get_card(card_name)
        if card.type == 'Treasure':
            return True
        else:
            print(f'{card.name} is not a Treasure')
            return False
            
    def _check_card_in_discard(self, card_name):
        if card_name in self.discard._get_names():
            return True
        else:
            print(f'{card_name} not in hand.')
            return False

    def _check_card_in_lookat(self, card_name):
        if card_name in self.lookat._get_names():
            return True
        else:
            print(f'{card_name} not an option.')
            return False

    

    

        
        


        