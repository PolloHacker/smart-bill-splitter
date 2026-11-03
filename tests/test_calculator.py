"""Unit tests for the Smart Bill Splitter calculator."""

import unittest
from bill_splitter.calculator import (
    calculate_split,
    calculate_uneven_split,
    format_currency,
)


class TestBillSplitter(unittest.TestCase):
    """Test suite for bill split and tip calculations."""

    def test_basic_equal_split(self):
        """Test a simple bill split with 10% tip among 2 people."""
        result = calculate_split(subtotal=100.0, people=2, tip_percent=10.0)

        self.assertEqual(result.subtotal, 100.0)
        self.assertEqual(result.tip_amount, 10.0)
        self.assertEqual(result.total, 110.0)
        self.assertEqual(result.people, 2)
        self.assertEqual(result.amount_per_person, 55.0)

    def test_zero_tip(self):
        """Test bill split with zero tip."""
        result = calculate_split(subtotal=60.0, people=3, tip_percent=0.0)

        self.assertEqual(result.tip_amount, 0.0)
        self.assertEqual(result.total, 60.0)
        self.assertEqual(result.amount_per_person, 20.0)

    def test_discount_application(self):
        """Test that fixed discount is deducted before calculating the tip."""
        # 100 subtotal - 20 discount = 80 discounted subtotal.
        # 10% tip on 80 = 8.00.
        # total = 88.00.
        # 2 people = 44.00 each.
        result = calculate_split(
            subtotal=100.0,
            people=2,
            tip_percent=10.0,
            discount=20.0,
        )

        self.assertEqual(result.discount, 20.0)
        self.assertEqual(result.discounted_subtotal, 80.0)
        self.assertEqual(result.tip_amount, 8.0)
        self.assertEqual(result.total, 88.0)
        self.assertEqual(result.amount_per_person, 44.0)

    def test_round_up_per_person(self):
        """Test rounding up per person to avoid centavos / pennies."""
        # subtotal 100 with 0 tip among 3 people = 33.33...
        # ceil -> 34.00 per person.
        # Adjusted total = 34 * 3 = 102. Rounding difference = 2.0.
        result = calculate_split(
            subtotal=100.0,
            people=3,
            tip_percent=0.0,
            round_up=True,
        )

        self.assertEqual(result.amount_per_person, 34.0)
        self.assertEqual(result.round_up, True)
        self.assertAlmostEqual(result.rounding_difference, 2.0, places=2)

    def test_single_person_bill(self):
        """Test bill calculation when only one person is paying."""
        result = calculate_split(subtotal=45.50, people=1, tip_percent=15.0)

        expected_tip = round(45.50 * 0.15, 2)  # 6.83
        expected_total = 45.50 + expected_tip   # 52.33

        self.assertEqual(result.tip_amount, expected_tip)
        self.assertEqual(result.total, expected_total)
        self.assertEqual(result.amount_per_person, expected_total)

    def test_invalid_people_raises_error(self):
        """Test that people <= 0 raises ValueError."""
        with self.assertRaises(ValueError) as ctx:
            calculate_split(subtotal=100.0, people=0)
        self.assertIn("Number of people must be at least 1", str(ctx.exception))

        with self.assertRaises(ValueError):
            calculate_split(subtotal=100.0, people=-2)

    def test_negative_subtotal_raises_error(self):
        """Test that negative subtotal raises ValueError."""
        with self.assertRaises(ValueError) as ctx:
            calculate_split(subtotal=-10.0, people=2)
        self.assertIn("Subtotal cannot be negative", str(ctx.exception))

    def test_discount_exceeds_subtotal_raises_error(self):
        """Test that discount greater than subtotal raises ValueError."""
        with self.assertRaises(ValueError) as ctx:
            calculate_split(subtotal=50.0, people=2, discount=60.0)
        self.assertIn("Discount cannot be greater than subtotal", str(ctx.exception))

    def test_uneven_split_with_shared_items(self):
        """Test itemized individual calculation with shared appetizer."""
        # Alice ordered 30, Bob ordered 50. Shared nachos: 20 (10 each).
        # Alice subtotal: 40. With 10% tip: 44.00.
        # Bob subtotal: 60. With 10% tip: 66.00.
        items = {"Alice": 30.0, "Bob": 50.0}
        shares = calculate_uneven_split(
            items_by_person=items,
            shared_amount=20.0,
            tip_percent=10.0,
        )

        alice = next(s for s in shares if s.name == "Alice")
        bob = next(s for s in shares if s.name == "Bob")

        self.assertEqual(alice.individual_subtotal, 30.0)
        self.assertEqual(alice.shared_subtotal, 10.0)
        self.assertEqual(alice.subtotal, 40.0)
        self.assertEqual(alice.tip_amount, 4.0)
        self.assertEqual(alice.total, 44.0)

        self.assertEqual(bob.individual_subtotal, 50.0)
        self.assertEqual(bob.shared_subtotal, 10.0)
        self.assertEqual(bob.subtotal, 60.0)
        self.assertEqual(bob.tip_amount, 6.0)
        self.assertEqual(bob.total, 66.0)

    def test_format_currency(self):
        """Test currency formatting with various symbols and numbers."""
        self.assertEqual(format_currency(1234.5, "$"), "$1,234.50")
        self.assertEqual(format_currency(99.0, "R$ "), "R$ 99.00")
        self.assertEqual(format_currency(0.0, "€"), "€0.00")


if __name__ == "__main__":
    unittest.main()
