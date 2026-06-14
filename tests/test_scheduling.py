"""Tests for cron schedule helpers."""

from datetime import datetime

import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone

from inject_message.scheduling import (
    SCHEDULE_WEEKDAYS,
    SCHEDULE_WEEKENDS,
    matches_cron_schedule,
    validate_cron_schedule,
)


def test_validate_cron_schedule_accepts_valid_expression():
    validate_cron_schedule(SCHEDULE_WEEKENDS)


def test_validate_cron_schedule_rejects_invalid_expression():
    with pytest.raises(ValidationError):
        validate_cron_schedule("not a cron")


def test_matches_cron_schedule_weekends():
    saturday = timezone.make_aware(datetime(2026, 6, 13, 12, 0))
    monday = timezone.make_aware(datetime(2026, 6, 15, 12, 0))

    assert matches_cron_schedule(SCHEDULE_WEEKENDS, saturday) is True
    assert matches_cron_schedule(SCHEDULE_WEEKENDS, monday) is False


def test_matches_cron_schedule_weekdays():
    saturday = timezone.make_aware(datetime(2026, 6, 13, 12, 0))
    monday = timezone.make_aware(datetime(2026, 6, 15, 12, 0))

    assert matches_cron_schedule(SCHEDULE_WEEKDAYS, monday) is True
    assert matches_cron_schedule(SCHEDULE_WEEKDAYS, saturday) is False


def test_matches_cron_schedule_empty_means_always():
    moment = timezone.now()

    assert matches_cron_schedule("", moment) is True
