import sys, os, time
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append('..')
from basegame import Copper, Silver, Gold, Estate, Duchy, Province, Curse, Cellar, Chapel, Harbinger, Merchant, Vassal, Village, Workshop, Bureaucrat, Militia, Gardens, Moneylender, Poacher, Remodel, Smithy, ThroneRoom, Bandit, CouncilRoom, Festival, Laboratory, Library, Market, Mine, Sentry, Witch, Artisan

def read_input(input, player):
    if input == 'Supply':
        if hasattr(player, 'conn'):
            player.supply._display(conn=player.conn)
        else:
            player.supply._display()
        return read_input('', player)
    elif input == 'Hand':
        if hasattr(player, 'conn'):
            player.hand._display(conn=player.conn)
        else:
            player.hand._display()
        return read_input('', player)
    elif '--help' in input:
        try:
            card_name = convert_shorthand(input.split()[0])
            card = get_card(card_name)
            if hasattr(player, 'conn'):
                msg = card.__str__() + '_n'
                player.conn.sendall(msg.encode())
                time.sleep(0.01)
            else:
                print(card)
            return convert_shorthand(input)
        except:
            return convert_shorthand(input)
    else:
        return convert_shorthand(input)

def convert_shorthand(sh):
    shorthand_map = {
        'c': 'Copper',
        's': 'Silver',
        'g': 'Gold',
        'e': 'Estate',
        'd': 'Duchy',
        'p': 'Province',
        'grd': 'Gardens',
        'crs': 'Curse',
        'clr': 'Cellar',
        'chp': 'Chapel',
        'hrb': 'Harbinger',
        'mrch': 'Merchant',
        'vsl': 'Vassal',
        'vlg': 'Village',
        'wrk': 'Workshop',
        'brc': 'Bureaucrat',
        'mlt': 'Militia',
        'mnl': 'Moneylender',
        'pch': 'Poacher',
        'rmd': 'Remodel',
        'smt': 'Smithy',
        'thr': 'Throne Room',
        'bnd': 'Bandit',
        'crm': 'Council Room',
        'fst': 'Festival',
        'lab': 'Laboratory',
        'lib': 'Library',
        'mrk': 'Market',
        'min': 'Mine',
        'snt': 'Sentry',
        'wtch': 'Witch',
        'art': 'Artisan'
    }

    if sh in shorthand_map.keys():
        return shorthand_map[sh]
    else:
        return sh


def get_card(card_name):
    card_classes = {
        'Copper': Copper(),
        'Silver': Silver(),
        'Gold': Gold(),
        'Estate': Estate(),
        'Duchy': Duchy(),
        'Province': Province(),
        'Gardens': Gardens(),
        'Curse': Curse(),
        'Cellar': Cellar(),
        'Chapel': Chapel(),
        'Harbinger': Harbinger(),
        'Merchant': Merchant(),
        'Vassal': Vassal(),
        'Village': Village(),
        'Workshop': Workshop(),
        'Bureaucrat': Bureaucrat(),
        'Militia': Militia(),
        'Moneylender': Moneylender(),
        'Poacher': Poacher(),
        'Remodel': Remodel(),
        'Smithy': Smithy(),
        'Throne Room': ThroneRoom(),
        'Bandit': Bandit(),
        'Council Room': CouncilRoom(),
        'Festival': Festival(),
        'Laboratory': Laboratory(),
        'Library': Library(),
        'Market': Market(),
        'Mine': Mine(),
        'Sentry': Sentry(),
        'Witch': Witch(),
        'Artisan': Artisan()
    }
    
    if card_name in card_classes.keys():
        return card_classes[card_name]
    else:
        raise Exception(f'Card {card_name} not found...')



    
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

def print_cards_in_row(card_objs, max_cards_per_row=9, conn=None):
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
            if conn is None:
                print("  ".join(card[i] for card in cards))  # Join corresponding rows
            else:
                msg = "  ".join(card[i] for card in cards) + "_n"
                conn.sendall(msg.encode())
                time.sleep(0.01)
        if conn is None:
            print()  # Print an empty line between rows of cards
        else:
            msg = '_n' 
            conn.sendall(msg.encode())
            time.sleep(0.01)
