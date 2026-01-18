"""Tests for poker strategy (discard decisions)."""

from poker import PokerStrategy, get_discard_positions, MAX_SWAP_PER_ROUND


class TestStrategy:
    """Test card swap decision logic."""

    def test_keep_royal_flush(self):
        """Royal flush should not trigger any discards."""
        hand = [(14, 'H'), (13, 'H'), (12, 'H'), (11, 'H'), (10, 'H')]
        discards = get_discard_positions(hand)
        assert discards == []

    def test_keep_straight_flush(self):
        """Straight flush should not trigger any discards."""
        hand = [(9, 'S'), (8, 'S'), (7, 'S'), (6, 'S'), (5, 'S')]
        discards = get_discard_positions(hand)
        assert discards == []

    def test_keep_straight(self):
        """Straight should not trigger any discards."""
        hand = [(9, 'H'), (8, 'D'), (7, 'C'), (6, 'S'), (5, 'H')]
        discards = get_discard_positions(hand)
        assert discards == []

    def test_keep_flush(self):
        """Flush should not trigger any discards."""
        hand = [(14, 'H'), (10, 'H'), (8, 'H'), (5, 'H'), (2, 'H')]
        discards = get_discard_positions(hand)
        assert discards == []

    def test_one_pair_discards_three(self):
        """One pair should discard the 3 non-pair cards."""
        # Pair of 10s at positions 0 and 1
        hand = [(10, 'H'), (10, 'D'), (5, 'C'), (3, 'S'), (7, 'H')]
        discards = get_discard_positions(hand)
        assert len(discards) == 3
        # Should keep positions 0 and 1 (the pair)
        assert 0 not in discards
        assert 1 not in discards
        # Should discard positions 2, 3, 4
        assert 2 in discards
        assert 3 in discards
        assert 4 in discards

    def test_two_pair_discards_one(self):
        """Two pair should discard the 1 kicker card."""
        # Pairs of 10s and 5s, kicker 7 at position 4
        hand = [(10, 'H'), (10, 'D'), (5, 'C'), (5, 'S'), (7, 'H')]
        discards = get_discard_positions(hand)
        assert len(discards) == 1
        assert 4 in discards  # The 7 is the kicker

    def test_three_of_a_kind_discards_two(self):
        """Three of a kind should discard 2 kickers."""
        # Three 7s at positions 0, 1, 2
        hand = [(7, 'H'), (7, 'D'), (7, 'C'), (2, 'S'), (9, 'H')]
        discards = get_discard_positions(hand)
        assert len(discards) == 2
        # Should keep positions 0, 1, 2 (the trips)
        assert 0 not in discards
        assert 1 not in discards
        assert 2 not in discards
        # Should discard positions 3 and 4
        assert 3 in discards
        assert 4 in discards

    def test_max_swap_limit(self):
        """Should never swap more than MAX_SWAP_PER_ROUND cards."""
        # High card hand - would want to swap 3+ cards
        hand = [(14, 'H'), (10, 'D'), (8, 'C'), (5, 'S'), (2, 'H')]
        discards = get_discard_positions(hand)
        assert len(discards) <= MAX_SWAP_PER_ROUND

    def test_aggressive_mode(self):
        """Aggressive mode affects threshold for keeping hands."""
        # Three of a kind - standard keeps it (rank 3 < threshold 4)
        # but aggressive still swaps the kickers trying for four of a kind
        hand = [(7, 'H'), (7, 'D'), (7, 'C'), (2, 'S'), (9, 'H')]

        standard_discards = get_discard_positions(hand, mode='standard')
        aggressive_discards = get_discard_positions(hand, mode='aggressive')

        # Standard swaps kickers (three of a kind < straight threshold)
        assert len(standard_discards) == 2
        # Aggressive also swaps (three of a kind < four of a kind threshold)
        assert len(aggressive_discards) == 2

    def test_conservative_mode(self):
        """Conservative mode keeps more hands."""
        # Two pair - normally we swap the kicker
        hand = [(10, 'H'), (10, 'D'), (5, 'C'), (5, 'S'), (7, 'H')]

        standard_discards = get_discard_positions(hand, mode='standard')
        conservative_discards = get_discard_positions(hand, mode='conservative')

        # Standard swaps the kicker (two pair rank 2 < straight threshold 4)
        assert len(standard_discards) == 1
        # Conservative also swaps (two pair rank 2 < full house threshold 6)
        assert len(conservative_discards) == 1

    def test_made_hands_never_broken(self):
        """Made hands (straight+) should never be broken regardless of mode."""
        # Flush should never be broken
        flush = [(14, 'H'), (10, 'H'), (8, 'H'), (5, 'H'), (2, 'H')]
        assert get_discard_positions(flush, mode='standard') == []
        assert get_discard_positions(flush, mode='aggressive') == []
        assert get_discard_positions(flush, mode='conservative') == []

        # Straight should never be broken
        straight = [(9, 'H'), (8, 'D'), (7, 'C'), (6, 'S'), (5, 'H')]
        assert get_discard_positions(straight, mode='standard') == []
        assert get_discard_positions(straight, mode='aggressive') == []
        assert get_discard_positions(straight, mode='conservative') == []


class TestStrategyEdgeCases:
    """Test edge cases in strategy."""

    def test_wheel_straight_kept(self):
        """Wheel straight (A-2-3-4-5) should be kept."""
        hand = [(14, 'H'), (2, 'D'), (3, 'C'), (4, 'S'), (5, 'H')]
        discards = get_discard_positions(hand)
        assert discards == []

    def test_four_to_flush_keeps_flush_draw(self):
        """Four cards of same suit should keep those four."""
        # 4 hearts, 1 spade
        hand = [(14, 'H'), (10, 'H'), (8, 'H'), (5, 'H'), (2, 'S')]
        discards = get_discard_positions(hand)
        assert len(discards) == 1
        assert 4 in discards  # The spade should be discarded
