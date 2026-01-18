"""Simple test runner that doesn't require pytest."""

import sys
import traceback


def run_tests():
    """Run all tests and report results."""
    passed = 0
    failed = 0
    errors = []

    # Import test modules
    from tests import test_deck, test_hand_evaluator, test_strategy, test_robot_actions

    # Collect all test classes
    test_modules = [
        test_deck,
        test_hand_evaluator,
        test_strategy,
        test_robot_actions,
    ]

    for module in test_modules:
        print(f"\n{'='*50}")
        print(f"Running tests from {module.__name__}")
        print('='*50)

        # Find test classes
        for name in dir(module):
            obj = getattr(module, name)
            if isinstance(obj, type) and name.startswith('Test'):
                print(f"\n{name}:")
                instance = obj()

                # Find test methods
                for method_name in dir(instance):
                    if method_name.startswith('test_'):
                        try:
                            method = getattr(instance, method_name)
                            method()
                            print(f"  [PASS] {method_name}")
                            passed += 1
                        except AssertionError as e:
                            print(f"  [FAIL] {method_name} - FAILED")
                            errors.append((f"{name}.{method_name}", str(e), traceback.format_exc()))
                            failed += 1
                        except Exception as e:
                            print(f"  [ERROR] {method_name} - ERROR: {e}")
                            errors.append((f"{name}.{method_name}", str(e), traceback.format_exc()))
                            failed += 1

    # Summary
    print(f"\n{'='*50}")
    print(f"RESULTS: {passed} passed, {failed} failed")
    print('='*50)

    if errors:
        print("\nFailed tests:")
        for test_name, error_msg, tb in errors:
            print(f"\n{test_name}:")
            print(f"  {error_msg}")

    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
