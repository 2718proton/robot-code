"""
Poker Robot Control System

A card game decision system for an IoT poker robot.

Main exports:
- get_poker_actions: Generate robot action sequence for card swapping
- Deck: Card deck management with tracking
- HandEvaluator: Poker hand evaluation
- PokerStrategy: Card swap decision logic

Example usage:
    from poker import Deck, get_poker_actions, HandEvaluator

    deck = Deck()
    hand = deck.generate_initial_hand()

    # Get robot actions
    actions = get_poker_actions(hand)

    # Evaluate hand
    rank, _, name = HandEvaluator.evaluate(hand)
"""

from .card import (
    Card,
    RANKS,
    SUITS,
    RANK_NAMES,
    SUIT_NAMES,
    card_to_string,
    card_to_full_string,
    create_full_deck,
    is_valid_card,
)

from .deck import Deck

from .hand_evaluator import (
    HandEvaluator,
    HAND_NAMES,
    HIGH_CARD,
    ONE_PAIR,
    TWO_PAIR,
    THREE_OF_A_KIND,
    STRAIGHT,
    FLUSH,
    FULL_HOUSE,
    FOUR_OF_A_KIND,
    STRAIGHT_FLUSH,
    ROYAL_FLUSH,
)

from .strategy import (
    PokerStrategy,
    get_discard_positions,
    MAX_SWAP_PER_ROUND,
)

from .robot_actions import (
    get_poker_actions,
    generate_swap_actions,
    generate_fill_actions,
    parse_action,
    count_swaps,
    get_swap_positions,
    HandWithEmpty,
)

__all__ = [
    # Card
    'Card',
    'RANKS',
    'SUITS',
    'RANK_NAMES',
    'SUIT_NAMES',
    'card_to_string',
    'card_to_full_string',
    'create_full_deck',
    'is_valid_card',
    # Deck
    'Deck',
    # Hand Evaluator
    'HandEvaluator',
    'HAND_NAMES',
    'HIGH_CARD',
    'ONE_PAIR',
    'TWO_PAIR',
    'THREE_OF_A_KIND',
    'STRAIGHT',
    'FLUSH',
    'FULL_HOUSE',
    'FOUR_OF_A_KIND',
    'STRAIGHT_FLUSH',
    'ROYAL_FLUSH',
    # Strategy
    'PokerStrategy',
    'get_discard_positions',
    'MAX_SWAP_PER_ROUND',
    # Robot Actions
    'get_poker_actions',
    'generate_swap_actions',
    'generate_fill_actions',
    'parse_action',
    'count_swaps',
    'get_swap_positions',
    'HandWithEmpty',
]

__version__ = '1.0.0'
