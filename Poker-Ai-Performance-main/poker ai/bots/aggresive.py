import random
from pypokerengine.players import BasePokerPlayer
from pypokerengine.api.emulator import Emulator
from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate
import time
class AggressivePokerPlayer(BasePokerPlayer):
    def __init__(self):
        super().__init__()

    def declare_action(self, valid_actions, hole_card, round_state, street=None):
        # Prioritize raise/bet actions, if available
        start = time.time()
        raise_action = [a for a in valid_actions if a['action'] in ['raise', 'bet']]

        if raise_action:
            action_option = raise_action[0]
        else:
            # If no raise/bet action is available, choose the first valid action (usually 'call' or 'check')
            action_option = valid_actions[0]
        end = time.time()
        print("\n Time taken to play: %.10f seconds" % (end - start) +" For Agrgresive player")
        return action_option['action'], action_option['amount']['max'] if 'max' in action_option['amount'] else action_option['amount']['min']

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
