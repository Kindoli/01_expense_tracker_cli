# Project 01 — Expense Tracker CLI

## What you'll build

A small command-line program that keeps track of your spending. You pick
options from a menu to add an expense, list everything, see totals per
category, check how much you spent in a given month, and delete mistakes.
Every change is saved to a CSV file (`data/expenses.csv`), so your data is
still there next time you run the program. Along the way you'll learn to split
a program into small functions, read and write files, and handle bad input
without crashing — the three habits every data engineer relies on daily.

**Estimated time:** 2 weeks (6–10 hours)

**Prerequisites:** variables, `if`/`elif`/`else`, `while` and `for` loops,
lists, dicts, tuples, `input()` and `print()`.

**Files**

```
01_expense_tracker_cli/
├── README.md
├── data/expenses.csv              ← 30 sample expenses
├── starter/expense_tracker.py     ← you write your code here
└── solution/expense_tracker.py    ← reference answer
```

Run your version from the project folder with:

```powershell
python starter/expense_tracker.py
```

> Tip: the program changes `data/expenses.csv`. Before you start, make a copy
> (`Copy-Item data/expenses.csv data/expenses_backup.csv`) or commit it to git,
> so you can always go back to the original sample.

---

## Concepts you'll learn

### 1. Functions — naming a piece of work

A function is a named, reusable block of code. You give it inputs
(*parameters*), it does some work, and it hands back a result with `return`.

```python
def add_vat(price, rate=0.2):      # rate has a default value
    """Return the price including VAT."""
    return price * (1 + rate)

print(add_vat(100))        # 120.0
print(add_vat(100, 0.1))   # 110.0  (overrides the default)
```

Why bother? Because `add_vat(100)` is easier to read than `100 * 1.2`, you
can test it on its own, and when the rule changes you fix it in one place.

Things to know:

- A function with no `return` returns `None`.
- `return` ends the function immediately.
- Variables created inside a function only exist inside it (*local scope*).
- A function can return several values as a tuple: `return total, count`,
  and you unpack them with `total, count = monthly_total(...)`.

**Rule of thumb:** if a function needs the word "and" to describe it, split it.

### 2. Docstrings — describing what a function does

The first string inside a function is its *docstring*. VS Code shows it when
you hover over the function name, and `help(add_vat)` prints it.

```python
def is_weekend(day):
    """Return True if `day` (a datetime.date) is a Saturday or Sunday."""
    return day.weekday() >= 5
```

Describe *what* the function does and what it returns, not *how*.

### 3. Functions are values

In Python a function is an object, like a number or a list. You can store
it in a variable or pass it to another function. Notice: no `()` — you
pass the function itself, not its result.

```python
def shout(text):
    return text.upper() + "!"

def apply(func, value):
    return func(value)

print(apply(shout, "hello"))   # HELLO!

words = ["banana", "Apple", "cherry"]
print(sorted(words, key=len))        # sort by length: ['Apple', 'banana', 'cherry']
print(sorted(words, key=str.lower))  # sort ignoring case
```

We'll use this to build one `ask()` function that works for amounts, dates
and categories.

### 4. f-strings — formatting text

Put an `f` before a string and anything in `{}` is evaluated. After a colon
you can control the format: width, alignment (`<` left, `>` right) and decimals.

```python
name, amount = "Coffee", 3.5
print(f"{name} cost {amount}")        # Coffee cost 3.5
print(f"{amount:.2f}")                # 3.50       (2 decimals)
print(f"[{name:<10}]")                # [Coffee    ] (left, width 10)
print(f"[{amount:>8.2f}]")            # [    3.50] (right, width 8)
print(f"{'-' * 20}")                  # 20 dashes
```

### 5. Reading and writing CSV files

A CSV ("comma-separated values") file is a plain-text table. The `csv` module
handles the tricky bits (commas inside values, quotes, line endings).

```python
import csv

# Writing
rows = [{"name": "Ann", "age": 31}, {"name": "Ben", "age": 27}]
with open("people.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age"])
    writer.writeheader()
    for row in rows:
        writer.writerow(row)

# Reading
with open("people.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        print(row["name"], int(row["age"]) + 1)   # values come back as TEXT
```

- `with open(...) as f:` closes the file automatically, even if an error happens.
- `"w"` overwrites the file, `"r"` (default) reads, `"a"` appends.
- Always pass `newline=""` when using `csv` — otherwise Windows adds blank lines.
- `DictReader` gives each row as a dict keyed by the header.
  **Every value is a string**, so convert with `int()`, `float()` etc.

### 6. `pathlib` — paths that work on every computer

