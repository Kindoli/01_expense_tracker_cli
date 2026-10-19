"""
Expense Tracker CLI - reference solution (Project 01).

A small menu-driven program that stores expenses in a CSV file.

Run it from anywhere:
    python solution/expense_tracker.py
"""

import csv
from datetime import date, datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants (UPPER_CASE = "please don't change me while the program runs")
# ---------------------------------------------------------------------------

# Path(__file__) is this .py file. .resolve() makes it absolute,
# .parent is the "solution" folder, .parent again is the project folder.
# This way the program finds the data no matter which folder you run it from.
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
DATE_FORMAT = "%Y-%m-%d"  # e.g. 2026-09-27


# ---------------------------------------------------------------------------
# Step 4: validation helpers - each one turns text into a clean value
# or raises ValueError with a friendly message.
# ---------------------------------------------------------------------------

def parse_amount(text):
    """Convert text like '12.5' into a positive float rounded to 2 decimals.

    Raises:
        ValueError: if the text is not a number or is not greater than zero.
    """
    try:
        amount = float(text.strip().replace(",", ""))
    except ValueError:
        # "from None" hides the original, less friendly error message.
        raise ValueError(f"'{text}' is not a number.") from None
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    return round(amount, 2)


def parse_date(text):
    """Convert text like '2026-09-27' into a datetime.date object.

    An empty string means "today".

    Raises:
        ValueError: if the text is not a valid YYYY-MM-DD date.
    """
    text = text.strip()
    if text == "":
        return date.today()
    try:
        return datetime.strptime(text, DATE_FORMAT).date()
    except ValueError:
        raise ValueError(f"'{text}' is not a valid date. Use YYYY-MM-DD.") from None


def parse_category(text):
    """Match text against CATEGORIES (case-insensitive) and return the
    properly spelled category name.

    Raises:
        ValueError: if the category is unknown.
    """
    cleaned = text.strip().lower()
    for category in CATEGORIES:
        if category.lower() == cleaned:
            return category
    raise ValueError(f"Unknown category. Choose one of: {', '.join(CATEGORIES)}")


def parse_description(text):
    """Return the stripped description. Raises ValueError if it is empty."""
    text = text.strip()
    if text == "":
        raise ValueError("Description cannot be empty.")
    return text


def parse_month(text):
    """Convert 'YYYY-MM' into a (year, month) tuple. Empty means this month.

    Raises:
        ValueError: if the text is not a valid month.
    """
    text = text.strip()
    if text == "":
        today = date.today()
        return today.year, today.month
    try:
        parsed = datetime.strptime(text, "%Y-%m")
    except ValueError:
        raise ValueError(f"'{text}' is not a valid month. Use YYYY-MM.") from None
    return parsed.year, parsed.month


def ask(prompt, parser):
    """Keep asking the user until `parser` accepts the answer.

    `parser` is a function (like parse_amount). Functions are values in
    Python, so we can pass them around just like numbers or strings.
    """
    while True:
        text = input(prompt)
        try:
            return parser(text)
        except ValueError as error:
            print(f"  ! {error}")


# ---------------------------------------------------------------------------
# Step 2 and 5: reading and writing the CSV file
# ---------------------------------------------------------------------------

def load_expenses(path=DATA_FILE):
    """Read all expenses from the CSV file.

    Returns a list of dicts with keys id, date, category, description, amount.
    Bad rows are skipped with a warning instead of crashing the program.
    A missing file simply means "no expenses yet".
    """
    expenses = []
    if not path.exists():
        return expenses

    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        # Line 1 is the header, so data starts on line 2.
        for line_number, row in enumerate(reader, start=2):
            try:
                expense = {
                    "id": int(row["id"]),
                    "date": parse_date(row["date"]),
                    "category": row["category"].strip(),
                    "description": row["description"].strip(),
                    "amount": parse_amount(row["amount"]),
                }
            except (KeyError, ValueError, AttributeError) as error:
                # KeyError: a column is missing. ValueError: bad number/date.
                # AttributeError: the row is too short (value is None).
                print(f"Warning: skipping line {line_number} of {path.name}: {error}")
                continue
            expenses.append(expense)
    return expenses


