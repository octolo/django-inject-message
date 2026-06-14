"""Cron schedule helpers for inject_message."""

from __future__ import annotations

from datetime import datetime

from croniter import croniter
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Standard 5-field cron: minute hour day month day_of_week
# day_of_week: 0=Sunday, 6=Saturday
SCHEDULE_WEEKENDS = "* * * * 0,6"
SCHEDULE_WEEKDAYS = "* * * * 1-5"
SCHEDULE_BUSINESS_HOURS = "0 9-17 * * 1-5"


def validate_cron_schedule(schedule: str) -> None:
    """Raise ValidationError when *schedule* is not a valid cron expression."""
    if not schedule:
        return
    try:
        croniter(schedule)
    except (ValueError, KeyError) as exc:
        raise ValidationError(_("Invalid cron expression: %(error)s") % {"error": exc}) from exc


def matches_cron_schedule(schedule: str, at: datetime) -> bool:
    """Return True when *at* matches the cron *schedule*."""
    if not schedule:
        return True
    return croniter.match(schedule, at)
