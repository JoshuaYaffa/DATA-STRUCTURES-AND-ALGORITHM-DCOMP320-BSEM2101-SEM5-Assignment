"""
Unit tests for the Math Expression Evaluator.

Run with:
    py -m unittest discover tests -v
or:
    py tests\test_stack.py
"""

import os
import sys
import unittest

# Make `src/` importable when tests run from project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
sys.path.insert(0, SRC_DIR)

from main import (  # noqa: E402
    Stack,
    tokenize,
    infix_to_postfix,
    eval_postfix,
    evaluate,
)


# ===============================================================
# Stack tests
# ===============================================================
class TestStack(unittest.TestCase):

    def test_new_stack_is_empty(self):
        s = Stack()
        self.assertTrue(s.is_empty())
        self.assertEqual(s.size(), 0)

    def test_push_and_size(self):
        s = Stack()
        s.push(1)
        s.push(2)
        s.push(3)
        self.assertFalse(s.is_empty())
        self.assertEqual(s.size(), 3)

    def test_peek_does_not_remove(self):
        s = Stack()
        s.push(10)
        s.push(20)
        self.assertEqual(s.peek(), 20)
        self.assertEqual(s.size(), 2)  # unchanged

    def test_pop_returns_last_in_first_out(self):
        s = Stack()
        s.push(1)
        s.push(2)
        s.push(3)
        self.assertEqual(s.pop(), 3)
        self.assertEqual(s.pop(), 2)
        self.assertEqual(s.pop(), 1)
        self.assertTrue(s.is_empty())

    def test_pop_empty_raises(self):
        s = Stack()
        with self.assertRaises(IndexError):
            s.pop()

    def test_peek_empty_raises(self):
        s = Stack()
        with self.assertRaises(IndexError):
            s.peek()

    def test_can_hold_mixed_types(self):
        s = Stack()
        s.push("hello")
        s.push(42)
        s.push(3.14)
        self.assertEqual(s.pop(), 3.14)
        self.assertEqual(s.pop(), 42)
        self.assertEqual(s.pop(), "hello")


# ===============================================================
# Tokenizer tests
# ===============================================================
class TestTokenizer(unittest.TestCase):

    def test_simple_expression(self):
        self.assertEqual(
            tokenize("3 + 5 * 2"),
            ["3", "+", "5", "*", "2"],
        )

    def test_multi_digit_numbers(self):
        self.assertEqual(
            tokenize("10 - 200 + 3000"),
            ["10", "-", "200", "+", "3000"],
        )

    def test_no_spaces(self):
        self.assertEqual(
            tokenize("10-(2+3)*4"),
            ["10", "-", "(", "2", "+", "3", ")", "*", "4"],
        )

    def test_extra_whitespace(self):
        self.assertEqual(
            tokenize("  42  "),
            ["42"],
        )

    def test_parentheses_are_individual_tokens(self):
        self.assertEqual(
            tokenize("((1))"),
            ["(", "(", "1", ")", ")"],
        )

    def test_bad_character_raises(self):
        with self.assertRaises(ValueError):
            tokenize("3 + $ 5")


# ===============================================================
# Infix -> Postfix tests
# ===============================================================
class TestInfixToPostfix(unittest.TestCase):

    def test_precedence(self):
        self.assertEqual(
            infix_to_postfix(tokenize("3 + 5 * 2")),
            ["3", "5", "2", "*", "+"],
        )

    def test_parentheses(self):
        self.assertEqual(
            infix_to_postfix(tokenize("(8 / 4) + 7 * 2")),
            ["8", "4", "/", "7", "2", "*", "+"],
        )

    def test_nested_parentheses(self):
        self.assertEqual(
            infix_to_postfix(tokenize("10 - (2 + 3) * 4")),
            ["10", "2", "3", "+", "4", "*", "-"],
        )

    def test_mismatched_parens_raises(self):
        with self.assertRaises(ValueError):
            infix_to_postfix(tokenize("(3 + 5"))


# ===============================================================
# Postfix evaluation tests
# ===============================================================
class TestEvalPostfix(unittest.TestCase):

    def test_single_number(self):
        self.assertEqual(eval_postfix(["42"]), 42)

    def test_simple_addition(self):
        self.assertEqual(eval_postfix(["3", "5", "+"]), 8)

    def test_precedence_via_postfix(self):
        self.assertEqual(eval_postfix(["3", "5", "2", "*", "+"]), 13)

    def test_subtraction_order(self):
        # 10 - 2 = 8  (order matters!)
        self.assertEqual(eval_postfix(["10", "2", "-"]), 8)

    def test_division(self):
        self.assertEqual(eval_postfix(["8", "4", "/"]), 2)

    def test_division_by_zero_raises(self):
        with self.assertRaises(ZeroDivisionError):
            eval_postfix(["8", "0", "/"])


# ===============================================================
# End-to-end evaluate() tests
# ===============================================================
class TestEvaluateEndToEnd(unittest.TestCase):

    def test_assignment_examples(self):
        self.assertEqual(evaluate("3 + 5 * 2"), 13)
        # NOTE: assignment brief shows 17 here, but standard precedence
        # gives 2 + 14 = 16. See report for discussion.
        self.assertEqual(evaluate("(8 / 4) + 7 * 2"), 16)
        self.assertEqual(evaluate("10 - (2 + 3) * 4"), -10)

    def test_no_spaces_variant(self):
        self.assertEqual(evaluate("3+5*2"), 13)
        self.assertEqual(evaluate("10-(2+3)*4"), -10)

    def test_nested_parentheses(self):
        self.assertEqual(evaluate("((2 + 3) * (4 + 1))"), 25)

    def test_left_to_right_same_precedence(self):
        # 10 - 3 - 2 = 5  (left associativity)
        self.assertEqual(evaluate("10 - 3 - 2"), 5)

    def test_large_numbers(self):
        self.assertEqual(evaluate("1000 + 2000 * 3"), 7000)

    def test_empty_expression_raises(self):
        with self.assertRaises(ValueError):
            evaluate("")

    def test_bad_character_raises(self):
        with self.assertRaises(ValueError):
            evaluate("3 + $")

    # -----------------------------------------------------------
    # Extended coverage — matches the 20-line extended input.txt
    # -----------------------------------------------------------
    def test_extended_input_examples(self):
        """Verify all 20 expressions from the extended input sample."""
        cases = [
            ("3 + 5 * 2", 13),
            ("(8 / 4) + 7 * 2", 16),   # assignment says 17 — see report
            ("10 - (2 + 3) * 4", -10),
            ("100 - 50 / 5", 90),
            ("((2 + 3) * (4 + 1))", 25),
            ("7 * 8 + 2 - 10", 48),
            ("20 / 4 / 5", 1),
            ("2 + 3 * 4 - 6 / 2", 11),
            ("(1 + 2) * (3 + 4) * (5 + 6)", 231),
            ("1000 + 2000 * 3", 7000),
            ("50 - (10 - 5) - 3", 42),
            ("9 * 9 + 9 - 9 / 9", 89),
            ("(100 / 10) + (200 / 20)", 20),
            ("7 + 7 * 7 - 7", 49),
            ("18 / 3 + 4 * 2 - 1", 13),
            ("((10 - 5) * (20 / 4)) + 7", 32),
            ("144 / 12 / 3 + 8 * 2", 20),
            ("500 - (100 + 200) / 5", 440),
            ("(9 + 11) * (7 - 4) - (6 / 2)", 57),
            ("10000 / 100 + 50 * 4 - 30", 270),
        ]
        for expr, expected in cases:
            with self.subTest(expr=expr):
                self.assertEqual(evaluate(expr), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)