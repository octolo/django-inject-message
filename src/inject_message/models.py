"""Models for inject_message."""

from __future__ import annotations

from datetime import datetime

from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.html import format_html
from django.utils.safestring import SafeString
from django.utils.translation import gettext_lazy as _

from .audit import AuditLogMixin
from .scheduling import matches_cron_schedule, validate_cron_schedule


class MessageLevel(models.TextChoices):
    """Severity levels for injected messages."""

    DEBUG = "debug", _("Debug")
    INFO = "info", _("Info")
    SUCCESS = "success", _("Success")
    WARNING = "warning", _("Warning")
    ERROR = "error", _("Error")


class Message(AuditLogMixin, models.Model):
    """Content to inject into HTTP responses."""

    label = models.CharField(
        max_length=255,
        blank=True,
        help_text=_("Optional name to identify this message in the admin."),
    )
    content = models.TextField(
        help_text=_("HTML or text injected into matching responses."),
    )
    level = models.CharField(
        max_length=20,
        choices=MessageLevel.choices,
        default=MessageLevel.INFO,
        help_text=_("Visual severity level applied when the message is rendered."),
    )
    is_active = models.BooleanField(
        default=True,
        help_text=_("Inactive messages are ignored during injection."),
    )
    active_from = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("Optional start date and time when the message becomes injectable."),
    )
    active_until = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("Optional end date and time after which the message is no longer injectable."),
    )
    schedule = models.CharField(
        max_length=100,
        blank=True,
        help_text=_(
            "Optional cron expression (minute hour day month weekday). "
            "Leave empty to ignore schedule. Examples: "
            "'* * * * 0,6' for weekends, '* * * * 1-5' for weekdays, "
            "'0 9-17 * * 1-5' for business hours."
        ),
    )

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
        ordering = ["-pk"]
        constraints = [
            models.CheckConstraint(
                condition=Q(active_until__isnull=True)
                | Q(active_from__isnull=True)
                | Q(active_until__gte=models.F("active_from")),
                name="inject_message_active_until_after_active_from",
            ),
        ]

    def __str__(self) -> str:
        if self.label:
            return self.label
        preview = self.content[:50].replace("\n", " ")
        return preview + ("…" if len(self.content) > 50 else "")

    def clean(self) -> None:
        validate_cron_schedule(self.schedule)

    def is_currently_active(self, at: datetime | None = None) -> bool:
        """Return True when the message is enabled for the given moment."""
        if not self.is_active:
            return False
        moment = at or timezone.now()
        if self.active_from and moment < self.active_from:
            return False
        if self.active_until and moment > self.active_until:
            return False
        if not matches_cron_schedule(self.schedule, moment):
            return False
        return True

    def render_html(self) -> SafeString:
        """Return message content wrapped with level-specific CSS classes."""
        return format_html(
            '<div class="inject-message inject-message--{}" data-level="{}" role="alert">{}</div>',
            self.level,
            self.level,
            self.content,
        )


class MessageInjection(AuditLogMixin, models.Model):
    """Placement rule: where and after which anchor a message is injected."""

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name="injections",
        verbose_name=_("Message"),
    )
    url_pattern = models.CharField(
        max_length=500,
        help_text=_(
            "URL path pattern where this message may be injected "
            "(e.g. /dashboard/ or ^/admin/products/)."
        ),
    )
    after_sequence = models.CharField(
        max_length=500,
        help_text=_(
            "Character sequence after which the message content is inserted "
            "in the response body."
        ),
    )
    is_active = models.BooleanField(
        default=True,
        help_text=_("Inactive rules are ignored during injection."),
    )
    priority = models.PositiveSmallIntegerField(
        default=0,
        help_text=_("Higher values are evaluated first when multiple rules match."),
    )

    class Meta:
        verbose_name = _("Message injection")
        verbose_name_plural = _("Message injections")
        ordering = ["-priority", "url_pattern"]

    def __str__(self) -> str:
        return f"{self.message} → {self.url_pattern} (after {self.after_sequence!r})"
