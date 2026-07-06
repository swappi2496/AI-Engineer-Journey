import json
import os
import re
from datetime import date

# ============================================================
# DATA PERSISTENCE (carried from v1)
# ============================================================

def load_transactions(filename = "transactions.json"):
    if not os.path.exists(filename):
        return []
    try:
        with open(filename) as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []
    
def save_transactions(transactions, filename = "transaction.json"):
    with open(filename, "w") as f:
        json.dump(transactions, f, indent = 2)

# ============================================================
# CUSTOM FUNCTION 1 — Auto-suggest category from description
# ============================================================

CATEGORY_KEYWORDS = {
    "groceries": ["tesco", "asda", "sainsburys", "morrisons", "lidl", "aldi", "co-op", "waitrose"],
    "transport": ["uber", "scotrail", "first bus", "train", "petrol", "fuel", "bp", "shell"],
    "rent": ["rent", "landlord", "letting"],
    "utilities": ["british gas", "scottish power", "edf", "ovo", "council tax", "water"],
    "internet": ["bt", "virgin media", "sky", "vodafone", "ee", "o2", "three"],
    "eating_out": ["mcdonalds", "kfc", "subway", "greggs", "domino", "deliveroo", "uber eats", "just eat"],
    "entertainment": ["netflix", "spotify", "youtube", "cinema", "vue", "odeon"],
    "fitness": ["pure gym", "gym", "fitness", "decathlon"],
    "shopping": ["amazon", "primark", "h&m", "zara", "ebay"],
    "income": ["salary", "wage", "freelance", "refund", "interest"],
}

def suggest_category(description):
    """Suggest a transaction category based on keywords in the description.
    
    Returns the matched category name (lowercase) or 'other' if no match.
    """
    if not description:
        return "other"
    desc_lower = description.lower()

    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in desc_lower:
                return category
            
    return "other"

# ============================================================
# CUSTOM FUNCTION 2 — plot_monthly_summary
# ============================================================

def plot_monthly_summary(transactions, year_month, output_file = "monthly_summary.png"):
    """Compute and plot expense breakdown by category for a given month.
    Args:
        transactions: list of transaction dicts (each with type, amount, category, date)
        year_month: string in 'YYYY-MM' format (e.g., '2026-06')
        output_file: filename for the saved bar chart PNG
    Returns:
        dict of {category: total_amount} for that month's expenses
    """
    import matplotlib.pyplot as plt

    # filter to expense in the specified month
    monthly_expense = [
        t for t in transactions
        if t["type"] == "expense" and t["date"].startswith(year_month)
    ]

    #Aggregate by category
    breakdown = {}
    for t in monthly_expense:
        cat = t["category"]
        breakdown[cat] = breakdown.get(cat, 0) + t["amount"]

    #plot if data exists
    if breakdown:

        #sort by amount descending for visual calrity
        sorted_items = sorted(breakdown.items(), key = lambda x:x[1], reverse = True)
        categories = [item[0] for item in sorted_items]
        amounts = [item[1] for item in sorted_items]

        plt.figure(figsize = (10, 6))
        plt.bar(categories, amounts, color = "steelblue", edgecolor = "navy")
        plt.xlabel("Category")
        plt.ylabel("Amount (£)")
        plt.title(f"Expense Breakdown - {year_month}")
        plt.xticks(rotation = 45, ha = "right")

        #Add value_lable on top of each bar
        for i, amount in enumerate(amounts):
            plt.text(i, amount + max(amounts) + 0.01, f"£{amount:.2f}", ha = "center", va = "bottom", fontsize = 9)

        plt.tight_layout()
        plt.savefig(output_file, dpi = 100)
        plt.close()

    return breakdown


# ============================================================
# CUSTOM FUNCTION 3 — top_categories
# ============================================================

def top_categories(transactions, n =3):
    """Return the top N spending categories sorted by total spent.
    Args:
        transactions: lost of transactions dicts
        n: number of top categories to return (default 3)
        
    Returns:
        list of tuples [(category, total_amount), ...] sorted decending by amount
        Returns fewer than N if there aren't that many expense categories.
        """
    #Aggregate expense by category (ignnore income)
    totals = {}
    for t in transactions:
        if t["type"] == "expense":
            cat = t["category"]
            totals[cat] = totals.get(cat, 0) + t["amount"]

    #sort categories by total amount descending
    sorted_categories = sorted(totals.items(), key = lambda x:x[1], reverse=True)

    #return top N
    return sorted_categories[:n]