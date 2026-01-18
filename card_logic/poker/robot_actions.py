"""
Robot action sequence generation for the card-playing robot arm.

Action format (positions are 1-indexed for robot):
- "take card N"      - Pick up card from holder position N (1-5)
- "default position" - Return arm to rest position
- "drop holding"     - Drop currently held card into trash
- "take deck"        - Pick up a card from the deck
- "place at N"       - Place held card at holder position N (1-5)
"""

from typing import List, Optional, Dict, Any, Union

from .card import Card
from .strategy import PokerStrategy, get_discard_positions

# Hand can contain None for empty positions
HandWithEmpty = List[Optional[Card]]


def generate_fill_actions(hand: HandWithEmpty) -> List[str]:
    """
    Generate actions to fill empty card holder positions from deck.

    Args:
        hand: Hand that may contain None for empty positions

    Returns:
        List of action strings to fill empty positions
    """
    actions = []

    for pos, card in enumerate(hand):
        if card is None:
            holder_pos = pos + 1  # Convert to 1-indexed

            # Pick from deck and place at empty position
            actions.append("take deck")
            actions.append("default position")
            actions.append(f"place at {holder_pos}")
            actions.append("default position")

    return actions


def generate_swap_actions(
    hand: List[Card],
    strategy: Optional[PokerStrategy] = None
) -> List[str]:
    """
    Generate action sequence for swapping cards.

    Args:
        hand: Current 5-card hand (positions 0-4 in holder) - must have no None values
        strategy: PokerStrategy instance (uses default if None)

    Returns:
        List of action strings for Arduino, empty if no swaps needed.
    """
    if strategy is None:
        strategy = PokerStrategy()

    # Get positions to discard (0-indexed internally)
    discard_positions = strategy.get_cards_to_discard(hand)

    if not discard_positions:
        return []  # Hand is good enough, no swaps

    actions = []

    # For each card to discard, generate the full action sequence
    for pos in discard_positions:
        # Convert 0-indexed to 1-indexed for robot (positions 1-5)
        holder_pos = pos + 1

        # Pick up card from holder
        actions.append(f"take card {holder_pos}")
        actions.append("default position")

        # Drop in trash
        actions.append("drop holding")
        actions.append("default position")

        # Pick from deck
        actions.append("take deck")
        actions.append("default position")

        # Place at same position
        actions.append(f"place at {holder_pos}")
        actions.append("default position")

    return actions


def parse_action(action: str) -> Dict[str, Any]:
    """
    Parse action string into components for debugging/testing.

    Args:
        action: Action string like "take card 3" or "default position"

    Returns:
        Dict with 'type' and optional 'position' keys.

    Raises:
        ValueError: If action format is unknown
    """
    action = action.strip().lower()

    if action == "default position":
        return {"type": "default"}
    elif action == "drop holding":
        return {"type": "drop"}
    elif action == "take deck":
        return {"type": "take_deck"}
    elif action.startswith("take card "):
        pos = int(action.split()[-1])
        return {"type": "take_card", "position": pos}
    elif action.startswith("place at "):
        pos = int(action.split()[-1])
        return {"type": "place", "position": pos}
    else:
        raise ValueError(f"Unknown action: {action}")


def get_poker_actions(hand: HandWithEmpty, mode: str = 'standard') -> List[str]:
    """
    Main entry point - evaluate hand and generate swap actions.

    This is the primary exportable function for Arduino integration.
    Call this function with the current hand to get robot instructions.
    Can be called multiple times for multi-round swaps (just pass updated hand).

    Handles empty positions (None) by generating fill actions first.

    Args:
        hand: List of 5 positions, each either a Card tuple or None for empty.
              Card format: (rank, suit) where rank=2-14, suit='H'/'D'/'C'/'S'
              Empty format: None
        mode: Strategy mode:
              - 'conservative': only swap if below full house
              - 'standard': only swap if below straight (default)
              - 'aggressive': only swap if below four of a kind

    Returns:
        List of action strings. First fills empty positions, then swaps bad cards.
        Returns empty list only if hand is full AND good enough.

    Example with empty positions:
        >>> hand = [(10, 'H'), None, (5, 'C'), None, (7, 'H')]
        >>> actions = get_poker_actions(hand)
        >>> # First fills positions 2 and 4, then evaluates for swaps

    Example with full hand:
        >>> hand = [(10, 'H'), (10, 'D'), (5, 'C'), (3, 'S'), (7, 'H')]
        >>> actions = get_poker_actions(hand)
        >>> # Returns swap actions for positions 3, 4, 5 (keeping the pair)
    """
    actions = []

    # Step 1: Fill any empty positions first
    empty_positions = [i for i, card in enumerate(hand) if card is None]
    if empty_positions:
        fill_actions = generate_fill_actions(hand)
        actions.extend(fill_actions)

        # Note: After filling, caller needs to update hand with actual drawn cards
        # and call again if they want swap recommendations.
        # We return just the fill actions since we don't know what cards will be drawn.
        return actions

    # Step 2: Hand is full, evaluate for swaps
    strategy = PokerStrategy(mode=mode)
    swap_actions = generate_swap_actions(hand, strategy)
    actions.extend(swap_actions)

    return actions


def count_swaps(actions: List[str]) -> int:
    """
    Count how many cards will be swapped based on action list.

    Args:
        actions: List of action strings

    Returns:
        Number of cards being swapped
    """
    return sum(1 for a in actions if a.startswith("take card "))


def get_swap_positions(actions: List[str]) -> List[int]:
    """
    Extract which positions (1-indexed) will be swapped.

    Args:
        actions: List of action strings

    Returns:
        List of 1-indexed positions being swapped
    """
    positions = []
    for action in actions:
        if action.startswith("take card "):
            pos = int(action.split()[-1])
            if pos not in positions:
                positions.append(pos)
    return positions
