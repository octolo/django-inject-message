"""Seed inject_message demo data for the test views."""

from __future__ import annotations

from django.core.management.base import BaseCommand
from django.db import transaction

from inject_message.models import Message, MessageInjection, MessageLevel

DEMO_LABEL_PREFIX = "demo:"

DEMO_MESSAGES: list[dict] = [
    {
        "label": f"{DEMO_LABEL_PREFIX}single",
        "content": "This is a single injected info message on the demo page.",
        "level": MessageLevel.INFO,
        "injections": [
            {
                "url_pattern": "/demo/single/",
                "after_sequence": "<body>",
            },
        ],
    },
    {
        "label": f"{DEMO_LABEL_PREFIX}multiple-warning",
        "content": "First warning message injected on the multiple-messages page.",
        "level": MessageLevel.WARNING,
        "injections": [
            {
                "url_pattern": "/demo/multiple/",
                "after_sequence": "<body>",
                "priority": 2,
            },
        ],
    },
    {
        "label": f"{DEMO_LABEL_PREFIX}multiple-error",
        "content": "Second error message injected on the multiple-messages page.",
        "level": MessageLevel.ERROR,
        "injections": [
            {
                "url_pattern": "/demo/multiple/",
                "after_sequence": "<body>",
                "priority": 1,
            },
        ],
    },
    {
        "label": f"{DEMO_LABEL_PREFIX}multiple-places",
        "content": "Same success message injected after the header, main, and footer.",
        "level": MessageLevel.SUCCESS,
        "injections": [
            {
                "url_pattern": "/demo/multiple-places/",
                "after_sequence": "</header>",
            },
            {
                "url_pattern": "/demo/multiple-places/",
                "after_sequence": "</main>",
            },
            {
                "url_pattern": "/demo/multiple-places/",
                "after_sequence": "</footer>",
            },
        ],
    },
]


class Command(BaseCommand):
    """Create demo Message and MessageInjection rows for the test views."""

    help = "Seed demo messages for /demo/single/, /demo/multiple/, and /demo/multiple-places/."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete existing demo messages before seeding.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["clear"]:
            deleted, _ = Message.objects.filter(label__startswith=DEMO_LABEL_PREFIX).delete()
            self.stdout.write(self.style.WARNING(f"Removed {deleted} demo row(s)."))

        for demo in DEMO_MESSAGES:
            message, _created = Message.objects.update_or_create(
                label=demo["label"],
                defaults={
                    "content": demo["content"],
                    "level": demo["level"],
                    "is_active": True,
                },
            )
            message.injections.exclude(
                url_pattern__in=[item["url_pattern"] for item in demo["injections"]],
            ).delete()

            for injection_data in demo["injections"]:
                MessageInjection.objects.update_or_create(
                    message=message,
                    url_pattern=injection_data["url_pattern"],
                    after_sequence=injection_data["after_sequence"],
                    defaults={
                        "priority": injection_data.get("priority", 0),
                        "is_active": True,
                    },
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Demo data ready: {len(DEMO_MESSAGES)} message(s), "
                f"{sum(len(item['injections']) for item in DEMO_MESSAGES)} injection rule(s)."
            )
        )
        self.stdout.write("Visit:")
        self.stdout.write("  /demo/single/")
        self.stdout.write("  /demo/multiple/")
        self.stdout.write("  /demo/multiple-places/")
