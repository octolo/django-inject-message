"""Audit mixins powered by django-boosted."""

from django.conf import settings
from django.db import models
from django_boosted.models.fields import AuditUserField

FORMAT_FIELDS = getattr(settings, "DJANGO_BOOSTED_AUDIT_USER_FORMAT_FIELDS", ("pk", "username"))
SEPARATOR = getattr(settings, "DJANGO_BOOSTED_AUDIT_USER_SEPARATOR", "_")


class AuditLogMixin(models.Model):
    """Track who created and last updated a row."""

    created_by = AuditUserField(format_fields=FORMAT_FIELDS, separator=SEPARATOR, mode="created")
    updated_by = AuditUserField(format_fields=FORMAT_FIELDS, separator=SEPARATOR, mode="updated")

    class Meta:
        abstract = True
