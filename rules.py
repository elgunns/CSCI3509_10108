from fines import days_late, fine_for_days

# How many loans at once each kind of member may have.
LOAN_LIMITS = {"student": 3, "staff": 5}
DEFAULT_LOAN_LIMIT = 3


def loan_limit(member_type):
    return LOAN_LIMITS.get(member_type, DEFAULT_LOAN_LIMIT)


def balance(loan_rows):
    """Return (amount owed, number of loans still out) for one member's loans.

    Owed = fines on overdue loans still out + unpaid fines on returned loans.
    """
    owed = 0
    open_loans = 0
    for loan in loan_rows:
        if loan[4] == 0:
            open_loans += 1
            owed += fine_for_days(days_late(loan[3]))
        elif loan[6] == 0:
            owed += loan[5]
    return owed, open_loans
