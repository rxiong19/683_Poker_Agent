from pypokerengine.engine.card import Card
from pypokerengine.players import BasePokerPlayer
from time import sleep
import pprint

from pypokerengine.utils.card_utils import estimate_hole_card_win_rate


class TestPlayer(BasePokerPlayer):

    # initialize tracker for opponent moves, and preset the opponent to do each move
    # 10 times at each stage so that it stays consistent early in the game
    opponent_moves = {'preflop': [], 'flop': [], 'turn': [], 'river': [], }
    for _ in range(10):
        for action in ['RAISE', 'CALL', 'FOLD']:
            for round in ['preflop', 'flop', 'turn', 'river']:
                opponent_moves[round].append(action)

    # frequencies (from simulating) of win probabilities at various stages f  the game
    probabilities = {'preflop': {
            '0-0.05': 0,
            '0.05-0.1': 0,
            '0.1-0.15': 0,
            '0.15-0.2': 0,
            '0.2-0.25': 13,
            '0.25-0.3': 408,
            '0.3-0.35': 1616,
            '0.35-0.4': 2874,
            '0.4-0.45': 3697,
            '0.45-0.5': 4259,
            '0.5-0.55': 4545,
            '0.55-0.6': 4243,
            '0.6-0.65': 2862,
            '0.65-0.7': 1198,
            '0.7-0.75': 247,
            '0.75-0.8': 224,
            '0.8-0.85': 235,
            '0.85-0.9': 98,
            '0.9-0.95': 1,
            '0.95-1': 0
        }, 'flop': {

            '0-0.05': 0,
            '0.05-0.1': 17,
            '0.1-0.15': 374,
            '0.15-0.2': 997,
            '0.2-0.25': 1463,
            '0.25-0.3': 1915,
            '0.3-0.35': 2150,
            '0.35-0.4': 2352,
            '0.4-0.45': 2472,
            '0.45-0.5': 2345,
            '0.5-0.55': 2183,
            '0.55-0.6': 1987,
            '0.6-0.65': 1727,
            '0.65-0.7': 1449,
            '0.7-0.75': 1266,
            '0.75-0.8': 1161,
            '0.8-0.85': 1160,
            '0.85-0.9': 764,
            '0.9-0.95': 539,
            '0.95-1': 199
        }, "turn": {

            '0-0.05': 37,
            '0.05-0.1': 543,
            '0.1-0.15': 980,
            '0.15-0.2': 1340,
            '0.2-0.25': 1609,
            '0.25-0.3': 1828,
            '0.3-0.35': 1836,
            '0.35-0.4': 1857,
            '0.4-0.45': 1904,
            '0.45-0.5': 1758,
            '0.5-0.55': 1877,
            '0.55-0.6': 1607,
            '0.6-0.65': 1445,
            '0.65-0.7': 1322,
            '0.7-0.75': 1256,
            '0.75-0.8': 1307,
            '0.8-0.85': 1290,
            '0.85-0.9': 1158,
            '0.9-0.95': 835,
            '0.95-1': 731
        }, "river": {
            '0-0.05': 1412,
            '0.05-0.1': 1317,
            '0.1-0.15': 1318,
            '0.15-0.2': 1386,
            '0.2-0.25': 1331,
            '0.25-0.3': 1278,
            '0.3-0.35': 1307,
            '0.35-0.4': 1304,
            '0.4-0.45': 1219,
            '0.45-0.5': 1320,
            '0.5-0.55': 1199,
            '0.55-0.6': 1288,
            '0.6-0.65': 1272,
            '0.65-0.7': 1213,
            '0.7-0.75': 1272,
            '0.75-0.8': 1212,
            '0.8-0.85': 1345,
            '0.85-0.9': 1373,
            '0.9-0.95': 1335,
            '0.95-1': 1819
        }
        }
    
    # how much to decrease win probability if the lower bound on opponent's expected win
    # probability exceeds the key
    prob_decreases = {
        'preflop': {
            0.0: 0.0,
            0.1: 0.0,
            0.2: 0.0,
            0.3: 0.0,
            0.4: 0.0,
            0.5: 0.02,
            0.6: 0.02,
            0.7: 0.02,
            0.8: 0.02,
            0.9: 0.02
        },
        'flop': {
            0.0: 0.0,
            0.1: 0.01,
            0.2: 0.02,
            0.3: 0.05,
            0.4: 0.08,
            0.5: 0.13,
            0.6: 0.17,
            0.7: 0.2,
            0.8: 0.2,
            0.9: 0.2,
        },
        'turn': {
            0.0: 0.0,
            0.1: 0.01,
            0.2: 0.03,
            0.3: 0.04,
            0.4: 0.06,
            0.5: 0.06,
            0.6: 0.14,
            0.7: 0.2,
            0.8: 0.2,
            0.9: 0.2,
        },
        'river': {
            0.0: 0.0,
            0.1: 0.02,
            0.2: 0.05,
            0.3: 0.08,
            0.4: 0.15,
            0.5: 0.2,
            0.6: 0.2,
            0.7: 0.2,
            0.8: 0.2,
            0.9: 0.2,
        }
    }

    def declare_action(self, valid_actions, hole_card, round_state):
        opponent_action = None
        opponent_uuid = ''
        # find opponent id
        for seat in round_state['seats']:
            if seat['uuid'] != self.uuid:
                opponent_uuid = seat['uuid']
                break
        # determine opponent move ensuring it is the first move they've made this round for move tracking
        for state in ['river', 'turn', 'flop', 'preflop']:
            if state in round_state["action_histories"].keys():
                river = round_state["action_histories"][state]
                if len(river) > 0 and river[-1]['uuid'] == opponent_uuid and river[-1]['action'] != 'SMALLBLIND' and river[-1]['action'] != 'BIGBLIND':
                    stopped = False
                    for i in range(len(river)-1):
                        if river[i]['uuid'] == opponent_uuid and river[i]['action'] != 'SMALLBLIND' and river[i]['action'] != 'BIGBLIND':
                            stopped = True
                            break
                    if not stopped:
                        self.opponent_moves[state].append(river[-1]['action'])
                        opponent_action = river[-1]['action']

       
       # For the game stage, find the expected lower bound win probability of opponent 
       # by using xth percentile of distribution
        def lower_bound_top_x_percent(probabilities, stage,  x):
            total_count = sum(probabilities[stage].values())
            total_prob = 0
            lower_bound = None

            for prob_range, count in probabilities[stage].items():
                prob_range_start, prob_range_end = map(
                    float, prob_range.split('-'))
                prob_range_width = prob_range_end - prob_range_start
                if total_count > 0:
                    prob_range_prob = count / total_count

                    total_prob += prob_range_prob

                    if total_prob >= x:
                        lower_bound = prob_range_start
                        break

            return lower_bound

        # same as above but in reverse
        def upper_bound_bottom_x_percent(probabilities, stage, x):
            total_count = sum(probabilities[stage].values())
            total_prob = 0
            lower_bound = None

            for prob_range, count in reversed(list(probabilities[stage].items())):
                prob_range_start, prob_range_end = map(
                    float, prob_range.split('-'))
                if total_count > 0:
                    prob_range_prob = count / total_count

                    total_prob += prob_range_prob

                    if total_prob >= x:
                        lower_bound = prob_range_end
                        break

            return lower_bound

        #test if an action is legal
        def move_is_valid(valid_actions, move):
            for action in valid_actions:
                if action['action'] == move:
                    return True
            return False
        
        #estimate a lower bound for opponent win probability at a stage if they raised
        def estimate_opponent_win_rate_raise(stage):
            raise_prob = self.opponent_moves[stage].count('RAISE') / len(self.opponent_moves[stage])
            return lower_bound_top_x_percent(self.probabilities, stage, raise_prob)
        
        #estimate an upper bound for opponent win probability at a stage if they called
        def estimate_opponent_win_rate_call(stage):
            raise_prob = self.opponent_moves[stage].count('RAISE') / len(self.opponent_moves[stage])
            return upper_bound_bottom_x_percent(self.probabilities, stage, 1-raise_prob)
        

        community_card = round_state['community_card']
        community_cards = []
        for card in community_card:
            community_cards.append(Card.from_str(card))
        hole_cards = [Card.from_str(
            hole_card[0]), Card.from_str(hole_card[1])]
        # 1500 simulations doesn't time out when we ran it, if it times out just decrement by 100 until it works
        # ideally we'd do at least 40k but that's not possible with the time constraint, and we'll still be in the right vicinity
        prob = estimate_hole_card_win_rate(
            1500, 2, hole_card=hole_cards, community_card=community_cards)
        # if opponent_action is not None and opponent_action == 'RAISE':
        #     est = estimate_opponent_win_rate_raise(round_state['street'])
        #     prob -= min(self.prob_decreases[round_state['street']][round(est * 10)/10], 0.0)


        # probability values were determined by making small adjustments and playing lots of game against each other
        # to find optimal values.
        if (round_state['street'] == 'preflop'):
            if prob > 0.62:
                if move_is_valid(valid_actions, 'raise'):
                    action = 'raise'
                elif move_is_valid(valid_actions, 'call'):
                    action = 'call'
                else:
                    action = 'fold'
            elif prob > 0.1:
                if move_is_valid(valid_actions, 'call'):
                    action = 'call'
                else:
                    action = 'fold'
            else:
                action = 'fold'
        else:
            if prob > 0.72:
                if move_is_valid(valid_actions, 'raise'):
                    action = 'raise'
                elif move_is_valid(valid_actions, 'call'):
                    action = 'call'
                else:
                    action = 'fold'
            elif prob > 0.19:
                if move_is_valid(valid_actions, 'call'):
                    action = 'call'
                else:
                    action = 'fold'
            else:
                action = 'fold'
        return action

    def receive_game_start_message(self, game_info):
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass


def setup_ai():
    return TestPlayer()
