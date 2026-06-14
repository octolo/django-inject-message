"""Django admin for inject_message."""

from __future__ import annotations

from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from inject_message.models import Message, MessageInjection
from inject_message.scheduling import (
    SCHEDULE_BUSINESS_HOURS,
    SCHEDULE_WEEKDAYS,
    SCHEDULE_WEEKENDS,
    validate_cron_schedule,
)

AUDIT_READONLY_FIELDS = ("created_by", "updated_by")
SCHEDULE_PRESETS = (
    ("", _("No schedule (always active within dates)")),
    (SCHEDULE_WEEKENDS, _("Weekends (Sat–Sun)")),
    (SCHEDULE_WEEKDAYS, _("Weekdays (Mon–Fri)")),
    (SCHEDULE_BUSINESS_HOURS, _("Business hours (Mon–Fri, 9am–5pm)")),
)


class MessageAdminForm(forms.ModelForm):
    """Admin form with cron validation and schedule presets."""

    schedule_preset = forms.ChoiceField(
        choices=SCHEDULE_PRESETS,
        required=False,
        label=_("Schedule preset"),
        help_text=_("Optional shortcut. Choosing a preset fills the cron expression below."),
    )

    class Meta:
        model = Message
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.schedule in dict(SCHEDULE_PRESETS):
            self.fields["schedule_preset"].initial = self.instance.schedule

    def clean_schedule(self) -> str:
        schedule = self.cleaned_data.get("schedule", "")
        validate_cron_schedule(schedule)
        return schedule

    def clean(self):
        cleaned_data = super().clean()
        preset = cleaned_data.get("schedule_preset")
        if preset:
            cleaned_data["schedule"] = preset
        return cleaned_data


class MessageInjectionInline(admin.TabularInline):
    model = MessageInjection
    extra = 1
    fields = ("url_pattern", "after_sequence", "priority", "is_active", "created_by", "updated_by")
    readonly_fields = AUDIT_READONLY_FIELDS


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    form = MessageAdminForm
    inlines = (MessageInjectionInline,)
    list_display = ("label", "level_badge", "is_active", "schedule", "injection_count", "updated_by")
    list_filter = ("is_active", "level")
    search_fields = ("label", "content", "schedule")
    readonly_fields = ("preview", *AUDIT_READONLY_FIELDS)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "label",
                    "content",
                    "level",
                    "is_active",
                    "preview",
                ),
            },
        ),
        (
            _("Activity"),
            {
                "fields": (
                    "active_from",
                    "active_until",
                    "schedule_preset",
                    "schedule",
                ),
            },
        ),
        (
            _("Audit"),
            {
                "fields": AUDIT_READONLY_FIELDS,
            },
        ),
    )

    @admin.display(description=_("Level"), ordering="level")
    def level_badge(self, obj: Message) -> str:
        return format_html(
            '<span class="inject-message inject-message--{}">{}</span>',
            obj.level,
            obj.get_level_display(),
        )

    @admin.display(description=_("Injections"))
    def injection_count(self, obj: Message) -> int:
        return obj.injections.count()

    @admin.display(description=_("Preview"))
    def preview(self, obj: Message) -> str:
        if not obj.pk:
            return "-"
        return obj.render_html()


@admin.register(MessageInjection)
class MessageInjectionAdmin(admin.ModelAdmin):
    list_display = ("message", "url_pattern", "after_sequence", "priority", "is_active")
    list_filter = ("is_active", "message__level")
    search_fields = ("url_pattern", "after_sequence", "message__label", "message__content")
    readonly_fields = AUDIT_READONLY_FIELDS
    autocomplete_fields = ("message",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "message",
                    "url_pattern",
                    "after_sequence",
                    "priority",
                    "is_active",
                ),
            },
        ),
        (
            _("Audit"),
            {
                "fields": AUDIT_READONLY_FIELDS,
            },
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("message")
