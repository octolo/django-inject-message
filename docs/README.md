## Assistant Guidelines

This file provides general guidelines for the AI assistant working on this project.

For detailed information, refer to:

- `AI.md` — Condensed reference guide for AI assistants (start here)
- `purpose.md` — Project purpose and goals
- `structure.md` — Project structure and module organization
- `development.md` — Development guidelines and best practices

### Quick Reference

- Use `manage.py` or `pytest` for local development in this repository
- Maintain clean module organization and separation of concerns
- Default to English for all code artifacts
- Keep dependencies minimal; prefer standard library when possible
- Ensure public APIs have type hints and docstrings
- Write tests for new functionality
- Source code lives in `src/inject_message/`

### django-inject-message Guidelines

- **Middleware**: Only process successful HTML responses; skip streaming responses
- **Injection**: Match URL patterns in `injector.url_matches()`; insert after anchor sequences
- **Activity**: Respect `is_active`, date window, and cron schedule via `Message.is_currently_active()`
- **Security**: Message content is trusted HTML — document and enforce admin-only editing
- **Audit**: Use `AuditLogMixin` with `CurrentUserMiddleware` from django-boosted

### Implementation Checklist

When changing injection behaviour:

- [ ] URL matching supports prefix and `^regex` patterns
- [ ] Activity checks include dates and cron schedule
- [ ] Stylesheet is injected once per response when messages are inserted
- [ ] Tests cover middleware and injector helpers
- [ ] Admin reflects model fields and validation
