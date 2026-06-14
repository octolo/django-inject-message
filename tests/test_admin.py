"""Tests for Django admin registration."""

import pytest
from django.contrib.admin.sites import site

from inject_message.models import Message, MessageInjection


@pytest.mark.django_db
def test_message_admin_is_registered():
    assert site.is_registered(Message)


@pytest.mark.django_db
def test_message_injection_admin_is_registered():
    assert site.is_registered(MessageInjection)
