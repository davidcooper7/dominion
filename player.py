from copy import deepcopy
from turn import Turn
from deck import *

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
        self._draw()
        self.turn = Turn()
        self._play_actions()
        self._buy_cards()
        self._cleanup()

    def _play_actions(self):
        print('Playing Actions...')
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
        print('Buying Cards...')
        self.turn.value += self.hand._get_value()
        self.turn.value += self.inplay._get_value()
        self.supply._display()

        choice = None
        while self.turn.buys > 0:
            self.hand._display()
            choice = convert_shorthand(input(f'You have {self.turn.value} to spend on {self.turn.buys} buys. What would you like to buy? (card name or N/n)'))
            if choice not in ['n', 'N']:
                if self._check_card_buy(choice):
                    print(f'Buying {choice}')
                    self._supply_to_discard(choice)
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
              CARD MOVEMENT
    """""""""""""""""""""""""""""""""

    def _draw(self, ncards=5):
        if len(self.draw.cards) >= ncards:
            for i in range(ncards):
                self.hand.cards.append(self.draw.cards[0])
                self.draw.cards.pop(0)
        else:
            self._discard_to_draw()
            self._draw(ncards)
    
    def _supply_to_discard(self, card_name):
        self.supply._reduce_qty(card_name)
        self.discard._add_card(card_name)

    def _user_discard(self):
        choice = convert_shorthand(input('Would you like to discard a card? (card name or n/N)'))
        if choice not in ['n', 'N']:
            if self._check_card_in_hand(choice):
                self._discard(choice)
                self.hand._display()
                return True
            else:
                return self._user_discard()
        else:
            return False
    
    def _discard(self, card_name):
        if card_name == 'Merchant' and self._check_card_in_hand('Silver'):
            self.turn.value -= 1
        
        self.hand._remove_card(card_name)
        self.discard._add_card(card_name)
        print(f'{self.name} discard a {card_name}.')

    def _discard_to_draw(self):
        self.discard._shuffle()
        print('Shuffling discard and adding to draw pile.')
        for card in self.discard.cards:
            self.draw._add_card(card.name)
        self.discard._empty()

    def _put_inplay(self, card_name):
        self.inplay._add_card(card_name)
        self.hand._remove_card(card_name)

    def _remove_cards_from_play(self):
        for card in self.inplay.cards:
            self.discard._add_card(card.name)
        self.inplay._empty()

    def _trash(self, card_name):
        self.hand._remove_card(card_name)

    def _user_trash(self):
        choice = convert_shorthand(input('Would you like to trash a card? (card name or n/N)'))
        if choice not in ['n', 'N']:
            if self._check_card_in_hand(choice):
                self._trash(choice)
                self.hand._display()
                return True
            else:
                return self._user_discard()
        else:
            return False        

    """""""""""""""""""""""""""""""""
                 CHECKS
    """""""""""""""""""""""""""""""""


    def _check_card_gain(self, card_name):
        if card_name in self.supply._get_card_names():
            if self.supply._check_qty(card_name) > 0:
                return True
            else:
                print(f'Cannot buy {card_name} with Qty 0.')
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
        if card_name in [c.name for c in self.hand.cards]:
            return True
        else:
            print(f'{card_name} not in hand.')
            return False

    def _check_card_is_action(self, card_name):
        card = get_card(card_name)
        if card.type == 'Action':
            return True
        else:
            return False

    def _check_card_in_discard(self, card_name):
        if card_name in [c.name for c in self.discard.cards]:
            return True
        else:
            print(f'{card_name} not in hand.')
            return False
    

        
        


        