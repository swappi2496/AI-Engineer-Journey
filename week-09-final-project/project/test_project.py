import pytest
from project import suggest_category


def test_suggest_category_groceries():
    assert suggest_category("Tesco shop") == "groceries"
    assert suggest_category("ASDA weekly") == "groceries"
    assert suggest_category("Lidl bread") == "groceries"


def test_suggest_category_transport():
    assert suggest_category("Uber ride to gym") == "transport"
    assert suggest_category("ScotRail Glasgow") == "transport"
    assert suggest_category("BP petrol") == "transport"


def test_suggest_category_case_insensitive():
    assert suggest_category("TESCO") == "groceries"
    assert suggest_category("tesco") == "groceries"
    assert suggest_category("Tesco") == "groceries"


def test_suggest_category_entertainment():
    assert suggest_category("Netflix subscription") == "entertainment"
    assert suggest_category("Spotify premium") == "entertainment"


def test_suggest_category_no_match():
    assert suggest_category("Random thing") == "other"
    assert suggest_category("xyz") == "other"


def test_suggest_category_empty():
    assert suggest_category("") == "other"
    assert suggest_category(None) == "other"


# Functions 2 and 3 tests added Tuesday and Thursday

# ============================================================
# Tests for Function 2 — plot_monthly_summary
# ============================================================

def test_plot_monthly_summary_basic():
    transactions = [
        {"type": "expense", "amount": 50.0, "category": "groceries", "date": "2026-06-15"},
        {"type": "expense", "amount": 30.0, "category": "transport", "date": "2026-06-20"},
        {"type": "expense", "amount": 20.0, "category": "groceries", "date": "2026-06-22"},
    ]
    breakdown = plot_monthly_summary(transactions, "2026-06")
    assert breakdown["groceries"] == 70.0
    assert breakdown["transport"] == 30.0


def test_plot_monthly_summary_excludes_income():
    transactions = [
        {"type": "income", "amount": 1000.0, "category": "salary", "date": "2026-06-01"},
        {"type": "expense", "amount": 50.0, "category": "groceries", "date": "2026-06-15"},
    ]
    breakdown = plot_monthly_summary(transactions, "2026-06")
    assert "salary" not in breakdown
    assert breakdown["groceries"] == 50.0


def test_plot_monthly_summary_filters_by_month():
    transactions = [
        {"type": "expense", "amount": 50.0, "category": "groceries", "date": "2026-05-15"},
        {"type": "expense", "amount": 30.0, "category": "groceries", "date": "2026-06-15"},
    ]
    breakdown = plot_monthly_summary(transactions, "2026-06")
    assert breakdown["groceries"] == 30.0
    assert len(breakdown) == 1


def test_plot_monthly_summary_empty():
    assert plot_monthly_summary([], "2026-06") == {}


def test_plot_monthly_summary_no_match_month():
    transactions = [
        {"type": "expense", "amount": 50.0, "category": "groceries", "date": "2026-05-15"},
    ]
    assert plot_monthly_summary(transactions, "2026-06") == {}


# ============================================================
# Tests for Function 3 — top_categories
# ============================================================

def test_top_categories_basic():
    transactions = [
        {"type": "expense", "amount": 100.0, "category": "groceries", "date": "2026-06-15"},
        {"type": "expense", "amount": 50.0, "category": "transport", "date": "2026-06-20"},
        {"type": "expense", "amount": 200.0, "category": "rent", "date": "2026-06-01"},
    ]
    top = top_categories(transactions, n=3)
    assert top == [("rent", 200.0), ("groceries", 100.0), ("transport", 50.0)]


def test_top_categories_aggregates_same_category():
    transactions = [
        {"type": "expense", "amount": 30.0, "category": "groceries", "date": "2026-06-15"},
        {"type": "expense", "amount": 70.0, "category": "groceries", "date": "2026-06-20"},
        {"type": "expense", "amount": 50.0, "category": "transport", "date": "2026-06-22"},
    ]
    top = top_categories(transactions, n=2)
    assert top == [("groceries", 100.0), ("transport", 50.0)]


def test_top_categories_n_limit():
    transactions = [
        {"type": "expense", "amount": 100.0, "category": "a", "date": "2026-06-15"},
        {"type": "expense", "amount": 50.0, "category": "b", "date": "2026-06-20"},
        {"type": "expense", "amount": 30.0, "category": "c", "date": "2026-06-22"},
        {"type": "expense", "amount": 20.0, "category": "d", "date": "2026-06-25"},
    ]
    top = top_categories(transactions, n=2)
    assert len(top) == 2
    assert top[0] == ("a", 100.0)
    assert top[1] == ("b", 50.0)


def test_top_categories_excludes_income():
    transactions = [
        {"type": "income", "amount": 1000.0, "category": "salary", "date": "2026-06-01"},
        {"type": "expense", "amount": 50.0, "category": "groceries", "date": "2026-06-15"},
    ]
    top = top_categories(transactions, n=3)
    assert top == [("groceries", 50.0)]


def test_top_categories_empty():
    assert top_categories([]) == []


def test_top_categories_fewer_than_n():
    transactions = [
        {"type": "expense", "amount": 100.0, "category": "groceries", "date": "2026-06-15"},
    ]
    top = top_categories(transactions, n=5)
    assert top == [("groceries", 100.0)]
    assert len(top) == 1


def test_top_categories_default_n_is_3():
    transactions = [
        {"type": "expense", "amount": 50.0, "category": f"cat_{i}", "date": "2026-06-15"}
        for i in range(10)
    ]
    top = top_categories(transactions)  # no n argument — should default to 3
    assert len(top) == 3