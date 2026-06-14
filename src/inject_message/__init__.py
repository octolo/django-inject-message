"""Django Inject Message - Inject content into HTTP responses by URL and anchor."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("django-inject-message")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = [
    "InjectMessageMiddleware",
    "Message",
    "MessageInjection",
    "MessageLevel",
    "SCHEDULE_BUSINESS_HOURS",
    "SCHEDULE_WEEKDAYS",
    "SCHEDULE_WEEKENDS",
    "__version__",
]


def __getattr__(name: str):
    if name == "InjectMessageMiddleware":
        from .middleware import InjectMessageMiddleware

        return InjectMessageMiddleware
    if name in {"SCHEDULE_BUSINESS_HOURS", "SCHEDULE_WEEKDAYS", "SCHEDULE_WEEKENDS"}:
        from .scheduling import SCHEDULE_BUSINESS_HOURS, SCHEDULE_WEEKDAYS, SCHEDULE_WEEKENDS

        return locals()[name]
    if name in {"Message", "MessageInjection", "MessageLevel"}:
        from .models import Message, MessageInjection, MessageLevel

        return locals()[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