```python
from pathlib import Path

here = Path(__file__).resolve().parent     # folder containing this .py file
data_file = here.parent / "data" / "expenses.csv"
print(data_file)            # D:\...\01_expense_tracker_cli\data\expenses.csv
print(data_file.exists())   # True / False
print(data_file.name)       # expenses.csv
```

The `/` operator joins path pieces and uses the right slash for Windows or
Linux. Building the path from `__file__` means your program finds its data
no matter which folder your terminal is in.

### 7. Errors and `try` / `except`

When something goes wrong, Python *raises an exception*. If nobody catches
it, the program crashes and prints a traceback. `try`/`except` lets you catch
it and decide what to do instead.

```python
text = "12,5"
try:
    amount = float(text)
except ValueError:
    print(f"'{text}' is not a number")
else:
    print("Got", amount)       # runs only if no exception happened
```

You can also **raise** your own exceptions to say "this input is invalid":

```python
def parse_age(text):
    age = int(text)                 # may raise ValueError by itself
    if age < 0:
        raise ValueError("Age cannot be negative.")
    return age

try:
    parse_age("-3")
except ValueError as error:         # `as error` gives you the message
    print("Problem:", error)        # Problem: Age cannot be negative.
```

Catch **specific** exceptions (`ValueError`, `KeyError`, `FileNotFoundError`),
never a bare `except:` — that would also hide your own bugs.

Common ones you'll meet:

| Exception | Typical cause |
|-----------|---------------|
| `ValueError` | right type, wrong value: `int("abc")` |
| `KeyError` | dict key doesn't exist: `d["missing"]` |
| `FileNotFoundError` | opening a file that isn't there |
| `KeyboardInterrupt` | the user pressed Ctrl+C |
| `EOFError` | `input()` had nothing left to read |

### 8. Dates with `datetime`

Dates as text (`"2026-09-27"`) can't be compared or grouped reliably. Convert
them to `date` objects.

```python
from datetime import date, datetime

d = datetime.strptime("2026-09-27", "%Y-%m-%d").date()   # text -> date
print(d.year, d.month, d.day)        # 2026 9 27
print(d.isoformat())                 # "2026-09-27"     (date -> text)
print(d.strftime("%B %Y"))           # "September 2026"
print(date.today())                  # today's date
print(d < date(2026, 12, 31))        # True - dates compare naturally
```

`strptime` = "string **p**arse time" (text in), `strftime` = "string
**f**ormat time" (text out). A bad date like `"2026-13-40"` raises `ValueError`.

### 9. `if __name__ == "__main__":`

Every Python file has a built-in variable `__name__`. When you run a file
directly, it is `"__main__"`. When another file *imports* it, it is the
module's name (`"expense_tracker"`).

```python
def main():
    print("Running the app")

if __name__ == "__main__":
    main()
```

This means "start the app only when run directly". Later you (or a test) can
`import expense_tracker` and reuse `parse_amount` without the menu popping up.

---

## Step-by-step

Write your code in `starter/expense_tracker.py`. Every function there already
exists with a docstring and a `# TODO (Step N)` comment. Unfinished functions
`raise NotImplementedError`, and the menu catches that and prints
"Not implemented yet", so the program runs from the very first step.

### Step 1 — Run the skeleton and read the menu loop

**Goal:** understand how the program is organised before changing it.

Open the starter file and read it top to bottom. Notice the structure:

1. Imports and constants at the top (`DATA_FILE`, `CATEGORIES`, ...).
2. Small *helper* functions (`parse_...`).
3. *Logic* functions that take data and return data, with no `input()` or
   `print()` (`summary_by_category`, `monthly_total`, ...).
4. *Screen* functions that talk to the user and call the logic functions.
5. `main()` with the menu loop, started by `if __name__ == "__main__":`.

Keeping logic separate from input/output is the most valuable habit in this
project. Logic functions are easy to test and reuse; screen functions are thin.

Add a `print(DATA_FILE)` at the start of `main()` to see the path that
`Path(__file__)` produced, then remove it.

✅ **Check:** run `python starter/expense_tracker.py`. You see
`Loaded 0 expenses from expenses.csv` and the menu. Choosing `2` prints
"Not implemented yet", choosing `x` says it's not an option, `q` quits.

### Step 2 — Load expenses from the CSV

**Goal:** turn `data/expenses.csv` into a list of dicts with proper types.

1. Write `parse_date(text)`: strip the text; if it's empty return
   `date.today()`; otherwise return
   `datetime.strptime(text, DATE_FORMAT).date()`.
