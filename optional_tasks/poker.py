#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------
# Реализуйте функцию best_hand, которая принимает на вход
# покерную 'руку' (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# 'руку' из 5ти карт. У каждой карты есть масть(suit) и
# ранг(rank)
# Масти: трефы(clubs, C), пики(spades, S), червы(hearts, H), бубны(diamonds, D)
# Ранги: 2, 3, 4, 5, 6, 7, 8, 9, 10 (ten, T), валет (jack, J), дама (queen, Q),
# король (king, K), туз (ace, A)
# Например: AS - туз пик (ace of spades), TH - десятка черв (ten of hearts),
# 3C - тройка треф (three of clubs)

# Задание со *.
# Реализуйте функцию best_wild_hand, которая принимает на вход
# покерную 'руку' (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# 'руку' из пяти карт. Кроме прочего в данном варианте 'рука'
# может включать джокера. Джокеры могут заменить карту любой
# масти и ранга того же цвета, в колоде два джокера.
# Черный джокер '?B' может быть использован в качестве треф
# или пик любого ранга, красный джокер '?R' - в качестве черв и бубен
# любого ранга.

# Одна функция уже реализована, сигнатуры и описания других даны.
# Вам наверняка пригодится itertools.
# Можно свободно определять свои функции и т.п.
# -----------------

from itertools import combinations, product
from collections.abc import Generator


RANK_MAP = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14
}
RED_JOKER = '?R'
BLACK_JOKER = '?B'
JOKERS = [RED_JOKER, BLACK_JOKER]
CLUBS, SPADES, HEARTS, DIAMONDS = 'C', 'S', 'H', 'D'
SUITS = [CLUBS, SPADES, HEARTS, DIAMONDS]


def hand_rank(hand: list[str]) -> tuple:
    """Возвращает значение определяющее ранг 'руки'"""
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):
        return 8, max(ranks)
    elif kind(4, ranks):
        return 7, kind(4, ranks), kind(1, ranks)
    elif kind(3, ranks) and kind(2, ranks):
        return 6, kind(3, ranks), kind(2, ranks)
    elif flush(hand):
        return 5, ranks
    elif straight(ranks):
        return 4, max(ranks)
    elif kind(3, ranks):
        return 3, kind(3, ranks), ranks
    elif two_pair(ranks):
        return 2, two_pair(ranks), ranks
    elif kind(2, ranks):
        return 1, kind(2, ranks), ranks
    else:
        return 0, ranks


def card_ranks(hand: list[str]) -> list[int]:
    """Возвращает список рангов (его числовой эквивалент),
    отсортированный от большего к меньшему"""

    result = sorted(list(map(get_rank, hand)), reverse=True)
    return result


def get_rank(card: str) -> int:
    return RANK_MAP.get(card[0])


def get_suit(card: str) -> str:
    return card[1]


def flush(hand: list[str]) -> bool:
    """Возвращает True, если все карты одной масти"""
    suits = list(map(get_suit, hand))
    return len(set(suits)) == 1


def straight(ranks: list[int]) -> bool:
    """Возвращает True, если отсортированные ранги формируют последовательность
    5ти, где у 5ти карт ранги идут по порядку (стрит)"""
    return ranks == list(range(ranks[0], ranks[-1] - 1, -1))


def kind(n: int, ranks: list[int]) -> int | None:
    """Возвращает первый ранг, который n раз встречается в данной руке.
    Возвращает None, если ничего не найдено"""

    current_rank = ranks[0]
    n_current_rank = 1
    for r in ranks[1:]:
        if r == current_rank:
            n_current_rank += 1
        else:
            if n_current_rank == n:
                break
            current_rank = r
            n_current_rank = 1
    else:
        if n_current_rank != n:
            current_rank = None
    return current_rank


def two_pair(ranks: list[int]) -> tuple[int, int] | None:
    """Если есть две пары, то возвращает два соответствующих ранга,
    иначе возвращает None"""
    result = None
    first_paired_rank = kind(2, ranks)
    if first_paired_rank is not None:
        rest_ranks = [r for r in ranks if r != first_paired_rank]
        second_paired_rank = kind(2, rest_ranks)
        if second_paired_rank is not None:
            result = first_paired_rank, second_paired_rank
    return result


