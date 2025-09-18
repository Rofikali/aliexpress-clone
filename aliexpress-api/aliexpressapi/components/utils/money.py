# components/utils/money.py
from decimal import Decimal

SYMBOLS = {
    "USD": "$",
    "NPR": "Rs",
    "EUR": "€",
    "GBP": "£",
    "INR": "₹",
}


def format_money(amount, currency="USD"):
    try:
        amt = Decimal(amount)
    except Exception:
        # fallback if amount is already a float/str
        try:
            amt = Decimal(str(amount))
        except Exception:
            return f"{currency} {amount}"
    symbol = SYMBOLS.get(currency.upper(), currency.upper() + " ")
    return f"{symbol}{amt:,.2f}"
