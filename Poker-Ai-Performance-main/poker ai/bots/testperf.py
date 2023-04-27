import sys

sys.path.insert(0, './pypokerengine/api/')

from pypokerengine.api.game import setup_config, start_poker

import time
from argparse import ArgumentParser


from fishplayer import FishPlayer
from consoleplayer import ConsolePlayer
from randomplayer import RandomPlayer
from honestplayer import HonestPlayer
from aggresive import AggressivePokerPlayer
from simplebot import SimplePokerPlayer
from realplayer import RealPlayer
from emulator_player import *
import sys
# redirect terminal output to a text file for processing the time taken for bots
sys.stdout = open("log.txt","w")

def testperf(agent_name1, agent1, agent_name2, agent2):
    start = time.time()
   
    num_game = 50
    max_round = 100
    initial_stack = 200
    smallblind_amount = 1

    # Init pot of players
    # Init number of wins
    agent1_win = 0
    agent2_win = 0
    agent1_total = 0
    agent2_total = 0
    # Setting configuration
    config = setup_config(max_round=max_round, initial_stack=initial_stack, small_blind_amount=smallblind_amount)
    emulator_player = EmulatorPlayer(opponents_model=MyModel())
    # Register players
    agent1_name = "FishPlayer"
    agent2_name = "RandomPlayer"
    config.register_player(name=agent1_name, algorithm=FishPlayer())
    config.register_player(name=agent2_name, algorithm=emulator_player)

    for game in range(1, num_game + 1):
        print("Game number: ", game)
        game_result = start_poker(config, verbose=0)
        # check which bot has a complete win against the other
        if game_result['players'][0]['stack'] == 400:
            agent1_win+=1
        elif game_result['players'][1]['stack'] == 400:
            agent2_win+=1
        else:
            agent2_win+=0
            agent2_win+=0
        # check the amount won per bot
        if game_result['players'][0]['stack'] ==0:
            agent2_total +=game_result['players'][1]['stack'] -200
        elif game_result['players'][1]['stack'] ==0:
            agent1_total +=game_result['players'][0]['stack'] -200
        else:
            agent2_total +=game_result['players'][1]['stack'] -200
            agent1_total +=game_result['players'][0]['stack'] -200
        end = time.time()
        if (end-start)> 3600:
            print("\n After playing {} games of {} rounds, the results are: ".format(num_game, max_round))
            print("\n " + agent1_name + "'s number of wins: ", agent1_win)
            print("\n " + agent2_name + "'s number of wins: ", agent2_win)
            print("agent1 total wins",agent1_total)
            print("agent2 total wins", agent2_total)
            if (agent1_win < agent2_win):
                print("\n Congratulations! " + agent2_name + " has won.")
            elif (agent1_win > agent2_win):
                print("\n Congratulations! " + agent1_name + " has won.")

            else:
                print("\n It's a draw!")
            sys.exit()

    print("\n After playing {} games of {} rounds, the results are: ".format(num_game, max_round))
    # print("\n Agent 1's final pot: ", agent1_pot)
    print("\n " + agent1_name + "'s number of wins: ", agent1_win)
    print("\n " + agent2_name + "'s number of wins: ", agent2_win)
    print("\n " + agent1_name +" total wins",agent1_total)
    print("\n " + agent2_name +" total wins",agent2_total)

    if (agent1_win < agent2_win):
        print("\n Congratulations! " + agent2_name + " has won big blinds.")
    elif (agent1_win > agent2_win):
        print("\n Congratulations! " + agent1_name + " has won big blinds.")
    else:
        print("\n It's a draw!")


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument('-n1', '--agent_name1', help="Name of agent 1", default="Your agent", type=str)
    parser.add_argument('-a1', '--agent1', help="Agent 1", default=RandomPlayer())
    parser.add_argument('-n2', '--agent_name2', help="Name of agent 2", default="Your agent", type=str)
    parser.add_argument('-a2', '--agent2', help="Agent 2", default=RandomPlayer())
    args = parser.parse_args()
    return args.agent_name1, args.agent1, args.agent_name2, args.agent2


if __name__ == '__main__':
    name1, agent1, name2, agent2 = parse_arguments()
    start = time.time()
    testperf(name1, agent1, name2, agent2)
    end = time.time()

    print("\n Time taken to play: %.4f seconds" % (end - start))
