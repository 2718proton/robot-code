"""Tests for robot action generation."""

from poker import (
    get_poker_actions,
    generate_fill_actions,
    parse_action,
    count_swaps,
    get_swap_positions,
)


class TestRobotActions:
    """Test robot action sequence generation."""

    def test_good_hand_returns_empty(self):
        """A flush should return no actions."""
        hand = [(14, 'H'), (10, 'H'), (8, 'H'), (5, 'H'), (2, 'H')]
        actions = get_poker_actions(hand)
        assert actions == []

    def test_pair_generates_actions(self):
        """One pair should generate swap sequences for 3 cards."""
        hand = [(10, 'H'), (10, 'D'), (5, 'C'), (3, 'S'), (7, 'H')]
        actions = get_poker_actions(hand)

        # 3 cards to swap, 8 actions each = 24 actions
        assert len(actions) == 24

        # Verify each swap has the right pattern
        swaps = count_swaps(actions)
        assert swaps == 3

    def test_action_sequence_pattern(self):
        """Each swap should follow the correct action pattern."""
        hand = [(10, 'H'), (10, 'D'), (5, 'C'), (5, 'S'), (7, 'H')]  # Two pair
        actions = get_poker_actions(hand)

        # Should have 1 swap (8 actions)
        assert len(actions) == 8

        # Check pattern: take card, default, drop, default, take deck, default, place, default
        assert actions[0].startswith("take card")
        assert actions[1] == "default position"
        assert actions[2] == "drop holding"
        assert actions[3] == "default position"
        assert actions[4] == "take deck"
        assert actions[5] == "default position"
        assert actions[6].startswith("place at")
        assert actions[7] == "default position"

    def test_positions_are_1_indexed(self):
        """Robot positions should be 1-indexed (1-5)."""
        hand = [(10, 'H'), (10, 'D'), (5, 'C'), (5, 'S'), (7, 'H')]  # Two pair
        actions = get_poker_actions(hand)

        # The kicker is at position 4 (0-indexed), should be position 5 (1-indexed)
        positions = get_swap_positions(actions)
        assert all(1 <= p <= 5 for p in positions)
        assert 5 in positions  # The 7 kicker

    def test_take_and_place_same_position(self):
        """Card should be placed back at the same position it was taken from."""
        hand = [(10, 'H'), (10, 'D'), (5, 'C'), (5, 'S'), (7, 'H')]
        actions = get_poker_actions(hand)

        # Find take and place positions
        take_pos = None
        place_pos = None
        for action in actions:
            if action.startswith("take card"):
                take_pos = int(action.split()[-1])
            elif action.startswith("place at"):
                place_pos = int(action.split()[-1])

        assert take_pos == place_pos


class TestParseAction:
    """Test action string parsing."""

    def test_parse_take_card(self):
        """Parse take card action."""
        result = parse_action("take card 3")
        assert result == {"type": "take_card", "position": 3}

    def test_parse_default_position(self):
        """Parse default position action."""
        result = parse_action("default position")
        assert result == {"type": "default"}

    def test_parse_drop_holding(self):
        """Parse drop holding action."""
        result = parse_action("drop holding")
        assert result == {"type": "drop"}

    def test_parse_take_deck(self):
        """Parse take deck action."""
        result = parse_action("take deck")
        assert result == {"type": "take_deck"}

    def test_parse_place_at(self):
        """Parse place at action."""
        result = parse_action("place at 2")
        assert result == {"type": "place", "position": 2}

    def test_parse_unknown_action(self):
        """Unknown action should raise ValueError."""
        try:
            parse_action("unknown action")
            assert False, "Should have raised ValueError"
        except ValueError:
            pass  # Expected

    def test_parse_case_insensitive(self):
        """Parsing should be case insensitive."""
        result = parse_action("TAKE CARD 3")
        assert result == {"type": "take_card", "position": 3}


