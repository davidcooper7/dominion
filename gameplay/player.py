import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append('..')
from copy import deepcopy
from turn import Turn
from deck import *
import numpy as np
from typing import List
from cards.utils import *

class Player():
    
    """""""""""""""""""""""""""""""""
              INIT PLAYER
    """""""""""""""""""""""""""""""""
    
    def __init__(self, name: str, conn=None):
        self.name = name
        self.conn = conn
        self._init_deck()
        self.opponents = []

    def _add_opponent(self, opponents):
        self.opponents.append(opponents)

    def _init_deck(self):
        self.deck = Deck()
        self.draw = DrawPile()
        self.hand = Hand()
        self.inplay = InPlay()
        self.discard = DiscardPile()
        self.draw._shuffle()
        self._draw(5)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


    """""""""""""""""""""""""""""""""
           COMMUNICATION METHODS
    """""""""""""""""""""""""""""""""

    def _send_recv(self, send_msg):
        if self.conn is not None:
            send_msg = send_msg + '_y'
            self.conn.sendall(send_msg.encode())
            print('sent', send_msg)
            while True:
                data = self.conn.recv(1024)
                if not data:
                    break
                recv_msg = data.decode()
                print('received', recv_msg)
                return read_input(recv_msg, self)
        else:
            return read_input(input(send_msg), self)

    def _send_to_all(self, to_self, to_opponents=None):
        if self.conn is not None:
            to_self = to_self + '_n'
            if to_opponents is None:
                to_opponents = to_self
            else:
                to_opponents = to_opponents + '_n'
            print('to_self', to_self)
            print('to_opponents', to_opponents)
            self.conn.sendall(to_self.encode())
            time.sleep(0.01)
            if hasattr(self, 'opponents'):
                for opp in self.opponents:
                    if hasattr(opp, 'conn'):
                        opp.conn.sendall(to_opponents.encode())
                        time.sleep(0.01)
        else:
            print(to_self)

    def _send_to_self(self, to_self):
        if self.conn is not None:
            to_self = to_self + '_n'
            self.conn.sendall(to_self.encode())
            time.sleep(0.01)
        else:
            print(to_self)

    """""""""""""""""""""""""""""""""
               TURN ACTIONS
    """""""""""""""""""""""""""""""""
    
    def take_turn(self, supply):
        self.supply = supply
        self.turn = Turn()
        self._play_actions()
        self._buy_cards()
        self._cleanup()
        self._draw(5)


    def _play_actions(self):
        if self.hand._has_action():
            while self.turn.actions > 0 and self.hand._has_action():
                self.hand._display(conn=self.conn)
                msg = '\n'.join([f'{self.name} has {self.inplay._get_inplay()} in-play with:',
                                                            f'\t{self.turn.actions} actions remaining', 
                                                            f'\t{self.turn.buys} buys remaining',
                                                            f'\t{self.turn.value} value in-play', 
                                                            f'What action would {self.name} like to play? (card name or N/n)'])
                choice = self._send_recv(msg)
                print('choice', choice)
                if choice not in ['n', 'N']:
                    if self._check_card_in_hand(choice) and self._check_card_is_action(choice):
                        card = get_card(choice)
                        self._put_inplay(choice)
                        card._play(self)
                        self.turn.actions -= 1
                else:
                    break   
        else:
            self._send_to_self('No Action Cards.')

    def _buy_cards(self):
        self.turn.value += self.hand._get_value()
        self.supply._display(conn=self.conn)

        choice = None
        while self.turn.buys > 0:
            self.hand._display(conn=self.conn)
            msg = f'{self.name} have {self.turn.value} to spend on {self.turn.buys} buys. What would {self.name} like to buy? (card name or N/n)'
            choice = self._send_recv(msg)
            print('choice', choice)
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
        self.hand._display(conn=self.conn)
        if self.hand._count_ncards() == 0:
            return False
        if force:
            send_msg = f'Which card would {self.name} like to discard? (card name)'
            choice = self._send_recv(send_msg)
        else:
            send_msg = f'Would {self.name} like to discard a card? (card name or n/N)'
            choice = self._send_recv(send_msg)
            if choice in ['n', 'N']:
                return False
        if self._check_card_in_hand(choice):
            self._discard(choice)
            self.hand._display(conn=self.conn)
            return True
        else:
            return self._user_discard(force=force)

    def _user_trash(self, force=False, type='all', min_cost=0, return_cost=False):
        if force:
            choice = self._send_recv(f'Which card would {self.name} like to trash of type {type} and min. cost {min_cost}? (card name)')
        else:
            choice = self._send_recv(f'Would {self.name} like to trash a card? (card name or n/N)')
            if choice in ['n', 'N']:
                return False
        if self._check_card_in_hand(choice):
            card = get_card(choice)
            if (type == 'all' or card.type == type):
                if card.cost >= min_cost:
                    self._trash(choice)
                    self.hand._display(conn=self.conn)
                    if return_cost:
                        return get_card(choice).cost
                    else:
                        return True
                else:
                    self._send_to_self(f'Cannot trash {choice} with cost {card.cost} and min. cost {min_cost}')
                    return self._user_trash(force=force, type=type, min_cost=min_cost, return_cost=return_cost)
            else:
                self._send_to_self(f'Cannot trash {choice} of type {card.type} and mandated type {type}')
                return self._user_trash(force=force, type=type, min_cost=min_cost, return_cost=return_cost)
                
        else:
            return self._user_trash(force=force, type=type, min_cost=min_cost, return_cost=return_cost)

    def _user_lookat_to_trash(self, force=False, type='all', min_cost=0, return_cost=False):
        self.lookat._display(conn=self.conn)
        if force:
            choice = self._send_recv(f'Which card would {self.name} like to trash of type {type} and min. cost {min_cost}? (card name)')
        else:
            choice = self._send_recv(f'Would {self.name} like to trash a card? (card name or n/N)')
            if choice in ['n', 'N']:
                return False
        if self._check_card_in_lookat(choice):
            card = get_card(choice)
            if (type == 'all' or card.type == type):
                if card.cost >= min_cost:
                    self._lookat_to_trash(choice)
                    if return_cost:
                        return get_card(choice).cost
                    else:
                        return True
                else:
                    self._send_to_self(f'Cannot trash {choice} with cost {card.cost} and min. cost {min_cost}')
                    return self._user_lookat_to_trash(force=force, type=type, min_cost=min_cost, return_cost=return_cost)
            else:
                self._send_to_self(f'Cannot trash {choice} of type {card.type} and mandated type {type}')
                return self._user_lookat_to_trash(force=force, type=type, min_cost=min_cost, return_cost=return_cost)
                
        else:
            return self._user_trash(force=force, type=type, min_cost=min_cost, return_cost=return_cost)

    def _user_lookat_to_discard(self):
        choice = ''
        while choice not in ['n', 'N'] and self.lookat._count_ncards() > 0:
            self.lookat._display(conn=self.conn)
            choice = self._send_recv(f'Would {self.name} like to discard a card? (card name or n/N)')
            if choice in ['n', 'N']:
                break
            elif self._check_card_in_lookat(choice):
                self._lookat_to_discard(choice)

    def _user_gain(self, force=False, max_cost=0):
        self.supply._display(conn=self.conn)
        if force:
            choice = self._send_recv(f'Which card would {self.name} like to gain for up to {max_cost}? (card name)')
        else:
            choice = self._send_recv(f'Would {self.name} like to gain a card for up to {max_cost}? (card name or n/N)')
            if choice in ['n', 'N']:
                return False
        if self._check_card_gain(choice, max_cost=max_cost):
            self._gain(choice)
        else:
            return self._user_gain(force=force, max_cost=max_cost)

    def _user_hand_to_topdeck(self, force=False, type='any'):
        if force:
            self.hand._display(conn=self.conn)
            choice = self._send_recv(f'Which card would {self.name} like to topdeck of type {type}? (card name)')
        else:
            choice = self._send_recv(f'Which card would {self.name} like to topdeck of type {type}? (card name or n/N)')
            if choice in ['n', 'N']:
                return False
        if self._check_card_in_hand(choice):
            if type == 'any' or get_card(choice).type == type:
                self._hand_to_topdeck(choice)
            else:
                return self._user_hand_to_topdeck(force=force, type=type)
        else:
            return self._user_hand_to_topdeck(force=force, type=type)

    def _user_discard_to_topdeck(self):
        if self.discard._count_ncards() > 0:
            self.discard._display(conn=self.conn)
            choice_selected = False
            while not choice_selected:
                choice = self._send_recv('Would you like to put a discarded card onto your deck? (card name or N/n)')
                if choice not in ['N', 'n']:
                    if self._check_card_in_discard(choice):
                        self._discard_to_topdeck(choice)
                        choice_selected = True
                else:
                    choice_selected = True
        else:
            self._send_to_self('There are no cards in the discard :(')
                
    """""""""""""""""""""""""""""""""
          INTERNAL CARD MOVEMENT
    """""""""""""""""""""""""""""""""
    def _draw(self, ncards=1):
        if len(self.draw.cards) >= ncards:
            for i in range(ncards):
                self.hand.cards.append(self.draw.cards[0])
                self._send_to_all(f'> {self.name} draws a {self.draw.cards[0].name}', f'> {self.name} draws a card.')
                self.draw.cards.pop(0)
        else:
            if self._discard_to_draw():
                self._draw(ncards)
    
    def _gain(self, card_name):
        self._send_to_all(f'> {self.name} gains a {card_name}')
        self.supply._reduce_qty(card_name)
        self.discard._add_card(card_name)

    def _gain_to_hand(self, card_name):
        self._send_to_all(f'> {self.name} gains a {card_name} to their hand.')
        self.supply._reduce_qty(card_name)
        self.hand._add_card(card_name)

    def _gain_to_draw(self, card_name):
        self._send_to_all(f'> {self.name} topdecks a {card_name}')
        self.supply._reduce_qty(card_name)
        self.draw._topdeck_card(card_name)  
        
    def _discard(self, card_name):
        if card_name == 'Merchant' and self._check_card_in_hand('Silver'):
            self.turn.value -= 1
        
        self.hand._remove_card(card_name)
        self.discard._add_card(card_name)
        self._send_to_all(f'> {self.name} discards a {card_name}.', f'> {self.name} discards a card.')
        
    def _discard_to_draw(self):
        self.discard._shuffle()
        if self.discard._count_ncards() == 0:
            self._send_to_self(f'No cards in discard...')
            return False
        else:
            self._send_to_all(f'> {self.name} shuffles')
            for card in self.discard.cards:
                self.draw._add_card(card.name)
            self.discard._empty()
            return True

    def _discard_to_topdeck(self, card_name):
        self.discard._remove_card(card_name)
        self.draw._topdeck_card(card_name)
        self._send_to_all(f'{self.name} topdecks a {card_name}')

    def _put_inplay(self, card_name):
        self._send_to_all(f'> {self.name} plays a {card_name}')
        self.inplay._add_card(card_name)
        self.hand._remove_card(card_name)

    def _remove_cards_from_play(self):
        for card in self.inplay.cards:
            self.discard._add_card(card.name)
        self.inplay._empty()

    def _trash(self, card_name):
        self._send_to_all(f'> {self.name} trashes a {card_name}')
        self.hand._remove_card(card_name)

    def _lookat_draw_top(self, ncards=1):
        self.lookat = LookAt()
        if self.draw._count_ncards() >= ncards:
            for i in range(ncards):
                self.lookat._add_card(self.draw.cards[0].name)
                self.draw._remove_top()
        else:
            if self._discard_to_draw():
                self._lookat_draw_top(ncards=ncards)

        self._send_to_all(f'> {self.name} looks at {self.lookat}.', f'> {self.name} looks at {self.lookat._count_ncards()} cards.')

    def _lookat_to_hand(self, card_name):
        self.lookat._remove_card(card_name)
        self.hand._add_card(card_name)
        self._send_to_all(f'> {self.name} draws a {card_name}.', f'> {self.name} draws a card.')

    def _lookat_to_discard(self, card_name):
        self.lookat._remove_card(card_name)
        self.discard._add_card(card_name)
        self._send_to_all(f'> {self.name} discards a {card_name}.', f'> {self.name} discards a card.')

    def _lookat_to_trash(self, card_name):
        self.lookat._remove_card(card_name)
        self._send_to_all(f'> {self.name} trashes a {card_name}.')

    def _lookat_to_topdeck(self, card_name):
        self.lookat._remove_card(card_name)
        self.draw._topdeck_card(card_name)
        self._send_to_all(f'> {self.name} topdecks a {card_name}.', f'> {self.name} topdecks a card.')

    def _lookat_to_inplay(self, card_name):
        self.lookat._remove_card(card_name)
        self._send_to_all(f'> {self.name} plays a {card_name}.')
        self.inplay._add_card(card_name)

    def _hand_to_topdeck(self, card_name):
        self.hand._remove_card(card_name)
        self.draw._topdeck_card(card_name)
        self._send_to_all(f'> {self.name} topdecks a {card_name}.', f'> {self.name} topdecks a card.')

    def _finish(self):
        for card_name in self.hand._get_names():
            self.deck._add_card(card_name)
        for card_name in self.draw._get_names():
            self.deck._add_card(card_name)
        for card_name in self.discard._get_names():
            self.deck._add_card(card_name)

        for card_name in ['Estate', 'Duchy', 'Province', 'Gardens', 'Curse']:
            count = self.deck._count_n_of_card(card_name)
            card = get_card(card_name)
            if card_name == 'Gardens':
                self._send_to_all(f'> {self.name} had {count} {card_name}s for {self.deck._count_garden_points()} points.')
            else:
                self._send_to_all(f'> {self.name} had {count} {card_name}s for {count * card.points} points.')

        return self.deck._count_victory_points()

        
    """""""""""""""""""""""""""""""""
                 CHECKS
    """""""""""""""""""""""""""""""""
    def _check_card_gain(self, card_name, max_cost=np.inf):
        if card_name in self.supply._get_card_names():
            if self.supply._check_qty(card_name) > 0:
                if get_card(card_name).cost <= max_cost:
                    return True
                else:
                    self._send_to_self(f'Cannot gain {card_name} with maximum cost {max_cost}')
                    return False
            else:
                self._send_to_self(f'Cannot gain {card_name} with Qty 0.')
                return False
        elif card_name == '':
            return False
        else:
            self._send_to_self(f'{card_name} does not exist in the supply.')
            self.supply._display(conn=self.conn)
            return False
            
    
    def _check_card_buy(self, card_name):
        if self._check_card_gain(card_name):
            if self.supply._get_card_cost(card_name) <= self.turn.value:
                return True
            else:
                self._send_to_self(f'Cannot buy {card_name} with cost {self.supply._get_card_cost(card_name)} with value {self.turn.value}.')
                return False

    def _check_card_in_hand(self, card_name):
        if card_name in self.hand._get_names():
            return True
        elif card_name == '':
            return False
        else:
            self._send_to_self(f'{card_name} not in hand.')
            return False

    def _check_card_is_action(self, card_name):
        card = get_card(card_name)
        if card.type == 'Action':
            return True
        elif card_name == '':
            return False
        else:
            self._send_to_self(f'{card.name} is not an Action')
            return False

    def _check_card_is_treasure(self, card_name):
        card = get_card(card_name)
        if card.type == 'Treasure':
            return True
        elif card_name == '':
            return False
        else:
            self._send_to_self(f'{card.name} is not a Treasure')
            return False
            
    def _check_card_in_discard(self, card_name):
        if card_name in self.discard._get_names():
            return True
        elif card_name == '':
            return False
        else:
            self._send_to_self(f'{card_name} not in hand.')
            return False

    def _check_card_in_lookat(self, card_name):
        if card_name in self.lookat._get_names():
            return True
        elif card_name == '':
            return False
        else:
            self._send_to_self(f'{card_name} not an option.')
            return False


    

    

        
        


        