# Smart Bill Splitter 🧾💸

[![CI](https://github.com/PolloHacker/smart-bill-splitter/actions/workflows/ci.yml/badge.svg)](https://github.com/PolloHacker/smart-bill-splitter/actions/workflows/ci.yml)

A lightweight, dependency-free Python CLI utility designed for everyday use: splitting restaurant checks, bar bills, delivery orders, or shared group expenses fairly with friends.

---

## ✨ Features

- **Equal Bill Splitting:** Divides total bills equally among any number of people.
- **Custom Tips & Discounts:** Deducts discounts and calculates tip percentages dynamically.
- **Round-Up Option:** Rounds up per-person amounts to whole currency units to avoid pennies or awkward cent transfers.
- **Itemized / Uneven Splits:** Computes individual totals when each person ordered specific items plus shared appetizers/drinks.
- **Cross-Platform & Zero External Dependencies:** Uses standard Python library modules (`dataclasses`, `argparse`, `unittest`).

---

## 🚀 Quick Start

### 1. Interactive Mode
Simply run the script without arguments:
```bash
python3 main.py
```
You will be prompted for:
- Subtotal
- Number of people
- Tip percentage (default: 10%)
- Discount amount (optional)
- Round-up preference

### 2. CLI Command with Flags
```bash
# Split a $120 bill among 4 people with a 15% tip:
python3 main.py --subtotal 120 --people 4 --tip 15

# Split an $85 bill with $10 discount among 3 people, rounded up:
python3 main.py -s 85 -p 3 -t 10 -d 10 -r
```

Example Output:
```text
========================================
           BILL SPLIT SUMMARY           
========================================
Subtotal:            $85.00
Discount:           -$10.00
Discounted Subtotal: $75.00
Tip (10.0%):        $7.50
----------------------------------------
Grand Total:         $82.50
Number of People:    3
----------------------------------------
AMOUNT PER PERSON:   $28.00
(Rounded up; surplus: $1.50)
========================================
```

---

## 🧪 Running Unit Tests Locally

Run the built-in test suite (10 unit tests):

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

---

## ⚙️ GitHub Actions CI / CD Matrix

This repository includes continuous integration (`.github/workflows/ci.yml`) that executes the test suite on every commit and pull request across a matrix of:

- **Operating Systems:**
  - Ubuntu (`ubuntu-latest`)
  - macOS (`macos-latest`)
  - Windows (`windows-latest`)
- **Python Versions:**
  - `3.10`
  - `3.11`
  - `3.12`

Total: **9 matrix test configurations** running in parallel to guarantee cross-platform compatibility.
