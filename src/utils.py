from datetime import datetime, time, timedelta


def calculate_initial_remind_time(now_utc: datetime, h: int, m: int, tz_offset: int, recurrence: str) -> datetime:
    # Convert local time to UTC
    target_utc_time = (datetime.combine(now_utc.date(), time(h, m)) - timedelta(hours=tz_offset)).time()

    remind_at = datetime.combine(now_utc.date(), target_utc_time)

    if remind_at <= now_utc:
        remind_at += timedelta(days=1)

    while True:
        if recurrence == "weekdays" and remind_at.weekday() >= 5:
            remind_at += timedelta(days=1)
        elif recurrence == "weekends" and remind_at.weekday() < 5:
            remind_at += timedelta(days=1)
        else:
            break

    return remind_at


def get_next_recurrence_time(current_remind_at: datetime, recurrence: str, now_utc: datetime) -> datetime | None:
    if recurrence == "none":
        return None

    next_remind = current_remind_at
    while True:
        if recurrence == "daily":
            next_remind += timedelta(days=1)
        elif recurrence == "weekdays":
            next_remind += timedelta(days=1)
            if next_remind.weekday() >= 5:
                continue
        elif recurrence == "weekends":
            next_remind += timedelta(days=1)
            if next_remind.weekday() < 5:
                continue
        elif recurrence == "weekly":
            next_remind += timedelta(days=7)

        # Stop if next_remind is in the future
        if next_remind > now_utc:
            break

    return next_remind
