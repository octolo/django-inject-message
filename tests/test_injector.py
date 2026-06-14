"""Tests for inject_message injector helpers."""

from datetime import datetime, timedelta

import pytest
from django.utils import timezone

from inject_message.injector import get_matching_injections, inject_messages, inject_stylesheet, url_matches
from inject_message.models import Message, MessageInjection, MessageLevel


@pytest.mark.parametrize(
    ("pattern", "path", "expected"),
    [
        ("/test-page/", "/test-page/", True),
        ("/test-page/", "/test-page/extra/", True),
        ("/test-page/", "/other/", False),
        ("^/admin/", "/admin/users/", True),
        ("^/admin/", "/public/admin/", False),
    ],
)
def test_url_matches(pattern, path, expected):
    assert url_matches(pattern, path) is expected


@pytest.mark.django_db
def test_inject_messages_inserts_after_anchor():
    message = Message.objects.create(content="Promo banner", level=MessageLevel.WARNING)
    injection = MessageInjection.objects.create(
        message=message,
        url_pattern="/ignored-in-this-test/",
        after_sequence="<body>",
    )
    html = "<html><body><main></main></body></html>"

    result, modified = inject_messages(html, [injection])

    assert modified is True
    assert "Promo banner" in result
    assert 'inject-message--warning' in result
    assert result.index("<body>") < result.index("Promo banner") < result.index("<main>")


@pytest.mark.django_db
def test_inject_messages_skips_missing_anchor():
    message = Message.objects.create(content="Hidden", level=MessageLevel.INFO)
    injection = MessageInjection.objects.create(
        message=message,
        url_pattern="/",
        after_sequence="<missing>",
    )

    html = "<html><body></body></html>"
    result, modified = inject_messages(html, [injection])

    assert modified is False
    assert result == html


def test_inject_stylesheet_before_head_close():
    html = "<html><head><title>Test</title></head><body></body></html>"

    result = inject_stylesheet(html, "/static/inject_message/inject_message.css")

    assert 'href="/static/inject_message/inject_message.css"' in result
    assert result.index("</head>") > result.index("inject_message.css")


def test_inject_stylesheet_is_idempotent():
    html = (
        '<html><head><link rel="stylesheet" '
        'href="/static/inject_message/inject_message.css"></head><body></body></html>'
    )

    result = inject_stylesheet(html, "/static/inject_message/inject_message.css")

    assert result.count("inject_message.css") == 1


@pytest.mark.django_db
def test_get_matching_injections_respects_active_period():
    now = timezone.now()
    message = Message.objects.create(
        content="Scheduled banner",
        level=MessageLevel.INFO,
        active_from=now - timedelta(hours=1),
        active_until=now + timedelta(hours=1),
    )
    injection = MessageInjection.objects.create(
        message=message,
        url_pattern="/demo/single/",
        after_sequence="<body>",
    )

    assert get_matching_injections("/demo/single/", at=now) == [injection]


@pytest.mark.django_db
def test_get_matching_injections_excludes_future_messages():
    now = timezone.now()
    message = Message.objects.create(
        content="Future banner",
        level=MessageLevel.INFO,
        active_from=now + timedelta(days=1),
    )
    MessageInjection.objects.create(
        message=message,
        url_pattern="/demo/single/",
        after_sequence="<body>",
    )

    assert get_matching_injections("/demo/single/", at=now) == []


@pytest.mark.django_db
def test_get_matching_injections_excludes_expired_messages():
    now = timezone.now()
    message = Message.objects.create(
        content="Expired banner",
        level=MessageLevel.INFO,
        active_until=now - timedelta(minutes=1),
    )
    MessageInjection.objects.create(
        message=message,
        url_pattern="/demo/single/",
        after_sequence="<body>",
    )

    assert get_matching_injections("/demo/single/", at=now) == []


@pytest.mark.django_db
def test_get_matching_injections_respects_weekend_schedule():
    saturday = timezone.make_aware(datetime(2026, 6, 13, 12, 0))
    monday = timezone.make_aware(datetime(2026, 6, 15, 12, 0))
    message = Message.objects.create(
        content="Weekend banner",
        level=MessageLevel.INFO,
        schedule="* * * * 0,6",
    )
    injection = MessageInjection.objects.create(
        message=message,
        url_pattern="/demo/single/",
        after_sequence="<body>",
    )

    assert get_matching_injections("/demo/single/", at=saturday) == [injection]
    assert get_matching_injections("/demo/single/", at=monday) == []
