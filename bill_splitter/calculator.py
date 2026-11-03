"""Core calculation logic for splitting bills, tips, and discounts."""

from dataclasses import dataclass
import math
from typing import Dict, List, Optional


@dataclass(frozen=True)
class BillSummary:
    """Summary of a calculated bill split."""
    subtotal: float
    discount: float
    discounted_subtotal: float
    tip_percent: float
    tip_amount: float
    total: float
    people: int
    amount_per_person: float
    round_up: bool
    rounding_difference: float


@dataclass(frozen=True)
class PersonShare:
    """Share breakdown for an individual in an uneven bill split."""
    name: str
    individual_subtotal: float
    shared_subtotal: float
    subtotal: float
    tip_amount: float
    total: float


def validate_split_inputs(
    subtotal: float,
    people: int,
    tip_percent: float,
    discount: float,
) -> None:
    """Validate input parameters for splitting a bill.

    Raises:
        ValueError: If any input fails validation constraints.
    """
    if subtotal < 0:
        raise ValueError("Subtotal cannot be negative.")
    if people <= 0:
        raise ValueError("Number of people must be at least 1.")
    if tip_percent < 0:
        raise ValueError("Tip percentage cannot be negative.")
    if discount < 0:
        raise ValueError("Discount cannot be negative.")
    if discount > subtotal:
        raise ValueError("Discount cannot be greater than subtotal.")


def calculate_split(
    subtotal: float,
    people: int = 1,
    tip_percent: float = 10.0,
    discount: float = 0.0,
    round_up: bool = False,
) -> BillSummary:
    """Calculate the split bill among a number of people.

    Args:
        subtotal: The original bill amount before discounts or tips.
        people: The number of people sharing the bill. Must be >= 1.
        tip_percent: Percentage of tip to add (default 10.0%).
        discount: Fixed discount amount to deduct before tip.
        round_up: Whether to round up each person's share to the nearest whole integer.

    Returns:
        BillSummary containing complete split details.
    """
    validate_split_inputs(subtotal, people, tip_percent, discount)

    subtotal = round(float(subtotal), 2)
    discount = round(float(discount), 2)
    discounted_subtotal = round(subtotal - discount, 2)

    tip_amount = round(discounted_subtotal * (tip_percent / 100.0), 2)
    total = round(discounted_subtotal + tip_amount, 2)

    raw_per_person = total / people

    if round_up:
        amount_per_person = float(math.ceil(raw_per_person))
        adjusted_total = round(amount_per_person * people, 2)
        rounding_difference = round(adjusted_total - total, 2)
    else:
        amount_per_person = round(raw_per_person, 2)
        rounding_difference = 0.0

    return BillSummary(
        subtotal=subtotal,
        discount=discount,
        discounted_subtotal=discounted_subtotal,
        tip_percent=round(float(tip_percent), 2),
        tip_amount=tip_amount,
        total=total,
        people=people,
        amount_per_person=amount_per_person,
        round_up=round_up,
        rounding_difference=rounding_difference,
    )


def calculate_uneven_split(
    items_by_person: Dict[str, float],
    shared_amount: float = 0.0,
    tip_percent: float = 10.0,
) -> List[PersonShare]:
    """Calculate individual payments when people consume different items.

    Args:
        items_by_person: Mapping of person names to their personal subtotal.
        shared_amount: Total cost of shared items (e.g. appetizers) split equally.
        tip_percent: Percentage of tip applied to each person's total consumption.

    Returns:
        List of PersonShare breakdown for each person.
    """
    if not items_by_person:
        raise ValueError("Must provide at least one person.")
    if shared_amount < 0:
        raise ValueError("Shared amount cannot be negative.")
    if tip_percent < 0:
        raise ValueError("Tip percentage cannot be negative.")

    for person, amount in items_by_person.items():
        if amount < 0:
            raise ValueError(f"Amount for '{person}' cannot be negative.")

    num_people = len(items_by_person)
    shared_per_person = round(shared_amount / num_people, 2)

    results: List[PersonShare] = []
    for person, individual_sub in items_by_person.items():
        individual_clean = round(float(individual_sub), 2)
        person_subtotal = round(individual_clean + shared_per_person, 2)
        tip_amount = round(person_subtotal * (tip_percent / 100.0), 2)
        total = round(person_subtotal + tip_amount, 2)

        results.append(
            PersonShare(
                name=person,
                individual_subtotal=individual_clean,
                shared_subtotal=shared_per_person,
                subtotal=person_subtotal,
                tip_amount=tip_amount,
                total=total,
            )
        )

    return results


def format_currency(amount: float, symbol: str = "$") -> str:
    """Format a monetary number into a clean currency string."""
    return f"{symbol}{amount:,.2f}"
