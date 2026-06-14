"""Django app configuration."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class InjectMessageConfig(AppConfig):
    """Configuration for the inject_message app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "inject_message"
    verbose_name = _("Inject Message")