class TestHelperFunctions:
    """Test helper functions."""

    def test_count_swaps(self):
        """Count swaps should return correct count."""
        actions = [
            "take card 1", "default position", "drop holding", "default position",
            "take deck", "default position", "place at 1", "default position",
            "take card 2", "default position", "drop holding", "default position",
            "take deck", "default position", "place at 2", "default position",
        ]
        assert count_swaps(actions) == 2

    def test_get_swap_positions(self):
        """Get swap positions should return correct positions."""
        actions = [
            "take card 3", "default position", "drop holding", "default position",
            "take deck", "default position", "place at 3", "default position",
            "take card 5", "default position", "drop holding", "default position",
            "take deck", "default position", "place at 5", "default position",
        ]
        positions = get_swap_positions(actions)
        assert positions == [3, 5]

    def test_get_swap_positions_no_duplicates(self):
        """Get swap positions should not have duplicates."""
        # Even if actions repeated (shouldn't happen), no duplicates
        actions = [
            "take card 3", "default position",
            "take card 3", "default position",  # Duplicate (shouldn't happen)
        ]
        positions = get_swap_positions(actions)
        assert positions == [3]


class TestEmptyPositions:
    """Test handling of empty card holder positions (None)."""

    def test_all_empty_fills_all_positions(self):
        """All empty positions should generate fill actions for all 5."""
        hand = [None, None, None, None, None]
        actions = get_poker_actions(hand)

        # 5 empty positions, 4 actions each (take deck, default, place, default)
        assert len(actions) == 20

        # Check pattern for first fill
        assert actions[0] == "take deck"
        assert actions[1] == "default position"
        assert actions[2] == "place at 1"
        assert actions[3] == "default position"

    def test_some_empty_fills_only_empty(self):
        """Only empty positions should be filled."""
        hand = [(10, 'H'), None, (5, 'C'), None, (7, 'H')]
        actions = get_poker_actions(hand)

        # 2 empty positions (indices 1 and 3), 4 actions each
        assert len(actions) == 8

        # Should fill positions 2 and 4 (1-indexed)
        assert "place at 2" in actions
        assert "place at 4" in actions
        assert "place at 1" not in actions
        assert "place at 3" not in actions
        assert "place at 5" not in actions

    def test_empty_at_end(self):
        """Empty position at end should be filled."""
        hand = [(10, 'H'), (10, 'D'), (5, 'C'), (3, 'S'), None]
        actions = get_poker_actions(hand)

        # 1 empty position, 4 actions
        assert len(actions) == 4
        assert "place at 5" in actions

    def test_empty_at_start(self):
        """Empty position at start should be filled."""
        hand = [None, (10, 'D'), (5, 'C'), (3, 'S'), (7, 'H')]
        actions = get_poker_actions(hand)

        # 1 empty position, 4 actions
        assert len(actions) == 4
        assert "place at 1" in actions

    def test_full_hand_no_fill_actions(self):
        """Full hand should not have fill actions, only swap actions."""
        hand = [(10, 'H'), (10, 'D'), (5, 'C'), (3, 'S'), (7, 'H')]
        actions = get_poker_actions(hand)

        # Should be swap actions, not fill actions
        # Fill actions don't have "take card", swaps do
        assert any(a.startswith("take card") for a in actions)

    def test_generate_fill_actions_directly(self):
        """Test generate_fill_actions function directly."""
        hand = [None, (10, 'D'), None, (3, 'S'), None]
        actions = generate_fill_actions(hand)

        # 3 empty positions
        assert len(actions) == 12

        # Check correct positions filled
        assert "place at 1" in actions
        assert "place at 3" in actions
        assert "place at 5" in actions

    def test_fill_action_pattern(self):
        """Fill action should be: take deck, default, place, default."""
        hand = [None, (10, 'D'), (5, 'C'), (3, 'S'), (7, 'H')]
        actions = generate_fill_actions(hand)

        assert actions[0] == "take deck"
        assert actions[1] == "default position"
        assert actions[2] == "place at 1"
        assert actions[3] == "default position"
