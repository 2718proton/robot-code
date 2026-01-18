"""Tests for poker hand evaluation."""

from poker import (
    HandEvaluator,
    ROYAL_FLUSH, STRAIGHT_FLUSH, FOUR_OF_A_KIND, FULL_HOUSE,
    FLUSH, STRAIGHT, THREE_OF_A_KIND, TWO_PAIR, ONE_PAIR, HIGH_CARD
)


class TestHandEvaluator:
    """Test poker hand evaluation."""

    def test_royal_flush(self):
        """Royal flush should be rank 9."""
        hand = [(14, 'H'), (13, 'H'), (12, 'H'), (11, 'H'), (10, 'H')]
        rank, _, name = HandEvaluator.evaluate(hand)
        assert rank == ROYAL_FLUSH
        assert name == "Royal Flush"

    def test_straight_flush(self):
        """Straight flush should be rank 8."""
        hand = [(9, 'S'), (8, 'S'), (7, 'S'), (6, 'S'), (5, 'S')]
        rank, _, name = HandEvaluator.evaluate(hand)
        assert rank == STRAIGHT_FLUSH
        assert name == "Straight Flush"

    def test_four_of_a_kind(self):
        """Four of a kind should be rank 7."""
        hand = [(7, 'H'), (7, 'D'), (7, 'C'), (7, 'S'), (2, 'H')]
        rank, _, name = HandEvaluator.evaluate(hand)
        assert rank == FOUR_OF_A_KIND
        assert name == "Four of a Kind"

    def test_full_house(self):
        """Full house should be rank 6."""
        hand = [(10, 'H'), (10, 'D'), (10, 'C'), (5, 'S'), (5, 'H')]
        rank, _, name = HandEvaluator.evaluate(hand)
        assert rank == FULL_HOUSE
        assert name == "Full House"

    def test_flush(self):
        """Flush should be rank 5."""
        hand = [(14, 'H'), (10, 'H'), (8, 'H'), (5, 'H'), (2, 'H')]
        rank, _, name = HandEvaluator.evaluate(hand)
        assert rank == FLUSH
        assert name == "Flush"

    def test_straight(self):
        """Straight should be rank 4."""
        hand = [(9, 'H'), (8, 'D'), (7, 'C'), (6, 'S'), (5, 'H')]
        rank, _, name = HandEvaluator.evaluate(hand)
        assert rank == STRAIGHT
        assert name == "Straight"

    def test_wheel_straight(self):
        """A-2-3-4-5 (wheel) should be recognized as straight."""
        hand = [(14, 'H'), (2, 'D'), (3, 'C'), (4, 'S'), (5, 'H')]
        rank, tiebreakers, name = HandEvaluator.evaluate(hand)
        assert rank == STRAIGHT
        assert name == "Straight"
        # Wheel straight is 5-high
        assert tiebreakers == [5]

    def test_three_of_a_kind(self):
        """Three of a kind should be rank 3."""
        hand = [(7, 'H'), (7, 'D'), (7, 'C'), (2, 'S'), (9, 'H')]
        rank, _, name = HandEvaluator.evaluate(hand)
        assert rank == THREE_OF_A_KIND
        assert name == "Three of a Kind"

    def test_two_pair(self):
        """Two pair should be rank 2."""
        hand = [(10, 'H'), (10, 'D'), (5, 'C'), (5, 'S'), (7, 'H')]
        rank, _, name = HandEvaluator.evaluate(hand)
        assert rank == TWO_PAIR
        assert name == "Two Pair"

    def test_one_pair(self):
        """One pair should be rank 1."""
        hand = [(10, 'H'), (10, 'D'), (5, 'C'), (3, 'S'), (7, 'H')]
        rank, _, name = HandEvaluator.evaluate(hand)
        assert rank == ONE_PAIR
        assert name == "One Pair"

    def test_high_card(self):
        """High card should be rank 0."""
        hand = [(14, 'H'), (10, 'D'), (8, 'C'), (5, 'S'), (2, 'H')]
        rank, _, name = HandEvaluator.evaluate(hand)
        assert rank == HIGH_CARD
        assert name == "High Card"

    def test_compare_hands_different_ranks(self):
        """Higher rank hand should win."""
        pair = [(10, 'H'), (10, 'D'), (5, 'C'), (3, 'S'), (7, 'H')]
        two_pair = [(10, 'H'), (10, 'D'), (5, 'C'), (5, 'S'), (7, 'H')]
        assert HandEvaluator.compare_hands(two_pair, pair) == 1
        assert HandEvaluator.compare_hands(pair, two_pair) == -1

    def test_compare_hands_same_rank_different_tiebreaker(self):
        """Same rank but higher tiebreaker should win."""
        pair_tens = [(10, 'H'), (10, 'D'), (5, 'C'), (3, 'S'), (7, 'H')]
        pair_jacks = [(11, 'H'), (11, 'D'), (5, 'C'), (3, 'S'), (7, 'H')]
        assert HandEvaluator.compare_hands(pair_jacks, pair_tens) == 1
        assert HandEvaluator.compare_hands(pair_tens, pair_jacks) == -1

    def test_compare_hands_tie(self):
        """Identical hands should tie."""
        hand1 = [(10, 'H'), (10, 'D'), (5, 'C'), (3, 'S'), (7, 'H')]
        hand2 = [(10, 'S'), (10, 'C'), (5, 'D'), (3, 'H'), (7, 'S')]
        assert HandEvaluator.compare_hands(hand1, hand2) == 0

    def test_invalid_hand_size(self):
        """Hand with wrong number of cards should raise error."""
        try:
            HandEvaluator.evaluate([(10, 'H'), (10, 'D')])
            assert False, "Should have raised ValueError"
        except ValueError:
            pass  # Expected
