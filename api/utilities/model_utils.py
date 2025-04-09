from datetime import timedelta, datetime, time


def next_sunday_noon():
    today = datetime.today()
    days_ahead = 6 - today.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    next_sunday = today + timedelta(days=days_ahead)
    return datetime.combine(next_sunday.date(), time(12, 0))

def next_sunday_14_30():
    today = datetime.today()
    days_ahead = 6 - today.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    next_sunday = today + timedelta(days=days_ahead)
    return datetime.combine(next_sunday.date(), time(14, 30))

