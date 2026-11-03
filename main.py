#!/usr/bin/env python3
"""Command-line interface for the Smart Bill Splitter."""

import argparse
import sys
from bill_splitter.calculator import calculate_split, format_currency


def build_parser() -> argparse.ArgumentParser:
    """Construct command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="bill-splitter",
        description="Split bills, calculate tips, and distribute expenses fairly among friends.",
    )
    parser.add_argument(
        "-s", "--subtotal",
        type=float,
        help="Subtotal bill amount before tip or discount.",
    )
    parser.add_argument(
        "-p", "--people",
        type=int,
        default=1,
        help="Number of people sharing the bill (default: 1).",
    )
    parser.add_argument(
        "-t", "--tip",
        type=float,
        default=10.0,
        help="Tip percentage (default: 10.0%%).",
    )
    parser.add_argument(
        "-d", "--discount",
        type=float,
        default=0.0,
        help="Discount amount to deduct before tip (default: 0.0).",
    )
    parser.add_argument(
        "-r", "--round-up",
        action="store_true",
        help="Round up per person share to the nearest whole integer.",
    )
    parser.add_argument(
        "--currency",
        type=str,
        default="$",
        help="Currency symbol to display (default: '$').",
    )
    return parser


def print_summary(summary, currency_symbol: str = "$") -> None:
    """Print formatted bill summary to terminal."""
    print("=" * 40)
    print("           BILL SPLIT SUMMARY           ")
    print("=" * 40)
    print(f"Subtotal:            {format_currency(summary.subtotal, currency_symbol)}")
    if summary.discount > 0:
        print(f"Discount:           -{format_currency(summary.discount, currency_symbol)}")
        print(f"Discounted Subtotal: {format_currency(summary.discounted_subtotal, currency_symbol)}")
    print(f"Tip ({summary.tip_percent:.1f}%):        {format_currency(summary.tip_amount, currency_symbol)}")
    print("-" * 40)
    print(f"Grand Total:         {format_currency(summary.total, currency_symbol)}")
    print(f"Number of People:    {summary.people}")
    print("-" * 40)
    print(f"AMOUNT PER PERSON:   {format_currency(summary.amount_per_person, currency_symbol)}")
    if summary.round_up and summary.rounding_difference > 0:
        print(f"(Rounded up; surplus: {format_currency(summary.rounding_difference, currency_symbol)})")
    print("=" * 40)


def prompt_float(prompt_text: str, default: float) -> float:
    """Prompt user for a float with fallback default."""
    raw = input(f"{prompt_text} [{default}]: ").strip()
    if not raw:
        return default
    return float(raw)


def prompt_int(prompt_text: str, default: int) -> int:
    """Prompt user for an integer with fallback default."""
    raw = input(f"{prompt_text} [{default}]: ").strip()
    if not raw:
        return default
    return int(raw)


def interactive_mode(currency_symbol: str = "$") -> None:
    """Run interactive question prompt for bill splitting."""
    print("\n--- Smart Bill Splitter (Interactive Mode) ---")
    try:
        subtotal_str = input(f"Enter bill subtotal ({currency_symbol}): ").strip()
        subtotal = float(subtotal_str)
        people = prompt_int("Number of people splitting", 1)
        tip_percent = prompt_float("Tip percentage (%)", 10.0)
        discount = prompt_float("Discount amount", 0.0)
        round_up_raw = input("Round up per-person amount? (y/N): ").strip().lower()
        round_up = round_up_raw in ("y", "yes")

        summary = calculate_split(
            subtotal=subtotal,
            people=people,
            tip_percent=tip_percent,
            discount=discount,
            round_up=round_up,
        )
        print()
        print_summary(summary, currency_symbol)
    except (ValueError, KeyboardInterrupt) as exc:
        print(f"\nError or aborted: {exc}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    """Main CLI entrypoint."""
    parser = build_parser()
    args = parser.parse_args()

    if args.subtotal is None:
        interactive_mode(args.currency)
        return

    try:
        summary = calculate_split(
            subtotal=args.subtotal,
            people=args.people,
            tip_percent=args.tip,
            discount=args.discount,
            round_up=args.round_up,
        )
        print_summary(summary, args.currency)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
