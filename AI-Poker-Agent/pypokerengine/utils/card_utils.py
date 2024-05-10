import random

from pypokerengine.engine.card import Card
from pypokerengine.engine.deck import Deck
from pypokerengine.engine.hand_evaluator import HandEvaluator

def gen_cards(cards_str):
    return [Card.from_str(s) for s in cards_str]

def estimate_hole_card_win_rate(nb_simulation, nb_player, hole_card, community_card=None):
    if not community_card: community_card = []
    win_count = sum([_montecarlo_simulation(nb_player, hole_card, community_card) for _ in range(nb_simulation)])
    return 1.0 * win_count / nb_simulation

def gen_deck(exclude_cards=None):
    deck_ids = range(1, 53)
    if exclude_cards:
        assert isinstance(exclude_cards, list)
        if isinstance(exclude_cards[0], str):
            exclude_cards = [Card.from_str(s) for s in exclude_cards]
        exclude_ids = [card.to_id() for card in exclude_cards]
        deck_ids = [i for i in deck_ids if not i in exclude_ids]
    return Deck(deck_ids)

def evaluate_hand(hole_card, community_card):
    assert len(hole_card)==2 and len(community_card)==5
    hand_info = HandEvaluator.gen_hand_rank_info(hole_card, community_card)
    return {
            "hand": hand_info["hand"]["strength"],
            "strength": HandEvaluator.eval_hand(hole_card, community_card)
            }

def _montecarlo_simulation(nb_player, hole_card, community_card):
    community_card = _fill_community_card(community_card, used_card=hole_card+community_card)
    unused_cards = _pick_unused_card((nb_player-1)*2, hole_card + community_card)
    opponents_hole = [unused_cards[2*i:2*i+2] for i in range(nb_player-1)]
    opponents_score = [HandEvaluator.eval_hand(hole, community_card) for hole in opponents_hole]
    my_score = HandEvaluator.eval_hand(hole_card, community_card)
    return 1 if my_score >= max(opponents_score) else 0

def _fill_community_card(base_cards, used_card):
    need_num = 5 - len(base_cards)
    return base_cards + _pick_unused_card(need_num, used_card)

def _pick_unused_card(card_num, used_card):
    used = [card.to_id() for card in used_card]
    unused = [card_id for card_id in range(1, 53) if card_id not in used]
    choiced = random.sample(unused, card_num)
    return [Card.from_id(card_id) for card_id in choiced]


