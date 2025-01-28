
class Card():
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name


"""
TREASURE CARDS
"""
class Treasure(Card):
    def __init__(self):
        self.type = 'Treasure'
        self.plus_action = 0
        self.plus_card = 0
        self.plus_buy = 0

class Copper(Treasure):
    def __init__(self):
        super().__init__()
        self.name = 'Copper'
        self.shorthand = 'c'
        self.cost = 0
        self.value_str = 1
        self.value = 1

class Silver(Treasure):
    def __init__(self):
        super().__init__()
        self.name = 'Silver'
        self.shorthand = 's'
        self.cost = 3
        self.value_str = 2
        self.value = 2

class Gold(Treasure):
    def __init__(self):
        super().__init__()
        self.name = 'Gold'
        self.shorthand = 'g'
        self.cost = 6
        self.value_str = 3
        self.value = 3

"""
VICTORY POINT CARDS
"""

class VictoryPointCard(Card):
    def __init__(self):
        self.type = 'Victory Point'
        self.value_str = 0
        self.value = 0
        self.plus_action = 0
        self.plus_card = 0
        self.plus_buy = 0
        
class Estate(VictoryPointCard):
    def __init__(self):
        super().__init__()
        self.name = 'Estate'
        self.shorthand = 'e'
        self.cost = 2
        self.points = 1

class Duchy(VictoryPointCard):
    def __init__(self):
        super().__init__()
        self.name = 'Duchy'
        self.shorthand = 'd'
        self.cost = 5
        self.points = 3

class Province(VictoryPointCard):
    def __init__(self):
        super().__init__()
        self.name = 'Province'
        self.shorthand = 'p'
        self.cost = 8
        self.points = 6

class Curse(VictoryPointCard):
    def __init__(self):
        super().__init__()
        self.name = 'Curse'
        self.shorthand = 'crs'
        self.cost = 0
        self.points = -1


"""
KINDGOM CARDS
"""

class ActionCard(Card):
    def __init__(self):
        self.type = 'Action'
        self.starting_qty = 10

    def _resolve_play(self, player):
        player.turn.actions += self.plus_action
        player.turn.buys += self.plus_buy
        player.turn.value += self.value
    
class Cellar(ActionCard):
    def __init__(self):
        super().__init__()
        self.name = 'Cellar'
        self.shorthand = 'clr'
        self.plus_action = 1
        self.plus_card = 0
        self.plus_buy = 0
        self.cost = 2
        self.value_str = 0
        self.value = 0
        self.descr = 'Discard any number of cards. +1 Card per card discarded.'

    def _play(self, player):
        player.hand._display()
        while player._user_discard():
            self.plus_card += 1
        player._draw(self.plus_card)
        self._resolve_play(player)

class Chapel(ActionCard):
    def __init__(self):
        super().__init__()
        self.name = 'Chapel'
        self.shorthand = 'chp'
        self.plus_action = 0
        self.plus_card = 0
        self.plus_buy = 0
        self.cost = 2
        self.value_str = 0
        self.value = 0
        self.descr = 'Trash up to 4 cards from your hand.'  

    def _play(self, player):
        player.hand._display()
        trashed = 0
        while trashed < 4 and player._user_trash():
            trashed += 1

class Harbinger(ActionCard):
    def __init__(self):
        super().__init__()
        self.name = 'Harbinger'
        self.shorthand = 'hrb'
        self.plus_action = 1
        self.plus_card = 1
        self.plus_buy = 0
        self.cost = 3
        self.value_str = 0
        self.value = 0
        self.descr = 'Look through your discard pile. You may put a card from it onto your deck.'   

    def _play(self, player):
        player._draw(self.plus_card)
        player.hand._display()
        if len(player.discard.cards) > 0:
            player.discard._display()
            choice_selected = False
            while not choice_selected:
                choice = convert_shorthand(input('Would you like to put a discarded card onto your deck? (card name or N/n)'))
                if choice not in ['N', 'n']:
                    if player._check_card_in_discard(choice):
                        player.discard._remove_card(choice)
                        player.draw._topdeck_card(choice)
                        choice_selected = True
                else:
                    choice_selected = True
        else:
            print('There are no cards in the discard :(')
        self._resolve_play(player)

class Merchant(ActionCard):
    def __init__(self):
        super().__init__()
        self.name = 'Merchant'
        self.shorthand = 'mrch'
        self.plus_action = 1
        self.plus_card = 1
        self.plus_buy = 0
        self.cost = 3
        self.value_str = 0
        self.value = 0
        self.descr = 'The first time you play a Silver this turn +1 Value.'   

    def _play(self, player):
        player._draw(self.plus_card)
        player.hand._display()
        if player._check_card_in_hand('Silver'):
            self.value = 1
        self._resolve_play(player)

class Vassal(ActionCard):
    def __init__(self):
        super().__init__()
        self.name = 'Vassal'
        self.shorthand = 'vsl'
        self.plus_action = 0
        self.plus_card = 0
        self.plus_buy = 0
        self.cost = 3
        self.value_str = 2
        self.value = 0
        self.descr = "Discard the top card of your deck. If it's an Action card, you may play it?"

    def _play(self, player):
        self.value += 2
        if len(player.draw.cards) > 0:
            top_card = player.draw.cards[0]
        else:
            player._discard_to_draw()
            top_card = player.draw.cards[0]
        print(f'{player.name} drew a {top_card.name}')
        if top_card.type == 'Action':
            player._draw(1)
            player.hand._display()
            choice_selected = False
            while not choice_selected:
                choice = convert_shorthand(input(f'Would {player.name} like to play it? (Y/y or N/n)'))
                if choice in ['N', 'n']:
                    choice_selected = True
                elif choice in ['Y', 'y']:
                    player._put_inplay(top_card.name)
                    top_card._play(player)
                    choice_selected = True
                
        else:
            player.draw._remove_card(top_card.name)
            player.discard._add_card(top_card.name)
            print(f'{player.name} discarded a {top_card.name}')
                
        self._resolve_play(player)
    
