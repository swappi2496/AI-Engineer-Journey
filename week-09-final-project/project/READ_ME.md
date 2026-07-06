# Personal Finance Tracker v2

#### Video Demo: [YouTube URL — added Sat 4 Jul]
#### Description:

A CLI Python application to track personal finances with auto-categorization of transactions, monthly visualization, and spending analysis. This is v2 of my Week 2 CS50P project, extended with classification logic, matplotlib charting, and reporting.

## Features

- Add income/expense transactions with auto-categorized suggestions
- View running balance and monthly summaries  
- Filter transactions by category
- Plot monthly expense breakdown as a bar chart
- Top spending categories report
- JSON persistence between runs

## Files

- `project.py` — Main file with menu loop and custom functions
- `test_project.py` — pytest tests for the custom functions
- `requirements.txt` — Required pip packages
- `transactions.json` — Auto-generated data file

## Design Decisions

[Section to write Fri 3 Jul — explain why you used regex over ML for categorization, why JSON over SQLite, etc.]

## How to Run

```bash
pip install -r requirements.txt
python project.py
```

## Custom Functions

### `suggest_category(description)`
[Explain what it does and why]

### `plot_monthly_summary(transactions, year_month)`
[To document Tuesday]

### `top_categories(transactions, n=3)`
[To document Thursday]

## Future Improvements

[Ideas for v3 — ML-based categorization, web UI, multi-currency support, etc.]