
from pypokerengine.players import BasePokerPlayer
from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate
import time
NB_SIMULATION = 1000

class HonestPlayer(BasePokerPlayer):

    def declare_action(self, valid_actions, hole_card, round_state):
        start = time.time()
        community_card = round_state['community_card']
        win_rate = estimate_hole_card_win_rate(
                nb_simulation=NB_SIMULATION,
                nb_player=self.nb_player,
                hole_card=gen_cards(hole_card),
                community_card=gen_cards(community_card)
                )
        if win_rate >= 1.0 / self.nb_player:
            action = valid_actions[1]  # fetch CALL action info
        else:
            action = valid_actions[0]  # fetch FOLD action info
        end = time.time()
        print("\n Time taken to play: %.10f seconds" % (end - start) +" For Honest player")    
        return action['action'], action['amount']

    def receive_game_start_message(self, game_info):
        self.nb_player = game_info['player_num']

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass
