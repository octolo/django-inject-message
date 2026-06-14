## Project Structure

django-inject-message follows a standard Python package layout with source code in `src/`.

### General Structure

```
django-inject-message/
├── src/
│   └── inject_message/
│       ├── __init__.py       # Public exports
│       ├── models.py          # Message, MessageInjection, MessageLevel
│       ├── admin.py           # Django admin
│       ├── middleware.py      # InjectMessageMiddleware
│       ├── injector.py        # HTML injection helpers
│       ├── scheduling.py      # Cron helpers and presets
│       ├── audit.py           # AuditLogMixin (django-boosted)
│       ├── apps.py
│       ├── migrations/
│       └── static/inject_message/inject_message.css
├── tests/
│   ├── settings.py
│   ├── demo/                  # Demo views, templates, seed command
│   └── test_*.py
├── docs/
├── manage.py
├── pyproject.toml
└── README.md
```

### Module Organization

- **`models.py`**: Data model and `Message.render_html()` / `is_currently_active()`
- **`middleware.py`**: Response processing entry point
- **`injector.py`**: `get_matching_injections()`, `inject_messages()`, `inject_stylesheet()`
- **`scheduling.py`**: `SCHEDULE_WEEKENDS`, `SCHEDULE_WEEKDAYS`, `SCHEDULE_BUSINESS_HOURS`
- **`admin.py`**: Message admin with inline injections and schedule presets

### Public API (`inject_message/__init__.py`)

- `InjectMessageMiddleware`
- `Message`, `MessageInjection`, `MessageLevel`
- `SCHEDULE_WEEKENDS`, `SCHEDULE_WEEKDAYS`, `SCHEDULE_BUSINESS_HOURS`
