from pypokerengine.players import BasePokerPlayer
from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate, Card

class PokerHandChartBot(BasePokerPlayer):
    HAND_CHART = [
        ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', '77', '66', '55', '44', '33', '22'],
        ['AKs', 'AQs', 'AJs', 'ATs', 'A9s', 'A8s', 'A7s', 'A6s', 'A5s', 'A4s', 'A3s', 'A2s'],
        ['KQs', 'KJs', 'KTs', 'K9s', 'K8s', 'K7s', 'K6s', 'K5s', 'K4s', 'K3s', 'K2s'],
        ['QJs', 'QTs', 'Q9s', 'Q8s', 'Q7s', 'Q6s', 'Q5s', 'Q4s', 'Q3s', 'Q2s'],
        ['JTs', 'J9s', 'J8s', 'J7s', 'J6s', 'J5s', 'J4s', 'J3s', 'J2s'],
        ['T9s', 'T8s', 'T7s', 'T6s', 'T5s', 'T4s', 'T3s', 'T2s'],
        ['98s', '97s', '96s', '95s', '94s', '93s', '92s'],
        ['87s', '86s', '85s', '84s', '83s', '82s'],
        ['76s', '75s', '74s', '73s', '72s'],
        ['65s', '64s', '63s', '62s'],
        ['54s', '53s', '52s'],
        ['43s', '42s'],
        ['32s'],
    ]

    def get_hand_strength(self, hole_card):
        hole_card_objects = [Card.from_str(card_str) for card_str in hole_card]
        hole_card_objects = sorted(hole_card_objects, key=lambda card: -card.rank)
        hole_card_str = ''.join([str(card.to_id()[0]) for card in hole_card_objects])

        if hole_card_objects[0].suit == hole_card_objects[1].suit:
            hole_card_str += 's'
        else:
            hole_card_str += 'o'

        for index, category in enumerate(self.HAND_CHART):
            if hole_card_str in category:
                return index

        return len(self.HAND_CHART)





    def declare_action(self, valid_actions, hole_card, round_state):
        hand_strength = self.get_hand_strength(hole_card)
        # Adjust the threshold based on your desired strategy
        play_threshold = 3

        if hand_strength <= play_threshold:
            action = "raise" if "raise" in [a["action"] for a in valid_actions] else "call"
        else:
            action = "fold"

        amount = [a["amount"] for a in valid_actions if a["action"] == action][0]
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
