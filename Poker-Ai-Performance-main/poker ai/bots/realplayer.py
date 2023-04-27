#from pypokerengine.api.game import setup_config, start_new_game
from pypokerengine.players import BasePokerPlayer
from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate, Card
import time
import random
NB_SIMULATION = 1000
class SelectivePokerPlayer(BasePokerPlayer):
    def is_strong_hand(self, hole_card_ranks):
        strong_hands = [
            [1, 1],  # A, A
            [13, 13],  # K, K
            [12, 12],  # Q, Q
            [11,11],
            [10,10],
            [9,9],
            [8,8],
            [7,7],
            [6,6],
            [14,14] # high A,A after K,Q,J
            
        ]
        return hole_card_ranks in strong_hands

    def is_connected_or_gapped(self, hole_card_ranks):
        card_values = hole_card_ranks
        gap = abs(card_values[0] - card_values[1])

        # Connected, 1-gapper, or 2-gapper
        return gap <= 2

    def declare_action(self, valid_actions, hole_card, round_state):
        start = time.time()

        hole_card_ranks = sorted([Card.from_str(card).rank for card in hole_card])
        is_strong = self.is_strong_hand(hole_card_ranks)
        is_connected_gapped = self.is_connected_or_gapped(hole_card_ranks)
        hole_card_suit = sorted([card[0] for card in hole_card])

        current_street = round_state['street']
        if hole_card_ranks[0] >= 10 or hole_card_ranks[1] >= 10:
            is_strong = True
        if current_street == 'preflop':
            if is_strong:
                last_bet = round_state['action_histories'][current_street][-1].get('amount', 0)
                raise_action = valid_actions[2]
                raise_amount = random.randint(3, 4) * last_bet
                action, amount = raise_action['action'], raise_amount
            elif is_connected_gapped:
                action, amount = valid_actions[1]['action'], valid_actions[1]['amount']
            elif hole_card_suit == ['D','D'] or hole_card_suit == ['S','S'] or hole_card_suit == ['C','C'] or hole_card_suit == ['H','H']: 
                action, amount = valid_actions[1]['action'], valid_actions[1]['amount']
            else:
                action, amount = valid_actions[0]['action'], valid_actions[0]['amount']
        else:
            call_action_info = valid_actions[1]
            action, amount = call_action_info["action"], call_action_info["amount"]
            
            community_card = round_state['community_card']
            win_rate = estimate_hole_card_win_rate(
                nb_simulation=NB_SIMULATION,
                nb_player=self.nb_player,
                hole_card=gen_cards(hole_card),
                community_card=gen_cards(community_card)
            )

            pot = round_state['pot']['main']['amount']
            
            if win_rate > 0.75:
                    bet_size = int(8 * pot / 10)
                    #min_raise = valid_actions[2] # Updated line
                    #max_raise = valid_actions[3]  # Updated line
                    #bet_size = min(max(min_raise, bet_size), max_raise)
                    action, amount = "raise", bet_size
            elif win_rate > 0.5:
                bet_size = int(pot / 3)
                #min_raise = valid_actions[2]  # Updated line
                #max_raise = valid_actions[2] # Updated line
                #bet_size = min(max(min_raise, bet_size), max_raise)
                action, amount = "raise", bet_size
            elif win_rate > 0.35:
                call_action_available = any(action["action"] == "call" for action in valid_actions)
                if call_action_available:
                    action, amount = "call", valid_actions[1]['amount']
                else:
                    action, amount = "check", 0
            else:
                action, amount = valid_actions[0]['action'], valid_actions[0]['amount']

        end = time.time()
        print("\n Time taken to play: %.10f seconds" % (end - start) + " For Real player")
        return action, amount


    
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

