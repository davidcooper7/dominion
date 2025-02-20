import sys, inspect, random
from supply import Supply


class Game():
    def __init__(self, players, packs=['basegame']):
        self.players = players
        self._set_supply(packs)
        self._add_opponents_to_player()
    
    def _set_supply(self, packs):
        card_pool = []
        for pack in packs:
            if pack == 'basegame':
                for name in ['Cellar', 'Chapel',  
                             'Harbinger', 'Merchant', 'Vassal', 'Village', 'Workshop',
                             'Bureaucrat', 'Militia', 'Gardens', 'Moneylender', 'Poacher', 'Remodel', 'Smithy', 'Throne Room',
                             'Bandit', 'Council Room', 'Festival', 'Laboratory', 'Library', 'Market', 'Mine', 'Sentry', 'Witch',
                             'Artisan']:
                    card_pool.append(name)

        kingdom_cards = random.sample(card_pool, 10)

        self.supply = Supply(len(self.players), kingdom_cards)

    def _add_opponents_to_player(self):
        for i, player_i in enumerate(self.players):
            for j, player_j in enumerate(self.players):
                if i != j:
                    player_i._add_opponent(player_j)
    
    def play(self):
        while not self._eval_winning_criterion():
            for player in self.players:
                print(f"\n***************It is {player.name}'s turn***************\n")
                player.take_turn(self.supply)
                if self._eval_winning_criterion():
                    break

        self._eval_win()

    def _eval_winning_criterion(self):
        if self.supply._check_qty('Province') == 0:
            return True
        elif self.supply._count_empty() >= 3:
            return True
        else:
            return False

    def _eval_win(self):
        most_points = 0
        wining_players = []
        for player in self.players:
            points = player._finish()
            print(f'> {player} finishes with {points} victory points!')
            if points > most_points:
                most_points = points
                wining_players = [player.name]
            elif points == most_points:
                wining_players.append(player.name)

        print(f'> Players {wining_players} win with {most_points}!!!')
            
                
    