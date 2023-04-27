from pypokerengine.players import BasePokerPlayer
from pypokerengine.api.emulator import Emulator
from pypokerengine.utils.card_utils import gen_cards
from pypokerengine.utils.game_state_utils import restore_game_state, attach_hole_card, attach_hole_card_from_deck
import time
NB_SIMULATION = 1000
DEBUG_MODE = True

def log(msg):
    if DEBUG_MODE: print("[debug_info] --> %s" % msg)

class MyModel(BasePokerPlayer):

    FOLD = 0
    CALL = 1
    MIN_RAISE = 2
    MAX_RAISE = 3

    def __init__(self):
        super().__init__()
        self.action = None

    def declare_action(self, valid_actions, hole_card, round_state):
        self.action = self.CALL
        return valid_actions[self.action]['action'], valid_actions[self.action]['amount']

class EmulatorPlayer(BasePokerPlayer):

    def __init__(self, opponents_model=None):
        super().__init__()
        self.opponents_model = opponents_model

    def set_opponents_model(self, model_player):
        self.opponents_model = model_player

    def receive_game_start_message(self, game_info):
        self.my_model = MyModel()
        nb_player = game_info['player_num']
        max_round = game_info['rule']['max_round']
        sb_amount = game_info['rule']['small_blind_amount']
        ante_amount = game_info['rule']['ante']

        self.emulator = Emulator()
        self.emulator.set_game_rule(nb_player, max_round, sb_amount, ante_amount)
        for player_info in game_info['seats']:
            uuid = player_info['uuid']
            player_model = self.my_model if uuid == self.uuid else self.opponents_model
            self.emulator.register_player(uuid, player_model)

    def declare_action(self, valid_actions, hole_card, round_state):
        start = time.time()
        try_actions = [MyModel.FOLD, MyModel.CALL, MyModel.MIN_RAISE, MyModel.MAX_RAISE]

        log("hole_card of emulator player is %s" % hole_card)
        action_results = []
        for action in try_actions:
            self.my_model.action = action
            simulation_results = []
            for _ in range(NB_SIMULATION):
                game_state = self._setup_game_state(round_state, hole_card)
                round_finished_state, _events = self.emulator.run_until_round_finish(game_state)
                my_stack = [player for player in round_finished_state['table'].seats.players if player.uuid == self.uuid][0].stack
                simulation_results.append(my_stack)
                
            action_results.append(sum(simulation_results) / NB_SIMULATION)
            log("average stack after simulation when declares %s : %s" % (
                {0:'FOLD', 1:'CALL', 2:'MIN_RAISE', 3:'MAX_RAISE'}[action], action_results[-1])
                )

        best_action = max(zip(action_results, try_actions))[1]
        self.my_model.action = best_action
        end = time.time()
        print("\n Time taken to play: %.10f seconds" % (end - start) + " Emulator player")
        return self.my_model.declare_action(valid_actions, hole_card, round_state)


    def _setup_game_state(self, round_state, my_hole_card):
        game_state = restore_game_state(round_state)
        game_state['table'].deck.shuffle()
        player_uuids = [player_info['uuid'] for player_info in round_state['seats']]
        for uuid in player_uuids:
            if uuid == self.uuid:
                game_state = attach_hole_card(game_state, uuid, gen_cards(my_hole_card))  # attach my holecard
            else:
                game_state = attach_hole_card_from_deck(game_state, uuid)  # attach opponents holecard at random
        return game_state

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, new_action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass


