import re
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta

WEEKDAYS = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}
QUARTER_START_MONTHS = (1, 4, 7, 10)


def get_nth_weekday(year, month, n, weekday):
    first_day_of_month = datetime(year, month, 1)
    first_occurrence = first_day_of_month + timedelta(days=(weekday - first_day_of_month.weekday()) % 7)
    return first_occurrence + timedelta(weeks=n - 1)


def is_today_nth_weekday(n, weekday, today):
    return today.date() == get_nth_weekday(today.year, today.month, n, weekday).date()


def get_next_month_nth_weekday(n, weekday, today):
    next_month = today.month % 12 + 1
    next_year = today.year + (today.month // 12)
    return get_nth_weekday(next_year, next_month, n, weekday)


def _next_quarter_start_after(today):
    for month in QUARTER_START_MONTHS:
        candidate = datetime(today.year, month, 1)
        if candidate.date() > today.date():
            return candidate
    return datetime(today.year + 1, QUARTER_START_MONTHS[0], 1)


def compute_next_action(action_interval, today=None):
    """
    Given a strategy's `action_interval` rule (as stored in the `strategies`
    table, e.g. "1st Monday of Every Month"), return the next date - strictly
    after `today` - on which this strategy needs action. Always returns a
    date for a recognised rule (regardless of whether today happens to be a
    trigger day), so every strategy's `next_action_date` stays current on
    every run. Returns None only if `action_interval` is empty or doesn't
    match any known pattern.

    Adding a new strategy that reuses one of the interval phrases below only
    requires a new row in the `strategies` table - no code change needed.
    """
    if not action_interval:
        return None

    today = today or datetime.now()
    text = action_interval.strip().lower()

    # "End of Day" -> action every day, next one is tomorrow
    if "end of day" in text:
        return (today + timedelta(days=1)).date()

    # "1st and 3rd Monday of the Month" (any weekday pair)
    match = re.search(
        r"(\d+)\w*\s+and\s+(\d+)\w*\s+(" + "|".join(WEEKDAYS) + r")",
        text,
    )
    if match:
        n1, n2 = sorted((int(match.group(1)), int(match.group(2))))
        weekday = WEEKDAYS[match.group(3)]
        candidates = [
            get_nth_weekday(today.year, today.month, n1, weekday),
            get_nth_weekday(today.year, today.month, n2, weekday),
            get_next_month_nth_weekday(n1, weekday, today),
            get_next_month_nth_weekday(n2, weekday, today),
        ]
        future = [c for c in candidates if c.date() > today.date()]
        return min(future).date()

    # "Every Monday" / "Every Friday of the Month" -> weekly trigger
    match = re.search(r"every\s+(" + "|".join(WEEKDAYS) + r")", text)
    if match:
        weekday = WEEKDAYS[match.group(1)]
        days_ahead = (weekday - today.weekday()) % 7
        if days_ahead == 0:
            days_ahead = 7
        return (today + timedelta(days=days_ahead)).date()

    # "2nd Monday of Every Month" (single nth weekday)
    match = re.search(
        r"(\d+)\w*\s+(" + "|".join(WEEKDAYS) + r")\s+of\s+every\s+month",
        text,
    )
    if match:
        n = int(match.group(1))
        weekday = WEEKDAYS[match.group(2)]
        candidate = get_nth_weekday(today.year, today.month, n, weekday)
        if candidate.date() <= today.date():
            candidate = get_next_month_nth_weekday(n, weekday, today)
        return candidate.date()

    # "1st of Every Quarter"
    if "quarter" in text:
        return _next_quarter_start_after(today).date()

    # "15th of Month" / "1st of Month" (also tolerates the "Momth" typo)
    match = re.search(r"(\d+)\w*\s+of\s+\w*mo\w*th", text)
    if match:
        n = int(match.group(1))
        candidate = today.replace(day=n)
        if candidate.date() <= today.date():
            candidate = candidate + relativedelta(months=1)
        return candidate.date()

    return None
