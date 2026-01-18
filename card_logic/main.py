"""
Poker Robot Control System - Demo and Test Runner

Run this file to see the system in action with random hands.
"""

from poker import (
    Deck,
    HandEvaluator,
    get_poker_actions,
    card_to_string,
    count_swaps,
    get_swap_positions,
)


def demo_single_round(seed=None):
    """Demonstrate a single round of poker with the robot."""
    print("=" * 50)
    print("POKER ROBOT - SINGLE ROUND DEMO")
    print("=" * 50)

    # Initialize deck
    deck = Deck(seed=seed)

    # Generate initial hand
    hand = deck.generate_initial_hand()

    print("\nInitial Hand:")
    for i, card in enumerate(hand, 1):
        print(f"  Position {i}: {card_to_string(card)}")

    # Evaluate hand
    rank, _, hand_name = HandEvaluator.evaluate(hand)
    print(f"\nHand Evaluation: {hand_name} (rank {rank})")

    # Get robot actions
    actions = get_poker_actions(hand)

    if not actions:
        print("\nDecision: Hand is good enough - NO SWAPS NEEDED")
        return hand, deck

    swap_count = count_swaps(actions)
    swap_positions = get_swap_positions(actions)
    print(f"\nDecision: Swap {swap_count} card(s) at positions {swap_positions}")

    print("\nRobot Action Sequence:")
    for i, action in enumerate(actions, 1):
        print(f"  {i:2}. {action}")

    # Simulate the swaps
    print("\n" + "-" * 30)
    print("Simulating swaps...")

    new_hand = list(hand)
    for pos in swap_positions:
        idx = pos - 1  # Convert to 0-indexed
        new_card = deck.draw_card()
        old_card = new_hand[idx]
        new_hand[idx] = new_card
        print(f"  Position {pos}: {card_to_string(old_card)} -> {card_to_string(new_card)}")

    # Evaluate new hand
    new_rank, _, new_hand_name = HandEvaluator.evaluate(new_hand)
    print(f"\nNew Hand: {new_hand_name} (rank {new_rank})")

    if new_rank > rank:
        print("Result: IMPROVED!")
    elif new_rank < rank:
        print("Result: Got worse...")
    else:
        print("Result: Same hand type")

    return new_hand, deck


def demo_multi_round(rounds=2, seed=None):
    """Demonstrate multiple swap rounds (for games that allow it)."""
    print("\n" + "=" * 50)
    print(f"POKER ROBOT - {rounds} ROUND DEMO")
    print("=" * 50)

    deck = Deck(seed=seed)
    hand = deck.generate_initial_hand()

    print("\nInitial Hand:")
    for i, card in enumerate(hand, 1):
        print(f"  Position {i}: {card_to_string(card)}")

    rank, _, hand_name = HandEvaluator.evaluate(hand)
    print(f"Evaluation: {hand_name}")

    for round_num in range(1, rounds + 1):
        print(f"\n--- Round {round_num} ---")

        actions = get_poker_actions(hand)

        if not actions:
            print("No swaps needed - hand is good enough!")
            break

        swap_positions = get_swap_positions(actions)
        print(f"Swapping positions: {swap_positions}")

        # Execute swaps
        for pos in swap_positions:
            idx = pos - 1
            new_card = deck.draw_card()
            if new_card is None:
                print("Deck is empty!")
                break
            old_card = hand[idx]
            hand[idx] = new_card
            print(f"  {card_to_string(old_card)} -> {card_to_string(new_card)}")

        rank, _, hand_name = HandEvaluator.evaluate(hand)
        print(f"New hand: {hand_name}")

    print("\nFinal Hand:")
    for i, card in enumerate(hand, 1):
        print(f"  Position {i}: {card_to_string(card)}")


