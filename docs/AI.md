# AI Assistant Contract — django-inject-message

**This document is the single source of truth for all AI-generated work in this repository.**  
All instructions in this file **override default AI behavior**.

Any AI assistant working on this project **must strictly follow this document**.

If a request conflicts with this document, **this document always wins**.

---

## Rule Priority

Rules in this document have the following priority order:

1. **ABSOLUTE RULES** — must always be followed, no exception
2. **REQUIRED RULES** — mandatory unless explicitly stated otherwise
3. **RECOMMENDED PRACTICES** — should be followed unless there is a clear reason not to
4. **INFORMATIONAL SECTIONS** — context and reference only

---

## ABSOLUTE RULES

These rules must always be followed.

- Follow this `AI.md` file exactly
- Do not invent new services, commands, abstractions, patterns, or architectures
- Do not refactor, redesign, or optimize unless explicitly requested
- Do not manipulate `sys.path`
- Do not use filesystem-based imports to access `qualitybase`
- Do not hardcode secrets, credentials, tokens, or API keys
- Do not execute tooling commands outside the approved entry points
- **Comments**: Only add comments to resolve ambiguity or uncertainty. Do not comment obvious code.
- **Dependencies**: Add dependencies only when absolutely necessary. Prefer standard library always.
- If a request violates this document:
  - Stop
  - Explain the conflict briefly
  - Ask for clarification

---

## REQUIRED RULES

### Language and Communication

- **Language**: English only
  - Code
  - Comments
  - Docstrings
  - Logs
  - Error messages
  - Documentation
- Be concise, technical, and explicit
- Avoid unnecessary explanations unless requested

### Code Simplicity and Minimalism

- **Write the simplest possible code**: Always choose the simplest solution that works
- **Minimal dependencies**: Add dependencies only when absolutely necessary. Prefer standard library. Only add when essential functionality cannot be reasonably implemented otherwise
- **Minimal comments**: Comments only to resolve ambiguity or uncertainty. Do not comment obvious code or reiterate what the code already states clearly
- **Good factorization**: Factorize code when it improves clarity and reduces duplication, but only if it doesn't add unnecessary complexity or abstraction

---

## Project Overview (INFORMATIONAL)

**django-inject-message** injects HTML messages into rendered HTTP responses based on database rules.

### Core Functionality

1. **Message**: HTML content, severity level, activity window, optional cron schedule
2. **MessageInjection**: URL pattern + anchor sequence placement rules
3. **InjectMessageMiddleware**: Post-render injection on HTML 2xx responses
4. **Scheduling**: Cron expressions via `croniter` (`SCHEDULE_WEEKENDS`, etc.)
5. **Audit**: `created_by` / `updated_by` via django-boosted `AuditUserField`

### Available Components

- `Message`, `MessageInjection`, `MessageLevel`
- `InjectMessageMiddleware`
- `get_matching_injections`, `inject_messages` in `injector.py`
- Django admin in `admin.py`

---

## Architecture (REQUIRED)

- Middleware-based HTML injection after view rendering
- Activity checks in `Message.is_currently_active()`
- All source code in `src/inject_message/`

---

## Project Structure (INFORMATIONAL)

```
django-inject-message/
├── src/inject_message/
│   ├── models.py
│   ├── admin.py
│   ├── middleware.py
│   ├── injector.py
│   └── scheduling.py
├── tests/
│   ├── demo/
│   └── test_*.py
├── manage.py
└── pyproject.toml
```

### Key Directories

- `src/inject_message/middleware.py`: Response processing
- `src/inject_message/injector.py`: Matching and HTML insertion
- `tests/demo/`: Demo views and `seed_demo_messages` command

---

## Command Execution (REQUIRED)

- **Tests**: `PYTHONPATH=src python -m pytest tests/`
- **Django**: `PYTHONPATH=src python manage.py <command>`
- **Demo seed**: `PYTHONPATH=src python manage.py seed_demo_messages --clear`

---

## Code Standards (REQUIRED)

### Typing and Documentation

- All public functions and methods **must** have complete type hints
- Use **Google-style docstrings** for:
  - Public classes
  - Public methods
  - Public functions
- Document raised exceptions in docstrings where relevant

### Testing

