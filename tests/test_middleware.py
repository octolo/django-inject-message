"""Tests for InjectMessageMiddleware using demo pages."""

from datetime import timedelta

import pytest
from django.test import Client
from django.utils import timezone

from inject_message.models import Message, MessageInjection, MessageLevel


@pytest.mark.django_db
def test_injects_single_message():
    message = Message.objects.create(content="Single banner", level=MessageLevel.INFO)
    MessageInjection.objects.create(
        message=message,
        url_pattern="/demo/single/",
        after_sequence="<body>",
    )

    content = Client().get("/demo/single/").content.decode()

    assert content.count("Single banner") == 1
    assert 'inject-message--info' in content
    assert "inject_message/inject_message.css" in content


@pytest.mark.django_db
def test_injects_multiple_messages():
    first = Message.objects.create(content="First alert", level=MessageLevel.WARNING)
    second = Message.objects.create(content="Second alert", level=MessageLevel.ERROR)
    MessageInjection.objects.create(
        message=first,
        url_pattern="/demo/multiple/",
        after_sequence="<body>",
        priority=2,
    )
    MessageInjection.objects.create(
        message=second,
        url_pattern="/demo/multiple/",
        after_sequence="<body>",
        priority=1,
    )

    content = Client().get("/demo/multiple/").content.decode()

    assert "First alert" in content
    assert "Second alert" in content
    assert content.count('role="alert"') == 2


@pytest.mark.django_db
def test_injects_one_message_in_multiple_places():
    message = Message.objects.create(content="Repeated banner", level=MessageLevel.SUCCESS)
    MessageInjection.objects.create(
        message=message,
        url_pattern="/demo/multiple-places/",
        after_sequence="</header>",
    )
    MessageInjection.objects.create(
        message=message,
        url_pattern="/demo/multiple-places/",
        after_sequence="</main>",
    )
    MessageInjection.objects.create(
        message=message,
        url_pattern="/demo/multiple-places/",
        after_sequence="</footer>",
    )

    content = Client().get("/demo/multiple-places/").content.decode()

    assert content.count("Repeated banner") == 3
    assert content.count('inject-message--success') == 3
    assert content.index("</header>") < content.index("Repeated banner")
    assert content.index("</main>") < content.rindex("Repeated banner")


@pytest.mark.django_db
def test_middleware_ignores_non_matching_url():
    message = Message.objects.create(content="Should not appear", level=MessageLevel.INFO)
    MessageInjection.objects.create(
        message=message,
        url_pattern="/demo/other/",
        after_sequence="<body>",
    )

    response = Client().get("/demo/single/")

    assert b"Should not appear" not in response.content


@pytest.mark.django_db
def test_middleware_ignores_inactive_rules():
    message = Message.objects.create(content="Inactive", level=MessageLevel.INFO, is_active=False)
    MessageInjection.objects.create(
        message=message,
        url_pattern="/demo/single/",
        after_sequence="<body>",
    )

    response = Client().get("/demo/single/")

    assert b"Inactive" not in response.content


@pytest.mark.django_db
def test_middleware_ignores_message_outside_active_period():
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

    response = Client().get("/demo/single/")

    assert b"Expired banner" not in response.content
