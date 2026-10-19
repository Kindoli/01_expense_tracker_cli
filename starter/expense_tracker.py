"""
Expense Tracker CLI - starter code (Project 01).

Work through the README step by step. Each TODO says which step it belongs to.
Run the program after every step:

    python starter/expense_tracker.py

Menu options whose functions are not written yet print
"Not implemented yet" instead of crashing, so you can run it from day one.
"""

import csv
from datetime import date, datetime
from pathlib import Path

# The CSV lives in the project's data folder, one level above starter/.
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "expenses.csv"

FIELDNAMES = ["id", "date", "category", "description", "amount"]
CATEGORIES = [
    "Food",
    "Transport",
    "Housing",
    "Utilities",
    "Health",
    "Entertainment",
    "Shopping",
    "Other",
]
DATE_FORMAT = "%Y-%m-%d"


# ---------------------------------------------------------------------------
# Step 4: validation helpers
# ---------------------------------------------------------------------------

def parse_amount(text):
    """Convert text like '12.5' into a positive float rounded to 2 decimals.

    Raises:
        ValueError: if the text is not a number or is not greater than zero.
    """
    # TODO (Step 4): use try/except around float(text.strip()).
    # If it fails, raise ValueError(f"'{text}' is not a number.") from None
    # If the amount is <= 0, raise ValueError("Amount must be greater than zero.")
    # Return round(amount, 2).
    raise NotImplementedError("Step 4")


def parse_date(text):
    """Convert text like '2026-09-27' into a datetime.date. Empty = today.

    Raises:
        ValueError: if the text is not a valid YYYY-MM-DD date.
    """
    # TODO (Step 2): strip the text. If it's empty, return date.today().
    # Otherwise return datetime.strptime(text, DATE_FORMAT).date()
    # TODO (Step 4): wrap strptime in try/except and raise a friendlier
    # ValueError: f"'{text}' is not a valid date. Use YYYY-MM-DD."
    raise NotImplementedError("Step 2")


def parse_category(text):
    """Return the properly spelled category matching text (case-insensitive).

    Raises:
        ValueError: if the category is not in CATEGORIES.
    """
    # TODO (Step 4): loop over CATEGORIES and compare .lower() versions.
    raise NotImplementedError("Step 4")


def parse_description(text):
    """Return the stripped description. Raises ValueError if it is empty."""
    # TODO (Step 4)
    raise NotImplementedError("Step 4")


def parse_month(text):
    """Convert 'YYYY-MM' into a (year, month) tuple. Empty = this month.

    Raises:
        ValueError: if the text is not a valid month.
    """
    # TODO (Step 7): hint - datetime.strptime(text, "%Y-%m") works for months.
    raise NotImplementedError("Step 7")


def ask(prompt, parser):
    """Keep asking until `parser` accepts the answer, then return the result.

    `parser` is a function such as parse_amount.
    """
    # TODO (Step 4): while True: input(prompt), try: return parser(text),
    # except ValueError as error: print the error and loop again.
    raise NotImplementedError("Step 4")


# ---------------------------------------------------------------------------
# Steps 2 and 5: reading and writing the CSV file
# ---------------------------------------------------------------------------

def load_expenses(path=DATA_FILE):
    """Read all expenses from the CSV file and return a list of dicts.

    Each dict has: id (int), date (date), category (str),
    description (str), amount (float).
    """
    expenses = []
    # TODO (Step 2): if the file doesn't exist, return the empty list.
    # TODO (Step 2): open the file with newline="" and encoding="utf-8",
    # use csv.DictReader, convert each row's values to the right types
    # and append the dict to `expenses`.
    # TODO (Step 9): skip bad rows with a warning instead of crashing
    # (catch KeyError, ValueError, AttributeError).
    return expenses