def get_joker_replaces(joker: str, used_cards) -> Generator[str, None, None]:
    if joker == RED_JOKER:
        suits = [HEARTS, DIAMONDS]
    elif joker == BLACK_JOKER:
        suits = [CLUBS, SPADES]
    else:
        raise ValueError(f'Unknown joker: {joker}')
    for rank, suit in product(RANK_MAP.keys(), suits):
        card = f'{rank}{suit}'
        if card not in used_cards:
            yield card


def get_red_joker_cards(used_cards: list[str]) -> Generator[str, None, None]:
    return get_joker_replaces(RED_JOKER, used_cards)


def get_black_joker_cards(used_cards: list[str]) -> Generator[str, None, None]:
    return get_joker_replaces(BLACK_JOKER, used_cards)


def prepare_hand(hand: list[str]) -> list[str]:
    return list(map(prepare_card, hand))


def prepare_card(card: str) -> str:
    if not isinstance(card, str):
        raise ValueError(
            f'Card should be a string, got: '
            f'{card.__class__.__name__} - `{card}`'
        )
    card = card.upper()
    if len(card) != 2:
        raise ValueError(f'Card should have 2 letters, got `{card}`')

    if card not in JOKERS:
        if card[0] not in RANK_MAP.keys():
            raise ValueError(
                f'Unknown rank: `{card}`. '
                f'Possible ranks: {list(RANK_MAP.keys())}'
            )
        if card[1] not in SUITS:
            raise ValueError(
                f'Unknown suit: `{card}`. Possible ranks: {SUITS}'
            )
    return card


def best_hand(hand: list[str]) -> list[str]:
    """Из 'руки' в 7 карт возвращает лучшую 'руку' в 5 карт"""
    hand = prepare_hand(hand)
    best_score = ()
    result = []
    for possible_hand in combinations(hand, 5):
        score = hand_rank(possible_hand)
        if score > best_score:
            best_score = score
            result = possible_hand
    return result


def best_wild_hand(hand: list[str]) -> list[str]:
    """best_hand но с джокерами"""
    hand = prepare_hand(hand)
    best_score = ()
    result = []
    for possible_hand in combinations(hand, 5):
        possible_hand = list(possible_hand)
        cards_options = []
        if RED_JOKER in possible_hand:
            possible_hand.remove(RED_JOKER)
            cards_options.append(get_red_joker_cards(possible_hand))
        if BLACK_JOKER in possible_hand:
            possible_hand.remove(BLACK_JOKER)
            cards_options.append(get_black_joker_cards(possible_hand))
        cards_options.insert(0, [possible_hand])
        for cards in product(*cards_options):
            cards = [*cards[0], *cards[1:]]
            score = hand_rank(cards)
            if score > best_score:
                best_score = score
                result = cards
    return result


def test_best_hand() -> None:
    print('test_best_hand...')
    assert (sorted(best_hand('6C 7C 8C 9C TC 5C JS'.split()))
            == ['6C', '7C', '8C', '9C', 'TC'])
    assert (sorted(best_hand('TD TC TH 7C 7D 8C 8S'.split()))
            == ['8C', '8S', 'TC', 'TD', 'TH'])
    assert (sorted(best_hand('JD TC TH 7C 7D 7S 7H'.split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print('OK')


def test_best_wild_hand() -> None:
    print('test_best_wild_hand...')
    assert (sorted(best_wild_hand('6C 7C 8C 9C TC 5C ?B'.split()))
            == ['7C', '8C', '9C', 'JC', 'TC'])
    assert (sorted(best_wild_hand('TD TC 5H 5C 7C ?R ?B'.split()))
            == ['7C', 'TC', 'TD', 'TH', 'TS'])
    assert (sorted(best_wild_hand('JD TC TH 7C 7D 7S 7H'.split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print('OK')


if __name__ == '__main__':
    test_best_hand()
    test_best_wild_hand()
