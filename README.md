# django-inject-message

Inject HTML messages into Django HTTP responses based on URL patterns, anchor sequences, and activity rules.

## Purpose

Manage banners, alerts, and notices from the database (or admin) without editing templates. Messages are inserted into rendered HTML responses by middleware after matching:

- URL path patterns
- Anchor sequences in the HTML body (e.g. `<body>`, `</header>`)
- Activity window (`active_from` / `active_until`)
- Optional cron schedule (weekends, business hours, etc.)
- Severity level with built-in CSS styling

## Installation

```bash
pip install django-inject-message
```

Add to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    "django_boosted",
    "inject_message",
]
```

Add middleware (before compression middleware if you use GZip):

```python
MIDDLEWARE = [
    # ...
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_boosted.middleware.CurrentUserMiddleware",
    "inject_message.middleware.InjectMessageMiddleware",
]
```

Run migrations:

```bash
python manage.py migrate inject_message
```

## Quick start

### 1. Create a message and injection rule

```python
from inject_message.models import Message, MessageInjection, MessageLevel

message = Message.objects.create(
    label="Maintenance",
    content="<strong>Scheduled maintenance tonight at 22:00.</strong>",
    level=MessageLevel.WARNING,
)

MessageInjection.objects.create(
    message=message,
    url_pattern="/dashboard/",
    after_sequence="<body>",
)
```

### 2. Or use the Django admin

Open `/admin/` and manage **Messages** with inline **Message injections**. Each message supports:

- Content and severity level (`debug`, `info`, `success`, `warning`, `error`)
- Activity dates and cron schedule (with presets for weekends / weekdays)
- Multiple injection rules per message

### 3. Schedule examples

```python
from inject_message import SCHEDULE_WEEKENDS, SCHEDULE_WEEKDAYS, SCHEDULE_BUSINESS_HOURS

Message.objects.create(
    label="Weekend promo",
    content="Special offer this weekend!",
    level=MessageLevel.SUCCESS,
    schedule=SCHEDULE_WEEKENDS,
)
```

Cron format: `minute hour day month weekday` (e.g. `* * * * 0,6` for weekends).

## Demo (development)

This repository includes a demo app under `tests/demo/`:

| URL | Scenario |
|---|---|
| `/demo/single/` | One message |
| `/demo/multiple/` | Several messages |
| `/demo/multiple-places/` | One message, multiple anchors |

Seed demo data:

```bash
PYTHONPATH=src python manage.py seed_demo_messages --clear
PYTHONPATH=src python manage.py runserver
```

## Security

Message `content` is injected as HTML. Only trusted staff should edit messages in the admin.

## Development

```bash
PYTHONPATH=src python -m pytest tests/ -v
PYTHONPATH=src python manage.py migrate
```

## License

MIT
