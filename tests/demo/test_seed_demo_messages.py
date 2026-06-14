"""Tests for the seed_demo_messages management command."""

import pytest
from django.core.management import call_command

from inject_message.models import Message, MessageInjection


@pytest.mark.django_db
def test_seed_demo_messages_creates_demo_data():
    call_command("seed_demo_messages", "--clear")

    assert Message.objects.filter(label__startswith="demo:").count() == 4
    assert MessageInjection.objects.filter(message__label__startswith="demo:").count() == 6


@pytest.mark.django_db
def test_seed_demo_messages_is_idempotent():
    call_command("seed_demo_messages", "--clear")
    call_command("seed_demo_messages")

    assert Message.objects.filter(label__startswith="demo:").count() == 4
    assert MessageInjection.objects.filter(message__label__startswith="demo:").count() == 6