# deck = gen_deck().deck
# values = []
# for i in range(len(deck)):
#     for j in range(i + 1, len(deck)):
#         for _ in range(20):
#             prob = estimate_hole_card_win_rate(500, 2, [deck[i], deck[j]])
#             values.append(prob)
# print('0 community cards')
# print("0-0.05", len([value for value in values if 0 <= value < 0.05]))
# print("0.05-0.1", len([value for value in values if 0.05 <= value < 0.1]))
# print("0.1-0.15", len([value for value in values if 0.1 <= value < 0.15]))
# print("0.15-0.2", len([value for value in values if 0.15 <= value < 0.2]))
# print("0.2-0.25", len([value for value in values if 0.2 <= value < 0.25]))
# print("0.25-0.3", len([value for value in values if 0.25 <= value < 0.3]))
# print("0.3-0.35", len([value for value in values if 0.3 <= value < 0.35]))
# print("0.35-0.4", len([value for value in values if 0.35 <= value < 0.4]))
# print("0.4-0.45", len([value for value in values if 0.4 <= value < 0.45]))
# print("0.45-0.5", len([value for value in values if 0.45 <= value < 0.5]))
# print("0.5-0.55", len([value for value in values if 0.5 <= value < 0.55]))
# print("0.55-0.6", len([value for value in values if 0.55 <= value < 0.6]))
# print("0.6-0.65", len([value for value in values if 0.6 <= value < 0.65]))
# print("0.65-0.7", len([value for value in values if 0.65 <= value < 0.7]))
# print("0.7-0.75", len([value for value in values if 0.7 <= value < 0.75]))
# print("0.75-0.8", len([value for value in values if 0.75 <= value < 0.8]))
# print("0.8-0.85", len([value for value in values if 0.8 <= value < 0.85]))
# print("0.85-0.9", len([value for value in values if 0.85 <= value < 0.9]))
# print("0.9-0.95", len([value for value in values if 0.9 <= value < 0.95]))
# print("0.95-1", len([value for value in values if value >= 0.95]))
#
#
# deck = gen_deck().deck
# values = []
# for i in range(len(deck)):
#     for j in range(i + 1, len(deck)):
#         for _ in range(20):
#             new_deck = gen_deck([deck[i], deck[j]])
#             new_deck.shuffle()
#             new_deck = new_deck.deck
#             prob = estimate_hole_card_win_rate(500, 2, [deck[i], deck[j]], [new_deck[0], new_deck[1], new_deck[2]])
#             values.append(prob)
#
# print('3 Community Cards')
# print("0-0.05", len([value for value in values if 0 <= value < 0.05]))
# print("0.05-0.1", len([value for value in values if 0.05 <= value < 0.1]))
# print("0.1-0.15", len([value for value in values if 0.1 <= value < 0.15]))
# print("0.15-0.2", len([value for value in values if 0.15 <= value < 0.2]))
# print("0.2-0.25", len([value for value in values if 0.2 <= value < 0.25]))
# print("0.25-0.3", len([value for value in values if 0.25 <= value < 0.3]))
# print("0.3-0.35", len([value for value in values if 0.3 <= value < 0.35]))
# print("0.35-0.4", len([value for value in values if 0.35 <= value < 0.4]))
# print("0.4-0.45", len([value for value in values if 0.4 <= value < 0.45]))
# print("0.45-0.5", len([value for value in values if 0.45 <= value < 0.5]))
# print("0.5-0.55", len([value for value in values if 0.5 <= value < 0.55]))
# print("0.55-0.6", len([value for value in values if 0.55 <= value < 0.6]))
# print("0.6-0.65", len([value for value in values if 0.6 <= value < 0.65]))
# print("0.65-0.7", len([value for value in values if 0.65 <= value < 0.7]))
# print("0.7-0.75", len([value for value in values if 0.7 <= value < 0.75]))
# print("0.75-0.8", len([value for value in values if 0.75 <= value < 0.8]))
# print("0.8-0.85", len([value for value in values if 0.8 <= value < 0.85]))
# print("0.85-0.9", len([value for value in values if 0.85 <= value < 0.9]))
# print("0.9-0.95", len([value for value in values if 0.9 <= value < 0.95]))
# print("0.95-1", len([value for value in values if value >= 0.95]))
#
#
# deck = gen_deck().deck
# values = []
# for i in range(len(deck)):
#     for j in range(i + 1, len(deck)):
#         for _ in range(20):
#             new_deck = gen_deck([deck[i], deck[j]])
#             new_deck.shuffle()
#             new_deck = new_deck.deck
#             prob = estimate_hole_card_win_rate(500, 2, [deck[i], deck[j]], [new_deck[0], new_deck[1], new_deck[2], new_deck[3]])
#             values.append(prob)
#
# print('4 community cards')
# print("0-0.05", len([value for value in values if 0 <= value < 0.05]))
# print("0.05-0.1", len([value for value in values if 0.05 <= value < 0.1]))
# print("0.1-0.15", len([value for value in values if 0.1 <= value < 0.15]))
# print("0.15-0.2", len([value for value in values if 0.15 <= value < 0.2]))
# print("0.2-0.25", len([value for value in values if 0.2 <= value < 0.25]))
# print("0.25-0.3", len([value for value in values if 0.25 <= value < 0.3]))
# print("0.3-0.35", len([value for value in values if 0.3 <= value < 0.35]))
# print("0.35-0.4", len([value for value in values if 0.35 <= value < 0.4]))
# print("0.4-0.45", len([value for value in values if 0.4 <= value < 0.45]))
# print("0.45-0.5", len([value for value in values if 0.45 <= value < 0.5]))
# print("0.5-0.55", len([value for value in values if 0.5 <= value < 0.55]))
# print("0.55-0.6", len([value for value in values if 0.55 <= value < 0.6]))
# print("0.6-0.65", len([value for value in values if 0.6 <= value < 0.65]))
# print("0.65-0.7", len([value for value in values if 0.65 <= value < 0.7]))
# print("0.7-0.75", len([value for value in values if 0.7 <= value < 0.75]))
# print("0.75-0.8", len([value for value in values if 0.75 <= value < 0.8]))
# print("0.8-0.85", len([value for value in values if 0.8 <= value < 0.85]))
# print("0.85-0.9", len([value for value in values if 0.85 <= value < 0.9]))
# print("0.9-0.95", len([value for value in values if 0.9 <= value < 0.95]))
# print("0.95-1", len([value for value in values if value >= 0.95]))
#
#
# deck = gen_deck().deck
# values = []
# for i in range(len(deck)):
#     for j in range(i + 1, len(deck)):
#         for _ in range(20):
#             new_deck = gen_deck([deck[i], deck[j]])
#             new_deck.shuffle()
#             new_deck = new_deck.deck
#             prob = estimate_hole_card_win_rate(500, 2, [deck[i], deck[j]], [new_deck[0], new_deck[1], new_deck[2], new_deck[3], new_deck[4]])
#             values.append(prob)
#
# print('5 community cards')
# print("0-0.05", len([value for value in values if 0 <= value < 0.05]))
# print("0.05-0.1", len([value for value in values if 0.05 <= value < 0.1]))
# print("0.1-0.15", len([value for value in values if 0.1 <= value < 0.15]))
# print("0.15-0.2", len([value for value in values if 0.15 <= value < 0.2]))
# print("0.2-0.25", len([value for value in values if 0.2 <= value < 0.25]))
# print("0.25-0.3", len([value for value in values if 0.25 <= value < 0.3]))
# print("0.3-0.35", len([value for value in values if 0.3 <= value < 0.35]))
# print("0.35-0.4", len([value for value in values if 0.35 <= value < 0.4]))
# print("0.4-0.45", len([value for value in values if 0.4 <= value < 0.45]))
# print("0.45-0.5", len([value for value in values if 0.45 <= value < 0.5]))
# print("0.5-0.55", len([value for value in values if 0.5 <= value < 0.55]))
# print("0.55-0.6", len([value for value in values if 0.55 <= value < 0.6]))
# print("0.6-0.65", len([value for value in values if 0.6 <= value < 0.65]))
# print("0.65-0.7", len([value for value in values if 0.65 <= value < 0.7]))
# print("0.7-0.75", len([value for value in values if 0.7 <= value < 0.75]))
# print("0.75-0.8", len([value for value in values if 0.75 <= value < 0.8]))
# print("0.8-0.85", len([value for value in values if 0.8 <= value < 0.85]))
# print("0.85-0.9", len([value for value in values if 0.85 <= value < 0.9]))
# print("0.9-0.95", len([value for value in values if 0.9 <= value < 0.95]))
# print("0.95-1", len([value for value in values if value >= 0.95]))

# import matplotlib.pyplot as plt
# plt.rcParams.update({'figure.figsize': (7, 5), 'figure.dpi': 100})
#
# # Plot Histogram on x
# plt.hist(values, bins=20)
# plt.show()
# plt.gca().set(title='Frequency Histogram', ylabel='Frequency')
# plt.plot()