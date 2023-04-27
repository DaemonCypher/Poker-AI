from pypokerengine.players import BasePokerPlayer
from pypokerengine.api.emulator import Emulator
from pypokerengine.utils.game_state_utils import restore_game_state
from pypokerengine.utils.card_utils import gen_cards
import time
class SimplePokerPlayer(BasePokerPlayer):

    def __init__(self):
        self.emulator = Emulator()

    # Setup Emulator object by registering game information
    def receive_game_start_message(self, game_info):
        player_num = game_info["player_num"]
        max_round = game_info["rule"]["max_round"]
        small_blind_amount = game_info["rule"]["small_blind_amount"]
        ante_amount = game_info["rule"]["ante"]
        blind_structure = game_info["rule"]["blind_structure"]
        
        self.emulator.set_game_rule(player_num, max_round, small_blind_amount, ante_amount)
        self.emulator.set_blind_structure(blind_structure)
        
        # Register players in the emulator
        for player_info in game_info["seats"]:
            self.emulator.register_player(player_info["uuid"], SimplePokerPlayer())

    def declare_action(self, valid_actions, hole_card, round_state):
        # This is a simple player that always calls
        start = time.time()
        end = time.time()
        print("\n Time taken to play: %.10f seconds" % (end - start) +"\n For Aggresive player")    
        return 'call', 0

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass


#nb_simulation = 1000
#nb_player = 3
#hole_card = ['H4', 'D7']
#community_card = ['D3', 'C5', 'C6']

#def estimate_hand_strength(nb_simulation, nb_player, hole_card, community_card):
#    simulation_results = []
#    for i in range(nb_simulation):
#        opponents_cards = []
#        for j in range(nb_player-1):  # nb_opponents = nb_player - 1
#            opponents_cards.append(draw_cards_from_deck(num=2))
#        nb_need_community = 5 - len(community_card)
#        community_card.append(draw_cards_from_deck(num=nb_need_community))
#        result = observe_game_result(hole_card, community_card, opponents_cards)  # return 1 if win else 0
#        simulation_results.append(result)
#    average_win_rate = 1.0 * sum(simulation_results) / len(simulation_results)
#    return average_win_rate