from datetime import date

# The single place where the fine rate is defined.
DAILY_FINE = 0.50


def days_late(due_date, today=None):
    """Days past the due date (an ISO date string). Negative if not due yet."""
    today = today or date.today()
    return (today - date.fromisoformat(due_date)).days


def fine_for_days(days):
    """Fine for a number of days late. Never negative."""
    return max(0, days) * DAILY_FINE


def money(x):
    return round(float(x), 2)
