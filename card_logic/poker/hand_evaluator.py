"""
Poker hand evaluation - determines hand rank and provides comparison.
"""

from typing import List, Tuple
from collections import Counter

from .card import Card

# Hand rank constants (higher = better)
HIGH_CARD = 0
ONE_PAIR = 1
TWO_PAIR = 2
THREE_OF_A_KIND = 3
STRAIGHT = 4
FLUSH = 5
FULL_HOUSE = 6
FOUR_OF_A_KIND = 7
STRAIGHT_FLUSH = 8
ROYAL_FLUSH = 9

# Human-readable names
HAND_NAMES = {
    0: "High Card",
    1: "One Pair",
    2: "Two Pair",
    3: "Three of a Kind",
    4: "Straight",
    5: "Flush",
    6: "Full House",
    7: "Four of a Kind",
    8: "Straight Flush",
    9: "Royal Flush"
}


class HandEvaluator:
    """Evaluates poker hands and returns ranking with details."""

    @staticmethod
    def evaluate(hand: List[Card]) -> Tuple[int, List[int], str]:
        """
        Evaluate a 5-card hand.

        Args:
            hand: List of 5 Card tuples

        Returns:
            Tuple of (rank_value, tiebreaker_ranks, hand_name)
            - rank_value: 0-9 indicating hand strength
            - tiebreaker_ranks: sorted ranks for comparing equal hands
            - hand_name: human-readable hand description

        Raises:
            ValueError: If hand doesn't contain exactly 5 cards
        """
        if len(hand) != 5:
            raise ValueError("Hand must contain exactly 5 cards")

        ranks = sorted([c[0] for c in hand], reverse=True)
        suits = [c[1] for c in hand]
        rank_counts = Counter(ranks)

        is_flush = len(set(suits)) == 1
        is_straight, straight_high = HandEvaluator._check_straight(ranks)

        # Royal Flush
        if is_flush and is_straight and straight_high == 14:
            return (ROYAL_FLUSH, [14], "Royal Flush")

        # Straight Flush
        if is_flush and is_straight:
            return (STRAIGHT_FLUSH, [straight_high], "Straight Flush")

        # Four of a kind
        if 4 in rank_counts.values():
            quad_rank = [r for r, c in rank_counts.items() if c == 4][0]
            kicker = [r for r, c in rank_counts.items() if c == 1][0]
            return (FOUR_OF_A_KIND, [quad_rank, kicker], "Four of a Kind")

        # Full house
        if 3 in rank_counts.values() and 2 in rank_counts.values():
            trip_rank = [r for r, c in rank_counts.items() if c == 3][0]
            pair_rank = [r for r, c in rank_counts.items() if c == 2][0]
            return (FULL_HOUSE, [trip_rank, pair_rank], "Full House")

        # Flush
        if is_flush:
            return (FLUSH, ranks, "Flush")

        # Straight
        if is_straight:
            return (STRAIGHT, [straight_high], "Straight")

        # Three of a kind
        if 3 in rank_counts.values():
            trip_rank = [r for r, c in rank_counts.items() if c == 3][0]
            kickers = sorted([r for r, c in rank_counts.items() if c == 1], reverse=True)
            return (THREE_OF_A_KIND, [trip_rank] + kickers, "Three of a Kind")

        # Two pair
        pairs = [r for r, c in rank_counts.items() if c == 2]
        if len(pairs) == 2:
            pairs.sort(reverse=True)
            kicker = [r for r, c in rank_counts.items() if c == 1][0]
            return (TWO_PAIR, pairs + [kicker], "Two Pair")

        # One pair
        if len(pairs) == 1:
            pair_rank = pairs[0]
            kickers = sorted([r for r, c in rank_counts.items() if c == 1], reverse=True)
            return (ONE_PAIR, [pair_rank] + kickers, "One Pair")

        # High card
        return (HIGH_CARD, ranks, "High Card")

    @staticmethod
    def _check_straight(ranks: List[int]) -> Tuple[bool, int]:
        """
        Check if sorted ranks form a straight.

        Args:
            ranks: List of ranks sorted descending

        Returns:
            Tuple of (is_straight, high_card_rank)
        """
        sorted_ranks = sorted(set(ranks), reverse=True)

        # Must have 5 unique ranks
        if len(sorted_ranks) != 5:
            return (False, 0)

        # Normal straight check (consecutive descending)
        if sorted_ranks[0] - sorted_ranks[4] == 4:
            return (True, sorted_ranks[0])

        # Wheel straight (A-2-3-4-5) - Ace counts as 1
        if sorted_ranks == [14, 5, 4, 3, 2]:
            return (True, 5)  # 5-high straight

        return (False, 0)

    @staticmethod
    def compare_hands(hand1: List[Card], hand2: List[Card]) -> int:
        """
        Compare two hands.

        Args:
            hand1: First hand
            hand2: Second hand

        Returns:
            1 if hand1 wins, -1 if hand2 wins, 0 if tie
        """
        eval1 = HandEvaluator.evaluate(hand1)
        eval2 = HandEvaluator.evaluate(hand2)

        # Compare hand ranks
        if eval1[0] != eval2[0]:
            return 1 if eval1[0] > eval2[0] else -1

        # Compare tiebreakers
        for r1, r2 in zip(eval1[1], eval2[1]):
            if r1 != r2:
                return 1 if r1 > r2 else -1

        return 0

    @staticmethod
    def get_hand_name(hand: List[Card]) -> str:
        """Get human-readable name for a hand."""
        _, _, name = HandEvaluator.evaluate(hand)
        return name

    @staticmethod
    def get_hand_rank(hand: List[Card]) -> int:
        """Get numeric rank (0-9) for a hand."""
        rank, _, _ = HandEvaluator.evaluate(hand)
        return rank