class Village(ActionCard):
    def __init__(self):
        super().__init__()
        self.name = 'Village'
        self.shorthand = 'vlg'
        self.plus_action = 2
        self.plus_card = 1
        self.plus_buy = 0
        self.cost = 3
        self.value_str = 0
        self.value = 0
        self.descr = ""

    def _play(self, player):
        player._draw(1)
        self._resolve_play(player)

class Workshop(ActionCard):
    def __init__(self):
        super().__init__()
        self.name = 'Workshop'
        self.shorthand = 'wks'
        self.plus_action = 0
        self.plus_card = 0
        self.plus_buy = 0
        self.cost = 3
        self.value_str = 0
        self.value = 0
        self.descr = "Gain a card costing up to 4."

    def _play(self, player):
        choice_selected = False
        while not choice_selected:
            player.supply._display()
            choice = convert_shorthand(input(f'Would {player.name} like to purchase a card up to 4? (card_name or N/n)'))
            if choice not in ['N', 'n']:
                if player._check_card_gain(choice):
                    card = get_card(choice)
                    if card.cost <= 4:
                        player.discard._add_card(choice)
                        print(f'{player.name} gained a {card.name}')
                        choice_selected = True
                    else:
                        print(f'The cost of {card.name} ({card.cost}) is > 4')
            else:
                choice_selected = True
            


def get_card(card_name):
    if card_name == 'Copper':
        return Copper()
    elif card_name == 'Silver':
        return Silver()
    elif card_name == 'Gold':
        return Gold()
    elif card_name == 'Estate':
        return Estate()
    elif card_name == 'Duchy':
        return Duchy()
    elif card_name == 'Province':
        return Province()
    elif card_name == 'Curse':
        return Curse()
    elif card_name == 'Cellar':
        return Cellar()
    elif card_name == 'Chapel':
        return Chapel()
    elif card_name == 'Harbinger':
        return Harbinger()
    elif card_name == 'Merchant':
        return Merchant()
    elif card_name == 'Vassal':
        return Vassal()
    elif card_name == 'Village':
        return Village()
    elif card_name == 'Workshop':
        return Workshop()
    
    else:
        raise Exception(f'Card {card_name} not found...')


def convert_shorthand(sh):
    if sh == 'c':
        return 'Copper'
    elif sh == 's':
        return 'Silver'
    elif sh == 'g':
        return 'Gold'
    elif sh == 'e':
        return 'Estate'
    elif sh == 'd':
        return 'Duchy'
    elif sh == 'p':
        return 'Province'
    elif sh == 'crs':
        return 'Curse'
    elif sh == 'clr':
        return 'Cellar'
    elif sh == 'chp':
        return 'Chapel'
    elif sh == 'hrb':
        return 'Harbinger'
    elif sh == 'mrch':
        return 'Merchant'
    elif sh == 'vsl':
        return 'Vassal'
    elif sh == 'vlg':
        return 'Village'
    elif sh == 'wks':
        return 'Workshop'
    else:
        return sh
    
def print_card(self):

    card_width = 15  # Minimum width of 20
    card_height = 9  # Fixed height

    # Create the top and bottom border
    border = "+" + "-" * (card_width - 2) + "+"
    empty_row = "|" + " " * (card_width - 2) + "|"

    # Build the card row by row
    card = [border]
    for row in range(card_height):
        if row == 1:
            card.append("|" + self.name.center(card_width - 2) + "|")
        elif row == 3:
            card.append("|" + " ".join(["+" + str(self.plus_card), "Card"]).center(card_width - 2) + "|")
        elif row == 4:
            card.append("|" + " ".join(["+" + str(self.plus_action), "Action"]).center(card_width - 2) + "|")
        elif row == 5:
            card.append("|" + " ".join(["+" + str(self.plus_buy), "Buy"]).center(card_width - 2) + "|")
        elif row == 6:
            card.append("|" + " ".join(["+" + str(self.value_str)]).center(card_width - 2) + "|")
        elif row == 8:
            card.append("| " + str(self.cost) + " " * ((card_width - 2) - 2) + "|")
        else:
            card.append(empty_row)
    card.append(border)

    return card

def chunk_list(lst, chunk_size):
    """Splits a list into chunks of a given size."""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

def print_cards_in_row(card_objs, max_cards_per_row=9):
    """
    Prints cards, splitting into multiple rows if necessary.
    max_cards_per_row defines how many cards to display per row.
    """
    if not card_objs:
        return

    # Split the cards into chunks
    chunks = list(chunk_list(card_objs, max_cards_per_row))

    for chunk in chunks:
        # Generate card representations for this chunk
        cards = [print_card(card_obj) for card_obj in chunk]

        # Combine cards line by line
        for i in range(len(cards[0])):  # Loop through each "row" of the cards
            print("  ".join(card[i] for card in cards))  # Join corresponding rows
        print()  # Print an empty line between rows of cards
