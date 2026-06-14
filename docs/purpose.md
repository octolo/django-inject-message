## Project Purpose

**django-inject-message** is a Django library that injects HTML messages into rendered HTTP responses based on configurable rules stored in the database.

### Core Functionality

The library enables you to:

1. **Define messages** with HTML content and severity levels (`debug`, `info`, `success`, `warning`, `error`)
2. **Control visibility** with:
   - `is_active` flag
   - Optional `active_from` / `active_until` datetime window
   - Optional cron `schedule` (e.g. weekends, business hours)
3. **Place messages** using `MessageInjection` rules:
   - URL path prefix or regex pattern
   - Anchor sequence in the HTML body (`after_sequence`)
   - Priority when multiple rules match
4. **Inject automatically** via `InjectMessageMiddleware` on successful HTML responses

### Architecture

- **`Message`**: Content, level, activity rules, audit fields (`created_by`, `updated_by` via django-boosted)
- **`MessageInjection`**: Placement rule linked to a message (OneToMany)
- **`InjectMessageMiddleware`**: Post-render HTML injection
- **`injector`**: URL matching, anchor insertion, stylesheet injection
- **`scheduling`**: Cron validation and matching (`croniter`)

### Use Cases

- Site-wide maintenance banners
- Promotional messages on selected pages
- Weekend-only notices
- Admin-managed alerts without template changes
