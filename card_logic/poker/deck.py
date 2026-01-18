"""
Deck management with card tracking to prevent duplicates.
"""

import random
from typing import List, Optional, Set

from .card import Card, create_full_deck


class Deck:
    """Manages a deck of cards with usage tracking."""

    def __init__(self, seed: Optional[int] = None):
        """
        Initialize deck with optional random seed for reproducibility.

        Args:
            seed: Random seed for reproducible draws (None for true random)
        """
        self._all_cards: List[Card] = create_full_deck()
        self._used_cards: Set[Card] = set()
        self._rng = random.Random(seed)

    def reset(self) -> None:
        """Reset deck to full 52 cards (clear all used cards)."""
        self._used_cards.clear()

    def draw_card(self) -> Optional[Card]:
        """
        Draw a single random card from remaining deck.

        Returns:
            A random card, or None if deck is empty.
        """
        available = [c for c in self._all_cards if c not in self._used_cards]
        if not available:
            return None
        card = self._rng.choice(available)
        self._used_cards.add(card)
        return card

    def draw_cards(self, count: int) -> List[Card]:
        """
        Draw multiple random cards.

        Args:
            count: Number of cards to draw

        Returns:
            List of drawn cards (may be fewer if deck runs out)
        """
        cards = []
        for _ in range(count):
            card = self.draw_card()
            if card is None:
                break
            cards.append(card)
        return cards

    def mark_used(self, card: Card) -> None:
        """
        Mark a card as used (e.g., when it goes to trash).

        Args:
            card: Card to mark as used
        """
        self._used_cards.add(card)

    def mark_cards_used(self, cards: List[Card]) -> None:
        """
        Mark multiple cards as used.

        Args:
            cards: List of cards to mark as used
        """
        for card in cards:
            self._used_cards.add(card)

    def remaining_count(self) -> int:
        """Return number of cards remaining in deck."""
        return 52 - len(self._used_cards)

    def is_available(self, card: Card) -> bool:
        """Check if a specific card is still available."""
        return card not in self._used_cards

    def generate_initial_hand(self) -> List[Card]:
        """
        Generate initial 5-card hand.

        Returns:
            List of 5 random cards
        """
        return self.draw_cards(5)

    def get_used_cards(self) -> Set[Card]:
        """Return copy of the set of used cards."""
        return self._used_cards.copy()
