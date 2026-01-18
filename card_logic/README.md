# Poker Robot Logic

Decision system for a poker-playing robot arm.

## Quick Start

```python
from poker import get_poker_actions, Deck

# Get actions for a hand
hand = [(10, 'H'), (10, 'D'), (5, 'C'), (3, 'S'), (7, 'H')]
actions = get_poker_actions(hand)
# Returns list of robot commands, or [] if hand is good
```

## Card Format

```python
# Card = (rank, suit)
# rank: 2-14 (11=J, 12=Q, 13=K, 14=A)
# suit: 'H', 'D', 'C', 'S'

(14, 'H')  # Ace of Hearts
(10, 'D')  # 10 of Diamonds
```

## Empty Positions

Use `None` for empty card holders:

```python
hand = [None, None, None, None, None]  # All empty
actions = get_poker_actions(hand)
# Returns fill actions: ['take deck', 'default position', 'place at 1', ...]

# After filling, update hand with actual cards and call again for swaps
```

## Action Commands

| Command | Meaning |
|---------|---------|
| `take card N` | Pick up card from holder N (1-5) |
| `default position` | Return arm to rest |
| `drop holding` | Drop card to trash |
| `take deck` | Pick card from deck |
| `place at N` | Place card at holder N (1-5) |

## Using the Deck (Optional)

```python
from poker import Deck

deck = Deck()
hand = deck.generate_initial_hand()  # 5 random cards
new_card = deck.draw_card()          # 1 random card (no duplicates)
deck.reset()                         # Reset for new game
```

## Multiple Swap Rounds

```python
# Round 1
actions1 = get_poker_actions(hand)
# ... robot executes, update hand with new cards ...

# Round 2
actions2 = get_poker_actions(updated_hand)
```

## Typical Game Flow

```python
from poker import get_poker_actions

hand = [None, None, None, None, None]  # Start empty
swap_rounds = 2  # Game rules allow 2 swap rounds

# Step 1: Fill empty slots
while None in hand:
    actions = get_poker_actions(hand)
    # Execute actions on robot...
    # Update hand with actual cards placed
    hand = [(10, 'H'), (10, 'D'), (5, 'C'), (3, 'S'), (7, 'H')]  # Example

# Step 2: Swap rounds (based on game rules)
for round in range(swap_rounds):
    actions = get_poker_actions(hand)
    if not actions:
        break  # Hand is good, no swaps needed
    # Execute actions on robot...
    # Update hand with new cards at swapped positions
```

## Run Tests

```
python run_tests.py
```