2. Write `load_expenses(path)`:
   - If `path.exists()` is `False`, return the empty list.
   - Open the file with `newline=""` and `encoding="utf-8"`.
   - Loop over `csv.DictReader(file)` and build a dict for each row:

```python
expense = {
    "id": int(row["id"]),
    "date": parse_date(row["date"]),
    "category": row["category"].strip(),
    "description": row["description"].strip(),
    "amount": float(row["amount"]),
}
```

Why convert? `"9.99" + "1"` is `"9.991"`, not `10.99`. Convert at the edge of
your program (when data comes in), and the rest of the code can trust the types.

✅ **Check:** run the program. You should see `Loaded 30 expenses from expenses.csv`.
Temporarily add `print(expenses[0])` in `main()` — you'll see
`{'id': 1, 'date': datetime.date(2026, 7, 1), 'category': 'Housing', ...}`.

### Step 3 — List expenses as a table

**Goal:** menu option 2 prints a neat, aligned table.

1. `total_amount(expenses)`: loop and add up `expense["amount"]`.
2. `format_expense(expense)`: return one line using f-string widths, e.g.

```python
return (
    f"{expense['id']:>4}  {expense['date'].isoformat():<10}  "
    f"{expense['category']:<13}  {expense['description'][:28]:<28}  "
    f"{expense['amount']:>9.2f}"
)
```

   (`[:28]` cuts long descriptions so the columns stay aligned.)
3. `show_expenses(expenses)`: print a header, a line of dashes, every
   expense sorted by date, another line and the total. To sort, write a tiny
   function that returns what to sort by, and pass it as `key`:

```python
def sort_key_by_date(expense):
    return (expense["date"], expense["id"])

for expense in sorted(expenses, key=sort_key_by_date):
    ...
```

✅ **Check:** option `2` shows 30 rows from `2026-07-01` to `2026-09-27`,
and the total line shows `3783.72`.

### Step 4 — Add an expense with validation

**Goal:** option 1 asks for each field and refuses bad input politely.

1. Write the parsers. Each one takes text and either returns a clean value
   or raises `ValueError` with a helpful message:
   - `parse_amount`: `float()` inside `try`; reject `<= 0`.
   - `parse_category`: compare `text.strip().lower()` with each category's
     `.lower()`; return the nicely spelled one.
   - `parse_description`: reject empty text.
   - Improve `parse_date`: wrap `strptime` in `try`/`except ValueError` and
     raise a friendlier message.
2. Write `ask(prompt, parser)` — one loop that works for every field:

```python
def ask(prompt, parser):
    while True:
        text = input(prompt)
        try:
            return parser(text)
        except ValueError as error:
            print(f"  ! {error}")
```

3. Write `next_id(expenses)` (highest id + 1).
4. Write `add_expense_screen(expenses)`: call `ask()` four times, build the
   dict, append it to the list, print a confirmation.

Tip: `raise ValueError("...") from None` hides Python's original error
message so the user only sees yours.