def save_expenses(expenses, path=DATA_FILE):
    """Write all expenses to the CSV file (overwriting it)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        for expense in expenses:
            writer.writerow(
                {
                    "id": expense["id"],
                    "date": expense["date"].isoformat(),  # date -> "YYYY-MM-DD"
                    "category": expense["category"],
                    "description": expense["description"],
                    "amount": f"{expense['amount']:.2f}",
                }
            )


# ---------------------------------------------------------------------------
# Pure "logic" functions: they take data and return data, no input()/print().
# These are easy to test and reuse.
# ---------------------------------------------------------------------------

def next_id(expenses):
    """Return the next free id (highest existing id + 1)."""
    highest = 0
    for expense in expenses:
        if expense["id"] > highest:
            highest = expense["id"]
    return highest + 1


def total_amount(expenses):
    """Return the sum of all amounts in the list."""
    total = 0.0
    for expense in expenses:
        total += expense["amount"]
    return total


def find_expense(expenses, expense_id):
    """Return the expense with this id, or None if there is none."""
    for expense in expenses:
        if expense["id"] == expense_id:
            return expense
    return None


def sort_key_by_date(expense):
    """Used by sorted(): sort by date, then by id for equal dates."""
    return (expense["date"], expense["id"])


def summary_by_category(expenses):
    """Return a dict {category: total amount}."""
    totals = {}
    for expense in expenses:
        category = expense["category"]
        totals[category] = totals.get(category, 0) + expense["amount"]
    return totals


def monthly_total(expenses, year, month):
    """Return (total, count) for all expenses in the given year and month."""
    total = 0.0
    count = 0
    for expense in expenses:
        if expense["date"].year == year and expense["date"].month == month:
            total += expense["amount"]
            count += 1
    return total, count


def delete_expense(expenses, expense_id):
    """Remove the expense with this id from the list.

    Returns the removed expense, or None if no expense has that id.
    """
    for index, expense in enumerate(expenses):
        if expense["id"] == expense_id:
            return expenses.pop(index)
    return None


# ---------------------------------------------------------------------------
# "Screen" functions: talk to the user, then call the logic functions.
# ---------------------------------------------------------------------------

def format_expense(expense):
    """Return one expense as a nicely aligned line of text."""
    return (
        f"{expense['id']:>4}  {expense['date'].isoformat():<10}  "
        f"{expense['category']:<13}  {expense['description'][:28]:<28}  "
        f"{expense['amount']:>9.2f}"
    )


def show_expenses(expenses):
    """Step 3: print all expenses as a table, sorted by date."""
    if not expenses:
        print("No expenses yet.")
        return
    header = f"{'ID':>4}  {'Date':<10}  {'Category':<13}  {'Description':<28}  {'Amount':>9}"
    print(header)
    print("-" * len(header))
    # key= takes a FUNCTION. sorted() calls it on each expense and sorts
    # by whatever it returns. Note: no () after sort_key_by_date!
    for expense in sorted(expenses, key=sort_key_by_date):
        print(format_expense(expense))
    print("-" * len(header))
    total = total_amount(expenses)
    print(f"{'TOTAL':>4}  {'':<10}  {'':<13}  {len(expenses):>3} expenses{'':<16}  {total:>9.2f}")


def add_expense_screen(expenses):
    """Step 4: ask the user for a new expense, validate it, save it."""
    print("\nAdd a new expense")
    expense_date = ask("  Date (YYYY-MM-DD, blank = today): ", parse_date)
    print(f"  Categories: {', '.join(CATEGORIES)}")
    category = ask("  Category: ", parse_category)
    description = ask("  Description: ", parse_description)
    amount = ask("  Amount: ", parse_amount)

    expense = {
        "id": next_id(expenses),
        "date": expense_date,
        "category": category,
        "description": description,
        "amount": amount,
    }
    expenses.append(expense)
    save_expenses(expenses)
    print(f"Saved expense #{expense['id']}: {description} ({amount:.2f})")


def show_summary(expenses):
    """Step 6: print totals per category, biggest first, with a bar chart."""
    totals = summary_by_category(expenses)
    if not totals:
        print("No expenses yet.")
        return
    grand_total = sum(totals.values())
    print(f"\n{'Category':<13}  {'Total':>9}  {'Share':>6}")
    # totals.get is a function: totals.get("Food") returns the Food total. Using
    # it as key= sorts the category names by their total;
    # reverse=True puts the biggest first.
    for category in sorted(totals, key=totals.get, reverse=True):
        total = totals[category]
        share = total / grand_total * 100
        bar = "#" * round(share / 2)  # 1 '#' per 2 percent
        print(f"{category:<13}  {total:>9.2f}  {share:>5.1f}%  {bar}")
    print(f"{'TOTAL':<13}  {grand_total:>9.2f}")


def show_monthly_total(expenses):
    """Step 7: ask for a month and print its total."""
    year, month = ask("Month (YYYY-MM, blank = this month): ", parse_month)
    total, count = monthly_total(expenses, year, month)
    # date(year, month, 1).strftime("%B %Y") gives e.g. "September 2026"
    month_name = date(year, month, 1).strftime("%B %Y")
    print(f"{month_name}: {total:.2f} spent across {count} expenses.")


def delete_expense_screen(expenses):
    """Step 8: ask for an id, confirm, delete and save."""
    if not expenses:
        print("Nothing to delete.")
        return
    text = input("Id of the expense to delete: ").strip()
    try:
        expense_id = int(text)
    except ValueError:
        print(f"  ! '{text}' is not a valid id.")
        return

    # Look first, delete only after the user confirms.
    expense = find_expense(expenses, expense_id)
    if expense is None:
        print(f"  ! No expense with id {expense_id}.")
        return
    print(format_expense(expense))
    answer = input("Delete this expense? (y/n): ").strip().lower()
    if answer != "y":
        print("Cancelled.")
        return
    delete_expense(expenses, expense_id)
    save_expenses(expenses)
    print(f"Deleted expense #{expense_id}.")


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
    """Step 1 and 9: load the data and run the menu loop."""
    expenses = load_expenses()
    print(f"Loaded {len(expenses)} expenses from {DATA_FILE.name}")

    while True:
        print(MENU)
        try:
            choice = input("Choose an option: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            # EOFError: input ran out (e.g. piped input). Ctrl+C: KeyboardInterrupt.
            print("\nGoodbye!")
            break

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
        except (EOFError, KeyboardInterrupt):
            print("\nCancelled. Goodbye!")
            break


# This block only runs when you execute this file directly
# (python expense_tracker.py), NOT when another file imports it.
if __name__ == "__main__":
    main()
