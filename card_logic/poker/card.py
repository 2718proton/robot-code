"""
Card representation and constants for poker.

Card format: tuple (rank, suit)
- rank: 2-14 where 14=Ace, 13=King, 12=Queen, 11=Jack
- suit: 'H' (Hearts), 'D' (Diamonds), 'C' (Clubs), 'S' (Spades)
"""

from typing import Tuple, List

# Type alias for a card
Card = Tuple[int, str]

# Valid ranks (2-14, where 14 is Ace)
RANKS = list(range(2, 15))

# Valid suits
SUITS = ['H', 'D', 'C', 'S']

# Human-readable rank names
RANK_NAMES = {
    2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8',
    9: '9', 10: '10', 11: 'J', 12: 'Q', 13: 'K', 14: 'A'
}

# Human-readable suit names
SUIT_NAMES = {
    'H': 'Hearts',
    'D': 'Diamonds',
    'C': 'Clubs',
    'S': 'Spades'
}


def card_to_string(card: Card) -> str:
    """Convert card tuple to readable string like 'AH' or '10D'."""
    return f"{RANK_NAMES[card[0]]}{card[1]}"


def card_to_full_string(card: Card) -> str:
    """Convert card tuple to full readable string like 'Ace of Hearts'."""
    return f"{RANK_NAMES[card[0]]} of {SUIT_NAMES[card[1]]}"


def create_full_deck() -> List[Card]:
    """Generate a complete 52-card deck."""
    return [(rank, suit) for suit in SUITS for rank in RANKS]


def is_valid_card(card: Card) -> bool:
    """Check if a card tuple is valid."""
    if not isinstance(card, tuple) or len(card) != 2:
        return False
    rank, suit = card
    return rank in RANKS and suit in SUITS
