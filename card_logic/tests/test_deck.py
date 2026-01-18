"""Tests for deck management."""

from poker import Deck


class TestDeck:
    """Test deck management and card tracking."""

    def test_initial_hand_size(self):
        """Initial hand should have 5 cards."""
        deck = Deck(seed=42)
        hand = deck.generate_initial_hand()
        assert len(hand) == 5

    def test_no_duplicates_in_hand(self):
        """Initial hand should have no duplicate cards."""
        deck = Deck(seed=42)
        hand = deck.generate_initial_hand()
        assert len(hand) == len(set(hand))

    def test_no_duplicates_in_full_draw(self):
        """Drawing all 52 cards should give unique cards."""
        deck = Deck(seed=42)
        drawn = deck.draw_cards(52)
        assert len(drawn) == 52
        assert len(set(drawn)) == 52

    def test_empty_deck_returns_none(self):
        """Drawing from empty deck should return None."""
        deck = Deck(seed=42)
        deck.draw_cards(52)
        assert deck.draw_card() is None
        assert deck.remaining_count() == 0

    def test_reset(self):
        """Reset should restore full deck."""
        deck = Deck(seed=42)
        deck.draw_cards(10)
        assert deck.remaining_count() == 42
        deck.reset()
        assert deck.remaining_count() == 52

    def test_reproducibility_with_seed(self):
        """Same seed should give same cards."""
        deck1 = Deck(seed=42)
        deck2 = Deck(seed=42)
        hand1 = deck1.draw_cards(5)
        hand2 = deck2.draw_cards(5)
        assert hand1 == hand2

    def test_different_seeds_give_different_cards(self):
        """Different seeds should give different cards."""
        deck1 = Deck(seed=42)
        deck2 = Deck(seed=123)
        hand1 = deck1.draw_cards(5)
        hand2 = deck2.draw_cards(5)
        assert hand1 != hand2

    def test_mark_used(self):
        """Marking a card as used should remove it from available pool."""
        deck = Deck(seed=42)
        card = (14, 'H')  # Ace of Hearts
        assert deck.is_available(card)
        deck.mark_used(card)
        assert not deck.is_available(card)
        assert deck.remaining_count() == 51

    def test_mark_cards_used(self):
        """Marking multiple cards as used."""
        deck = Deck(seed=42)
        cards = [(14, 'H'), (13, 'H'), (12, 'H')]
        deck.mark_cards_used(cards)
        assert deck.remaining_count() == 49
        for card in cards:
            assert not deck.is_available(card)

    def test_get_used_cards(self):
        """Should return copy of used cards set."""
        deck = Deck(seed=42)
        hand = deck.generate_initial_hand()
        used = deck.get_used_cards()
        assert len(used) == 5
        for card in hand:
            assert card in used