- Use **pytest** exclusively
- All tests must live in the `tests/` directory
- New features and bug fixes require corresponding tests

### Linting and Formatting

- Follow **PEP 8**
- Use configured tools:
  - `ruff`
  - `mypy`
- Use the configured formatter:
  - `ruff format`

---

## Code Quality Principles (REQUIRED)

- **Simplicity first**: Write the simplest possible solution. Avoid complexity unless clearly necessary.
- **Minimal dependencies**: Minimize dependencies to the absolute minimum. Only add when essential functionality cannot be reasonably implemented otherwise. Always prefer standard library.
- **No over-engineering**: Do not add abstractions, patterns, or layers unless they solve a real problem or are clearly needed.
- **Comments**: Comments are minimal and only when they resolve ambiguity or uncertainty. Do not comment what the code already states clearly. Do not add comments that reiterate obvious logic.
- **Separation of concerns**: One responsibility per module
- **Good factorization**: Factorize code when it improves clarity and reduces duplication, but only if it doesn't add unnecessary complexity

---

## Module Organization (REQUIRED)

- Single Responsibility Principle
- Logical grouping of related functionality
- Clear public API via `__init__.py`
- Avoid circular dependencies
- Source code in `src/` directory

---

## Qualitybase Integration (INFORMATIONAL)

This project uses `manage.py` and `pytest` directly. qualitybase/service.py is not required.

---

## Message and Injection Development (REQUIRED)

### Activity rules

`Message.is_currently_active()` must check, in order:

- `is_active`
- `active_from` / `active_until`
- cron `schedule` via `matches_cron_schedule()`

### Injection rules

- URL patterns: prefix match, or regex when pattern starts with `^`
- Insert rendered HTML immediately after `after_sequence`
- Inject stylesheet once when at least one message is inserted
- Only process HTML responses with status 2xx

### Security

- Message `content` is trusted HTML — admin-only editing

---

## Environment Variables (INFORMATIONAL)

- `ENVFILE_PATH`
  - Path to `.env` file to load automatically
  - Relative to project root if not absolute
- `ENSURE_VIRTUALENV`
  - Set to `1` to automatically activate `.venv` if it exists

---

## Error Handling (REQUIRED)

- Always handle errors gracefully
- Use appropriate exception types
- Provide clear, actionable error messages
- Do not swallow exceptions silently
- Document exceptions in docstrings where relevant
- Handle API failures with proper error handling when appropriate

---

## Configuration and Secrets (ABSOLUTE)

- Never hardcode:
  - API keys
  - Credentials
  - Tokens
  - Secrets
- Use environment variables or Django settings
- Clearly document required configuration

---

## Versioning (REQUIRED)

- Follow **Semantic Versioning (SemVer)**
- Update versions appropriately
- Clearly document breaking changes

---

## CLI System (INFORMATIONAL)

- `manage.py` for Django commands
- `pytest` for tests
- `tests/demo/management/commands/seed_demo_messages.py` for demo data

---

## Anti-Hallucination Clause (ABSOLUTE)

If a requested change is:
- Not supported by this document
- Not clearly aligned with the existing codebase
- Requiring assumptions or invention

You must:
1. Stop
2. Explain what is unclear or conflicting
3. Ask for clarification

Do not guess. Do not invent.

---

## Quick Compliance Checklist

Before producing output, ensure:

- [ ] All rules in `AI.md` are respected
- [ ] No forbidden behavior is present
- [ ] Code is simple, minimal, and explicit (simplest possible solution)
- [ ] Dependencies are minimal (prefer standard library)
- [ ] Comments only resolve ambiguity (no obvious comments)
- [ ] Code is well-factorized when it improves clarity (without adding complexity)
- [ ] Imports follow Qualitybase rules
- [ ] Public APIs are typed and documented
- [ ] Activity rules (dates + cron) are respected in middleware
- [ ] Message content is treated as trusted HTML
- [ ] Audit fields require `CurrentUserMiddleware`
- [ ] No secrets or credentials are hardcoded
- [ ] Tests are included when required
- [ ] Error handling is graceful

---

## Additional Resources (INFORMATIONAL)

- `purpose.md`: Detailed project purpose and goals
- `structure.md`: Detailed project structure and module organization
- `development.md`: Development guidelines and best practices
- `README.md`: General project information