def save_expenses(expenses, path=DATA_FILE):
    """Write all expenses to the CSV file (overwriting it)."""
    # TODO (Step 5): use csv.DictWriter with FIELDNAMES.
    # Remember: dates must be turned back into text with .isoformat(),
    # and amounts formatted with f"{amount:.2f}".
    raise NotImplementedError("Step 5")


# ---------------------------------------------------------------------------
# Logic functions: take data, return data. No input() or print() here.
# ---------------------------------------------------------------------------

def next_id(expenses):
    """Return the highest existing id + 1 (or 1 if the list is empty)."""
    # TODO (Step 4)
    raise NotImplementedError("Step 4")


def total_amount(expenses):
    """Return the sum of all amounts in the list."""
    # TODO (Step 3)
    raise NotImplementedError("Step 3")


def find_expense(expenses, expense_id):
    """Return the expense with this id, or None."""
    # TODO (Step 8)
    raise NotImplementedError("Step 8")


def summary_by_category(expenses):
    """Return a dict {category: total amount}."""
    # TODO (Step 6): start with totals = {} and use totals.get(category, 0).
    raise NotImplementedError("Step 6")


def monthly_total(expenses, year, month):
    """Return (total, count) for expenses in the given year and month."""
    # TODO (Step 7): expense["date"].year and expense["date"].month help here.
    raise NotImplementedError("Step 7")


def delete_expense(expenses, expense_id):
    """Remove the expense with this id. Return it, or None if not found."""
    # TODO (Step 8): enumerate() gives you the index; list.pop(index) removes it.
    raise NotImplementedError("Step 8")


# ---------------------------------------------------------------------------
# Screen functions: talk to the user, then call the logic functions.
# ---------------------------------------------------------------------------

def format_expense(expense):
    """Return one expense as an aligned line of text."""
    # TODO (Step 3): use f-string alignment, e.g. f"{expense['id']:>4}"
    raise NotImplementedError("Step 3")


def show_expenses(expenses):
    """Print all expenses as a table, sorted by date, with a total line."""
    # TODO (Step 3)
    raise NotImplementedError("Step 3")


def add_expense_screen(expenses):
    """Ask for a new expense, validate each field, append it and save."""
    # TODO (Step 4): use ask() with each parse_ function.
    # TODO (Step 5): call save_expenses(expenses) after appending.
    raise NotImplementedError("Step 4")


def show_summary(expenses):
    """Print totals per category, biggest first."""
    # TODO (Step 6)
    raise NotImplementedError("Step 6")


def show_monthly_total(expenses):
    """Ask for a month and print its total."""
    # TODO (Step 7)
    raise NotImplementedError("Step 7")


def delete_expense_screen(expenses):
    """Ask for an id, show the expense, confirm, delete and save."""
    # TODO (Step 8)
    raise NotImplementedError("Step 8")


MENU = """
===== Expense Tracker =====
1) Add expense
2) List expenses
3) Summary by category
4) Monthly total
5) Delete expense
q) Quit
"""


def main():
    """Load the data and run the menu loop."""
    expenses = load_expenses()
    print(f"Loaded {len(expenses)} expenses from {DATA_FILE.name}")

    # TODO (Step 1): read this loop and make sure you understand every line.
    while True:
        print(MENU)
        # TODO (Step 9): catch EOFError and KeyboardInterrupt around input()
        # so Ctrl+C exits politely.
        choice = input("Choose an option: ").strip().lower()

        try:
            if choice == "1":
                add_expense_screen(expenses)
            elif choice == "2":
                show_expenses(expenses)
            elif choice == "3":
                show_summary(expenses)
            elif choice == "4":
                show_monthly_total(expenses)
            elif choice == "5":
                delete_expense_screen(expenses)
            elif choice == "q":
                print("Goodbye!")
                break
            else:
                print(f"'{choice}' is not an option. Try again.")
        except NotImplementedError as error:
            # Remove this except block once every step is done.
            print(f"Not implemented yet - see README {error}.")


if __name__ == "__main__":
    main()