def run_test_scenarios():
    """Run specific test scenarios to verify logic."""
    print("\n" + "=" * 50)
    print("TEST SCENARIOS")
    print("=" * 50)

    # Test case 1: Royal Flush - should not swap
    print("\n[Test 1] Royal Flush:")
    hand = [(14, 'H'), (13, 'H'), (12, 'H'), (11, 'H'), (10, 'H')]
    for i, card in enumerate(hand, 1):
        print(f"  Position {i}: {card_to_string(card)}")
    actions = get_poker_actions(hand)
    print(f"  Hand: {HandEvaluator.get_hand_name(hand)}")
    print(f"  Actions: {actions if actions else 'None (keep hand)'}")
    assert len(actions) == 0, "Royal flush should not swap!"

    # Test case 2: One Pair - should swap 3
    print("\n[Test 2] One Pair (10s):")
    hand = [(10, 'H'), (10, 'D'), (5, 'C'), (3, 'S'), (7, 'H')]
    for i, card in enumerate(hand, 1):
        print(f"  Position {i}: {card_to_string(card)}")
    actions = get_poker_actions(hand)
    print(f"  Hand: {HandEvaluator.get_hand_name(hand)}")
    print(f"  Swap positions: {get_swap_positions(actions)}")
    assert count_swaps(actions) == 3, "One pair should swap 3 cards!"

    # Test case 3: Three of a Kind - should swap 2
    print("\n[Test 3] Three of a Kind (7s):")
    hand = [(7, 'H'), (7, 'D'), (7, 'C'), (2, 'S'), (9, 'H')]
    for i, card in enumerate(hand, 1):
        print(f"  Position {i}: {card_to_string(card)}")
    actions = get_poker_actions(hand)
    print(f"  Hand: {HandEvaluator.get_hand_name(hand)}")
    print(f"  Swap positions: {get_swap_positions(actions)}")
    assert count_swaps(actions) == 2, "Three of a kind should swap 2 cards!"

    # Test case 4: Flush - should not swap
    print("\n[Test 4] Flush (Hearts):")
    hand = [(14, 'H'), (10, 'H'), (8, 'H'), (5, 'H'), (2, 'H')]
    for i, card in enumerate(hand, 1):
        print(f"  Position {i}: {card_to_string(card)}")
    actions = get_poker_actions(hand)
    print(f"  Hand: {HandEvaluator.get_hand_name(hand)}")
    print(f"  Actions: {actions if actions else 'None (keep hand)'}")
    assert len(actions) == 0, "Flush should not swap!"

    # Test case 5: Straight - should not swap
    print("\n[Test 5] Straight (5-9):")
    hand = [(9, 'H'), (8, 'D'), (7, 'C'), (6, 'S'), (5, 'H')]
    for i, card in enumerate(hand, 1):
        print(f"  Position {i}: {card_to_string(card)}")
    actions = get_poker_actions(hand)
    print(f"  Hand: {HandEvaluator.get_hand_name(hand)}")
    print(f"  Actions: {actions if actions else 'None (keep hand)'}")
    assert len(actions) == 0, "Straight should not swap!"

    # Test case 6: Wheel Straight (A-5)
    print("\n[Test 6] Wheel Straight (A-2-3-4-5):")
    hand = [(14, 'H'), (2, 'D'), (3, 'C'), (4, 'S'), (5, 'H')]
    for i, card in enumerate(hand, 1):
        print(f"  Position {i}: {card_to_string(card)}")
    actions = get_poker_actions(hand)
    print(f"  Hand: {HandEvaluator.get_hand_name(hand)}")
    print(f"  Actions: {actions if actions else 'None (keep hand)'}")
    assert len(actions) == 0, "Wheel straight should not swap!"

    # Test case 7: Two Pair - should swap 1
    print("\n[Test 7] Two Pair (10s and 5s):")
    hand = [(10, 'H'), (10, 'D'), (5, 'C'), (5, 'S'), (7, 'H')]
    for i, card in enumerate(hand, 1):
        print(f"  Position {i}: {card_to_string(card)}")
    actions = get_poker_actions(hand)
    print(f"  Hand: {HandEvaluator.get_hand_name(hand)}")
    print(f"  Swap positions: {get_swap_positions(actions)}")
    assert count_swaps(actions) == 1, "Two pair should swap 1 card!"

    print("\n" + "=" * 50)
    print("ALL TESTS PASSED!")
    print("=" * 50)


if __name__ == "__main__":
    # Run test scenarios first
    run_test_scenarios()

    # Demo with random hand
    print("\n")
    demo_single_round()

    # Demo multi-round
    demo_multi_round(rounds=2)
