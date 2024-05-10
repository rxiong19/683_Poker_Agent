import random
import time

from matplotlib import pyplot as plt

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

# FIGURE OUT HOW MANY SIMULATIONS MONTE CARLO STABILIZES AT
# values = []
# total = 0
# hole_card = [Card(4, 13), Card(4, 11)]
# print(hole_card[0])
# print(hole_card[1])
# community_card = []
# limit = 500
# for j in range(limit):
#     community_card = []
#     community_card = _fill_community_card(community_card, used_card=hole_card + community_card)
#     unused_cards = _pick_unused_card((2 - 1) * 2, hole_card + community_card)
#     opponents_hole = [unused_cards[2 * i:2 * i + 2] for i in range(2 - 1)]
#     opponents_score = [HandEvaluator.eval_hand(hole, community_card) for hole in opponents_hole]
#     my_score = HandEvaluator.eval_hand(hole_card, community_card)
#     if my_score >= max(opponents_score):
#         total += 1
#     values.append(total / (j+1))
#     print(j)
#
# ax = plt.gca()
# ax.set_xlim([1, limit])
# ax.set_ylim([0.5, 0.7])
# x_vals = list(range(1, len(values) + 1))
# plt.plot(x_vals, values)
# plt.show()

def estimate_hole_card_win_rate_against_good_hand(nb_simulation, nb_player, hole_card, community_card=None):
    if not community_card: community_card = []
    plays = [0,0,0,0,0,0,0,0,0,0]
    wins = [0,0,0,0,0,0,0,0,0,0]
    for _ in range(nb_simulation):
        score, prob = montecarlo_simulation_extra_high(nb_player, hole_card, community_card)
        for i in range(len(plays)):
            if prob >= (i+1) * 0.1:
                plays[i] += 1
                if score == 1:
                    wins[i] += 1
    probs = []
    for i in range(len(plays)):
        if plays[i] > 0:
            probs.append(wins[i] / plays[i])
        else:
            probs.append(None)
    return probs

def montecarlo_simulation_extra_high(nb_player, hole_card, orig_community_card):
    community_card = _fill_community_card(orig_community_card, used_card=hole_card+orig_community_card)
    unused_cards = _pick_unused_card((nb_player-1)*2, hole_card + community_card)
    opponents_hole = [unused_cards[2*i:2*i+2] for i in range(nb_player-1)]
    opponent_prob = estimate_hole_card_win_rate(750, 2, opponents_hole[0], orig_community_card)
    opponents_score = [HandEvaluator.eval_hand(hole, community_card) for hole in opponents_hole]
    my_score = HandEvaluator.eval_hand(hole_card, community_card)
    return 1 if my_score >= max(opponents_score) else 0, opponent_prob



def estimate_hole_card_win_rate_against_bad_hand(nb_simulation, nb_player, hole_card, community_card=None):
    if not community_card: community_card = []
    plays = [0,0,0,0,0,0,0,0,0,0]
    wins = [0,0,0,0,0,0,0,0,0,0]
    for _ in range(nb_simulation):
        score, prob = montecarlo_simulation_extra_high(nb_player, hole_card, community_card)
        for i in range(len(plays)):
            if prob < i * 0.1:
                plays[i] += 1
                if score == 1:
                    wins[i] += 1
    probs = []
    for i in range(len(plays)):
        if plays[i] > 0:
            probs.append(wins[i] / plays[i])
        else:
            probs.append(None)

def montecarlo_simulation_extra_high(nb_player, hole_card, orig_community_card):
    community_card = _fill_community_card(orig_community_card, used_card=hole_card+orig_community_card)
    unused_cards = _pick_unused_card((nb_player-1)*2, hole_card + community_card)
    opponents_hole = [unused_cards[2*i:2*i+2] for i in range(nb_player-1)]
    opponent_prob = estimate_hole_card_win_rate(500, 2, opponents_hole[0], orig_community_card)
    opponents_score = [HandEvaluator.eval_hand(hole, community_card) for hole in opponents_hole]
    my_score = HandEvaluator.eval_hand(hole_card, community_card)
    return 1 if my_score >= max(opponents_score) else 0, opponent_prob


for _ in range(5):
    deck = gen_deck()
    deck.shuffle()
    hole_card = [deck.deck[0], deck.deck[1]]
    community_card = [deck.deck[2], deck.deck[3], deck.deck[4], deck.deck[5], deck.deck[6]]
    print(estimate_hole_card_win_rate(10000, 2, hole_card, community_card)) #baseline

    num_sims = 5000
    start = time.time()
    print(estimate_hole_card_win_rate_against_good_hand(750, 2, hole_card, community_card))
    print(time.time() - start)