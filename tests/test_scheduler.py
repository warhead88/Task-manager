from datetime import datetime
from src.utils import calculate_initial_remind_time, get_next_recurrence_time


def test_initial_remind_time_same_day():
    # It is 10:00 UTC. User timezone is +3 (Moscow). Local time is 13:00.
    # User sets reminder for 15:30 local time.
    # Local time 15:30 -> UTC 12:30.
    now_utc = datetime(2026, 1, 1, 10, 0, 0)

    remind_at = calculate_initial_remind_time(
        now_utc=now_utc,
        h=15,
        m=30,
        tz_offset=3,
        recurrence="none"
    )

    # Needs to be today at 12:30 UTC.
    assert remind_at == datetime(2026, 1, 1, 12, 30, 0)


def test_initial_remind_time_next_day():
    # It is 10:00 UTC. User timezone is +3 (Moscow). Local time is 13:00.
    # User sets reminder for 12:00 local time (which already passed today).
    # Local time 12:00 -> UTC 09:00.
    # So it should be scheduled for tomorrow 09:00 UTC.
    now_utc = datetime(2026, 1, 1, 10, 0, 0)

    remind_at = calculate_initial_remind_time(
        now_utc=now_utc,
        h=12,
        m=0,
        tz_offset=3,
        recurrence="none"
    )

    # Needs to be tomorrow at 09:00 UTC.
    assert remind_at == datetime(2026, 1, 2, 9, 0, 0)


def test_initial_remind_time_negative_timezone():
    # It is 02:00 UTC on Jan 2nd. User timezone is -5 (NY).
    # Local time is 21:00 on Jan 1st.
    # User sets reminder for 22:30 local time.
    # Local time 22:30 -> UTC 03:30 (next day from user perspective).
    now_utc = datetime(2026, 1, 2, 2, 0, 0)

    remind_at = calculate_initial_remind_time(
        now_utc=now_utc,
        h=22,
        m=30,
        tz_offset=-5,
        recurrence="none"
    )

    assert remind_at == datetime(2026, 1, 2, 3, 30, 0)


def test_initial_remind_time_weekdays():
    # It is Friday 10:00 UTC. Target is today 15:00 UTC.
    now_utc = datetime(2026, 1, 2, 10, 0, 0)  # Jan 2 2026 is Friday
    remind_at = calculate_initial_remind_time(now_utc, 15, 0, 0, "weekdays")
    assert remind_at == datetime(2026, 1, 2, 15, 0, 0)

    # It is Friday 20:00 UTC. Target is yesterday's 15:00 UTC.
    # So next should be next Monday!
    now_utc2 = datetime(2026, 1, 2, 20, 0, 0)
    remind_at2 = calculate_initial_remind_time(now_utc2, 15, 0, 0, "weekdays")
    assert remind_at2 == datetime(2026, 1, 5, 15, 0, 0)


def test_next_recurrence_daily():
    current_remind_at = datetime(2026, 1, 1, 15, 0, 0)
    now_utc = datetime(2026, 1, 1, 15, 5, 0)  # Just after it fired

    next_remind = get_next_recurrence_time(current_remind_at, "daily", now_utc)
    assert next_remind == datetime(2026, 1, 2, 15, 0, 0)


def test_next_recurrence_weekends():
    # Current remind is Sunday (Jan 4) 15:00.
    current_remind_at = datetime(2026, 1, 4, 15, 0, 0)
    now_utc = datetime(2026, 1, 4, 15, 5, 0)

    # Should skip Mon-Fri and schedule for Saturday (Jan 10).
    next_remind = get_next_recurrence_time(current_remind_at, "weekends", now_utc)
    assert next_remind == datetime(2026, 1, 10, 15, 0, 0)
