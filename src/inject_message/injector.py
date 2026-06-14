"""HTML injection helpers for inject_message."""

from __future__ import annotations

import re
from collections.abc import Iterable
from datetime import datetime

from django.db.models import Q
from django.templatetags.static import static
from django.utils import timezone

from .models import MessageInjection

STYLESHEET_PATH = "inject_message/inject_message.css"


def url_matches(pattern: str, path: str) -> bool:
    """Return True when *path* matches *pattern* (regex or prefix)."""
    if pattern.startswith("^"):
        return re.search(pattern, path) is not None
    return path.startswith(pattern)


def get_matching_injections(path: str, at: datetime | None = None) -> list[MessageInjection]:
    """Return active injection rules matching *path*, ordered by priority."""
    moment = at or timezone.now()
    injections = MessageInjection.objects.filter(
        is_active=True,
        message__is_active=True,
    ).filter(
        Q(message__active_from__isnull=True) | Q(message__active_from__lte=moment),
    ).filter(
        Q(message__active_until__isnull=True) | Q(message__active_until__gte=moment),
    ).select_related("message")
    return [
        injection
        for injection in injections.order_by("-priority", "pk")
        if url_matches(injection.url_pattern, path)
        and injection.message.is_currently_active(at=moment)
    ]


def inject_messages(content: str, injections: Iterable[MessageInjection]) -> tuple[str, bool]:
    """Insert rendered messages after each rule's anchor sequence."""
    modified = False
    for injection in injections:
        anchor = injection.after_sequence
        index = content.find(anchor)
        if index == -1:
            continue
        insert_at = index + len(anchor)
        content = content[:insert_at] + str(injection.message.render_html()) + content[insert_at:]
        modified = True
    return content, modified


def inject_stylesheet(content: str, css_url: str | None = None) -> str:
    """Insert the inject_message stylesheet link before </head>."""
    href = css_url or static(STYLESHEET_PATH)
    if STYLESHEET_PATH in content:
        return content
    link = f'<link rel="stylesheet" href="{href}">'
    head_close = content.lower().find("</head>")
    if head_close != -1:
        return content[:head_close] + link + content[head_close:]
    return link + content
