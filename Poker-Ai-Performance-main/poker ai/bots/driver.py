from pypokerengine.api.game import setup_config, start_poker
from fishplayer import FishPlayer
from consoleplayer import ConsolePlayer
from randomplayer import RandomPlayer
from honestplayer import HonestPlayer
from aggresive import AggressivePokerPlayer
from emulator_player import *
from realplayer import SelectivePokerPlayer


emulator_player = EmulatorPlayer(opponents_model=MyModel())

config = setup_config(max_round=10000, initial_stack=1000, small_blind_amount=20)
config.register_player(name="f1", algorithm=FishPlayer())
#config.register_player(name="r1", algorithm=RandomPlayer())
#config.register_player(name="b1", algorithm=SelectivePokerPlayer())
#config.register_player(name="h1", algorithm=HonestPlayer())
#config.register_player(name="a1", algorithm=AggressivePokerPlayer())
config.register_player(name="em1", algorithm=emulator_player)

game_result = start_poker(config, verbose=1)

#fish
#aggresive
#honest
#random
