"""
Poker strategy - determines which cards to discard for best winning chance.
"""

from typing import List, Set, Optional
from collections import Counter

from .card import Card
from .hand_evaluator import (
    HandEvaluator,
    STRAIGHT, FLUSH, FULL_HOUSE, FOUR_OF_A_KIND, STRAIGHT_FLUSH, ROYAL_FLUSH
)

# Maximum cards to swap per round (standard draw poker rule)
MAX_SWAP_PER_ROUND = 3


class PokerStrategy:
    """Determines which cards to swap in 5-card draw poker."""

    # Minimum hand rank to keep (don't swap if hand is this good or better)
    KEEP_THRESHOLD = {
        'conservative': FULL_HOUSE,      # 6 - Full house or better
        'standard': STRAIGHT,            # 4 - Straight or better
        'aggressive': FOUR_OF_A_KIND     # 7 - Four of a kind or better
    }

    def __init__(self, mode: str = 'standard'):
        """
        Initialize strategy with a play mode.

        Args:
            mode: 'conservative', 'standard', or 'aggressive'
        """
        self.mode = mode
        self.threshold = self.KEEP_THRESHOLD.get(mode, STRAIGHT)

    def get_cards_to_discard(self, hand: List[Card]) -> List[int]:
        """
        Determine which card positions (0-4) to discard.

        Args:
            hand: Current 5-card hand (positions 0-4)

        Returns:
            List of position indices to discard (empty if hand is good enough).
            Maximum 3 positions returned (standard draw poker rule).
        """
        hand_rank, tiebreakers, hand_name = HandEvaluator.evaluate(hand)

        # Keep if hand meets threshold
        if hand_rank >= self.threshold:
            return []

        ranks = [c[0] for c in hand]
        suits = [c[1] for c in hand]
        rank_counts = Counter(ranks)
        suit_counts = Counter(suits)

        discard_positions = []

        # Four of a kind - keep all
        if hand_rank == FOUR_OF_A_KIND:
            return []

        # Full house - keep all
        if hand_rank == FULL_HOUSE:
            return []

        # Flush - keep all
        if hand_rank == FLUSH:
            return []

        # Straight - keep all
        if hand_rank == STRAIGHT:
            return []

        # Three of a kind - discard the two non-matching cards
        if hand_rank == 3:  # THREE_OF_A_KIND
            trip_rank = [r for r, c in rank_counts.items() if c == 3][0]
            discard_positions = [i for i, card in enumerate(hand) if card[0] != trip_rank]

        # Two pair - discard the odd card
        elif hand_rank == 2:  # TWO_PAIR
            pair_ranks = [r for r, c in rank_counts.items() if c == 2]
            discard_positions = [i for i, card in enumerate(hand) if card[0] not in pair_ranks]

        # One pair - discard the three non-pair cards
        elif hand_rank == 1:  # ONE_PAIR
            pair_rank = [r for r, c in rank_counts.items() if c == 2][0]
            discard_positions = [i for i, card in enumerate(hand) if card[0] != pair_rank]

        # High card - check for flush/straight draws first
        else:
            # Four to a flush - keep the four matching suits
            for suit, count in suit_counts.items():
                if count == 4:
                    discard_positions = [i for i, card in enumerate(hand) if card[1] != suit]
                    break

            # If no flush draw, check for straight draw
            if not discard_positions:
                straight_keep = self._find_straight_draw(hand)
                if straight_keep is not None:
                    discard_positions = [i for i in range(5) if i not in straight_keep]

            # No draw - keep highest cards, discard lowest 3
            if not discard_positions:
                indexed_ranks = [(i, card[0]) for i, card in enumerate(hand)]
                indexed_ranks.sort(key=lambda x: x[1])
                discard_positions = [x[0] for x in indexed_ranks[:3]]

        # Enforce max swap limit
        return discard_positions[:MAX_SWAP_PER_ROUND]

    def _find_straight_draw(self, hand: List[Card]) -> Optional[Set[int]]:
        """
        Find 4 cards that could form a straight (open-ended or gutshot draw).

        Args:
            hand: Current hand

        Returns:
            Set of position indices to keep, or None if no straight draw.
        """
        # Get ranks with positions, handling Ace as both high (14) and low (1)
        ranks_with_pos = [(card[0], i) for i, card in enumerate(hand)]

        # Add Ace as rank 1 for low straight potential
        ace_positions = [i for i, card in enumerate(hand) if card[0] == 14]
        for pos in ace_positions:
            ranks_with_pos.append((1, pos))

        # Sort by rank
        ranks_with_pos.sort(key=lambda x: x[0])

        # Look for 4 cards within a span of 5 (potential straight)
        best_keep = None

        for i in range(len(ranks_with_pos)):
            # Collect cards that could form a straight starting near this rank
            base_rank = ranks_with_pos[i][0]
            candidates = []

            for rank, pos in ranks_with_pos:
                # Card is within straight range (5 consecutive ranks)
                if base_rank <= rank <= base_rank + 4:
                    # Avoid duplicates (same position from ace dual-counting)
                    if pos not in [p for r, p in candidates]:
                        candidates.append((rank, pos))

            # Check if we have 4 unique ranks (can make a straight with 1 more card)
            unique_ranks = set(r for r, p in candidates)
            if len(unique_ranks) >= 4:
                # Take the 4 positions
                keep_positions = set(p for r, p in candidates[:4])
                if len(keep_positions) == 4:
                    best_keep = keep_positions
                    break

        return best_keep


def get_discard_positions(hand: List[Card], mode: str = 'standard') -> List[int]:
    """
    Convenience function to get discard positions.

    Args:
        hand: Current 5-card hand
        mode: Strategy mode ('conservative', 'standard', 'aggressive')

    Returns:
        List of 0-indexed positions to discard (max 3)
    """
    strategy = PokerStrategy(mode=mode)
    return strategy.get_cards_to_discard(hand)
