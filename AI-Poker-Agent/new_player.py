from pypokerengine.engine.card import Card
from pypokerengine.players import BasePokerPlayer
from time import sleep
import pprint

from pypokerengine.utils.card_utils import estimate_hole_card_win_rate


class NewPlayer(BasePokerPlayer):

    def declare_action(self, valid_actions, hole_card, round_state):
        def move_is_valid(valid_actions, move):
            for action in valid_actions:
                if action['action'] == move:
                    return True
            return False
        community_card = round_state['community_card']
        community_cards = []
        for card in community_card:
            community_cards.append(Card.from_str(card))
        hole_cards = [Card.from_str(hole_card[0]), Card.from_str(hole_card[1])]
        prob = estimate_hole_card_win_rate(
            500, 2, hole_card=hole_cards, community_card=community_cards)
        if (prob > 0.5 and move_is_valid(valid_actions, 'raise')):
            action = 'raise'
        elif move_is_valid(valid_actions, 'call'):
            action = 'call'
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
    return NewPlayer()