✅ **Check:** choose `1`, type `abc` as amount → `! 'abc' is not a number.`;
type `-5` → `! Amount must be greater than zero.`; type `food` as category →
it is saved as `Food`. Option `2` now shows your expense with id `31`.
(It disappears when you restart — that's Step 5.)

### Step 5 — Save expenses to the CSV

**Goal:** changes survive a restart.

Write `save_expenses(expenses, path)` with `csv.DictWriter`. Open the file
in `"w"` mode with `newline=""`. Convert values back to text:
`expense["date"].isoformat()` and `f"{expense['amount']:.2f}"`.
Call it at the end of `add_expense_screen`.

Why rewrite the whole file instead of appending? Because delete (Step 8)
also needs to save, and rewriting the full list is the simplest way to keep
the file and your list identical. For a few thousand rows this is instant.

✅ **Check:** add an expense, quit, run again. You see `Loaded 31 expenses`
and the new row is in `data/expenses.csv` (open it in VS Code).

### Step 6 — Summary by category

**Goal:** option 3 shows how much went to each category, biggest first.

1. `summary_by_category(expenses)` returns a dict like
   `{"Housing": 2550.0, "Food": 442.95, ...}`. The trick is `dict.get`
   with a default:

```python
totals = {}
for expense in expenses:
    category = expense["category"]
    totals[category] = totals.get(category, 0) + expense["amount"]
```

2. `show_summary(expenses)` prints each category, its total and its share
   of the grand total in percent. Sort the categories by their total with
   `sorted(totals, key=totals.get, reverse=True)` (`totals.get` is a
   function that takes a category and returns its total!). For a little bar
   chart: `"#" * round(share / 2)`.

✅ **Check:** with the original sample data, `Housing` is first with
`2550.00` (`67.4%`), then `Food` with `442.95`, and the total is `3783.72`.

### Step 7 — Monthly total

**Goal:** option 4 asks for a month and prints how much was spent.

1. `parse_month(text)`: empty means this month
   (`date.today().year, date.today().month`); otherwise use
   `datetime.strptime(text, "%Y-%m")` and return `(parsed.year, parsed.month)`.
2. `monthly_total(expenses, year, month)` returns a tuple `(total, count)`.
3. `show_monthly_total(expenses)`: use `ask()` with `parse_month`, then print
   with a friendly month name: `date(year, month, 1).strftime("%B %Y")`.

✅ **Check:** option `4`, type `2026-08` →
`August 2026: 1351.42 spent across 11 expenses.` Type `banana` → an error
message and the question again.

### Step 8 — Delete an expense

**Goal:** option 5 removes an expense after confirmation.

1. `find_expense(expenses, expense_id)`: return the matching dict or `None`.
2. `delete_expense(expenses, expense_id)`: use `enumerate()` to get the
   index, then `expenses.pop(index)`; return the removed expense or `None`.
3. `delete_expense_screen(expenses)`: ask for the id (handle non-numbers
   with `try`/`except`), show the expense, ask `y/n`, delete, save.

Always confirm destructive actions. It costs the user one keystroke and saves
them from a typo.

✅ **Check:** delete the expense you added in Step 4. Typing `99` prints
`No expense with id 99.` Answering `n` prints `Cancelled.` and nothing changes.

### Step 9 — Make it robust

**Goal:** the program never crashes with a traceback in normal use.

1. In `load_expenses`, wrap the row conversion in
   `try` / `except (KeyError, ValueError, AttributeError) as error:`,
   print a warning with the line number (`enumerate(reader, start=2)`) and
   `continue`. One bad row shouldn't lose all your data.
2. In `main()`, wrap `input("Choose an option: ")` in
   `try` / `except (EOFError, KeyboardInterrupt):` and exit with "Goodbye!".
3. Remove the `except NotImplementedError` block — you don't need it anymore.

✅ **Check:** add a line `99,not-a-date,Food,Broken,abc` to the end of the CSV
and run. You see `Warning: skipping line 32 ...` and the other 30 rows still
load. Press Ctrl+C at the menu — you get `Goodbye!`, not a traceback.
Remove the broken line afterwards.

---

## Common mistakes

- **Forgetting that CSV values are strings.** `row["amount"] * 2` gives
  `"9.999.99"`. Convert with `float()` when loading.
- **Forgetting `newline=""`** when opening CSV files on Windows → blank line
  between every row.
- **Calling a function when you meant to pass it.** `ask("Amount: ", parse_amount())`
  calls `parse_amount` with no argument and crashes. Pass `parse_amount` without `()`.
- **`print` instead of `return`.** If a function prints its result, other
  code can't use it. Logic functions should `return`.
- **A bare `except:`** that hides every error, including typos in your own code.
- **Opening in `"w"` mode by accident** — it empties the file immediately.
  Keep a backup of the sample data.
- **Running from the wrong folder** with a relative path like `"data/expenses.csv"`.
  That's exactly why we build paths from `Path(__file__)`.

## Stretch goals

1. **Edit an expense:** option 6 lets you change one field of an existing expense.
2. **Budgets:** store a monthly budget per category in a dict and warn when
   a month's spending goes over it.
3. **Date range filter:** list only expenses between two dates.
4. **Export a report:** write the category summary to `data/summary.csv`.
5. **Monthly breakdown:** a table with one row per month and one column per category.

## Self-check

Can you explain, out loud, without looking...

- [ ] the difference between a parameter and a return value?
- [ ] why `load_expenses` converts `"64.35"` to `64.35` right away?
- [ ] what `with open(...)` does for you?
- [ ] why we use `newline=""` with the `csv` module?
- [ ] the difference between `raise` and `except`?
- [ ] why `ask()` can take `parse_amount` as an argument?
- [ ] what `if __name__ == "__main__":` protects against?
- [ ] why logic functions shouldn't call `input()` or `print()`?
- [ ] how `Path(__file__).resolve().parent.parent` finds the data folder?

## How this connects to data engineering

What you just built is a tiny pipeline: **read** raw text from a file,
**validate and convert** it into typed records, **transform** it
(group by category, filter by month), and **write** it back. Real data
pipelines do exactly this, just at a larger scale. Rejecting bad rows with a
warning instead of crashing is a *data-quality check*; separating pure logic
from input/output is what makes pipelines testable. In Project 05 pandas will
do the grouping in one line — and you'll understand what it's doing for you.
